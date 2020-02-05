import re
from abc import ABC
from collections.abc import Sequence

from pyats.utils.schemaengine import Schema, Optional, Any, Or
from pyats.utils.schemaengine import Use, And, Default, Fallback
from pyats.utils.import_utils import import_from_name
from genie.metaparser.util.exceptions import SchemaError

from .device import Device
from .interface import Interface
from .link import Link

NoneType = type(None)

from .exceptions import YamlConfigError


class Predicate(ABC):

    def __instancecheck__(cls, instance):
        return callable(instance)


class SequenceOfPredicates(Sequence):

    def __instancecheck__(cls, instance):
        return (isinstance(instance, Sequence) and
                isinstance(e, Predicate) for e in instance)


class SequenceOf(Schema):

    def validate(self, data, top=False):
        sub_schema = self.schema \
            if isinstance(self.schema, Schema) \
            else Schema(self.schema)
        if not isinstance(data, Sequence):
            raise SchemaError('Not a sequence: %r' % (data,))
        return [sub_schema.validate(e, top=top) for e in data]


def predicate_importer(value):
    if callable(value):
        return value
    return import_from_name(value)


Predicate = Use(predicate_importer)
SequenceOfPredicates = SequenceOf(Predicate)


def transform_to_list(value):
    if value is None:
        value = []
    elif isinstance(value, (str,)):
        value = [value]
    elif isinstance(value, (Sequence,)):
        value = list(value)
    else:
        raise YamlConfigError('Expected a string, sequence or None: %r' % (value,))
    return value


def transform_to_list_or_None(value):
    value = transform_to_list(value)
    if not value:
        value = None
    return value


def regex(expression):

    def match(value):
        if re.match(expression, value):
            return value
        else:
            raise YamlConfigError("Value '%s' does not match regex '%s'" %
                                  (value, expression))

    return match


production_schema = {

    Optional('name'): str,  # not to be filled by hand
    Optional('topology_file'): str,  # not to be filled by hand

    Optional('subsets'): {
        Any(): Use(transform_to_list),
    },

    'devices': {
        Any(): {  # TODO Optional(Device.validate_name)

            # Parameters
            Optional('label'): Use(transform_to_list),
            Optional('role'): Use(transform_to_list),
            Optional('draw_rank'): int,
            Optional('draw_cluster'): str,

            # Constraints
            Optional('type'): Use(transform_to_list_or_None),  # TODO platform vs type
            Optional('name'): Use(transform_to_list_or_None),  # -> match_name
            Optional('platform'): Use(transform_to_list_or_None),  # TODO platform vs type
            Optional('tgen_platform'): Use(transform_to_list_or_None),
            Optional('os'): Use(transform_to_list_or_None),
            # TODO Optional('series'): Use(transform_to_list_or_None),
            # TODO Optional('model'): Use(transform_to_list_or_None),
            Optional('multinode_requested'): Or(bool, NoneType),
            Optional('predicates'): SequenceOfPredicates,

        },
    },

    Optional('topology'): {
        Optional('links'): {
            Any(): {  # TODO Optional(Link.validate_name)

                # Parameters
                Optional('label'): Use(transform_to_list),

                # Constraints
                Optional('type'): Use(transform_to_list_or_None),
                Optional('interface'): Use(transform_to_list_or_None),
                Optional('name'): Use(transform_to_list_or_None),  # -> match_name
                Optional('predicates'): SequenceOfPredicates,

            }
        },
        Any(): {
            'interfaces': {
                Any(): {  # TODO Optional(Interface.validate_name_I)

                    # Parameters
                    'link': Link.validate_name,
                    Optional('label'): Use(transform_to_list),

                    # Constraints
                    #Optional('router'): Use(transform_to_list_or_None),
                    Optional('name'): Use(transform_to_list_or_None),  # -> match_name
                    Optional('type'): Use(transform_to_list_or_None),
                    #Optional('engine'): Use(transform_to_list_or_None),
                    Optional('product_id'): Use(transform_to_list_or_None),
                    #Optional('diff_slot'): Use(transform_to_list_or_None),
                    #Optional('same_slot'): Use(transform_to_list_or_None),
                    Optional('predicates'): SequenceOfPredicates,

                },
            },
        },
    },
}

# vim: ft=python ts=8 sw=4 et
