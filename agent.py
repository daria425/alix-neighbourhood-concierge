from response_generator import ResponseGenerator
from vertexai.generative_models import FunctionDeclaration, Tool
from datetime import datetime
from abc import ABC, abstractmethod
from config.agent_config import AgentConfig

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
                "date_and_time": {
                    "type": "string",
                    "description": "Date and time when the event is scheduled to occur",
                },
                "location": {
                    "type": "string",
                    "description": "Venue or address where the event will take place",
                },
                "cost": {
                    "type": "string",
                    "description": "The cost of the event, if available",
                },
                "booking_details": {
                    "type": "string",
                    "description": "A link to book the event or get additional details, if available",
                },
                "url": {
                    "type": "string",
                    "description": "Link to the original webpage containing the event details",
                },
                "is_within_2_weeks":{
                    "type":"boolean", 
                    "description":f"whether the event is within 2 weeks. False if there is no event date, the event date is uncertain or event date is not within 2 weeks of {datetime.now().strftime('%d %b %Y')}"
                }
            },
            "required": ["tag","event_name", "is_within_2_weeks"],
        },
    )
        return function
    def run_task(self, contents:str):
        model_name=self.config['model_name']
        system_instruction=self.config['system_instruction']
        extract_function=self._create_extract_function_declaration()
        tools=self.create_tools(function_declarations=[extract_function])
        res=self.response_generator.generate_response(model_name=model_name, system_instruction=system_instruction, contents=contents, tools=[tools])
        print(res.candidates[0].function_calls)
        
extract_agent=EventInfoExtractionAgent()
contents="""
-----------
BEGIN ENTRY
-----------
As part of our programme of events to mark #IDAHOBIT forum+ will be screening 'The Matthew Shepard Story', based on the true life story of openly gay US college student Matthew Shepard killed in an act of hate crime in 1998. The screening will take place on Monday 13th May at the Hugh Cubitt Centre, N1 9QZ.
----------
END ENTRY
----------
"""
extract_agent.run_task(contents)