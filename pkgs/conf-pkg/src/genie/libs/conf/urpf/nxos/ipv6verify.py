"""
Urpf Genie Conf Object Implementation for NXOS:
    - IPv6 verify source multi-line configuration implementation for NXOS - CLI
"""

# Python
import warnings
from abc import ABC
from attr import attrib

# Genie
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.attributes import AttributesHelper


class Ipv6Verify(ABC):

    def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
        assert not kwargs, kwargs
        attributes = AttributesHelper(self, attributes)
        configurations = CliConfigBuilder(unconfig=unconfig)

        # ipv6 verify unicast source reachable-via any
        # ipv6 verify unicast source reachable-via any allow-default
        # ipv6 verify unicast source reachable-via rx
        # ipv6 verify unicast source reachable-via rx allow vni-hosts

        ip_str = "ipv6 verify unicast source reachable-via"

        if attributes.value("ipv6_verify_strict"):
            ip_str += " rx"
            if attributes.value("ipv6_strict_allow_vnihosts"):
                ip_str += " allow vni-hosts"
        elif attributes.value("ipv6_verify_loose"):
            ip_str += " any"
            if attributes.value("ipv6_loose_allow_default"):
                ip_str += " allow-default"

        configurations.append_line(attributes.format(ip_str))

        return str(configurations)

    def build_unconfig(self, apply=True, attributes=None, **kwargs):
        return self.build_config(
            apply=apply, attributes=attributes, unconfig=True, **kwargs
        )
