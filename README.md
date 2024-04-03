# signpdf2

* This package is used to insert a signature image (png) into a pdf at a specified location using python.
* We use units instead of pixel. Units are pdf-standard units (1/72 inch).
* You may have your input files stored on your system or on cloud with a GET url to them.
    * Following example shows how you can insert a signature in a pdf (stored locally or available through a GET url)
    * Then save the signed pdf locally or make a PUT request to a PUT url
* Works for python 3.12

* `pdf_utilities.py` files is not used anywhere in this package. It's just provided as an accessory.

### Github

https://github.com/aseem-hegshetye/signpdf

### Installation

Install with pip:

    pip install signpdf2

### Example

```python
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



```