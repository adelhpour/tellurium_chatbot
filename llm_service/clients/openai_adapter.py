import os
import json
import asyncio
from typing import Dict, Any, List
import logging

from ..utils.logging_utils import setup_logging

logger = setup_logging("llm_service.openai_adapter")


class OpenAIAdapter:
    """
    Adapter for OpenAI API interactions
    """

    def __init__(self, model_name="gpt-4o"):
        """
        Initialize OpenAI adapter

        Args:
            model_name: OpenAI model to use
        """
        try:
            from openai import AsyncOpenAI
            from dotenv import load_dotenv

            load_dotenv()
            api_key = os.getenv("OPENAI_API_KEY")

            if not api_key:
                logger.warning("OPENAI_API_KEY environment variable not set. Please set it in your .env file.")
                print("Warning: OPENAI_API_KEY environment variable not set.")
                print("Set it in your .env file like: OPENAI_API_KEY='your-api-key'")

            self.client = AsyncOpenAI(api_key=api_key)
            self.model_name = model_name

        except ImportError:
            logger.error("OpenAI Python package not installed. Install with: pip install openai")
            raise ImportError("OpenAI Python package required for OpenAI models")

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
        Process a query using the OpenAI API

        Args:
            messages: List of message objects
            tools: List of MCP Tool objects
            mcp_session: MCP client session

        Returns:
            Interaction history
        """
        interaction_history = []

        # Format tools for OpenAI
        openai_tools = self._convert_tools_to_openai_format(tools)

        # First chat invocation
        logger.info(f"Sending initial query to OpenAI model: {self.model_name}")
        response = await self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
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
        messages.append({
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
                messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "name": fname,
                    "content": tool_output
                })

            except Exception as e:
                error_msg = f"Error executing tool {fname}: {str(e)}"
                logger.error(error_msg)
                messages.append({
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
        if tool_calls:
            logger.info("Getting final response after tool calls")
            follow_response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=messages
            )
            follow_text = follow_response.choices[0].message.content or ""

            interaction_history.append({
                "role": "assistant_final",
                "content": follow_text
            })

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