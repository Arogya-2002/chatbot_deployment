import sys
from src.Exceptions import CustomException
from src.Logs import logging
from src.constants import OLLAMA_API, OLLAMA_VIA_OPENAI, HEADERS, MODEL

class OllamaClient:
    def __init__(self):
        pass

    def answer_resume_question(self, question, resume_text, history):
        try:
            logging.info("Question is loaded")

            # Ensure non-empty inputs
            if not question or not resume_text:
                raise ValueError("Question and resume text cannot be empty")

            prompt = (
                f"The following is a resume text:\n\n{resume_text}\n\n"
                f"Answer the following question based on the resume content:\n\n"
                f"Question: {question}\n\nAnswer:"
            )

            response = OLLAMA_VIA_OPENAI.completions.create(
                model=MODEL,
                prompt=prompt,
                max_tokens=150,
                temperature=0.6
            )

            answer = response.choices[0].text.strip()

            history.append({"role": "user", "content": question})
            history.append({"role": "assistant", "content": answer})

            logging.info("Response generated successfully")
            return answer, history

        except Exception as e:
            logging.error(f"Error during completion request: {e}")
            raise CustomException(e, sys)
