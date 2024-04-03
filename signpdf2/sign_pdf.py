import datetime

import pypdf
import pytz
from reportlab.pdfgen import canvas

from signpdf2.create_tmp_file import CreateTmpFileMixin


class SignPdf(CreateTmpFileMixin):
    """
    Sign a pdf with signature image at desired location.
    A signature image is placed(overlayed) at desired location on a pdf page.
    we use units instead of pixel. Units are pdf-standard units (1/72 inch)
    """

    def __init__(
            self,
            sign_w: int,
            sign_h: int,
            page_num: int,
            offset_x: int,
            offset_y: int,
            pdf_file: str,
            signature_file: str,
            signature_expand: bool = False,
            signature_over: bool = True,
            sign_timestamp: bool = True,
            timezone: str = 'UTC'
    ):
        """
        :param sign_w: signature width in units
        :param sign_h: signature height in units
        :param pdf_file:  name and path of pdf file on local system
        :param signature_file: name and path of signature image file
        :param page_num: page number of pdf to sign. Index starts at 0
        :param offset_x: offset units horizontally from left
        :param offset_y: offset units vertically from bottom
        :param signature_expand: Original page dimension is expanded to
            accomodate signature if signature dimensions are more than original
        :param signature_over: Signature is over or under the original pdf
        :param sign_timestamp: Bool. If true, then add current timestamp below
            signature
        """
        self.sign_w = sign_w
        self.sign_h = sign_h
        self.page_num = page_num
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.pdf_file = pdf_file
        self.signature_file = signature_file
        self.signature_expand = signature_expand
        self.signature_over = signature_over
        self.sign_timestamp = sign_timestamp
        self.timezone = timezone

    def sign_pdf(self):
        """
        Draw signature on a temporary empty single page pdf.
        Then merge this page with original pdf page. If signature is needed
        on 2nd page, then merge this temp signed page on page2.

        :param sign_timestamp: Bool. If true, then add current timestamp below
            signature
        :return: PdfFileWriter object with signed pdf
        """
        writer = pypdf.PdfWriter()
        pdf_reader = pypdf.PdfReader(self.pdf_file)

        for i in range(0, len(pdf_reader.pages)):
            orignal_pdf_page = pdf_reader.pages[i]

            if i == self.page_num:
                temp_signature_pdf = self.create_tmp_file()

                self.draw_signature_on_pdf(
                    temp_signature_pdf,
                    page_size=orignal_pdf_page.cropbox,
                    sign_date=self.sign_timestamp
                )

                # Merge signed temp PDF in to original page
                signed_pdf_reader = self.get_pdf_file_reader(temp_signature_pdf)
                signed_page = signed_pdf_reader.pages[0]
                orignal_pdf_page = self.merge_two_pdf_pages(orignal_pdf_page,
                                                            signed_page)

            writer.add_page(orignal_pdf_page)  # addPage

        return writer

    def get_pdf_file_reader(self, file: str = None):
        """
        :param file: pdf file name with path
        :return: file reader object , keeping file open in read mode. if we
        close the file, then that pdf_reader is of no use
        """
        if file is None:
            file = self.pdf_file

        return pypdf.PdfReader(file)

    def merge_two_pdf_pages(
            self,
            page1: pypdf.PageObject,
            page2: pypdf.PageObject
    ) -> pypdf.PageObject:  # PyPDF2.pdf.PageObject:
        """
        Merge page2 in page1
        :param page1: pdf page
        :param page2: pdf page
        :return: page1 after page2 is merged in it
        """
        page2.mediabox = page1.mediabox
        page1.merge_page(
            page2,
            over=self.signature_over,
            expand=self.signature_expand
        )
        return page1

    def get_current_timestamp_str(self):
        """
        :return: current timestamp in string format and timezone
        """
        timezone = pytz.timezone(self.timezone)
        return datetime.datetime.now(timezone).strftime(
            "%m-%d-%Y - %I:%M %p - %Z"
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
