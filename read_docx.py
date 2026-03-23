import docx

def extract_text(file_path):
    doc = docx.Document(file_path)
    with open("doc_content.txt", "w", encoding="utf-8") as f:
        for i, para in enumerate(doc.paragraphs):
            text = para.text.strip()
            if text:
                f.write(f"[{i}]: {text}\n")

extract_text('ieee-conference-template...docx')
