from fpdf import FPDF
from typing import List, Dict
from autogen import register_function
import random

def generate_pastel_color():
    return (
        random.randint(180, 255),
        random.randint(180, 255),
        random.randint(180, 255),
    )

class CustomPDF(FPDF):
    def set_background_color(self, rgb):
        self.set_fill_color(*rgb)
        self.rect(0, 0, self.w, self.h, "F")

def qna_to_pdf(json_array: List[Dict], output_file: str = "qna_output.pdf") -> str:
    pdf = CustomPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for idx, qa_pair in enumerate(json_array):
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
        a_color = generate_pastel_color()
        pdf.add_page()
        pdf.set_background_color(a_color)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, f"Answer {idx + 1}", align="C", ln=True)
        pdf.ln(10)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, qa_pair["answer"])

    pdf.output(output_file)
    return output_file
