import tempfile


class CreateTmpFileMixin:
    def create_tmp_file(self, suffix=".pdf"):
        """
        :param suffix: temp file extention
        :return: create a temp file and return its name with entire path
        """
        with tempfile.NamedTemporaryFile(suffix=suffix) as fh:
            return fh.name
