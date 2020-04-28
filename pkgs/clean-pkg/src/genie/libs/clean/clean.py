
# Python
import os
import json
import yaml
import logging
import importlib
from inspect import unwrap
from functools import partial
from collections import OrderedDict

# pyATS
from pyats.aetest import Testcase
from pyats.aetest.base import Source
from pyats.aetest import base, processors
from pyats.kleenex.bases import BaseCleaner
from pyats.aetest.parameters import ParameterDict
from pyats.aetest.loop import loopable, get_iterations

# Genie
from genie.libs import clean
from genie.testbed import load
from genie.harness.utils import load_class
from genie.harness.discovery import copy_func
from genie.libs.clean.utils import update_clean_section
from genie.metaparser.util.schemaengine import Schema
from genie.libs.clean.stages.recovery import recovery_processor, block_section
from genie.metaparser.util.exceptions import SchemaMissingKeyError,\
                                             SchemaTypeError,\
                                             SchemaUnsupportedKeyError

# PROTO - Should be somewhere else
from genie.abstract import Lookup

# Logger
log = logging.getLogger(__name__)


def _load_function_json():
    """get all clean data in json file"""
    try:
        mod = importlib.import_module("genie.libs.clean")
        functions = os.path.join(mod.__path__[0], "clean.json")
    except Exception:
        functions = ""
    if not os.path.isfile(functions):
        log.warning(
            "clean.json does not exist, make sure you "
            "are running with latest version of "
            "genie.clean"
        )
        clean_data = {}
    else:
        # Open all the parsers in json file
        with open(functions) as f:
            clean_data = json.load(f)
    return clean_data

clean_data = _load_function_json()

def _get_clean(clean_name, clean_data, device):
    """From a clean function and device, return the function object"""

    # Support calling multiple time the same section
    name = clean_name.split('__')[0]
    try:
        data = clean_data[name]
    except KeyError:
        raise Exception("Could not find a clean stage called '{c}'".format(
            c=name)) from None

    # Load SDK abstraction
    lookup = Lookup.from_device(device, packages={"clean": clean})

    # if this is true after below loop, it means the function not under any os
    is_com = True

    # find the token in the lowest level of the json
    for token in lookup._tokens:
        if token in data:
            data = data[token]
            is_com = False

    # if not found, search under 'com' token
    if is_com:
        data = data['com']

    try:
        mod = getattr(_get_submodule(lookup.clean, data["module_name"]), name)
        mod.__name__ = clean_name
        return mod

    except Exception:
        raise Exception("Could not find '{cn}' clean section under '{o}', "
                        "and common".format(cn=name,
                                            o=device.os)) from None


def _get_submodule(abs_mod, mods):
    """recursively find the submodule"""
    ret = abs_mod
    for mod in mods.split('.'):
        ret = getattr(ret, mod)
    return ret


