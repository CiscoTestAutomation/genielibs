
from abc import ABC
import warnings
import contextlib

from genie.conf.base.attributes import UnsupportedAttributeWarning,\
    AttributesHelper
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.config import CliConfig

from genie.libs.conf.interface import EthernetInterface
from genie.libs.conf.interface.iosxe import EFPInterface
from genie.libs.conf.l2vpn.pseudowire import PseudowireNeighbor,\
    PseudowireIPv4Neighbor


class BridgeDomain(ABC):

    class DeviceAttributes(ABC):

        def build_config(self, apply=True, attributes=None, unconfig=False,
                         contained=False, **kwargs):
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            # create vfi configurations
            for vfi, attributes2 in attributes.sequence_values('vfis'):
                configurations.append_block(str(vfi.build_config(apply=False, attributes=attributes2, unconfig=unconfig, **kwargs)))

            with configurations.submode_context(attributes.format('bridge-domain {name}', force=True)):
                if unconfig and attributes.iswildcard:
                    configurations.submode_unconfig()

                for evi, attributes2 in attributes.mapping_values('evi_attr', keys=self.evis, sort=True):
                    cfg = attributes2.format('member evpn-instance {evi_id}')
                    if cfg:
                        cfg += attributes2.format(' vlan {vlan}', force=True)
                        configurations.append_line(cfg)

                for vfi, attributes2 in attributes.sequence_values('vfis'):
                    configurations.append_line(attributes2.format('member vfi {name}'))

                for sub, attributes2 in attributes.mapping_values('interface_attr', keys=self.interfaces, sort=True):
                    if isinstance(sub.interface, EFPInterface):
                        configurations.append_line(attributes2.format('member {interface.parent_interface.name} service-instance {interface.service_instance}'))
                    elif isinstance(sub.interface, EthernetInterface):
                        configurations.append_line(attributes2.format('member {interface.name}'))
                    else:
                        raise NotImplementedError(sub.interface)

            if apply:
                if configurations:
                    self.device.configure(str(configurations), fail_invalid=True)
            else:
                return CliConfig(device=self.device, unconfig=unconfig,
                                 cli_config=configurations, fail_invalid=True)

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

