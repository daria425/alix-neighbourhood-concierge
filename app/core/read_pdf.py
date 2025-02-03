from pypdf import PdfReader
from response_generator import ResponseGenerator
from vertexai.generative_models import Part, FunctionDeclaration, ToolConfig, Tool
from datetime import datetime
from dotenv import load_dotenv
import os
load_dotenv()
input_file_path=os.getenv("SAMPLE_PDF_URI")

prompt = """
You are a very professional document information extraction specialist. 
The document contains a table with a schedule of events. 
Please extract the tabular data
"""
extraction_function=FunctionDeclaration(
        name="get_event_data",
        description="Extract and structure event information from the table",
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
                "is_within_2_weeks":{
                    "type":"boolean", 
                    "nullable":False,
                    "description":f"True if the domain name is wherecanwego.com or if date and time of event is within 2 weeks of {datetime.now().strftime('%d %b %Y')}. False otherwise"
                }
            },
            "required": ["tag","event_name", "description", "date_and_time", "location", "cost", "is_within_2_weeks"],
        })
tool_config=ToolConfig(function_calling_config=ToolConfig.FunctionCallingConfig(
            mode=ToolConfig.FunctionCallingConfig.Mode.ANY,
            allowed_function_names=["get_event_data"]))
tools=[Tool(function_declarations=[extraction_function])]
pdf_file = Part.from_uri(
    uri=input_file_path,
    mime_type="application/pdf",
)
print(pdf_file)
contents = [pdf_file, prompt]
model_name="gemini-1.5-flash-002"
res=ResponseGenerator().generate_response(model_name=model_name, system_instruction=None, tools=tools, tool_config=tool_config, contents=contents)
print(res)