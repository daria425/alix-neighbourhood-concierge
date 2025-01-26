from vertexai.generative_models import GenerationResponse, ToolConfig
from model_factory import ModelFactoryProvider
from typing import List, Any
import logging
class ResponseGenerator:
    def __init__(self):
        self.model_factory=ModelFactoryProvider.get_instance()
    
    def generate_response(self, model_name: str, system_instruction: str, contents: List[str], tools: List[Any]=None,tool_config:ToolConfig=None )->GenerationResponse:
        """
        Generates a response based on the provided model name, system instruction, contents, response schema, and tools.

        Args:
            model_name (str): Name of the model for generation.
            system_instruction (str): Instruction or prompt for the model.
            contents(List[str]): Content input for response generation
            tools (List[Any]): Tools passed to the model for content generation (default is None).

        Returns:
            GenerationResponse: Generated response object.

        Raises:
            Exception: If an error occurs during response generation.
        """
        try:
            logging.info(f"Creating instance of {model_name}")
            model=self.model_factory.create_model(model_name, system_instruction)
            response=model.generate_content(contents, tools=tools, tool_config=tool_config )
            logging.info("Response generated")
            return response
        except Exception as e:
            logging.error(f"Error generating response {e}")
            raise
