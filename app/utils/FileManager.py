class FileManager:
    """
      reading from a file by line and returning a list of lines in the file
    """

    @staticmethod
    def getListFromFile(path, mode='r'):
        file = open(path, mode)
        fileList = []

        while True:
            line = file.readline()

            # trimming the additional newline '\n' in every word
            line = line.strip()

            # finish if there are no lines
            if not line or line == '':
                break

            fileList.append(line)

        return fileList

    """
    get all text in a file
    """

    def getFileData(self, path: str, mode='r'):
        file = open(path, mode)
        return file.read()

    def putDataInFile(self, path, text: str, mode='w'):
        file = open(path, 'w')
        file.write(text)
        return path


fileService = FileManager()
