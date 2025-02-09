from app.core.response_generator import ResponseGenerator
from vertexai.generative_models import FunctionDeclaration, Tool, GenerationResponse, ToolConfig
from datetime import datetime
from abc import ABC, abstractmethod
from app.core.agent_config import AgentConfig
import logging
class Agent(ABC):
    def __init__(self):
        self.response_generator=ResponseGenerator()
        self.agent_config= AgentConfig()
    @abstractmethod
    def run_task(self):
        raise NotImplementedError("Agent subclasses must implement the `run_task` method")
    
class AgentWithTools(Agent):
    def __init__(self):
        super().__init__()
    def create_tools(self, function_declarations)->Tool:
        return Tool(function_declarations=function_declarations)
    def _get_function_output(self, response: GenerationResponse):
            try:
                if not response.candidates:
                    raise ValueError("No candidates found in the response.")
                first_candidate = response.candidates[0]
                if not first_candidate.content.parts:
                    raise ValueError("Candidate content has no parts.")

                first_part = first_candidate.content.parts[0]
                if not hasattr(first_part, "function_call") or not first_part.function_call:
                    raise ValueError("No function call found in the response part.")

                logging.info("Extracting function arguments from the response.")
                return dict(first_part.function_call.args) if first_part.function_call.args else None
            except ValueError as e:
                logging.error(f"Error processing response: {e}")
                return None
            except Exception as e:
                logging.error(f"Unexpected error: {e}")
                return None



class EventInfoExtractionAgent(AgentWithTools):
    task="EXTRACT_EVENT_INFO"
    def __init__(self):
        super().__init__()
        self.config=self.agent_config.get_config(self.task)
    def _create_extract_function_declaration(self)->FunctionDeclaration:
        function = FunctionDeclaration(
        name="get_event_data",
        description="Extract and structure event information from a given entry",
        parameters={
            "type": "object",
            "properties": {
                "tag":{
                    "type":"string", 
                    "nullable":False,
                    "description": "A category tag for the event, must be one from the provided list: Arts, Children's Channel, Community Support, Festive, Health & Sport, Music, Playtime, Skill & Professional Development, Social, Workshop"
                }, 
                "event_name": {
                    "type": "string",
                    "nullable":False,
                    "description": "Title or name of the event",
                },
                "description": {
                    "type": "string",
                    "nullable": True,
                    "description": "A brief description of the event based on the provided information in the entry or null",
                },
                "date_and_time": {
                    "type": "string",
                    "nullable": True,
                    "description": "Date and time when the event is scheduled to occur or null",
                },
                "location": {
                    "type": "string",
                    "nullable": True,
                    "description": "Venue or address where the event will take place or null",
                },
                "cost": {
                    "type": "string",
                    "nullable": True,
                    "description": "The cost of the event, if available or null",
                },
                "booking_details": {
                    "type": "string",
                    "nullable": True,
                    "description": "A link to book the event or get additional details, if available or null",
                },
                "url": {
                    "type": "string",
                    "nullable":False,
                    "description": "Link to the original webpage containing the event details or null",
                },
                "is_within_2_weeks":{
                    "type":"boolean", 
                    "nullable":False,
                    "description":f"True if the domain name is wherecanwego.com or if date and time of event is within 2 weeks of {datetime.now().strftime('%d %b %Y')}. False otherwise"
                }
            },
            "required": ["tag","event_name", "description", "date_and_time", "location", "cost", "booking_details","is_within_2_weeks"],
        },
    )
        return function
    
    def run_task(self, contents:str):
        model_name=self.config['model_name']
        system_instruction=self.config['system_instruction']
        extract_function=self._create_extract_function_declaration()
        tools=self.create_tools(function_declarations=[extract_function])
        tool_config=ToolConfig(
        function_calling_config=ToolConfig.FunctionCallingConfig(
            # ANY mode forces the model to predict only function calls
            mode=ToolConfig.FunctionCallingConfig.Mode.ANY,
            # Allowed function calls to predict when the mode is ANY. If empty, any  of
            # the provided function calls will be predicted.
            allowed_function_names=["get_event_data"])
        )
        res=self.response_generator.generate_response(model_name=model_name, system_instruction=system_instruction, contents=contents, tools=[tools], tool_config=tool_config)
        output=self._get_function_output(res)
        return output
    
        
