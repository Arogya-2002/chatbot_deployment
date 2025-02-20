import gradio as gr
import os
import sys
from src.Exceptions import CustomException
from src.Logs import logging
from src.components.pdf_utils import PdfExtraction
from src.components.ollama_client import OllamaClient

class GradioInterface:
    def __init__(self):
        pass

    def chat_with_resume_qa(self, pdf_file, question, history):
        try:
            logging.info("The chat has started")

            # Ensure history is a list (if None, initialize as an empty list)
            history = history or []
        
            pe = PdfExtraction()
            logging.info("PdfExtraction object created successfully")

            # Extract the text from the PDF
            resume_text = pe.extract_text_from_pdf(pdf_file.name)
        

            if "Error" in resume_text or "No extractable text found" in resume_text:
                print(f"PDF extraction error: {resume_text}")  # Log extraction error
                return resume_text, history
        
            ol = OllamaClient()
            logging.info("OllamaClient object created successfully")

            # Call the function to generate an answer based on the resume
            response, history = ol.answer_resume_question(question, resume_text, history)
            return response, history
        except Exception as e:
            raise CustomException(e,sys)

gi = GradioInterface()

# Initialize the Gradio interface for resume-based Q&A
gr.Interface(
    fn=gi.chat_with_resume_qa,
    inputs=[
        gr.File(label="Upload Your Resume (PDF)", type="filepath"),
        gr.Textbox(label="Ask a Question about the Resume", placeholder="Enter your question...", lines=2),
        gr.State()  # State object for maintaining conversation history
    ],
    outputs=[
        gr.Textbox(label="Assistant's Answer", interactive=False),
        gr.State()  # Updated state for conversation history
    ],
    live=False,  # Disable real-time submission
    title="Resume Q&A Chatbot",
    description="Upload your resume and ask questions about it. The chatbot will answer based on the resume content.",
    allow_flagging="never"
).launch(share=True)
