''' 
OSPF Genie Conf Object Implementation for IOSXE:
    - GracefulRestart multi-line configuration implementation for IOSXE - CLI
'''

# Python
import warnings
from abc import ABC

# Genie
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.attributes import AttributesHelper


class GracefulRestart(ABC):

    def build_config(self, apply=True, attributes=None, unconfig=False,
                         **kwargs):
        assert not kwargs, kwargs
        attributes = AttributesHelper(self, attributes)
        configurations = CliConfigBuilder(unconfig=unconfig)

        # router ospf 1
        #   nsf cisco helper
        #   nsf cisco helper disable
        #   nsf ietf helper
        #   nsf ietf helper disable
        #   nsf ietf helper strict-lsa-checking
        #   nsf ietf restart-interval 50
        if attributes.value('gr_enable'):
            
            # nsf
            gr_str = 'nsf'

            # + {gr_type}
            if attributes.value('gr_type'):
                grtype = attributes.value('gr_type').value
                gr_str += ' {}'.format(grtype)

            # + helper
            # + helper disable
            # + helper strict-lsa-checking
            # + restart-interval {gr_restart_interval}
            if attributes.value('gr_helper_enable') is True:
                gr_str += ' helper'
            elif attributes.value('gr_helper_enable') is False:
                gr_str += ' helper disable'
            elif attributes.value('gr_helper_strict_lsa_checking') and grtype == 'ietf':
                gr_str += ' helper strict-lsa-checking'
            elif attributes.value('gr_restart_interval') and grtype == 'ietf':
                gr_str += ' restart-interval {gr_restart_interval}'

            configurations.append_line(attributes.format(gr_str))

        return str(configurations)

    def build_unconfig(self, apply=True, attributes=None, **kwargs):
        return self.build_config(apply=apply, attributes=attributes,
                                 unconfig=True, **kwargs)