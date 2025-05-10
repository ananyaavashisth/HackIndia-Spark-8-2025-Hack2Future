from fastapi import FastAPI, UploadFile, File, Form
from app.chat import (
    unified_search, add_pdf_to_vectorstore, load_faqs_to_vectorstore,
    add_to_chat_history, get_chat_history
)
from app.reminders import create_reminder
from app.food import find_best_food_nearby
from app.chai import detect_chai_break
from app.forms import autofill_form
from app.voice import transcribe_audio
from app.hate_speech import detect_hate_speech

GOOGLE_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSezQ24GhKxSiiupKbhsKbkORkHQEqbZjqo9zYAjJdhsW3e72Q/viewform?usp=dialog"  # Replace with your actual Google Form link
ANTI_RAGGING_CONTACTS = """
Anti-Ragging Committee:
- Phone: +91-1234567890
- Email: antiragging@college.edu
"""

def get_hate_speech_response():
    return {
        "response": (
            "Your message has been flagged as a serious issue. Please select an option below to proceed:\n"
            "1. [Report Bullying]({form_url}?issue=bullying)\n"
            "2. [Report Harassment]({form_url}?issue=harassment)\n"
            "3. [File a Complaint]({form_url}?issue=complaint)\n"
            "4. [Others]({form_url}?issue=others)\n\n"
            "After submitting the form, you will receive the contact details of the anti-ragging committee."
        ).format(form_url=GOOGLE_FORM_URL),
        "contacts": ANTI_RAGGING_CONTACTS
    }

app = FastAPI()

@app.on_event("startup")
def startup_event():
    load_faqs_to_vectorstore()

@app.post("/chat")
async def chat(
    message: str = Form(...),
    website_url: str = Form(None),
    user_id: str = Form("default_user")
):
    # 1. Hate speech detection FIRST
    if detect_hate_speech(message):
        add_to_chat_history(user_id, "user", message)
        hate_response = get_hate_speech_response()
        add_to_chat_history(user_id, "bot", hate_response["response"])
        return {
            "response": hate_response["response"],
            "contacts": hate_response["contacts"],
            "history": get_chat_history(user_id)
        }
    # 2. Chai break detection
    chai = detect_chai_break(message)
    add_to_chat_history(user_id, "user", message)
    if chai:
        add_to_chat_history(user_id, "bot", chai)
        return {"response": chai, "history": get_chat_history(user_id)}
    # 3. Normal chatbot logic (with memory)
    answer = unified_search(message, website_url, user_id)
    add_to_chat_history(user_id, "bot", answer)
    return {"response": answer, "history": get_chat_history(user_id)}

@app.post("/voice")
async def voice(file: UploadFile = File(...), user_id: str = Form("default_user")):
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    text = transcribe_audio(file_path)
    add_to_chat_history(user_id, "user", text)
    chai = detect_chai_break(text)
    if chai:
        add_to_chat_history(user_id, "bot", chai)
        return {"response": chai, "history": get_chat_history(user_id)}
    add_to_chat_history(user_id, "bot", text)
    return {"response": text, "history": get_chat_history(user_id)}

@app.post("/reminder")
async def reminder(text: str = Form(...), time: str = Form(...)):
    link = create_reminder(text, time)
    return {"response": link}

@app.post("/food")
async def food(query: str = Form(...), location: str = Form("12.9716,77.5946")):
    result = find_best_food_nearby(query, location)
    return {"response": result}

@app.post("/form")
async def form(form_type: str = Form(...), name: str = Form(...)):
    result = autofill_form(form_type, {"name": name})
    return {"response": result}