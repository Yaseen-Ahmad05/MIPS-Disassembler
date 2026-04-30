from docx import Document
doc = Document('report.docx')
for i, p in enumerate(doc.paragraphs):
    if p.text.strip():
        print(f"{i}: {p.text}")
