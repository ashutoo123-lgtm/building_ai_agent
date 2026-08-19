import json
import os
from .Tools import calculate_sum
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import AsyncOpenAI
from pydantic import BaseModel , Field
from .TOOL_SCHEMA import TOOLS
from typing import Annotated , Literal , Union

load_dotenv()

API_KEY = os.getenv("NVIDIA-API-KEY")

if not API_KEY:
    raise RuntimeError("NVIDIA-API-KEY not found in environment")


client = AsyncOpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=API_KEY,
)


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SendPrompt(BaseModel):
    prompt: str


class StructuredResponse(BaseModel):
    action : Literal["nameandlanguage"]
    name: str
    language : str
class weather(BaseModel):
    action : Literal["weather"] = "weather"
    location: str
    weather : str
UnifiedOutputUnion = Annotated[Union[StructuredResponse, weather], Field(discriminator="action")]    
class CombinedResponseContainer(BaseModel):
    data: UnifiedOutputUnion

class calculation_structured_output(BaseModel):
    tool_used : str| None
    action : str | None
    name : str | None

    a : int 
    b : int
    expression : str | None
    result : float | None
   
@app.post("/chat")
async def here_send_llm_request(request: SendPrompt):
    messages  = [
                {
                    "role": "system",
                    "content": "You are an helpful assitant given tools when required"
                },
                {
                    "role": "user",
                    "content": request.prompt
                }
            ]


    try:
        response = await client.chat.completions.create(
            model="nvidia/nemotron-3-ultra-550b-a55b",
            messages=messages,
            # response_format={
            #     "type": "json_schema",
            #     "json_schema": {
            #         "name": "structured_response",
            #         "schema": StructuredResponse.model_json_schema()
            #     }
            # },
            tools= TOOLS,
            tool_choice= "auto",
        
        )
        Content = response.choices[0].message
        if Content.tool_calls:

            tool_call = Content.tool_calls[0]
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            if tool_name == "calculate_sum":


                tool_result = calculate_sum(arguments["a"],arguments["b"],arguments["expression"]) 
            else:    
                raise ValueError(f"tool name {tool_name} is not valid")
            

            messages.append(Content)
            messages.append({"role": "tool",
                             "tool_call_id" : tool_call.id,
                             "content" : json.dumps(tool_result)})
            RESPONSE = await client.chat.completions.parse(model="nvidia/nemotron-3-ultra-550b-a55b",
                        messages=messages,
                        response_format= calculation_structured_output,
                        
                        
                        
                        
                        
                    )
            return (RESPONSE.choices[0].message.parsed)
        else :
            output =  await client.chat.completions.parse(model="nvidia/nemotron-3-ultra-550b-a55b",
                                                          
                        messages= [
                {
                    "role": "system",
                    "content": "You are an helpful assitant given tools when required"
                },
                {
                    "role": "user",
                    "content": request.prompt
                }
            ],
                  response_format   = CombinedResponseContainer, 



                        
                        
                        )  
            return (output.choices[0].message.parsed)
        
    
    
          

    



    except Exception as exc :
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )
    
       