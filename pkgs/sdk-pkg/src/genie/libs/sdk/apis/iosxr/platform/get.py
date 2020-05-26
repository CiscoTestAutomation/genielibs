'''IOSXR get functions for platform'''

# Python
import re
import logging

# Logger
log = logging.getLogger(__name__)


def get_module_info(device, module, key='sn'):

    ''' Get a module's information

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


def get_current_active_pies(device):

    '''Gets the current active pies on a device

        Args:
            device (`obj`): Device object

        Returns:
            List of active pies on the device
    '''

    log.info("Getting current active pies on device {}".format(device.name))

    try:
        out = device.parse("show install active summary")
    except SchemaEmptyParserError:
        out = {}

    # Trim out mini package as thats the image, not the pie
    regex = re.compile(r'.*mini.*')

    return [i for i in out.get('active_packages', []) if not regex.match(i)]
