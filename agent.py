from response_generator import ResponseGenerator
from vertexai.generative_models import FunctionDeclaration, Tool, GenerationResponse
from datetime import datetime
from abc import ABC, abstractmethod
from config.agent_config import AgentConfig
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
                    "description": "A category tag for the event, must be one from the provided list: Arts, Children's Channel, Community Support, Festive, Health & Sport, Music, Playtime, Skill & Professional Development, Social, Workshop"
                }, 
                "event_name": {
                    "type": "string",
                    "description": "Title or name of the event",
                },
                "description": {
                    "type": "string",
                    "description": "A brief description of the event based on the provided information in the entry or null",
                },
                "date_and_time": {
                    "type": "string",
                    "description": "Date and time when the event is scheduled to occur or null",
                },
                "location": {
                    "type": "string",
                    "description": "Venue or address where the event will take place or null",
                },
                "cost": {
                    "type": "string",
                    "description": "The cost of the event, if available or null",
                },
                "booking_details": {
                    "type": "string",
                    "description": "A link to book the event or get additional details, if available or null",
                },
                "url": {
                    "type": "string",
                    "description": "Link to the original webpage containing the event details or null",
                },
                "is_within_2_weeks":{
                    "type":"boolean", 
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
        res=self.response_generator.generate_response(model_name=model_name, system_instruction=system_instruction, contents=contents, tools=[tools])
        output=self._get_function_output(res)
        return output
    def _get_function_output(self, response: GenerationResponse):
            first_candidate = response.candidates[0]
            first_part = first_candidate.content.parts[0]
            function_call = first_part.function_call
            logging.info("Extracting function arguments from the response.")
            return dict(function_call.args) if function_call else None

        
