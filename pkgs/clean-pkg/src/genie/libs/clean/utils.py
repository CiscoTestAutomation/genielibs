'''
Common Utilities for Genie Clean
'''

# Python
import re
import os
import logging
import json
import importlib
from functools import wraps

# Genie
from genie.libs import clean
from genie.abstract import Lookup
from genie.harness.utils import load_class
from genie.metaparser.util.schemaengine import Schema, Optional, Any, Use, And, Or
from genie.metaparser.util.exceptions import SchemaMissingKeyError,\
                                             SchemaTypeError,\
                                             SchemaUnsupportedKeyError

# pyATS
from pyats.topology.loader import load as testbed_loader

# Unicon
from unicon.core.errors import (SubCommandFailure, TimeoutError,
                                StateMachineError)

# Logger
log = logging.getLogger(__name__)

SECTIONS_WITH_IMAGE = ['tftp_boot',
                       'copy_to_linux',
                       'copy_to_device',
                       'change_boot_variable',
                       'verify_running_image']


def clean_schema(schema):
    """decorator for defining schema"""
    def schema_decorator(func):
        @wraps(func)
        def wrapped(section, *args, **kwargs):
            return func(section, *args, **kwargs)
        wrapped.schema = schema
        return wrapped
    return schema_decorator


def find_clean_variable(section, key):
    # a set makes sure values are unique
    found = set()
    for stage, data in section.history.items():
        if key in data.parameters:
            value = data.parameters[key]
            # todo handle dict value
            # the value could be either a string or list
            found.update(value if isinstance(value, list) else [value])

    return list(found)


def print_message(spawn, message, status=1):
    if status:
        spawn.log.info(message)
    else:
        spawn.log.error(message)
        raise Exception(message)


def verify_num_images_provided(image_list, expected_images=1):
    num_images = len(image_list)
    if num_images != expected_images:
        log.warning("Expecting {} images, however {} images provided".\
                    format(expected_images, num_images))
        return False
    else:
        log.info("Provided {} image(s) as expected".format(num_images))
        return True


def _apply_configuration(device, configuration=None, file=None, timeout=60):

    # It is currently needed as hostname can be changed while applying
    # configuration. Unicon will add an enhnacement to learn hostname
    # at configuration service but until then, this is it.

    # Apply raw configuration strings or copy file provided to running-config
    try:
        if configuration and not file:
            log.info("Apply raw configuration provided to device {}".\
                     format(device.name))

            # Apply raw config strings
            device.configure(configuration, timeout=timeout)

        elif file and not configuration:
            log.info("Copy configuration file '{}' to running-config on "
                     "device {}".format(file, device.name))

            # Copy file to running-config
            device.api.\
                execute_copy_to_running_config(file=file,
                                               copy_config_timeout=timeout)
    except Exception as e:
        # Check if StateMachineError (expected) else fail
        if not isinstance(e, StateMachineError):
            # Something else went wrong, destroy and attempt reconnect
            log.error(str(e))
            log.error("Error while applying configuration to {} after reload".\
                      format(device.name))
            log.info("Destroying connecting and attempting reconnection...")
            try:
                device.destroy()
                device.connect(learn_hostname=True)
            except Exception as e:
                log.error("Error while reconnecting to device {} after "
                          "applying configuration".format(device.name))
                raise e from None
            else:
                raise Exception("Error while applying configuration to device "
                                "{}".format(device.name))

        # StateMachineError is expected as the hostname would change after
        # applying config. Reconnect to the device and learn new hostname
        log.info("Device hostname might have changed - Attempting reconnect")
        try:
            device.destroy()
            device.connect(learn_hostname=True)
        except Exception as e:
            # Okay, cannot reconnect, fail, stop clean
            log.error("Failed to reconnect to device after applying "
                      "configuration on {}".format(device.name))
            raise e from None


def update_clean_section(device, order, images):
    '''Updates given section with images provided'''

    # Get abstracted ImageHandler class
    abstract = Lookup.from_device(device, packages={'clean': clean})
    ImageHandler = abstract.clean.stages.image_handler.ImageHandler

    # Image handler
    image_handler = ImageHandler(device, images)

    # Update section with image information if needed
    for section in order:

        if section not in SECTIONS_WITH_IMAGE:
            continue
        elif not device.clean[section]:
            device.clean[section] = {}

        # Section: tftp_boot
        if section == 'tftp_boot':
            image_handler.update_tftp_boot()
            continue

        # Section: copy_to_linux
        if section == 'copy_to_linux':
            image_handler.update_copy_to_linux()
            continue

        # Section: copy_to_device
        if section == 'copy_to_device':
            image_handler.update_copy_to_device()
            continue

        # Section: change_boot_variable
        if section == 'change_boot_variable':
            image_handler.update_change_boot_variable()
            continue

        # Section: verify_running_image
        if section == 'verify_running_image':
            image_handler.update_verify_running_image()
            continue


