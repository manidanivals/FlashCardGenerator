import json

from fpdf import FPDF
from typing import List, Dict

from packaging.markers import Operator
from pydantic import BaseModel, Field
import random

from typing_extensions import Annotated


def generate_pastel_color():
    return (
        random.randint(180, 255),
        random.randint(180, 255),
        random.randint(180, 255),
    )
class FlashcardInput(BaseModel):
    json_array: Annotated[str, Field(description="The string that contains a json list entity that will be used to make the questions and answers")]
    output_file: Annotated[str, Field(description="the name of the file that will be outputted")]

class CustomPDF(FPDF):
    def set_background_color(self, rgb):
        self.set_fill_color(*rgb)
        self.rect(0, 0, self.w, self.h, "F")

def qna_to_pdf(json_array: str, output_file: str = "qna_output.pdf") -> str:
    json_array_deserialize = json.loads(json_array)  # Convert to Python object

    pdf = CustomPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for idx, qa_pair in enumerate(json_array_deserialize):
        # Add Question page
        q_color = generate_pastel_color()
        pdf.add_page()
        pdf.set_background_color(q_color)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, f"Question {idx + 1}", align="C", ln=True)
        pdf.ln(10)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, qa_pair["question"])

        # Add Answer page
        pdf.add_page()
        pdf.set_background_color(q_color)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, f"Answer {idx + 1}", align="C", ln=True)
        pdf.ln(10)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, qa_pair["answer"])

    pdf.output(output_file)
    return output_file
