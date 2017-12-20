from fpdf import FPDF

class PDF_Manager:

    def __init__(self):
        self.pdf = FPDF()
        self.pdf.add_page()
        self.pdf.add_font('nanum_bold', '', '../Core Class/nanum_bold.ttf', uni=True)
        self.pdf.set_font('nanum_bold', '', 14)

    def write_pdf(self, contents, line):
        self.pdf.ln(line)
        self.pdf.write(5, contents)
        self.pdf.output("account_report.pdf", 'F')

