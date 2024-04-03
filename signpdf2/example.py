from file_utilities import GetFileFromUrl, WritePdfToDisk, WritePdfToUrl
from sign_pdf import SignPdf


class SigningExample:
    @classmethod
    def sign_using_urls(cls):
        put_url = 'xyz/xyz'
        pdfurl = 'https:/xyz.pdf'
        sign_url = 'https://xyz.png'
        output_file_name = 'signed_pdf.pdf'

        pdf_file_name = GetFileFromUrl().get_file_from_url(pdfurl)
        signature_file_name = GetFileFromUrl().get_file_from_url(sign_url)

        sign_pdf = SignPdf(
            sign_w=100,
            sign_h=60,
            page_num=0,
            offset_x=400,
            offset_y=200,
            pdf_file=pdf_file_name,
            signature_file=signature_file_name
        )
        pdf_writer = sign_pdf.sign_pdf()
        WritePdfToUrl().write_pdf_to_url(pdf_writer, put_url)
        WritePdfToDisk().write_pdf_to_disk(pdf_writer, output_file_name)

    @classmethod
    def sign_using_local_files(
            cls,
            pdf_file_name: str,
            signature_file_name: str,
            signature_expand: bool = False,
            signature_over: bool = True
    ):
        """
        Sign without any urls
        """
        output_file_name = 'signed_pdf.pdf'
        sign_pdf = SignPdf(
            sign_w=100,
            sign_h=60,
            page_num=0,
            offset_x=54,  # margin from left side
            offset_y=237,  # margin from bottom
            pdf_file=pdf_file_name,
            signature_file=signature_file_name,
            signature_expand=signature_expand,
            signature_over=signature_over,
            sign_timestamp=True
        )
        pdf_writer = sign_pdf.sign_pdf()
        WritePdfToDisk().write_pdf_to_disk(pdf_writer, output_file_name)


if __name__ == '__main__':
    pdf_file_name = 'file1.pdf'
    signature_file_name = 'sample_signature.png'
    SigningExample.sign_using_local_files(
        pdf_file_name=pdf_file_name,
        signature_file_name=signature_file_name,
        signature_expand=False,
        signature_over=False

    )
