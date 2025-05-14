import json
import asyncio
from typing import Dict, Any, List
import logging

from ..utils.logging_utils import setup_logging

logger = setup_logging("llm_service.ollama_adapter")


class OllamaAdapter:
    """
    Adapter for Ollama API interactions
    """

    def __init__(self, model_name="llama3.2"):
        """
        Initialize Ollama adapter

        Args:
            model_name: Ollama model to use
        """
        try:
            from ollama import chat
            self.chat = chat
            self.model_name = model_name
        except ImportError:
            logger.error("Ollama Python package not installed. Install with: pip install ollama")
            raise ImportError("Ollama Python package required for Ollama models")

    async def process_query(self, messages, tools, mcp_session):
        """
        Process a query using the Ollama API

        Args:
            messages: List of message objects
            tools: List of MCP Tool objects
            mcp_session: MCP client session

        Returns:
            Interaction history
        """
        interaction_history = []
        loop = asyncio.get_event_loop()

        # Format tools for Ollama
        ollama_tools = [{
            "name": t.name,
            "description": t.description,
            "input_schema": t.inputSchema
        } for t in tools]

        # First chat invocation
        logger.info(f"Sending initial query to Ollama model: {self.model_name}")
        ollama_resp = await loop.run_in_executor(
            None,
            lambda: self.chat(
                model=self.model_name,
                messages=messages,
                tools=ollama_tools,
                stream=False
            )
        )

        first_text = ollama_resp.message.content or ""
        tool_calls = getattr(ollama_resp.message, 'tool_calls', []) or []

        # Record initial response
        interaction_history.append({
            "role": "assistant",
            "content": first_text,
            "has_tool_calls": bool(tool_calls)
        })

        # Add assistant reply to history for tool-call context
        messages.append({"role": "assistant", "content": first_text})

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

                # Feed the result back into the model as a function response
                messages.append({
                    "role": "function",
                    "name": fname,
                    "content": tool_output
                })

            except Exception as e:
                error_msg = f"Error executing tool {fname}: {str(e)}"
                logger.error(error_msg)
                messages.append({
                    "role": "function",
                    "name": fname,
                    "content": f"ERROR: {error_msg}"
                })
                interaction_history.append({
                    "role": "tool_error",
                    "name": fname,
                    "error": str(e)
                })

        # Get follow-up from the model to synthesize results if tools were used
        if tool_calls:
            logger.info("Getting final response after tool calls")
            ollama_resp = await loop.run_in_executor(
                None,
                lambda: self.chat(
                    model=self.model_name,
                    messages=messages,
                    stream=False
                )
            )
            follow_text = ollama_resp.message.content or ""

            interaction_history.append({
                "role": "assistant_final",
                "content": follow_text
            })

        return interaction_history

    async def list_models(self):
        """
        List available Ollama models

        Returns:
            List of model names
        """
        try:
            # For Ollama, we need to use a different API
            # This is simplified; you might want to implement a proper Ollama model listing
            return ["llama3.2", "mistral", "phi3", "gemma3:27b", "codellama", "llama3.1:70b",
                    "(Note: This is a partial list. Use 'ollama list' in your terminal for a complete list)"]
        except Exception as e:
            logger.error(f"Error listing models: {e}")
            return ["llama3.2", "Unable to fetch complete list"]