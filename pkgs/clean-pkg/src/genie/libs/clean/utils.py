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


def print_message(spawn, message, raise_exception=False):
    if raise_exception:
        spawn.log.error(message)
        raise Exception(message)
    else:
        spawn.log.info(message)


def verify_num_images_provided(image_list, expected_images=1):
    num_images = len(image_list)
    if num_images != expected_images:
        log.warning("Expecting {} images, however {} images provided".\
                    format(expected_images, num_images))
        return False
    else:
        log.info("Provided {} image(s) as expected".format(num_images))
        return True


def _apply_configuration(device, configuration=None, configuration_from_file=None,
                         file=None, configure_replace=False, timeout=60):

    if configuration or configuration_from_file and not file:
        # Apply raw configuration using configure service

        if configuration_from_file:
            log.info("Reading configuration from '{}'"
                     .format(configuration_from_file))

            with open(configuration_from_file, 'r') as f:
                configuration = f.read()

        log.info("Applying configuration on '{}'".format(device.name))

        try:
            device.configure(configuration, timeout=timeout)
        except Exception as e:
            if isinstance(e, StateMachineError):
                # StateMachineError is expected as the hostname could change after
                # applying config. Reconnect to the device and learn new hostname.

                log.warning("Device hostname might have changed. Attempting to "
                            "recover...")

                try:
                    device.destroy()
                except Exception:
                    pass # This is fine as long as we can reconnect

                try:
                    device.connect(learn_hostname=True)
                except Exception as e:
                    # Cannot reconnect, stop clean
                    log.error("Failed to reconnect to device after applying "
                              "configuration on {}".format(device.name))
                    raise e from None

            else:
                # Something else went wrong, stop clean
                raise e

    elif file and not configuration:
        # Apply configuration from file

        try:
            if configure_replace:
                log.info("Applying configuration from '{}' via "
                         "'configure replace'".format(file))
                device.api.restore_running_config(
                    path='', file=file, timeout=timeout)
            else:
                log.info("Applying configuration from '{}' via "
                         "'copy to running-config'".format(file))
                device.api.execute_copy_to_running_config(
                    file=file, copy_config_timeout=timeout)
        except Exception:
            # Best effort, until Unicon supports 'learn_hostname' in configure
            # and execute services.
            # ----------------------------------------------------------------

            # If the configuration API fails, we dont know if it timed out
            # due to hostname change or if the configuration failed to apply.
            # This is because the exception raised for either is the same
            # type of exception

            log.warning("The device hostname changed or the configuration "
                        "failed to apply. Attempting to recover...")

            try:
                device.destroy()
            except Exception:
                pass # This is fine as long as we can reconnect

            try:
                device.connect(learn_hostname=True)
            except Exception as e:
                log.error("Error while reconnecting to device '{}'"
                          .format(device.name))
                raise e

            # Reapply the configuration. If it passes, we know that it was
            # a hostname change that caused the exception. If it fails, we
            # know the configuration failed to apply.

            log.info("Reapplying the configuration to verify the cause of failure")

            try:
                if configure_replace:
                    device.api.restore_running_config(
                        path='', file=file, timeout=timeout)
                else:
                    device.api.execute_copy_to_running_config(
                        file=file, copy_config_timeout=timeout)
            except Exception as e:
                log.error("Configuration failed to apply on '{}'"
                          .format(device.name))
                raise e

            log.info("The configuration caused the hostname to change. "
                     "Continuing clean.")


def initialize_clean_sections(image_handler, order):
    '''Updates given section with images provided'''

    # Update section with image information if needed
    for section in order:
        getattr(image_handler, 'update_section')(section)


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
        return ValueError(
            "Clean schema check failed. The following keys are missing from clean yaml file:\n\n{}".format(
                format_missing_key_msg(e.missing_list)))
    elif isinstance(e, SchemaTypeError):
        return TypeError(
            "Clean schema check failed. Incorrect value type was provided for the "
            "following key:\n\n{}\n\nExpected type {} but got type {}".format(
                format_missing_key_msg([e.path]), str(e.type),
                type(e.data)))
    if isinstance(e, SchemaUnsupportedKeyError):
        return ValueError(
            "Clean schema check failed. The following keys are not supported:\n\n{}".format(
                format_missing_key_msg(e.unsupported_keys)))
    else:
        return e


