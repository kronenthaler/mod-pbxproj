class PBXKey(unicode):
    def __new__(cls, value, parent):
        obj = unicode.__new__(cls, value)
        obj._parent = parent
        return obj

    def __repr__(self):
        comment = self._get_comment()
        if comment is not None:
            comment = u' /* {0} */'.format(comment)
        else:
            comment = u''

        return u'{0}{1}'.format(self.__str__(), comment)

    def get_parent(self):
        return self._parent

    def _get_comment(self):
        return self.get_parent()._resolve_comment(self)
