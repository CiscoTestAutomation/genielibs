'''Common get info functions for platform'''
# Python
import re
import logging

log = logging.getLogger(__name__)


def get_module_info(device, module, key='sn'):
    ''' Get a module's infomation

        Args:
            device (`obj`): Device object
            module (`str`): Module name
            key (`str`): Key name
        Returns:
            field (`str`): Field value
    '''
    log.info("Getting module '{}' key '{}' from {}".format(
             module, key, device.name))
    try:
        out = device.parse('show inventory')
    except Exception as e:
        log.error("Failed to parse 'show inventory' on {}:\n{}"
            .format(device.name, e))
        raise Exception from e

    if module in out['module_name']:
        if key in out['module_name'][module]:
            return out['module_name'][module][key]
        else:
            raise Exception("module '{}' doesn't have a key named '{}'"
                    .format(module, key))
    else:
        raise Exception("Can not find a module name '{}' on device {}"
                .format(module, device.name))