def load_clean_json():
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
            "genie.libs.clean"
        )
        clean_data = {}
    else:
        # Open all the parsers in json file
        with open(functions) as f:
            clean_data = json.load(f)
    return clean_data


def get_clean_function(clean_name, clean_data, device):
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


def format_missing_key_msg(missing_list):
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

    return _pprint_missing_key(missing_dict, max_path_len, max_key_len, indent)


def _pprint_missing_key(missing_dict, max_path_len, max_key_len, indent):
    """format missing key dict into a yaml-like human readable output"""
    def __pprint_missing_key(missing_dict, lines, level=0):

        for key, value in missing_dict.items():
            line = []
            # indentation
            line.extend([' '] * indent * level)
            # key and colon
            line.extend([key, ':'])
            if value:

                lines.append(''.join(line))
                __pprint_missing_key(value, lines, level=level+1)

            else:
                key_len = len(key)
                line.extend([' '] * (
                            indent * (max_path_len - level) + (max_key_len - key_len)))
                line.append('   <<<')
                lines.append(''.join(line))

    lines = []
    __pprint_missing_key(missing_dict, lines)
    return '\n'.join(lines)


def pretty_schema_exception(e):
    if isinstance(e, SchemaMissingKeyError):
        # proto type
        raise ValueError(
            "Clean schema check failed. The following keys are missing from clean yaml file:\n\n{}".format(
                format_missing_key_msg(e.missing_list))) from None
    elif isinstance(e, SchemaTypeError):
        raise TypeError(
            "Clean schema check failed. Incorrect value type was provided for the "
            "following key:\n\n{}\n\nExpected type {} but got type {}".format(
                format_missing_key_msg([e.path]), str(e.type),
                type(e.data))) from None
    if isinstance(e, SchemaUnsupportedKeyError):
        raise ValueError(
            "Clean schema check failed. The following keys are not supported:\n\n{}".format(
                format_missing_key_msg(e.unsupported_keys))) from None
    else:
        raise e


def validate_schema(clean, testbed):
    """ Validates the clean yaml using device abstraction to collect
        the proper schemas

        Args:
            clean (dict): clean datafile
            testbed (dict): testbed datafile
    """
    # these sections are not true stages and therefore cant be loaded
    sections_to_ignore = [
        'images',
        'order'
    ]

    base_schema = {
        'cleaners': {
            Any(): Any()
        },
        'devices': {

        }
    }

    try:
        loaded_tb = testbed_loader(testbed)
    except Exception:
        raise Exception("Could not load the testbed file. Use 'pyats validate "
                        "testbed <file>' to validate the testbed file.")

    clean_json = load_clean_json()
    from genie.libs.clean.stages.recovery import recovery_processor

    warning_messages = []
    for dev in clean["devices"]:
        schema = base_schema.setdefault('devices', {}).setdefault(dev, {})
        schema.update({Optional('order'): list})
        schema.update({Optional('device_recovery'): dict})
        schema.update({Optional('images'): Or(list, dict)})

        clean_data = clean["devices"][dev]

        try:
            dev = loaded_tb.devices[dev]
        except KeyError as e:
            warning_messages.append("The device {dev} specified in the clean "
                                    "yaml does not exist in the testbed."
                                    .format(dev=e))
            # cant validate schema so allow anything under dev
            schema.update({Any(): Any()})
            continue

        # update stages with image
        if clean_data.get('images'):
            setattr(dev, 'clean', clean_data)
            update_clean_section(dev, clean_data.keys(), clean_data['images'])

        for section in clean_data:
            # ignore sections that aren't true stages
            if section in sections_to_ignore:
                continue

            if section == 'device_recovery':
                schema.update({'device_recovery': recovery_processor.schema})
                continue

            # when no data is provided under stage, change None to dict
            # this is needed for schema validation
            if clean_data[section] is None:
                clean_data[section] = {}


            # Load it up so we can grab the schema from the stage
            # If source isnt provided then check if it is inside the clean json
            if 'source' not in clean_data:
                task = get_clean_function(section, clean_json, dev)
            else:
                task = load_class(clean_data, dev)

            # Add the stage schema to the base schema
            if hasattr(task, 'schema'):
                schema.update({task.__name__: task.schema})

    if warning_messages:
        log.warning('\nWarning Messages')
        log.warning('----------------')
        log.warning(' - ' + '\n - '.join(warning_messages))

    try:
        Schema(base_schema).validate(clean)
    except Exception as e:
        log.error('\nExceptions')
        log.error('----------')
        pretty_schema_exception(e)


def handle_rommon_exception(spawn, context):
    log.error('Device is in Rommon')
    raise Exception('Device is in Rommon')


def remove_string_from_image(images, string='tftpboot/'):
    ''' Removes user given string from any provided image path

        Args:
            string (str): String to remove from the image path
            images (dict): List of image files to remove the user provided string from
                           Default: 'tftpboot/'
    '''

    regex = re.compile(r'.*{}.*'.format(string))

    return [item.replace(string, "") if regex.match(item) else item for item in images]

