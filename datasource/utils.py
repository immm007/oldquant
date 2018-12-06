def addPrefix(code,sh,sz):
    if code[0] == '6':
        return sh + code
    elif code[0] == '0' or code[0] == '3':
        return sz + code
    raise RuntimeError('unsupoorted code %s' % code)


def addSinaPrefix(code):
    return addPrefix(code,'sh','sz')


def addWangyiPrefix(code):
    return addPrefix(code,'0','1')


class CSVHelper:
    def __init__(self, s):
        self.__s = s
        self.__len = len(s)
        self.__newLinePos = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.__newLinePos == self.__len:
            raise StopIteration
        startPos = self.__newLinePos
        while self.__s[self.__newLinePos] != '\n':
            self.__newLinePos += 1
        self.__newLinePos += 1
        return self.__s[startPos:self.__newLinePos]


class WYRCSVHelper:
    def __init__(self, s):
        self.__s = s
        self.__len = len(s)
        self.__newLinePos = self.__len-2

    def __iter__(self):
        return self

    def __next__(self):
        if self.__newLinePos < 62:
            raise StopIteration
        endPos = self.__newLinePos
        while self.__s[self.__newLinePos] != '\n':
            self.__newLinePos -= 1
        self.__newLinePos -= 1
        return self.__s[self.__newLinePos+2:endPos+1]
