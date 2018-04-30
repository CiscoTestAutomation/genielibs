
# import python
from abc import ABC

# import genie
from genie.conf.base.config import CliConfig
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.attributes import UnsupportedAttributeWarning, \
                                       AttributesHelper


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
                    attributes.format('lldp run'))
            
            # lldp timer <hello_timer>
            if attributes.value('hello_timer'):
                configurations.append_line(
                    attributes.format('lldp timer {hello_timer}'))
            
            # lldp holdtime <hold_timer>
            if attributes.value('hold_timer'):
                configurations.append_line(
                    attributes.format('lldp holdtime {hold_timer}'))
            
            # lldp reinit <reinit_timer>
            if attributes.value('reinit_timer'):
                configurations.append_line(
                    attributes.format('lldp reinit {reinit_timer}'))

            # tlv select attributes
            sub, attributes2 = attributes.namespace('tlv_select_attr')
            if sub is not None:
                configurations.append_block(
                    sub.build_config(apply=False, attributes=attributes2,
                                     unconfig=unconfig))

            # interface attributes
            for sub, attributes2 in attributes.mapping_values('interface_attr',
                sort=True, keys=self.interface_attr):
                configurations.append_block(
                    sub.build_config(apply=False,
                                     attributes=attributes2,
                                     unconfig=unconfig))

            if apply:
                if configurations:
                    self.device.configure(configurations)
            else:
                return CliConfig(device=self.device, unconfig=unconfig,
                                 cli_config=configurations)

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes,
                                     unconfig=True, **kwargs)

        class TlvSelectAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False,
                             **kwargs):
                assert not apply
                assert not kwargs, kwargs
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)
            
                # no lldp tlv-select port-description
                if attributes.value('suppress_tlv_port_description'):
                    configurations.append_line(
                        attributes.format('no lldp tlv-select port-description'),
                        unconfig_cmd='lldp tlv-select port-description')
                if attributes.value('suppress_tlv_port_description') == False:
                    configurations.append_line(
                        attributes.format('lldp tlv-select port-description'))

                # no lldp tlv-select system-name
                if attributes.value('suppress_tlv_system_name'):
                    configurations.append_line(
                        attributes.format('no lldp tlv-select system-name'),
                        unconfig_cmd='lldp tlv-select system-name')
                if attributes.value('suppress_tlv_system_name') == False:
                    configurations.append_line(
                        attributes.format('lldp tlv-select system-name'))

                # no lldp tlv-select system-description
                if attributes.value('suppress_tlv_system_description'):
                    configurations.append_line(
                        attributes.format('no lldp tlv-select system-description'),
                        unconfig_cmd='lldp tlv-select system-description')
                if attributes.value('suppress_tlv_system_description') == False:
                    configurations.append_line(
                        attributes.format('lldp tlv-select system-description'))

                # no lldp tlv-select system-capabilities
                if attributes.value('suppress_tlv_system_capabilities'):
                    configurations.append_line(
                        attributes.format('no lldp tlv-select system-capabilities'),
                        unconfig_cmd='lldp tlv-select system-capabilities')
                if attributes.value('suppress_tlv_system_capabilities') == False:
                    configurations.append_line(
                        attributes.format('lldp tlv-select system-capabilities'))

                # no lldp tlv-select port-description
                if attributes.value('suppress_tlv_management_address'):
                    configurations.append_line(
                        attributes.format('no lldp tlv-select management-address'),
                        unconfig_cmd='lldp tlv-select management-address')
                if attributes.value('suppress_tlv_management_address') == False:
                    configurations.append_line(
                        attributes.format('lldp tlv-select management-address'))

                return str(configurations)

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