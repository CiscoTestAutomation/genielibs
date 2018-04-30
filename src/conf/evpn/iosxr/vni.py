
from abc import ABC
import warnings
import contextlib

from genie.conf.base.attributes import UnsupportedAttributeWarning,\
    AttributesHelper
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.config import CliConfig


class Vni(ABC):

    def build_config(self, apply=True, attributes=None, unconfig=False,
                     contained=False, **kwargs):
        assert not kwargs, kwargs
        attributes = AttributesHelper(self, attributes)
        configurations = CliConfigBuilder(unconfig=unconfig)

        # iosxr: interface nve1 (config-nve)
        submode_stack = contextlib.ExitStack()
        if not contained and self.nve:
            submode_stack.enter_context(
                self.nve._build_config_create_interface_submode_context(configurations))

        # iosxr: interface nve1 / member vni 1 (config-nve-vni)
        # iosxr: interface nve1 / member vni 1-2 (config-nve-vni)
        with configurations.submode_context(attributes.format('member vni {vni_id}', force=True)):
            if unconfig and attributes.iswildcard:
                configurations.submode_unconfig()

            # iosxr: interface nve1 / member vni 1 / host-reachability protocol bgp
            configurations.append_line(attributes.format('host-reachability protocol {host_reachability_protocol}'))

            # iosxr: interface nve1 / member vni 1 / mcast-group 1.2.3.4
            # iosxr: interface nve1 / member vni 1 / mcast-group 1.2.3.4 1.2.3.4
            configurations.append_line(attributes.format('mcast-group {mcast_group}'))

            # iosxr: interface nve1 / member vni 1 / vrf someword
            configurations.append_line(attributes.format('vrf {vrf.name}'))

            # iosxr: interface nve1 / member vni 1 / load-balance ...
            configurations.append_line(attributes.format('load-balance {load_balance}'))

        submode_stack.close()
        if apply:
            if configurations:
                self.device.configure(str(configurations), fail_invalid=True)
        else:
            return CliConfig(device=self.device, unconfig=unconfig,
                             cli_config=configurations, fail_invalid=True)

    def build_unconfig(self, apply=True, attributes=None, **kwargs):
        return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

