from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.ingestion.load_documents import load_pdf_text


def split_text(text: str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    chunks = splitter.split_text(text)
    
    return chunks

if __name__ == "__main__":
    file_path = "data/raw/Curriculo_pedro_v2.pdf"

    text = load_pdf_text(file_path)
    chunks = split_text(text)

    print(f"Total de chunks criados: {len(chunks)}")
    print("\nPrimeiro chunk")
    print(chunks[0])