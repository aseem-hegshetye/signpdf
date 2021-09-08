from pdfminer import high_level
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import resolve1
from pdfminer.pdfparser import PDFParser


class PdfUtilities:

    def get_total_number_of_pages(self, pdf_file_name):
        with open(pdf_file_name, 'rb') as file:
            parser = PDFParser(file)
            document = PDFDocument(parser)
            total_pages = resolve1(document.catalog['Pages'])['Count']

        return total_pages

    def get_text_for_a_page(self, pdf_file_name, page_num):
        text = high_level.extract_text(
            pdf_file_name, "", page_num
        )
        return text

    def get_page(self, pdf_file_name, page_num):
        return high_level.extract_pages(pdf_file_name, page_numbers=page_num)
