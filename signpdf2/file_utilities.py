import requests

from signpdf2.create_tmp_file import CreateTmpFileMixin


class GetFileFromUrl(CreateTmpFileMixin):
    def get_file_from_url(self, url):
        """
        :param url: url to get the file
        :return: temp filename
        """
        temp_file = self.create_tmp_file()
        with open(temp_file, "wb") as file:
            response = requests.get(url)
            file.write(response.content)

        return temp_file


class WritePdfToDisk:
    def write_pdf_to_disk(self, pdf_writer, pdf_name):
        """
        :param pdf_writer: PdfFileWriter object
        :param pdf_name: pdf file name along with entire path
        :return: write pdf to pdf_name
        """
        with open(pdf_name, 'wb') as file:
            pdf_writer.write(file)


class WritePdfToUrl(CreateTmpFileMixin,
                    WritePdfToDisk):
    def write_pdf_to_url(self, pdf_writer, url):
        """
        Upload pdf file to url using PUT req.
        We write contents of a pdf_writer to temp file and then upload that
        temp file to url.
        :param pdf_writer: PdfFileWriter object
        :param url: PUT url to make a put req with file as data.
        :return: None
        """
        temp_file = self.create_tmp_file()
        self.write_pdf_to_disk(pdf_writer, pdf_name=temp_file)

        with open(temp_file, 'rb') as tf:
            requests.put(url, data=tf)
