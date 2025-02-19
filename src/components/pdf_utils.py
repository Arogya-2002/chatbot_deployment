from openai import OpenAI
import subprocess
import fitz
import sys

from src.Exceptions import CustomException
from src.Logs import logging

class PdfExtraction:
    def __init__(self):
        logging.info("Pulling the Ollama model")
        self.result = subprocess.run(["ollama", "pull", "llama3.2"], capture_output=True, text=True, encoding='utf-8')
        
        # Check if the command was successful
        if self.result.returncode == 0:
            logging.info("Model pulled successfully!")
        else:
            logging.error(f"Error pulling model: {self.result.stderr}")

    def extract_text_from_pdf(self, pdf_file, max_pages=7):
        try:
            logging.info("Extracting text from pdf")
            doc = fitz.open(pdf_file)
            text = ""
            page_count = min(doc.page_count, max_pages)

            for page_num in range(page_count):
                page = doc.load_page(page_num)
                text += page.get_text("text")

            return text.strip() if text.strip() else "No extractable text found in the PDF."

        except Exception as e:
            logging.error(f"Error during PDF extraction: {e}")
            raise CustomException(e, sys)
