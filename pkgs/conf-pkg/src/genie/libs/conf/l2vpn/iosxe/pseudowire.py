
from abc import ABC
import warnings
import contextlib

from genie.conf.base.attributes import UnsupportedAttributeWarning,\
    AttributesHelper
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.config import CliConfig

from ..bridge_domain import BridgeDomain
from ..xconnect import Xconnect
from ..vfi import Vfi
from ..pseudowire import Pseudowire as _Pseudowire, \
    PseudowireIPv4Neighbor, PseudowireIPv6Neighbor


class PseudowireClass(ABC):

    class DeviceAttributes(ABC):

        def build_config(self, apply=True, attributes=None, unconfig=False,
                         contained=False, **kwargs):
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            # iosxr: l2vpn / pw-class someword (config-l2vpn)
            with configurations.submode_context(attributes.format('pw-class {name}', force=True)):
                if unconfig and attributes.iswildcard:
                    configurations.submode_unconfig()

                ns, attributes2 = attributes.namespace('encapsulation')
                if ns is not None:
                    configurations.append_block(
                        ns.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

            if apply:
                if configurations:
                    self.device.configure(configurations, fail_invalid=True)
            else:
                return CliConfig(device=self.device, unconfig=unconfig,
                                 cli_config=configurations, fail_invalid=True)

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

        class EncapsulationAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False,
                             **kwargs):
                assert not apply
                assert not kwargs, kwargs
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                if self.type is None:
                    pass
                elif self.type is _Pseudowire.EncapsulationType.mpls:
                    configurations.append_line('encapsulation mpls')

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

