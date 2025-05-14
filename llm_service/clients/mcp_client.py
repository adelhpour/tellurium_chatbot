import json
import asyncio
import os
from typing import Optional, Dict, Any, List, Callable
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters, Tool
from mcp.client.stdio import stdio_client

from ..utils.logging_utils import setup_logging
from .openai_adapter import OpenAIAdapter
from .ollama_adapter import OllamaAdapter

# Set up logging
logger = setup_logging("llm_service.mcp_client")


class MCPClient:
    """
    Client for interacting with MCP (Model Control Protocol) server
    """

    def __init__(self, server_script: str, model_name: str):
        """
        Initialize MCP client

        Args:
            server_script: Path to MCP server script
            model_name: Model to use for queries
        """
        self.server_script = server_script
        self.model_name = model_name
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.available_tools: List[Tool] = []
        self.tool_map: Dict[str, Tool] = {}
        self.using_openai = self._is_openai_model(model_name)

        # Initialize appropriate model adapter
        if self.using_openai:
            self.model_adapter = OpenAIAdapter(model_name=model_name)
        else:
            self.model_adapter = OllamaAdapter(model_name=model_name)

    def _is_openai_model(self, model_name: str) -> bool:
        """
        Determine if model is OpenAI based on prefix

        Args:
            model_name: Name of the model

        Returns:
            True if OpenAI model, False otherwise
        """
        openai_prefixes = ["gpt"]
        return any(model_name.startswith(prefix) for prefix in openai_prefixes)

    async def connect_to_server(self):
        """
        Connect to the MCP server

        Returns:
            self for method chaining
        """
        try:
            server_script_path = self.server_script
            is_python = server_script_path.endswith('.py')
            is_js = server_script_path.endswith('.js')
            if not (is_python or is_js):
                raise ValueError("Server script must be a .py or .js file")

            command = "python" if is_python else "node"
            server_params = StdioServerParameters(
                command=command,
                args=[server_script_path],
                env=None
            )

            logger.info(f"Connecting to MCP server: {server_script_path}")
            stdio_transport = await self.exit_stack.enter_async_context(
                stdio_client(server_params)
            )
            self.stdio, self.write = stdio_transport
            self.session = await self.exit_stack.enter_async_context(
                ClientSession(self.stdio, self.write)
            )

            await self.session.initialize()

            # Get and store available tools
            await self._refresh_tools()
            return self

        except Exception as e:
            logger.error(f"Failed to connect to MCP server: {e}")
            raise

    async def _refresh_tools(self):
        """
        Fetch and cache available tools from the server

        Returns:
            List of tool names
        """
        if not self.session:
            raise RuntimeError("Not connected to MCP server")

        response = await self.session.list_tools()
        self.available_tools = response.tools
        self.tool_map = {t.name: t for t in response.tools}
        tool_names = [t.name for t in response.tools]
        logger.info(f"Available tools: {tool_names}")
        return tool_names

    def _validate_tool_args(self, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate tool arguments against the tool's schema

        Args:
            tool_name: Name of the tool
            args: Tool arguments

        Returns:
            Validated tool arguments
        """
        if tool_name not in self.tool_map:
            raise ValueError(f"Unknown tool: {tool_name}")

        tool = self.tool_map[tool_name]

        # Basic validation - could be enhanced with full JSON schema validation
        if not tool.inputSchema:
            return args

        try:
            required_props = tool.inputSchema.get("required", [])
            for prop in required_props:
                if prop not in args:
                    raise ValueError(f"Missing required argument '{prop}' for tool '{tool_name}'")

            return args
        except Exception as e:
            logger.error(f"Error validating tool arguments: {e}")
            raise ValueError(f"Invalid arguments for tool '{tool_name}': {e}")

    async def process_query(self, query: str) -> str:
        """
        Process a query using the model and available tools

        Args:
            query: User query text

        Returns:
            Response text
        """
        if not self.session:
            await self.connect_to_server()

        # Start with the user message
        messages = [{"role": "user", "content": query}]

        try:
            # Process with appropriate adapter
            interaction_history = await self.model_adapter.process_query(
                messages,
                self.available_tools,
                self.session
            )
            return self._format_output(interaction_history)
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return f"Error processing your query: {str(e)}"

    def _format_output(self, history):
        """
        Format the interaction history into a readable output

        Args:
            history: Interaction history

        Returns:
            Formatted output text
        """
        output_parts = []

        # First assistant response
        first_response = next((h for h in history if h["role"] == "assistant"), None)
        if first_response:
            output_parts.append(first_response["content"])

        # Final response (if tools were used)
        final_response = next((h for h in history if h["role"] == "assistant_final"), None)
        if final_response:
            output_parts.append(f"\n{final_response['content']}")

        return "\n".join(output_parts)

    async def get_tool_details(self, tool_name=None):
        """
        Get detailed information about available tools

        Args:
            tool_name: Optional name of specific tool

        Returns:
            Tool details or list of tools
        """
        if not self.session:
            await self.connect_to_server()

        if not tool_name:
            return self.available_tools
        elif tool_name in self.tool_map:
            return self.tool_map[tool_name]
        else:
            return f"Tool '{tool_name}' not found"

    async def list_available_models(self):
        """
        List available models

        Returns:
            List of model names
        """
        return await self.model_adapter.list_models()

    async def set_model(self, model_name):
        """
        Change the current model

        Args:
            model_name: New model name

        Returns:
            Status message
        """
        new_is_openai = self._is_openai_model(model_name)

        # If switching between API types, initialize the new adapter
        if new_is_openai != self.using_openai:
            if new_is_openai:
                self.model_adapter = OpenAIAdapter(model_name=model_name)
            else:
                self.model_adapter = OllamaAdapter(model_name=model_name)

        self.model_name = model_name
        self.using_openai = new_is_openai
        logger.info(f"Model changed to: {model_name} (API: {'OpenAI' if self.using_openai else 'Ollama'})")
        return f"Model changed to: {model_name} (API: {'OpenAI' if self.using_openai else 'Ollama'})"

    async def cleanup(self):
        """
        Close all connections and clean up resources
        """
        logger.info("Cleaning up resources")
        await self.exit_stack.aclose()

    async def ask_async(self, query: str) -> str:
        """
        Send a single query and return the response

        Args:
            query: User query text

        Returns:
            Response text
        """
        try:
            await self.connect_to_server()
            return await self.process_query(query)
        finally:
            await self.cleanup()

    def ask(self, query: str) -> str:
        """
        Synchronous wrapper around ask_async

        Args:
            query: User query text

        Returns:
            Response text
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(self.ask_async(query))
        finally:
            loop.close()