# MIT License
#
# Copyright (c) 2016 Ignacio Calderon aka kronenthaler
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from pbxproj.PBXList import PBXList
from pbxproj.PBXGenericObject import PBXGenericObject
from pbxproj.PBXObjects import objects
from pbxproj.PBXRootObject import rootObject
from pbxproj.XcodeProject import XcodeProject
from pbxproj.pbxsections import *

__version__ = '2.10.2'


def is_in_save(current_obj):
    return _get_save_caches(current_obj) is not None


def get_from_cache_during_save(current_obj, caches_key_type, caches_key_obj, fill_cache_func, target_key):
    save_caches = _get_save_caches(current_obj)
    assert save_caches is not None, 'Must only call this during a save operation!'
    cache_key = (caches_key_type, id(caches_key_obj))
    cache = save_caches.get(cache_key)
    if cache is None:
        cache = {}
        fill_cache_func(cache)
        save_caches[cache_key] = cache
    return cache.get(target_key)


def _get_save_caches(current_obj):
    parent = current_obj._parent
    while parent is not None:
        current_obj = parent
        parent = current_obj._parent
    return getattr(current_obj, '_save_caches', None)
