class PBXKey(unicode):
    def __new__(cls, value, parent):
        obj = unicode.__new__(cls, value)
        obj._parent = parent
        return obj

    def __repr__(self):
        return "{0} /* {1} */".format(self.__str__(), self._resolve_comment())

    # TODO: this method should call to an object implementation that allows it to change the comment content based on
    # class that is used
    def _resolve_comment(self):
        parent = self._parent

        while parent is not None:
            obj = parent[self.__str__()]
            if obj is not None:
                if hasattr(obj, "name"):
                    return obj.name
                if hasattr(obj, 'path'):
                    return obj.path

            parent = parent._parent

        return "-" #str(type(self._parent))