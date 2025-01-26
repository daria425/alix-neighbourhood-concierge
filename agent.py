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
                    "description":f"True if date and time of event is within 2 weeks of {datetime.now().strftime('%d %b %Y')}. False otherwise"
                }
            },
            "required": ["tag","event_name", "is_within_2_weeks"],
        },
    )
        print(function)
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
{
    "event_title": "Bach and Vivaldi Violin Concertos by Candlelight",
    "description": "The exceptional musicians of the Piccadilly Sinfonietta perform a selection of Bach's magnificent Violin concertos by candlelight in the...",
    "location": "St Mary Le Strand Church, London WC2R 1ES",
    "url": "https://www.wherecanwego.com/item/e1550848",
    "event_id": "e1550848",
    "event_detail": {
      "event_id": "e1550848",
      "sections": [
        {
          "text_content": "\n\n\n\n\n\nBach and Vivaldi Violin Concertos by Candlelight\n\n\nSt Mary Le Strand Church, London WC2R 1ES\n\n\nview on map\n\n\n\n\nSaturday 1 February\n\n\n",
          "links": ["https://www.wherecanwego.com/item/e1550848?map=1#mapPanel"]
        },
        {
          "text_content": "\n\n\n6pm-7pm\u00a325, \u00a335, \u00a345\n\n\n\n\n\n\n\n\n\n\n\nBuy Tickets\n\n\n\n\n\n03336663366\nfor\u00a0latest\u00a0times\u00a0or\u00a0cancellations.\n\n",
          "links": [
            "https://www.eventim-light.com/uk/a/63c82ca274fb184f4eebf902/e/667d729d286e5b6c4634ee06?lang=en",
            "tel:03336663366"
          ]
        },
        { "text_content": "\nSpread the word\n\n\n\n\n\n", "links": [] },
        {
          "text_content": "\nAbout this Event\n\nBach and Vivaldi Violin Concertos by Candlelight\n\nThe exceptional musicians of the Piccadilly Sinfonietta perform a selection of Bach's magnificent Violin concertos by candlelight in the beautiful setting of St Mary Le Strand, London.  A hugely appealing evening designed to help you celebrate the weekend in style! There are also plenty of bars and restaurants nearby to complete your night.\r 'Stunning' - Classic FM\r Note - there are two performances available: 6pm and 8pm\r Featuring\rThe Piccadilly Sinfonietta\rVictoria Lyon (violin)\r Programme\r Bach - Violin Concerto in E Major, BWV 1042\r Bach - Air on a G String (from Orchestral Suite No. 3 in D Major, BWV 1068)\r Vivaldi - Double Violin Concerto in A Minor, RV 522\r Bach - Concerto for Two Violins in D Minor, BWV 1043\r Since its formation in 2017, the Piccadilly Sinfonietta have become a regular feature on the UK concert scene, giving over 200 performances a year in some of the country\u2019s most beautiful and prestigious venues. The ensemble comprises some of the most prodigious musical talent and performs exclusively with leading virtuoso soloists. The group performs under the artistic direction of its founder, concert pianist Warren Mailley-Smith and focuses on the virtuoso concerto repertoire of the baroque, classical and early romantic periods.\r Here's a short video of the Piccadilly Sinfonietta performing:\r youtu.be/gN157xwtsnM\n\n\n\n\n",
          "links": []
        }
      ]
    }
  }
----------
END ENTRY
----------
"""
extract_agent.run_task(contents)