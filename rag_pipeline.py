from typing import List
from langchain_core.messages import SystemMessage, HumanMessage

from models import embedding_model, index, llm


def retrieve_context(query: str, top_k: int = 4) -> str:
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


def chat_model(user_question: str) -> str:
    context = retrieve_context(user_question)

    messages = [
        SystemMessage(
            content=(
                "You are an AI assistant for AI interns.\n"
                "Answer ONLY using the provided context.\n"
                "If the answer is not present, say:\n"
                "'I don't have that information in my knowledge base.'"
            )
        ),
        HumanMessage(
            content=f"Context:\n{context}\n\nQuestion:\n{user_question}"
        )
    ]

    return llm.invoke(messages).content.strip()
