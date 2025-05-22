import os
import json
import asyncio
from typing import Dict, Any, List
import logging
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

from ..utils.logging_utils import setup_logging

logger = setup_logging("llm_service.openai_adapter")


class OpenAIAdapter:
    """
    Adapter for OpenAI API interactions
    """

    def __init__(self, model_name="gpt-4o", embed_model_name="all-MiniLM-L6-v2", top_k=5):
        """
        Initialize OpenAI adapter with retrieval capabilities

        Args:
            model_name: OpenAI model to use
            embed_model_name: SentenceTransformer model for embeddings
            top_k: Number of similar past interactions to retrieve
        """
        try:
            from openai import AsyncOpenAI
            from dotenv import load_dotenv

            load_dotenv()
            api_key = os.getenv("OPENAI_API_KEY")

            if not api_key:
                warning_msg = "OPENAI_API_KEY not found in environment."
                logger.warning(warning_msg)
                print(f"Error: {warning_msg}")
                print("You can either:")
                print("  • Add it to your .env file, e.g.:")
                print("      OPENAI_API_KEY='your-api-key'")
                print("  • Or export it in your shell, e.g.:")
                print("      export OPENAI_API_KEY='your-api-key'")
                raise RuntimeError("Cannot initialize OpenAIAdapter without OPENAI_API_KEY")

            self.client = AsyncOpenAI(api_key=api_key)
            self.model_name = model_name

            # Initialize embedding model
            self.embedder = SentenceTransformer(embed_model_name)
            self.embed_dim = self.embedder.get_sentence_embedding_dimension()

            # Initialize FAISS index for similarity search
            self.index = faiss.IndexFlatL2(self.embed_dim)

            # Storage for past interactions
            self.memories = []  # List of (user_message, assistant_response) tuples

            # Retrieval settings
            self.top_k = top_k

        except ImportError as e:
            logger.error(f"Required package not installed: {str(e)}")
            logger.error("Install with: pip install openai sentence-transformers faiss-cpu")
            raise ImportError("Required packages: openai, sentence-transformers, faiss-cpu")

    def _embed_interaction(self, user_msg: str, assistant_msg: str) -> np.ndarray:
        """
        Create an embedding for a user-assistant interaction
        """
        combined = f"User: {user_msg}\nAssistant: {assistant_msg}"
        return self.embedder.encode(combined)

    def _embed_query(self, query: str) -> np.ndarray:
        """
        Create an embedding for a user query
        """
        return self.embedder.encode(query)

    def _get_latest_user_message(self, messages: List[Dict[str, str]]) -> str:
        """
        Extract the content of the most recent user message
        """
        # Find the last user message in the list
        for msg in reversed(messages):
            if msg.get('role') == 'user':
                return msg.get('content', '')
        return ''

    def _store_interaction(self, user_msg: str, assistant_response: str):
        """
        Store an interaction in memory and update the index
        """
        # Create embedding
        embedding = self._embed_interaction(user_msg, assistant_response)

        # Add to FAISS index
        self.index.add(np.vstack([embedding]))

        # Store in memory
        self.memories.append((user_msg, assistant_response))

        logger.debug(f"Stored interaction in memory (total: {len(self.memories)})")

    def _retrieve_relevant_memories(self, query: str) -> List[Dict[str, str]]:
        """
        Retrieve relevant past interactions based on query similarity
        """
        if len(self.memories) == 0:
            return []

        # Embed the query
        query_emb = self._embed_query(query)

        # Find similar past interactions
        k = min(self.top_k, len(self.memories))
        distances, indices = self.index.search(np.vstack([query_emb]), k)

        # Convert to message format
        messages = []
        for idx in indices[0]:
            if idx < 0 or idx >= len(self.memories):  # Handle potential out-of-bounds
                continue

            user_msg, assistant_msg = self.memories[idx]
            messages.append({"role": "user", "content": user_msg})
            messages.append({"role": "assistant", "content": assistant_msg})

        logger.info(f"Retrieved {len(messages) // 2} relevant past interactions")
        return messages

    def _convert_tools_to_openai_format(self, tools: List) -> List[Dict[str, Any]]:
        """
        Convert MCP tools to OpenAI tools format

        Args:
            tools: List of MCP Tool objects

        Returns:
            List of tools in OpenAI format
        """
        openai_tools = []

        for tool in tools:
            openai_tool = {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema if tool.inputSchema else {"type": "object", "properties": {}}
                }
            }
            openai_tools.append(openai_tool)

        return openai_tools

    async def process_query(self, messages, tools, mcp_session):
        """
        Process a query using the OpenAI API with retrieval augmentation

        Args:
            messages: List of message objects
            tools: List of MCP Tool objects
            mcp_session: MCP client session

        Returns:
            Interaction history
        """
        interaction_history = []

        # Get the latest user message
        current_query = self._get_latest_user_message(messages)

        # Retrieve relevant past interactions
        retrieved_messages = self._retrieve_relevant_memories(current_query)

        # Augment the messages with retrieved context
        # We'll inject the retrieved messages at the beginning, preserving the recent conversation flow
        augmented_messages = retrieved_messages + messages
        logger.info(f"Augmented messages with {len(retrieved_messages)} retrieved messages")

        # Format tools for OpenAI
        openai_tools = self._convert_tools_to_openai_format(tools)

        # First chat invocation with augmented context
        logger.info(f"Sending augmented query to OpenAI model: {self.model_name}")
        response = await self.client.chat.completions.create(
            model=self.model_name,
            messages=augmented_messages,
            tools=openai_tools,
            tool_choice="auto"
        )

        first_message = response.choices[0].message
        first_text = first_message.content or ""
        tool_calls = getattr(first_message, 'tool_calls', []) or []

        # Record initial response
        interaction_history.append({
            "role": "assistant",
            "content": first_text,
            "has_tool_calls": bool(tool_calls)
        })

        # Add assistant reply to history for tool-call context
        augmented_messages.append({
            "role": "assistant",
            "content": first_text,
            "tool_calls": tool_calls if tool_calls else None
        })

        # Handle any tool/function calls
        for call in tool_calls:
            try:
                fname = call.function.name
                logger.info(f"Processing tool call: {fname}")

                # Parse arguments properly
                try:
                    if isinstance(call.function.arguments, str):
                        fargs = json.loads(call.function.arguments)
                    else:
                        fargs = call.function.arguments
                except json.JSONDecodeError:
                    logger.error(f"Invalid JSON in tool arguments: {call.function.arguments}")
                    fargs = {}

                # Run the tool via MCP
                logger.info(f"Calling tool {fname} with args: {fargs}")
                result = await mcp_session.call_tool(fname, fargs)

                # Extract raw text from TextContent list
                tool_output = "".join([tc.text for tc in result.content])

                # Record tool interaction
                interaction_history.append({
                    "role": "tool",
                    "name": fname,
                    "arguments": fargs,
                    "result": tool_output
                })

                # Feed the result back into the model as a tool message
                augmented_messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "name": fname,
                    "content": tool_output
                })

            except Exception as e:
                error_msg = f"Error executing tool {fname}: {str(e)}"
                logger.error(error_msg)
                augmented_messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "name": fname,
                    "content": f"ERROR: {error_msg}"
                })
                interaction_history.append({
                    "role": "tool_error",
                    "name": fname,
                    "error": str(e)
                })

        # Get follow-up from the model to synthesize results if tools were used
        final_response = first_text
        if tool_calls:
            logger.info("Getting final response after tool calls")
            follow_response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=augmented_messages
            )
            final_response = follow_response.choices[0].message.content or ""

            interaction_history.append({
                "role": "assistant_final",
                "content": final_response
            })

        # Store this interaction in memory for future retrieval
        self._store_interaction(current_query, final_response)

        return interaction_history

    async def list_models(self):
        """
        List available OpenAI models

        Returns:
            List of model IDs
        """
        try:
            models = await self.client.models.list()
            return [model.id for model in models.data if "gpt" in model.id]
        except Exception as e:
            logger.error(f"Error listing models: {e}")
            return ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo", "Unable to fetch complete list"]