class CleanTestcase(Testcase):
    def __init__(self, device, *args, **kwargs):
        self.device = device
        super().__init__(*args, **kwargs)

    def __iter__(self):
        '''Built-in function __iter__

        Generator function, yielding each testable item within this container
        in the order of appearance inside the test cases. This is the main
        mechanism that allows looping through CleanTestcase Section's child
        items.

        This function relies on discover's returned list of sub sections in
        their sorted runtime order. It then takes each object class,
        instantiate them and run each. In case an object is looped, the loop
        iterations are processed.
        '''
        for section in self.discover():
            if not hasattr(section, '__testcls__'):
                raise TypeError("Expected a subsection object with "
                                "'__testcls__' set by the section decorator")
            # discovered Subsection
            # ------------------------
            if loopable(section):
                # section is marked to be looped
                # offer up each iteration in its own class instance
                for iteration in get_iterations(section):
                    new_section = section.__testcls__(section,
                                              uid = iteration.uid,
                                              parameters = iteration.parameters,
                                              parent = self)
                    yield new_section
            else:
                # run section a single time.
                new_section = section.__testcls__(section, parent = self)
                yield new_section

    def discover(self):
        self.history = OrderedDict()
        try:
            order = self.device.clean['order']
        except KeyError:
            raise Exception("Key 'order' is missing for device "
                            "'{d}'".format(d=self.device.name))

        # Insert the 'images' value into necessary clean sections
        if self.device.clean['images']:
            update_clean_section(self.device, order, self.device.clean['images'])

        all_data = {}
        all_schema = {}
        sections = []
        common_data = {}
        self.parameters['common_data'] = common_data
        for section in order:
            try:
                data = self.device.clean[section] or {}
            except KeyError:
                # Cannot find section - raise exception
                raise Exception("Cannot find '{section}' in the provided "
                                "sections even though it was provided in "
                                "the order list '{order}'".\
                                        format(section=section, order=order))

            # Load it up
            # If source isnt provided then check if it is inside the clean json
            if 'source' not in data:
                # Check if that one exists in the json
                task = _get_clean(section, clean_data, self.device)
            else:
                task = load_class(data, self.device)

            # Verify if schema exists for this section
            if hasattr(task, 'schema'):
                # if the stage has schema defined then build the bigger schema
                all_schema[task.__name__] = task.schema
                all_data[task.__name__] = data
                # unwrap to get original method, tmp fix need to handle in genie core infra
                task = unwrap(task)

            func = copy_func(task)
            func.uid = task.__name__
            func.parameters = ParameterDict()
            func.parameters['device'] = self.device
            func.parameters['common_data'] = common_data
            func.source = Source(self,
                                 objcls=func.__class__)

            for parameter, value in data.items():
                func.parameters[parameter] = value

            # Bind it and append to the section list
            new_section = func.__get__(self, func.__testcls__)
            self.history[new_section.uid] = new_section

            # Add processor, add parameters to it if any
            if self.device.clean.get('device_recovery'):
                processor = partial(recovery_processor,
                                    **self.device.clean.get('device_recovery'))
                processors.add(new_section, pre=[block_section],
                               post=[processor], exception=[])

            sections.append(new_section)

        recovery_data = self.device.clean.get('device_recovery')
        # if recovery info not provided, don't need to check schema
        if recovery_data:
            recovery_schema = recovery_processor.schema
            all_schema['device_recovery'] = recovery_schema
            all_data['device_recovery'] = recovery_data

        try:
            Schema(all_schema).validate(all_data)
        except SchemaMissingKeyError as e:
            # proto type
            raise ValueError(
                "Clean schema check failed. The following keys are missing from clean yaml file:\n\n{}".format(
                    self._format_missing_key_msg(e.missing_list))) from None
        except SchemaTypeError as e:

            raise TypeError(
                "Clean schema check failed. Incorrect value type was provided for the "
                "following key:\n\n{}\n\nExpected type {} but got type {}".format(
                    self._format_missing_key_msg([e.path]), str(e.type), type(e.data))) from None
        except SchemaUnsupportedKeyError as e:
            raise ValueError(
                "Clean schema check failed. The following keys are not supported:\n\n{}".format(
                    self._format_missing_key_msg(e.unsupported_keys))) from None

        return sections


    def _format_missing_key_msg(self, missing_list):
        """Beautifully populate missing keys in to human readable format
        i.e
        """
        # indentation for each nested level
        indent = 4
        # find horizontal position of the arrow by using max missing path len plus
        # max missing key len
        max_path_len = max(map(len, missing_list))
        max_key_len = max(map(len, [l[-1] for l in missing_list]))

        missing_dict = {}
        for missing_key in missing_list:
            d = missing_dict
            for path in missing_key:
                    d = d.setdefault(path, {})

        return self.pprint_missing_key(missing_dict, max_path_len, max_key_len, indent)


    def pprint_missing_key(self, missing_dict, max_path_len, max_key_len, indent):
        """format missing key dict into a yaml-like human readable output"""
        def _pprint_missing_key(missing_dict, lines, level=0):

            for key, value in missing_dict.items():
                line = []
                # indentation
                line.extend([' '] * indent * level)
                # key and colon
                line.extend([key, ':'])
                if value:

                    lines.append(''.join(line))
                    _pprint_missing_key(value, lines, level=level+1)

                else:
                    key_len = len(key)
                    line.extend([' '] * (
                                indent * (max_path_len - level) + (max_key_len - key_len)))
                    line.append('   <<<')
                    lines.append(''.join(line))

        lines = []
        _pprint_missing_key(missing_dict, lines)
        return '\n'.join(lines)


class DeviceClean(BaseCleaner):

    def clean(self, device, reporter, *args, **kwargs):

        # In this section we will convert to Genie Testbed
        testbed = load(device.testbed)
        device = testbed.devices[device.name]

        clean_testcase = CleanTestcase(device)
        clean_testcase.reporter = reporter.testcase(clean_testcase)
        with clean_testcase:
            # 1. Figure out what section to run
            # 2. Run them
            result = clean_testcase()
            if not result:
                raise Exception("Clean {result}.".format(result=str(result)))

