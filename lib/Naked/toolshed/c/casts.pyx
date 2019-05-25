#!/usr/bin/env python
# encoding: utf-8
# cython: profile=True

cdef inline int increment(object iterable, object test_string):
    cdef int count = 0
    cdef object thing
    for thing in iterable:
        if thing == test_string:
            count += 1
    return count

from Naked.toolshed.c.types import NakedObject, XFSet, XDict, XList, XQueue, XSet, XString
from Naked.settings import debug as DEBUG_FLAG

#------------------------------------------------------------------------------
# [ nob ] (NakedObject)
#  Cast a dictionary of attributes to a NakedObject with key>attribute mapping
#------------------------------------------------------------------------------
def nob(attributes={}):
    try:
        return NakedObject(attributes)
    except Exception as e:
        if DEBUG_FLAG:
            print("Naked Framework Error: unable to create a NakedObject with the requested argument using the nobj() function (Naked.toolshed.casts.py).")
        raise e

#------------------------------------------------------------------------------
# [ xd function ] (XDict)
#   Cast a Python dictionary to a XDict
#------------------------------------------------------------------------------
def xd(dictionary_arg, attributes={}):
    try:
        return XDict(dictionary_arg, attributes)
    except TypeError:
        raise TypeError("Attempted to cast to a XDict with an incompatible type")
    except Exception as e:
        if DEBUG_FLAG:
            print("Naked Framework Error: unable to cast object to a XDict with the xd() function (Naked.toolshed.casts.py).")
        raise e

#------------------------------------------------------------------------------
# [ xl function ] (XList)
#  Cast a Python list, set, or tuple to a XList
#------------------------------------------------------------------------------
def xl(list_arg, attributes={}):
    try:
        return XList(list_arg, attributes)
    except TypeError:
        raise TypeError("Attempted to cast to a XList with an incompatible type")
    except Exception as e:
        if DEBUG_FLAG:
            print("Naked Framework Error: unable to cast object to a XList with the xl() function (Naked.toolshed.casts.py).")
        raise e

#------------------------------------------------------------------------------
# [ xq function ] (XQueue)
#  Cast a Python list, set, tuple to a XQueue
#------------------------------------------------------------------------------
def xq(queue_arg, attributes={}):
    try:
        return XQueue(queue_arg, attributes)
    except TypeError:
        raise TypeError("Attempted to cast to a XQueue with an incompatible type")
    except Exception as e:
        if DEBUG_FLAG:
            print("Naked Framework Error: unable to cast object to a XQueue with the xq() function (Naked.toolshed.casts.py).")
        raise e

#------------------------------------------------------------------------------
# [ xset function ] (XSet)
#   Cast a Python set to a XSet
#------------------------------------------------------------------------------
def xset(set_arg, attributes={}):
    try:
        return XSet(set_arg, attributes)
    except TypeError:
        raise TypeError("Attempted to cast to a XSet with an incompatible type")
    except Exception as e:
        if DEBUG_FLAG:
            print("Naked Framework Error: unable to cast object to a XSet with the xset() function (Naked.toolshed.casts.py).")
        raise e

#------------------------------------------------------------------------------
# [ xfset function ] (XFSet)
#   Cast a Python set to a XFSet
#------------------------------------------------------------------------------
def xfset(set_arg, attributes={}):
    try:
        return XFSet(set_arg, attributes)
    except TypeError:
        raise TypeError("Attempted to cast to a XSet with an incompatible type")
    except Exception as e:
        if DEBUG_FLAG:
            print("Naked Framework Error: unable to cast object to a XSet with the xset() function (Naked.toolshed.casts.py).")
        raise e

#------------------------------------------------------------------------------
# [ xstr function ] (XString)
#  Cast a Python string to a XString
#------------------------------------------------------------------------------
def xstr(string_arg, attributes={}):
    try:
        return XString(string_arg, attributes)
    except TypeError as te:
        raise TypeError("Attempted to cast to a XString with an incompatible type")
    except Exception as e:
        if DEBUG_FLAG:
            print("Naked Framework Error: unable to cast object to a XString with the xstr() function (Naked.toolshed.casts.py).")
        raise e

if __name__ == '__main__':
    test = xstr("A test", {'arg1': '2'})
    print(test)
    print(test[0])
    print(test.arg1)
    print(type(test))
