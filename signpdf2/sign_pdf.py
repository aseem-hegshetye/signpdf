import datetime

import PyPDF2
from reportlab.pdfgen import canvas

from signpdf2.create_tmp_file import CreateTmpFileMixin
from signpdf2.pdf_utilites import PdfUtilities


class SignPdf(PdfUtilities,
              CreateTmpFileMixin):
    """
    Sign a pdf with signature image at desired location.
    we use units instead of pixel. Units are pdf-standard units (1/72 inch)
    """

    def __init__(self, sign_w: int, sign_h: int,
                 page_num: int, offset_x: int, offset_y: int,
                 pdf_file: str, signature_file: str):
        """
        :param sign_w: signature width in units
        :param sign_h: signature height in units
        :param pdf_file:  name and path of pdf file on local system
        :param signature_file: name and path of signature image file
        :param page_num: page number of pdf to sign. Index starts at 0
        :param offset_x: offset units horizontally from left
        :param offset_y: offset units vertically from bottom
        """
        self.sign_w = sign_w
        self.sign_h = sign_h
        self.page_num = page_num
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.pdf_file = pdf_file
        self.signature_file = signature_file

    def sign_pdf(self, sign_date: bool = True):
        """
        Draw signature on a temporary empty single page pdf.
        Then merge this page with original pdf page. If signature is needed
        on 2nd page, then merge this temp signed page on page2.

        :param sign_date: Bool. If true, then add current timestamp below
            signature
        :return: PdfFileWriter object with signed pdf
        """
        writer = PyPDF2.PdfFileWriter()
        pdf_reader = self.get_pdf_file_reader()

        for i in range(0, pdf_reader.getNumPages()):
            orignal_pdf_page = pdf_reader.getPage(i)

            if i == self.page_num:
                temp_signature_pdf = self.create_tmp_file()

                self.draw_signature_on_pdf(
                    temp_signature_pdf,
                    page_size=orignal_pdf_page.cropBox,
                    sign_date=sign_date
                )

                # Merge signed temp PDF in to original page
                signed_pdf_reader = self.get_pdf_file_reader(temp_signature_pdf)
                signed_page = signed_pdf_reader.getPage(0)
                orignal_pdf_page = self.merge_two_pdf_pages(orignal_pdf_page,
                                                            signed_page)

            writer.addPage(orignal_pdf_page)

        return writer

    def get_pdf_file_reader(self, file: str = None):
        """
        :param file: pdf file name with path
        :return: file reader object , keeping file open in read mode. if we
        close the file, then that pdf_reader is of no use
        """
        if file is None:
            file = self.pdf_file

        pdf_file = open(file, 'rb')
        return PyPDF2.PdfFileReader(pdf_file)

    def merge_two_pdf_pages(
            self,
            page1: PyPDF2.pdf.PageObject,
            page2: PyPDF2.pdf.PageObject
    ) -> PyPDF2.pdf.PageObject:
        """
        Merge page2 in page1
        :param page1: pdf page - PyPDF2.pdf.PageObject
        :param page2: pdf page
        :return: page1 after page2 is merged in it
        """
        page2.mediaBox = page1.mediaBox
        page1.mergePage(page2)
        return page1

    def get_current_timestamp_str(self):
        return datetime.datetime.now().strftime(
            "%m-%d-%Y - %H:%M"
        )

    def draw_signature_on_pdf(
            self,
            pdf_file_name,
            page_size,
            sign_date
    ):
        """
        Draw signature on a pdf page , same size as page_size.
        Create canvas of page_size for pdf_file_name, draw signature,
        add timestamp and save it.
        :param pdf_file_name: name of pdf_file where signature is drawn
        :param page_size: size of canvas to draw on
        :param sign_date: bool - if True,add timestamp under signature
        """
        c = canvas.Canvas(pdf_file_name, pagesize=page_size)
        c.drawImage(self.signature_file, self.offset_x, self.offset_y,
                    self.sign_w, self.sign_h, mask='auto')
        if sign_date:
            timestmp = self.get_current_timestamp_str()
            c.drawString(
                self.offset_x, self.offset_y, timestmp
            )
        c.showPage()
        c.save()
