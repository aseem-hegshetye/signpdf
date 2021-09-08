from file_utilities import GetFileFromUrl, WritePdfToDisk, WritePdfToUrl
from sign_pdf import SignPdf

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
