from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.style import WD_STYLE_TYPE

class StyleManager:
    def __init__(self, document):
        self.document = document

    def create_or_update_style(self, style_name, font_name, font_size, font_color=RGBColor(0, 0, 0), bold=False, italic=False):
        styles = self.document.styles
        if style_name in styles:
            style = styles[style_name]
        else:
            style = styles.add_style(style_name, WD_STYLE_TYPE.PARAGRAPH)
        
        font = style.font
        font.name = font_name
        font.size = Pt(font_size)
        font.color.rgb = font_color
        font.bold = bold
        font.italic = italic

    def apply_styles(self):
        self.create_or_update_style("Title", "Arial", 28, bold=True)
        self.create_or_update_style("Heading 1", "Arial", 18, bold=True)
        self.create_or_update_style("Heading 2", "Arial", 16, bold=True)
        self.create_or_update_style("Normal", "Arial", 12)

    def apply_style_to_paragraph(self, paragraph, style_name):
        paragraph.style = self.document.styles[style_name]