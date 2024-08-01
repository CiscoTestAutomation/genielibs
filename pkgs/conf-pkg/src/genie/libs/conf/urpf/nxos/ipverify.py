'''
Urpf Genie Conf Object Implementation for NXOS:
    - IP verify source multi-line configuration implementation for NXOS - CLI
'''

# Python
import warnings
from abc import ABC
from attr import attrib

# Genie
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.attributes import AttributesHelper


class IpVerify(ABC):

    def build_config(self, apply=True, attributes=None, unconfig=False,
                     **kwargs):
        assert not kwargs, kwargs
        attributes = AttributesHelper(self, attributes)
        configurations = CliConfigBuilder(unconfig=unconfig)

        # ip verify unicast source reachable-via any
        # ip verify unicast source reachable-via any allow-default
        # ip verify unicast source reachable-via rx

        ip_str = 'ip verify unicast source reachable-via'

        if attributes.value('ip_verify_strict'):
            ip_str += ' rx'
        elif attributes.value('ip_verify_loose'):
            ip_str += ' any'
            if attributes.value('ip_loose_allow_default'):
                ip_str += ' allow-default'

        configurations.append_line(attributes.format(ip_str))

        return str(configurations)

    def build_unconfig(self, apply=True, attributes=None, **kwargs):
        return self.build_config(apply=apply, attributes=attributes,
                                 unconfig=True, **kwargs)