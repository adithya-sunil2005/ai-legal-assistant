import pdfplumber

def extract_text_from_pdf(pdf_path):
    text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    return text


if __name__ == "__main__":
    pdf_file = "sample.pdf"   # Replace with your PDF file
    print(extract_text_from_pdf(pdf_file))