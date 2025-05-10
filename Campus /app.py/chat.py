import json
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import OpenAI
from app.utils import get_env_var

# Initialize embedding model
embeddings = OpenAIEmbeddings(openai_api_key=get_env_var("OPENAI_API_KEY"))
vectorstore = Chroma(persist_directory="./faqs", embedding_function=embeddings)

# Dictionary to hold conversation memory per user
user_memories = {}

def load_faqs_to_vectorstore():
    with open("data/faqs.json", "r") as f:
        faqs = json.load(f)
    texts = [
        f"{item.get('question', '').strip()} {item.get('answer', '').strip()}"
        for item in faqs
    ]
    metadatas = [{"source": "FAQ"} for _ in texts]
    vectorstore.add_texts(texts, metadatas=metadatas)

def add_pdf_to_vectorstore(chunks, source_name):
    metadatas = [{"source": source_name}] * len(chunks)
    vectorstore.add_texts(chunks, metadatas=metadatas)

def get_user_memory(user_id):
    if user_id not in user_memories:
        user_memories[user_id] = ConversationBufferMemory(return_messages=True)
    return user_memories[user_id]

def get_chat_history(user_id):
    memory = get_user_memory(user_id)
    return [{"role": m.type, "content": m.data["content"]} for m in memory.chat_memory.messages]

def add_to_chat_history(user_id, role, message):
    memory = get_user_memory(user_id)
    if role == "user":
        memory.chat_memory.add_user_message(message)
    elif role == "ai":
        memory.chat_memory.add_ai_message(message)

def unified_search(query, website_url=None, user_id=None):
    memory = get_user_memory(user_id)
    llm = OpenAI(model="gpt-3.5-turbo", openai_api_key=get_env_var("OPENAI_API_KEY"))

    chain = ConversationalRetrievalChain.from_llm(
        llm, retriever=vectorstore.as_retriever(), memory=memory
    )

    result = chain({"question": query, "chat_history": memory.buffer})
    answer = result.get("answer", "").strip()

    # Fallback logic if answer is not useful
    if not answer or any(x in answer.lower() for x in ["i don't know", "sorry"]):
        from app.wiki import search_wikipedia
        wiki_result = search_wikipedia(query)
        if wiki_result:
            return f"**From Wikipedia:**\n{wiki_result}"

        if website_url:
            from app.web_reader import extract_text_from_url
            web_text = extract_text_from_url(website_url)
            if web_text:
                return f"**From {website_url}:**\n{web_text}"

        return "Sorry, I couldn't find an answer."

    return answer