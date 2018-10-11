''' 
OSPF Genie Conf Object Implementation for IOSXR:
    - GracefulRestart multi-line configuration implementation for IOSXR - CLI
'''

# Python
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
        #   nsf cisco
        #   nsf ietf
        #   nsf ietf helper disable
        #   nsf interval 500
        if attributes.value('gr_enable'):
            
            # nsf
            gr_str = 'nsf'

            # + {gr_type}
            if attributes.value('gr_type').value == 'cisco':
                gr_str += ' cisco'
            elif attributes.value('gr_type').value == 'ietf':
                gr_str += ' ietf'
                # + helper disable
                if attributes.value('gr_helper_enable') is False:
                    gr_str += ' helper disable'
            elif attributes.value('gr_restart_interval'):
                gr_str += ' interval {gr_restart_interval}'

            configurations.append_line(attributes.format(gr_str))

        return str(configurations)

    def build_unconfig(self, apply=True, attributes=None, **kwargs):
        return self.build_config(apply=apply, attributes=attributes,
                                 unconfig=True, **kwargs)