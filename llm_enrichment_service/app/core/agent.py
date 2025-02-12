from vertexai.generative_models import (
    FunctionDeclaration,
    Tool,
    GenerationResponse,
    ToolConfig,
    GenerativeModel,
)
from datetime import datetime
from abc import ABC, abstractmethod
from app.core.agent_config import AgentConfig
from typing import List, Any
import logging


class Agent(ABC):
    def __init__(self, task):
        self.agent_config = AgentConfig().get_config(task)
        self.model = GenerativeModel(
            model_name=self.agent_config["model_name"],
            system_instruction=self.agent_config["system_instruction"],
        )

    def generate_response(
        self,
        contents: List[str],
        tools: List[Any] = None,
        tool_config: ToolConfig = None,
    ):
        try:
            response = self.model.generate_content(
                contents, tools=tools, tool_config=tool_config
            )
            logging.info("Response generated")
            return response
        except Exception as e:
            logging.error(f"Error generating response {e}")
            raise

    @abstractmethod
    def run_task(self):
        raise NotImplementedError(
            "Agent subclasses must implement the `run_task` method"
        )


class AgentWithTools(Agent):
    def __init__(self, task):
        super().__init__(task)

    def create_tools(self, function_declarations) -> List[Tool]:
        return [Tool(function_declarations=function_declarations)]

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
            return (
                dict(first_part.function_call.args)
                if first_part.function_call.args
                else None
            )
        except ValueError as e:
            logging.error(f"Error processing response: {e}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return None


class EventInfoExtractionAgent(AgentWithTools):
    def __init__(self):
        super().__init__(task="EXTRACT_EVENT_INFO")

    def _create_extract_function_declaration(self) -> FunctionDeclaration:
        function = FunctionDeclaration(
            name="get_event_data",
            description="Extract and structure event information from a given entry",
            parameters={
                "type": "object",
                "properties": {
                    "tag": {
                        "type": "string",
                        "nullable": False,
                        "description": "A category tag for the event, must be one from the provided list: Arts, Children's Channel, Community Support, Festive, Health & Sport, Music, Playtime, Skill & Professional Development, Social, Workshop",
                    },
                    "event_name": {
                        "type": "string",
                        "nullable": False,
                        "description": "Title or name of the event",
                    },
                    "description": {
                        "type": "string",
                        "nullable": True,
                        "description": "A 1-2 sentence description of the event based on the provided information in the entry or null",
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
                    "is_within_2_weeks": {
                        "type": "boolean",
                        "nullable": False,
                        "description": f"True if the domain name is wherecanwego.com or if date and time of event is within 2 weeks of {datetime.now().strftime('%d %b %Y')}. False otherwise",
                    },
                },
                "required": [
                    "tag",
                    "event_name",
                    "description",
                    "date_and_time",
                    "location",
                    "cost",
                    "booking_details",
                    "is_within_2_weeks",
                ],
            },
        )
        return function

    def run_task(self, contents: str):
        extract_function = self._create_extract_function_declaration()
        tools = self.create_tools(function_declarations=[extract_function])
        tool_config = ToolConfig(
            function_calling_config=ToolConfig.FunctionCallingConfig(
                mode=ToolConfig.FunctionCallingConfig.Mode.ANY,
                allowed_function_names=["get_event_data"],
            )
        )
        res = self.generate_response(
            contents=contents, tools=tools, tool_config=tool_config
        )
        output = self._get_function_output(res)
        return output


class EventResearchAgent(AgentWithTools):
    def __init__(self):
        super().__init__(task="RESEARCH_EVENTS")

    def _create_event_research_function_declaration(self) -> FunctionDeclaration:
        function = FunctionDeclaration(
            name="extract_event_info_from_html",
            description="Process HTML structure of page and extract information in a structured format",
            parameters={
                "type": "object",
                "properties": {
                    "events": {
                        "type": "array",
                        "description": "List of events",
                        "items": {
                            "type": "object",
                            "properties": {
                                "title": {
                                    "type": "string",
                                    "description": "Title or name of the event",
                                },
                                "content": {
                                    "type": "string",
                                    "description": "Additional text from the HTML relating to details of the event",
                                },
                                "event_details": {
                                    "type": "object",
                                    "properties": {
                                        "sections": {
                                            "type": "array",
                                            "description": "Details about the event in sections, typically in a list type structure (for example in <li> elements or a set of divs)",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "content": {
                                                        "type": "string",
                                                        "description": "Text content of the section",
                                                    },
                                                    "links": {
                                                        "type": "array",
                                                        "description": "List of links in this section, extracted from <a> elements",
                                                        "items": {
                                                            "type": "string",
                                                            "format": "uri",
                                                        },
                                                    },
                                                },

                                            },
                                        }
                                    },
                                    "required": ["sections"],
                                },
                            },
                            "required": ["title", "content", "event_details"],
                        },
                    }
                },
                 "required": ["events"],
            },
        )
        return function
    def run_task(self, contents:str):
        research_function=self._create_event_research_function_declaration()
        tools=self.create_tools(function_declarations=[research_function])
        tool_config = ToolConfig(
            function_calling_config=ToolConfig.FunctionCallingConfig(
                mode=ToolConfig.FunctionCallingConfig.Mode.ANY,
                allowed_function_names=["extract_event_info_from_html"],
            )
        )
        res = self.generate_response(
            contents=contents, tools=None, 
        )
        print(res)
        output = self._get_function_output(res)
        return output


