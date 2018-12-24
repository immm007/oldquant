import abc
from datasource import Maintainer

class Period:
    Day = 24*60*60
    Week = 5*24*60*60

class Stock:
    __ma = Maintainer()
    def __init__(self,code):
        self.__code = code

    @property
    def code(self):
        return self.__code

    def loadData(self):
        pass

class Technical:
    abc.abstractclassmethod
    def onNewValue(self,value,dt):
        raise NotImplementedError()

    abc.abstractclassmethod
    def onUpdateValue(self,value,dt):
        raise NotImplementedError()

    abc.abstractproperty
    def period(self):
        raise NotImplementedError()
