from typing import List
import asyncio
from langchain_core.messages import SystemMessage, HumanMessage

from models import embedding_model, index, llm

from chat_history import get_recent_history, store_message

from config import (
    ENABLE_CHAT_HISTORY
)

def retrieve_context(query: str, top_k: int = 8) -> str:
    query_embedding = embedding_model.encode(
        query,
        normalize_embeddings=True
    ).tolist()

    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )

    return "\n\n".join(
        match["metadata"]["text"]
        for match in results["matches"]
    )


async def chat_model(user_id: str, user_question: str) -> str:
    if ENABLE_CHAT_HISTORY:
        history = await asyncio.to_thread(get_recent_history, user_id)
    else:
        history = ""

    context = retrieve_context(user_question)

    messages = [
        SystemMessage(
            content=(
                "You are a friendly and helpful AI Internship Assistant on Discord.\n\n"

                "Your primary role is to answer questions for interns using ONLY the provided knowledge base context.\n"
                "When answering knowledge-related questions:\n"
                "- Use ONLY the information present in the context.\n"
                "- Do NOT mention phrases like 'based on the provided context' or 'according to the document'.\n"
                "- Respond naturally, as if you already know the information.\n"
                "- Be clear, concise, and friendly.\n\n"

                "If the answer to a knowledge-related question is NOT found in the context, respond politely with:\n"
                "'I don’t have that information in my knowledge base right now.'\n\n"

                "For casual or conversational messages (such as greetings, small talk, or friendly remarks like "
                "'hi', 'hello', 'hey', 'how are you', 'good morning'):\n"
                "- Respond warmly and naturally.\n"
                "- Do NOT say that the information is missing from the knowledge base.\n"
                "- Keep responses short and friendly.\n\n"

                "You must NEVER:\n"
                "- Make up information.\n"
                "- Use external knowledge.\n"
                "- Answer questions beyond the knowledge base.\n\n"

                "Your tone should feel like a real, approachable intern support assistant on Discord.\n\n" \
                "Note that the final answer should be in less than 2000 characters"
            )
        ),
        HumanMessage(
            content=f"Context:\n{context}\n\nUser message:\n{user_question}"
        )
    ]

    if history and ENABLE_CHAT_HISTORY:
        messages.append(
            HumanMessage(content=f"Conversation so far:\n{history}")
        )

    messages.append(
        HumanMessage(
            content=f"Knowledge Base Context:\n{context}\n\nUser Question:\n{user_question}"
        )
    )

    response = llm.invoke(messages).content.strip()

    # Store messages asynchronously
    if ENABLE_CHAT_HISTORY:
        await asyncio.to_thread(store_message, user_id, "user", user_question)
        await asyncio.to_thread(store_message, user_id, "assistant", response)

    return response