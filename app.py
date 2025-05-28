# AIzaSyAEBvPQikDPLJGd010Nv4Q2ONi4NI6dXs8



# AIzaSyDJDWED2XmoaMDWlqsYux3vD9VWMRoTZuc

import json
import re
from fastapi.responses import JSONResponse
from google import genai
from google.genai import types
from pydantic import BaseModel
import prompt
import os
import saveAppointments
from fastapi import FastAPI, Request

app = FastAPI()

client = genai.Client(api_key="AIzaSyDJDWED2XmoaMDWlqsYux3vD9VWMRoTZuc")
# chat=client.chats.create(model="gemini-2.0-flash",config= types.GenerateContentConfig(
#             system_instruction=prompt.prompt1,temperature=0.3),)


chat_sessions = {} 
chat_histories = {}  

class UserMessage(BaseModel):
    message: str
    chatId: str

@app.post("/chat")
def chat_with_user(user_msg: UserMessage):
    chatId=user_msg.chatId
    if chatId  not in chat_sessions:
        chat_sessions[chatId] = client.chats.create(model="gemini-2.0-flash",config= types.GenerateContentConfig(
            system_instruction=prompt.prompt1,temperature=0.3),)
        chat_histories[chatId]=""
        
    chat=chat_sessions[chatId] # for continuty in the chat 
    history =chat_histories[chatId] # for storing the history

    response=chat.send_message(user_msg.message)
    bot_reply = response.text
    history += f'\nYou:{user_msg.message}\n Neko:{bot_reply}'
    chat_histories[chatId]=history
    
    # for auto saving
    auto_saved = False
    saved = None
    
    json_match = re.search(r'```json\s*(\{.*?\})\s*```', bot_reply, re.DOTALL)
    if json_match:
        try:
            json_obj=json.loads(json_match.group(1))
            json_obj['chat_id']=chatId
            required_fields = ["name", "appointment_type", "contact_number", "date", "time"]
            if all(json_obj.get(field) for field in required_fields):
                saved = saveAppointments.saveAppointments(json_obj)
                auto_saved=True
        except Exception as e:
            print("Error extracting JSON:", e)
    
     
    return {"response": bot_reply,"auto_saved": auto_saved,
        "saved_appointment": saved}


# @app.post("/save")
# def saveAppointment(user_msg: UserMessage):
#     chatId=user_msg.chatId
#     if chatId not in chat_histories:
#         return {"error": "No chat history found for this user."}
    
#     chat_history=chat_histories[chatId]
    
#     response = client.models.generate_content(
#         model="gemini-2.0-flash",
#         contents=chat_history,
#         config= types.GenerateContentConfig(
#             system_instruction=prompt.prompt2)
        
#     )
#     json_response = re.search(r'```json\s*(\{.*?\})\s*```', response.text, re.DOTALL).group(1)
#     savedAppointment = saveAppointments.saveAppointments(json_response,chatId)
#     return {"status": "Appointment saved", "data": savedAppointment}


@app.get("/getAllAppointments")
def getAllAppointments():
    try:
        if os.path.getsize('appointments.json') ==0:
            return JSONResponse(content=[],status_code=200)
        with open('appointments.json','r') as f:
            appointments = json.load(f)
            return appointments if appointments else ''
        
    except FileNotFoundError:
        return JSONResponse(content=[],status_code=200)
        
        
