import unittest
from pbxproj.pbxsections.PBXVariantGroup import *
from pbxproj.PBXObjects import *


class PBXVariantGroupTest(unittest.TestCase):
    def testAddVariantInvalidFileRef(self):
        variant = PBXVariantGroup.create(u'texts')
        self.assertFalse(variant.add_variant(PBXGenericObject().parse({u'isa': ''})))

    def testAddVariantValidFileRef(self):
        variant = PBXVariantGroup.create(u'texts')
        self.assertTrue(variant.add_variant(PBXFileReference().parse({u'_id': '1', u'isa': 'PBXFileReference'})))
        self.assertIn('1', variant.children)

    def testRemoveVariantInvalidFileRef(self):
        variant = PBXVariantGroup.create(u'texts')
        self.assertFalse(variant.remove_variant(PBXGenericObject().parse({u'isa': ''})))

    def testRemoveVariantValidFileRef(self):
        objs = objects().parse({u'1': {u'isa': 'PBXFileReference'}})
        file_ref = objs['1']

        variant = PBXVariantGroup.create(u'texts')
        objs[variant.get_id()] = variant

        variant.add_variant(file_ref)

        self.assertTrue(variant.remove_variant(file_ref))
        self.assertNotIn('1', variant.children)
