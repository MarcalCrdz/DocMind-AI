from pypdf import PdfReader

def load_pdf_text(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = " "

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"
        return text
    
if __name__ == "__main__":
    file_path = "data/raw/Curriculo_pedro_v2.pdf"

    text = load_pdf_text(file_path)

    print("Texto extraído com sucesso!")
    print(text[:1000])