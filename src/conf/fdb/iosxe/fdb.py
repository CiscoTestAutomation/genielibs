
# import python
from abc import ABC

# import genie
from genie.conf.base.config import CliConfig
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.attributes import AttributesHelper


class Fdb(ABC):

    class DeviceAttributes(ABC):

        def build_config(self, apply=True, attributes=None, unconfig=False,
                         **kwargs):
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)
            
            # mac address-table aging-time <mac_aging_time>
            configurations.append_line(
                attributes.format('mac address-table aging-time {mac_aging_time}'))

            # vlan attributes
            for sub, attributes2 in attributes.mapping_values('vlan_attr',
                sort=True, keys=self.vlan_attr):
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

        class VlanAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False,
                             **kwargs):
                assert not apply
                assert not kwargs, kwargs
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                # mac address-table learning vlan <vlan_id>
                if attributes.value('vlan_mac_learning'):
                    configurations.append_line(
                        attributes.format('mac address-table learning vlan {vlan_id}', force=True))

                # mac address-table aging-time <vlan_mac_aging_time> vlan <vlan_id>
                configurations.append_line(
                    attributes.format('mac address-table aging-time '
                        '{vlan_mac_aging_time} vlan {vlan_id}', force=True))

                # mac_address_attr
                for sub, attributes2 in attributes.mapping_values('mac_address_attr',
                    sort=True, keys=self.mac_address_attr):
                    configurations.append_block(
                        sub.build_config(apply=False,
                                         attributes=attributes2,
                                         unconfig=unconfig))

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes,
                                         unconfig=True, **kwargs)


            class MacAddressAttributes(ABC):

                def build_config(self, apply=True, attributes=None,
                                 unconfig=False, **kwargs):
                    assert not apply
                    assert not kwargs, kwargs
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)

                    self.vlan_id = self.parent.vlan_id

                    # mac address-table static <mac_address> vlan <vlan_id> interface <interface>
                    if attributes.value('interface'):
                        interface = ' '.join(attributes.value('interface'))
                        cmd = 'mac address-table static {mac_address} vlan {vlan_id}'
                        cmd += ' interface {interface}'.format(interface=interface)
                        configurations.append_line(attributes.format(cmd, force=True))

                    # mac address-table static <mac_address> vlan <vlan_id> drop
                    if attributes.value('drop'):
                        configurations.append_line(attributes.format(
                            'mac address-table static {mac_address} vlan {vlan_id} drop'))

                    return str(configurations)

                def build_unconfig(self, apply=True, attributes=None,
                                   **kwargs):
                    return self.build_config(apply=apply,
                                             attributes=attributes,
                                             unconfig=True, **kwargs)
