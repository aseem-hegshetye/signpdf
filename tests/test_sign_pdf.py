from unittest import mock
from unittest.mock import MagicMock

from signpdf2.sign_pdf import SignPdf


class TestSignPdf:
    def __init__(self):
        pass

    def setup_method(self, method):
        self.sign_pdf = SignPdf(
            sign_w=100,
            sign_h=60,
            page_num=0,
            offset_x=400,
            offset_y=200,
            pdf_file='xyz.pdf',
            signature_file='signature.png'
        )

    @mock.patch('signpdf2.sign_pdf.canvas.Canvas')
    def test_draw_signature_on_pdf(self, canvas_class):
        canvas_obj = MagicMock()
        canvas_class.return_value = canvas_obj
        self.sign_pdf.draw_signature_on_pdf('f1.pdf', 100, False)
        canvas_obj.drawImage.assert_called_once()
        canvas_obj.showPage.assert_called_once()
        canvas_obj.save.assert_called_once()

    def test_merge_two_pdf_pages(self):
        mock_page1 = MagicMock()
        mock_page2 = MagicMock()
        op = self.sign_pdf.merge_two_pdf_pages(mock_page1, mock_page2)
        mock_page1.mergePage.assert_called_once()
        assert op == mock_page1
