'''
    Generic Device class for Cisco-based devices.
'''

__all__ = (
    'Device',
)

import re
import logging
logger = logging.getLogger(__name__)

from genie.decorator import managedattribute
from genie.conf.base.attributes import AttributesHelper
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.config import CliConfig

import genie.libs.conf.device
from genie.libs.conf.base.ipaddress import ip_address, IPv4Network

debug_clean_config = False


class Device(genie.libs.conf.device.Device):
    '''Base Device class for Cisco devices'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def build_unconfig(self, apply=True, attributes=None,
                       **kwargs):

        attributes = AttributesHelper(self, attributes)
        configurations = CliConfigBuilder(unconfig=True)

        configurations.append_block(
            super().build_unconfig(apply=False, attributes=attributes,
                **kwargs))

        if apply:
            if configurations:
                self.configure(str(configurations),
                               # fail_invalid=True, -- best effort?
                               )
        else:
            # Return configuration
            return CliConfig(device=self, unconfig=True,
                             cli_config=configurations, fail_invalid=True)

