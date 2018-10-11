
from abc import ABC
import warnings

from genie.conf.base.attributes import UnsupportedAttributeWarning,\
    AttributesHelper
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.config import CliConfig


class L2vpn(ABC):

    class DeviceAttributes(ABC):

        def build_config(self, apply=True, attributes=None, unconfig=False,
                         **kwargs):
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)


            for bd, attributes2 in attributes.sequence_values('bridge_domains'):
                configurations.append_block(
                    str(bd.build_config(apply=False, attributes=attributes2, unconfig=unconfig,
                                    contained=True)))

            for xc, attributes2 in attributes.sequence_values('xconnects'):
                configurations.append_block(
                    str(xc.build_config(apply=False, attributes=attributes2, unconfig=unconfig,
                                    contained=True)))

            for pwc, attributes2 in attributes.sequence_values('pseudowire_classes'):
                configurations.append_block(
                    str(pwc.build_config(apply=False, attributes=attributes2, unconfig=unconfig,
                                     contained=True)))

            if apply:
                if configurations:
                    self.device.configure(configurations, fail_invalid=True)
            else:
                return CliConfig(device=self.device, unconfig=unconfig,
                                 cli_config=configurations, fail_invalid=True)

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

        class PbbAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False,
                             **kwargs):
                assert not apply
                assert not kwargs, kwargs
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

