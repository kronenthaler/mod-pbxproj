class PBXKey(unicode):
    def __new__(cls, value, parent):
        obj = unicode.__new__(cls, value)
        obj._parent = parent
        return obj

    def __repr__(self):
        return "{0} /* {1} */".format(self.__str__(), self._get_comment())

    def _get_comment(self):
        return self._parent._resolve_comment(self)

