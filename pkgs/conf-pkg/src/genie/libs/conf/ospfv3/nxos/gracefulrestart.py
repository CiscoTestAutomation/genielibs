''' 
OSPFv3 Genie Conf Object Implementation for NXOS:
    - GracefulRestart multi-line configuration implementation for NXOS - CLI
'''

# Python
import warnings
from abc import ABC
from attr import attrib

# Genie
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.attributes import AttributesHelper


class GracefulRestart(ABC):

    def build_config(self, apply=True, attributes=None, unconfig=False,
                     **kwargs):
        assert not kwargs, kwargs
        attributes = AttributesHelper(self, attributes)
        configurations = CliConfigBuilder(unconfig=unconfig)

        # router ospfv3 1
        #   graceful-restart
        #   graceful-restart helper-disable
        #   graceful-restart grace-period 50
        #   graceful-restart planned-only
        if attributes.value('gr_enable'):

            # graceful-restart
            gr_str = 'graceful-restart'

            # + helper-disable
            # + grace-period {gr_restart_interval}
            # + planned-only
            if attributes.value('gr_helper_enable') is False:
                gr_str += ' helper-disable'
            elif attributes.value('gr_restart_interval'):
                gr_str += ' grace-period {gr_restart_interval}'
            elif attributes.value('gr_planned_only'):
                gr_str += ' planned-only'

            configurations.append_line(attributes.format(gr_str))

        return str(configurations)

    def build_unconfig(self, apply=True, attributes=None, **kwargs):
        return self.build_config(apply=apply, attributes=attributes,
                                 unconfig=True, **kwargs)
