__all__ = (
    #'ABCBaseMeta',
    'ABCBase',
)

from genie.conf.base.base import Base as genieBase
from abc import ABCMeta as _ABCMeta, ABC as _ABC


class ABCBaseMeta(_ABCMeta, type(genieBase)):
    '''Metaclass for declaring Abstract Base Classes (ABCs) derived from
    genie.conf.base's Base.'''
    pass


class ABCBase(genieBase, _ABC, metaclass=ABCBaseMeta):
    '''Class for declaring Abstract Base Classes (ABCs) derived from
    genie.conf.base's Base.'''
    pass

