''' 
OSPF Genie Conf Object Implementation for IOSXR:
    - InterfaceStaticNeighbor multi-line configuration implementation for IOSXR - CLI
'''

# Python
from abc import ABC

# Genie
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.attributes import AttributesHelper


class InterfaceStaticNeighbor(ABC):

    def build_config(self, apply=True, attributes=None, unconfig=False,
                         **kwargs):
        assert not kwargs, kwargs
        attributes = AttributesHelper(self, attributes)
        configurations = CliConfigBuilder(unconfig=unconfig)

        # interface GigabitEthernet1
        #   neighbor 10.10.10.10 cost 100 poll-interval 66 priority 12
        if attributes.value('if_static_neighbor'):
            
            # neighbor 10.10.10.10 
            intf_cfg_str = 'neighbor {if_static_neighbor}'

            # + cost {if_static_cost}
            if attributes.value('if_static_cost'):
                intf_cfg_str += ' cost {if_static_cost}'

            # + poll-interval {if_static_poll_interval}
            if attributes.value('if_static_poll_interval'):
                intf_cfg_str += ' poll-interval {if_static_poll_interval}'

            # + priority {if_static_priority}
            if attributes.value('if_static_priority'):
                intf_cfg_str += ' priority {if_static_priority}'

            configurations.append_line(attributes.format(intf_cfg_str))

        return str(configurations)

    def build_unconfig(self, apply=True, attributes=None, **kwargs):
        return self.build_config(apply=apply, attributes=attributes,
                                 unconfig=True, **kwargs)