def validate_clean(clean_dict, testbed_dict):
    """ Validates the clean yaml using device abstraction to collect
        the proper schemas

        Args:
            clean_dict (dict): clean datafile
            testbed_dict (dict): testbed datafile

        Returns:
            {
                'warnings' ['Warning example', ...],
                'exceptions: [ValueError, ...]
            }
    """
    warnings = []
    exceptions = []
    validation_results = {'warnings': warnings, 'exceptions': exceptions}

    # these sections are not true stages and therefore cant be loaded
    sections_to_ignore = [
        'images',
        'order'
    ]

    base_schema = {
        'cleaners': {
            Any(): {
                'module': str,
                Optional('devices'): list,
                Optional('platforms'): list,
                Optional('groups'): list,
                Any(): Any()
            }
        },
        'devices': {

        }
    }

    try:
        loaded_tb = testbed_loader(testbed_dict)
    except Exception:
        exceptions.append(
            Exception("Could not load the testbed file. Use "
                      "'pyats validate testbed <file>' to validate "
                      "the testbed file.")
        )

    try:
        clean_json = load_clean_json()
    except Exception as e:
        exceptions.append(e)

    from genie.libs.clean.recovery import recovery_processor

    for dev in clean_dict.get('devices', {}):
        schema = base_schema.setdefault('devices', {}).setdefault(dev, {})
        schema.update({Optional('order'): list})
        schema.update({Optional('device_recovery'): dict})
        schema.update({Optional('images'): Or(list, dict)})

        clean_data = clean_dict["devices"][dev]

        try:
            dev = loaded_tb.devices[dev]
        except Exception as e:
            warnings.append(
                "The device {dev} specified in the clean yaml does "
                "not exist in the testbed.".format(dev=e))
            # cant validate schema so allow anything under dev
            schema.update({Any(): Any()})
            continue

        # update stages with image
        if clean_data.get('images'):
            setattr(dev, 'clean', clean_data)
            try:
                # Get abstracted ImageHandler class
                abstract = Lookup.from_device(dev, packages={'clean': clean})
                ImageHandler = abstract.clean.stages.image_handler.ImageHandler
                image_handler = ImageHandler(dev, dev.clean['images'])
                initialize_clean_sections(image_handler, clean_data['order'])
            except Exception as e:
                # If the device does not have custom.abstraction defined
                # then we cannot load the correct stages to test the
                # correct schema. Skip this device.
                exceptions.append(Exception(dev.name+': '+str(e)))
                schema.update({Any(): Any()})
                continue


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
            try:
                if 'source' not in clean_data:
                    task = get_clean_function(section, clean_json, dev)
                else:
                    task = load_class(clean_data, dev)
            except Exception as e:
                # Stage cannot be found. Allow any schema to prevent schema error
                # and skip this stage
                exceptions.append(str(e))
                schema.update({section: Any()})
                continue


            # Add the stage schema to the base schema
            if hasattr(task, 'schema'):
                schema.update({task.__name__: task.schema})

    try:
        Schema(base_schema).validate(clean_dict)
    except Exception as e:
        exceptions.append(pretty_schema_exception(e))

    return validation_results


def handle_rommon_exception(spawn, context):
    log.error('Device is in Rommon')
    raise Exception('Device is in Rommon')


def remove_string_from_image(images, string):
    ''' Removes user given string from any provided image path

        Args:
            images (dict): List of image files to remove the user provided string from
            string (str): String to remove from the image path
    '''

    regex = re.compile(r'.*{}.*'.format(string))

    return [item.replace(string, "") if regex.match(item) else item for item in images]
