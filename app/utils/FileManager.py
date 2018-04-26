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


fileService = FileManager()
