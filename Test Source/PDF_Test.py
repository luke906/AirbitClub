
from fpdf import FPDF

class PDF_Manager(FPDF):
    def header(self):
        # Logo
        self.image('logo_pb.png', 5, 5, 30)
        self.add_font('nanum_bold', '', '../Core Class/nanum_bold.ttf', uni=True)
        self.set_font('nanum_bold', '', 35)
        # Move to the right
        self.cell(30)
        # Title
        self.set_draw_color(0, 80, 180)
        self.set_fill_color(230, 230, 0)
        self.set_text_color(0, 0, 0)
        self.set_line_width(1)
        self.cell(160, 20, 'AirBitClub  자금이체  보고서', 1, 1, 'C', 1)
        # Line break
        self.ln(20)

        self.set_title("Airbitclub_account_report")
        self.set_author('Luke LEE')

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        self.add_font('nanum_bold', '', '../Core Class/nanum_bold.ttf', uni=True)
        self.set_font('nanum_bold', '', 14)
        self.set_text_color(128)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def chapter_title(self, num, label):
        # Arial 12
        self.add_font('nanum_bold', '', '../Core Class/nanum_bold.ttf', uni=True)
        self.set_font('nanum_bold', '', 12)
        # Background color
        self.set_fill_color(200, 220, 255)
        # Title
        self.cell(0, 6, 'Chapter %d : %s' % (num, label), 0, 1, 'L', 1)
        # Line break
        self.ln(4)

    def user_chapter_title(self, chapter_contents):
        # Arial 12
        self.add_font('nanum_bold', '', '../Core Class/nanum_bold.ttf', uni=True)
        self.set_font('nanum_bold', '', 12)
        # Background color
        self.set_fill_color(200, 220, 255)
        # Title
        self.cell(0, 6, chapter_contents, 0, 1, 'L', 1)
        # Line break
        self.ln(4)

    def chapter_body(self, txt):
        # Read text file
        #with open(name, 'rb') as fh:
        #    txt = fh.read().decode('latin-1')
        # Times 12
        self.add_font('nanum_bold', '', '../Core Class/nanum_bold.ttf', uni=True)
        self.set_font('nanum_bold', '', 12)
        # Output justified text
        self.multi_cell(0, 5, txt)
        # Line break
        self.ln()
        # Mention in italics
        self.add_font('nanum_bold', '', '../Core Class/nanum_bold.ttf', uni=True)
        self.set_font('nanum_bold', '', 12)
        #self.cell(0, 5, '(end of excerpt)')

    def print_chapter(self, num, title, name):
        self.add_page()
        self.chapter_title(num, title)
        self.chapter_body(name)

    def print_chapter_user(self, title, contents):
        self.user_chapter_title(title)
        self.chapter_body(contents)

# Instantiation of inherited class

pdf = PDF_Manager()

#pdf.print_chapter(1, 'A RUNAWAY REEF', '보고서1\n보고서2\n보고서3\n보고서4\n')
#pdf.print_chapter(2, 'THE PROS AND CONS', '보고서2')
pdf.add_page()
pdf.print_chapter_user('※ 전 계좌 이체 현황 ※', '보고서1\n보고서2\n보고서3\n보고서4\n')
pdf.output('계좌현황 보고서.pdf', 'F')