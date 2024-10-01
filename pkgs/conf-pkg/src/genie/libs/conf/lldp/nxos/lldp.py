
# import python
from abc import ABC

# import genie
from genie.conf.base.config import CliConfig
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.attributes import UnsupportedAttributeWarning, \
                                       AttributesHelper, DeviceSubAttributes


class Lldp(ABC):

    class DeviceAttributes(ABC):

        def build_config(self, apply=True, attributes=None, unconfig=False,
                         **kwargs):
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            # lldp run
            if attributes.value('enabled'):
                configurations.append_line(
                    attributes.format('feature lldp'))

            if apply:
                if configurations:
                    self.device.configure(configurations)
            else:
                return CliConfig(device=self.device, unconfig=unconfig,
                                 cli_config=configurations)

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes,
                                     unconfig=True, **kwargs)

        class InterfaceAttributes(ABC):

            def build_config(self, apply=True, attributes=None,
                             unconfig=False, **kwargs):
                assert not apply
                assert not kwargs, kwargs
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                with configurations.submode_context(
                    attributes.format('interface {intf}', force=True)):
                    # lldp transmit
                    # lldp receive
                    if attributes.value('if_enabled'):
                        configurations.append_line(
                            attributes.format('lldp transmit'))
                        configurations.append_line(
                            attributes.format('lldp receive'))

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None,
                               **kwargs):
                return self.build_config(apply=apply,
                                         attributes=attributes,
                                         unconfig=True, **kwargs)