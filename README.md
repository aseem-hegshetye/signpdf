# signpdf2

* This package is used to insert a signature image (png) into a pdf at a specified location using python.
* We use units instead of pixel. Units are pdf-standard units (1/72 inch).
* You may have your input files stored on your system or on cloud with a GET url to them.
    * Following example shows how you can insert a signature in a pdf (stored locally or available through a GET url)
    * Then save the signed pdf locally or make a PUT request to a PUT url

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
:param sign_date: Bool. If true, then add current timestamp below
            signature
"""
from signpdf2.file_utilities import GetFileFromUrl, WritePdfToDisk, WritePdfToUrl
from signpdf2.sign_pdf import SignPdf

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



```