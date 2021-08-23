''' Common Config functions for IOX / app-hosting '''

import logging
import time

log = logging.getLogger(__name__)

# Unicon
from unicon.core.errors import SubCommandFailure

# Genie
from genie.utils.timeout import Timeout


def configure_template(device, template_name="test", loopdetect_enable=False, loopdetect_interval=5, loopdetect_source_port=False):
    ''' 
    Configures Template with various sub-options    
    e.g.
    template loop-detect
      loopdetect
      loopdetect 2
    Args:
        device ('obj') : Device object
        template_name ('str'): Template name
        loopdetect_enable ('bool'): configure 'loopdetect' or not
        loopdetect_interval ('int'): loopdetect interval integer in seconds
        loopdetect_source_port ('bool'): configure 'loopdetect source-port' or not

    Returns:
        None
    '''

    template_configuration_list = []    
    template_configuration_list.append('template {name}'.format(name=template_name))
    
    if loopdetect_enable:
        template_configuration_list.append('loopdetect')
    if loopdetect_interval:
        interval = 'loopdetect ' + str(loopdetect_interval)
        template_configuration_list.append(interval)
    if loopdetect_source_port:
        template_configuration_list.append('loopdetect source-port')

    template_configuration_string = '\n'.join(template_configuration_list)

    try:
        output = device.configure(template_configuration_string)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not Configure Template - Error:\n{error}".format(error=e)
        )

def unconfigure_template(device, template_name="test"):
    ''' 
    UnConfigures specified Template 
    Args:
        device ('obj') : Device object
        template_name ('str'): Template name
    Returns:
        None
    '''

    try:
        output = device.configure('no template {template}'.format(template=template_name))

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not UnConfigure Template - Error:\n{error}".format(error=e)
        )