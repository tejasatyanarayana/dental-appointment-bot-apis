import json,os

file_path = "appointments.json"

def saveAppointments(response,chatId):
    

    if os.path.exists(file_path):
        with open(file_path,'r') as f:
            try:
                appointments=json.load(f)
            except json.JSONDecodeError:
                appointments=[]
                
    else:
        appointments=[]

    new_appointment=json.loads(response)
    new_appointment["chat_id"] = chatId
    existing_appointment=False
    for i,appointment in enumerate(appointments):
        if appointment.get("chat_id") == new_appointment.get("chat_id"):
            appointments[i]=new_appointment
            existing_appointment=True
            break
        
    if not existing_appointment:
        appointments.append(new_appointment)

    with open(file_path,'w') as f:
        json.dump(appointments,f,indent=2)
        
    print("Appointment added to appointments.json")

    return new_appointment