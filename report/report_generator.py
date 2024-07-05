from docx import Document
from docx.shared import Inches, Pt
from docx.enum.style import WD_STYLE_TYPE
from tkinter import filedialog, messagebox
import io

class ReportGenerator:
    def __init__(self, intro_tab, param_tab, results_tab):
        self.intro_tab = intro_tab
        self.param_tab = param_tab
        self.results_tab = results_tab

    def generate(self):
        try:
            doc = Document('template.docx')

            # Add introduction section
            self.add_introduction_section(doc)

            # Add parameter sets section
            self.add_parameter_sets_section(doc)

            # Add results section
            self.add_results_section(doc)

            # Save the document
            self.save_document(doc)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while generating the report: {str(e)}")

    def add_introduction_section(self, doc):
        self.replace_placeholder(doc, "[strategy_name]", self.intro_tab.get_strategy_name())
        self.replace_placeholder(doc, "[target_performance_parameter]", self.intro_tab.get_target_performance())
        self.replace_placeholder(doc, "[optimisation_method]", self.intro_tab.get_optimisation_method())
        self.add_intro_table(doc)

    def add_parameter_sets_section(self, doc):
        self.add_parameter_table(doc)
        
    def add_results_section(self, doc):
        self.add_results(doc)
        

    def add_results(self, doc):
        for i, paragraph in enumerate(doc.paragraphs):
            if "[results_table]" in paragraph.text:
                # Create a new style for market titles
                self.create_market_title_style(doc)

                results_data = self.results_tab.get_results_data()

                # Insert content before the placeholder paragraph
                for index, (market, data) in enumerate(results_data.items(), start=1):
                    # Add market title with numbering
                    market_title = doc.add_paragraph(f"3.{index} {market}", style='MarketTitle')
                    paragraph._element.addnext(market_title._element)

                    # Add Equity Curve image
                    if data['equity_curve']:
                        image_stream = io.BytesIO(data['equity_curve'])
                        img_paragraph = doc.add_paragraph()
                        img_paragraph.add_run().add_picture(image_stream, width=Inches(6))
                        market_title._element.addnext(img_paragraph._element)

                    # Add Performance Metrics image
                    if data['performance_metrics']:
                        image_stream = io.BytesIO(data['performance_metrics'])
                        img_paragraph = doc.add_paragraph()
                        img_paragraph.add_run().add_picture(image_stream, width=Inches(6))
                        market_title._element.addnext(img_paragraph._element)

                    # Add notes
                    if data['notes']:
                        notes_paragraph = doc.add_paragraph(data['notes'])
                        market_title._element.addnext(notes_paragraph._element)

                    # Add an empty paragraph for spacing between markets
                    spacing_paragraph = doc.add_paragraph()
                    market_title._element.addnext(spacing_paragraph._element)

                # Remove the original placeholder paragraph
                p = paragraph._element
                p.getparent().remove(p)
                break


    def create_market_title_style(self, doc):
        styles = doc.styles
        market_title_style = styles.add_style('MarketTitle', WD_STYLE_TYPE.PARAGRAPH)
        font = market_title_style.font
        font.name = 'Arial'
        font.size = Pt(16)
        font.bold = False

    def replace_placeholder(self, doc, placeholder, replacement):
        for paragraph in doc.paragraphs:
            if placeholder in paragraph.text:
                paragraph.text = paragraph.text.replace(placeholder, replacement)

        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        if placeholder in paragraph.text:
                            paragraph.text = paragraph.text.replace(placeholder, replacement)

    def add_intro_table(self, doc):
        for paragraph in doc.paragraphs:
            if "[intro_table]" in paragraph.text:
                table = doc.add_table(rows=1, cols=5)
                table.style = 'Table Grid'
                
                # Add headers
                headers = ["Market", "Timeframe", "Data Source", "Optimisation Timespan", "Out-of-Sample Timespan"]
                for i, header in enumerate(headers):
                    table.cell(0, i).text = header

                # Add data
                for row_data in self.intro_tab.get_intro_table_data():
                    cells = table.add_row().cells
                    for i, value in enumerate(row_data):
                        cells[i].text = str(value)

                # Replace the placeholder paragraph with the table
                p = paragraph._element
                p.getparent().replace(p, table._element)
                break

    def add_parameter_table(self, doc):
        for paragraph in doc.paragraphs:
            if "[parameter_set_table]" in paragraph.text:
                table = doc.add_table(rows=1, cols=7)
                table.style = 'Table Grid'
                
                # Add headers
                headers = ["Name", "Description", "Default", "Start", "Step", "End", "Best"]
                for i, header in enumerate(headers):
                    table.cell(0, i).text = header

                # Add data
                for row_data in self.param_tab.get_parameter_data():
                    cells = table.add_row().cells
                    for i, value in enumerate(row_data):
                        cells[i].text = str(value)

                # Replace the placeholder paragraph with the table
                p = paragraph._element
                p.getparent().replace(p, table._element)
                break

    def save_document(self, doc):
        save_path = filedialog.asksaveasfilename(defaultextension=".docx")
        if save_path:
            doc.save(save_path)
            messagebox.showinfo("Success", "Report generated successfully!")
        else:
            messagebox.showwarning("Cancelled", "Report generation cancelled.")
