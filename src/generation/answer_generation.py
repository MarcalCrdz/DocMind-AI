from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

from src.retrieval.retriever import search_documents


MODEL_NAME = "google/flan-t5-base"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)


def clean_context(text: str) -> str:
    lines = text.splitlines()
    cleaned_lines = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if line.isdigit():
            continue

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def clean_answer(answer: str) -> str:
    answer = answer.strip()

    answer = answer.replace(" • ", "\n- ")
    answer = answer.replace("• ", "\n- ")

    if "\n-" in answer and not answer.startswith("-"):
        answer = "- " + answer

    return answer.strip()


def format_sources(results: dict):
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    formatted_sources = []

    for doc, metadata, distance in zip(documents, metadatas, distances):
        preview = doc[:400].replace("\n", " ")

        formatted_sources.append({
            "source": metadata.get("source"),
            "document_id": metadata.get("document_id"),
            "chunk_id": metadata.get("chunk_id"),
            "distance": distance,
            "preview": preview
        })

    return formatted_sources


def generate_answer(
    question: str,
    n_results: int = 1,
    document_id: str | None = None
) -> dict:
    results = search_documents(
        query=question,
        n_results=n_results,
        document_id=document_id
    )

    retrieved_docs = results["documents"][0]
    formatted_sources = format_sources(results)

    context = "\n\n".join(clean_context(doc) for doc in retrieved_docs)

    prompt = f"""
You are DocMind AI, an assistant that answers questions based on documents.

Use only the context below to answer the question.
Answer in Portuguese using bullet points when possible.
Be clear, concise and organized.
Do not invent information that is not in the context.

Context:
{context}

Question:
{question}

Answer:
"""

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        max_length=1024,
        truncation=True
    )

    outputs = model.generate(
        **inputs,
        max_new_tokens=200,
        num_beams=4,
        do_sample=False
    )

    answer = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    answer = clean_answer(answer)

    return {
        "question": question,
        "answer": answer,
        "sources": formatted_sources,
        "model": MODEL_NAME,
        "document_id": document_id
    }


if __name__ == "__main__":
    question = "Quais informações adicionais aparecem no currículo?"

    result = generate_answer(
        question=question,
        n_results=1,
        document_id=None
    )

    print("\nPergunta:")
    print(result["question"])

    print("\nResposta:")
    print(result["answer"])

    print("\nFontes usadas:")
    for source in result["sources"]:
        print("\n---")
        print(source)