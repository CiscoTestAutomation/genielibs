
# import python
from abc import ABC

# import genie
from genie.conf.base.config import CliConfig
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.attributes import UnsupportedAttributeWarning, \
                                       AttributesHelper


class Acl(ABC):

    class DeviceAttributes(ABC):

        def build_config(self, apply=True, attributes=None, unconfig=False,
                         **kwargs):
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)
            
            # acl attributes
            for sub, attributes2 in attributes.mapping_values('acl_attr',
                sort=True, keys=self.acl_attr):
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

        class AclAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False,
                             **kwargs):
                assert not apply
                assert not kwargs, kwargs
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)
                # acl_type
                # 'ipv4-acl-type','ipv6-acl-type','eth-acl-type
                if attributes.value('acl_type'):
                    if 'ipv4-acl-type' in attributes.value('acl_type'):
                        self.cmd = 'ip access-list extended '
                    elif 'ipv6-acl-type' in attributes.value('acl_type'):
                        self.cmd = 'ipv6 access-list '
                    elif 'eth-acl-type' in attributes.value('acl_type'):
                        self.cmd = 'mac access-list extended '
                    else:
                        self.cmd = None
                else:
                    self.cmd = None

                with configurations.submode_context(
                    attributes.format('{cmd}{name}'.format(
                        cmd=self.cmd, name=self.acl_name), force=True)):
                    if unconfig and attributes.iswildcard:
                        configurations.submode_unconfig()

                        self.acl_type = self.parent.acl_type

                    # ace attributes
                    for sub, attributes2 in attributes.mapping_values('ace_attr',
                        sort=True, keys=self.ace_attr):
                        configurations.append_block(
                            sub.build_config(apply=False,
                                             attributes=attributes2,
                                             unconfig=unconfig))
                # interface attributes
                for sub, attributes2 in attributes.mapping_values('interface_attr',
                    sort=True, keys=self.interface_attr):
                    configurations.append_block(
                        sub.build_config(apply=False,
                                         attributes=attributes2,
                                         unconfig=unconfig))

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes,
                                         unconfig=True, **kwargs)


            class AceAttributes(ABC):

                def build_config(self, apply=True, attributes=None,
                                 unconfig=False, **kwargs):
                    assert not apply
                    assert not kwargs, kwargs
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)

                    self.acl_type = self.parent.acl_type

                    # [<seq>] {deny|permit} <protocol> <src> [<src_operator> <src_port>]
                    #   <dst> [<dst_operator> <dst_port>] [option <option>] 
                    #    [precedence <precedence>] [established] [log] [ttl <ttl_operator> <ttl>]
                    if 'ipv4' in self.parent.acl_type:
                        cmd = '{seq} {actions_forwarding} {protocol} {src}' if self.seq else \
                              '{actions_forwarding} {protocol} {src}'
                        if attributes.value('src_operator') and attributes.value('src_port'):
                            cmd += ' {src_operator} {src_port}'
                        cmd += ' {dst}'
                        if attributes.value('dst_operator') and attributes.value('dst_port'):
                            cmd += ' {dst_operator} {dst_port}'
                        if attributes.value('option'):
                            cmd += ' option {option}'
                        if attributes.value('precedence'):
                            cmd += ' precedence {precedence}'
                        if attributes.value('established'):
                            cmd += ' established'
                        if attributes.value('actions_logging') and \
                           'syslog' in attributes.value('actions_logging'):
                            cmd += ' log'
                        if attributes.value('ttl_operator') and attributes.value('ttl'):
                            cmd += ' ttl {ttl_operator} {ttl}'

                    # [sequence <seq>] {permit|deny} [<protocol>]  <src>
                    #   [<src_operator> <src_port>] <dst> [<dst_operator> <dst_port>]
                    #    [dscp <dscp>] [established] [log]
                    elif 'ipv6' in self.parent.acl_type:
                        cmd = 'sequence {seq} {actions_forwarding} {protocol} {src}' if self.seq else \
                              '{actions_forwarding} {protocol} {src}'
                        if attributes.value('src_operator') and attributes.value('src_port'):
                            cmd += ' {src_operator} {src_port}'
                        cmd += ' {dst}'
                        if attributes.value('dst_operator') and attributes.value('dst_port'):
                            cmd += ' {dst_operator} {dst_port}'
                        if attributes.value('dscp'):
                            cmd += ' dscp {dscp}'
                        if attributes.value('established'):
                            cmd += ' established'
                        if attributes.value('actions_logging') and \
                           'syslog' in attributes.value('actions_logging'):
                            cmd += ' log'
                    elif 'eth' in self.parent.acl_type:
                        # {permit|deny} <src> <dst> [<ether_type>]
                        cmd = '{actions_forwarding} {src} {dst}'
                        if attributes.value('ether_type'):
                            cmd += ' {ether_type}'

                    # append the line configuration
                    configurations.append_line(attributes.format(cmd, force=True),
                        unconfig_cmd=attributes.format('no ' + cmd, force=True))

                    return str(configurations)

                def build_unconfig(self, apply=True, attributes=None,
                                   **kwargs):
                    return self.build_config(apply=apply,
                                             attributes=attributes,
                                             unconfig=True, **kwargs)


            class InterfaceAttributes(ABC):

                def build_config(self, apply=True, attributes=None,
                                 unconfig=False, **kwargs):
                    assert not apply
                    assert not kwargs, kwargs
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)

                    self.acl_name = self.parent.acl_name

                    with configurations.submode_context(
                        attributes.format('interface {interface_id}', force=True)): 
                    
                        if attributes.value('if_in') and 'ipv4' in self.parent.acl_type:
                            configurations.append_line(
                                attributes.format('ip access-group {acl_name} in', force=True))
                        elif attributes.value('if_in') and 'ipv6' in self.parent.acl_type:
                            configurations.append_line(
                                attributes.format('ipv6 traffic-filter {acl_name} in', force=True))
                        elif attributes.value('if_in') and 'eth' in self.parent.acl_type:
                            configurations.append_line(
                                attributes.format('mac access-group {acl_name} in', force=True))

                        if attributes.value('if_out') and 'ipv4' in self.parent.acl_type:
                            configurations.append_line(
                                attributes.format('ip access-group {acl_name} out', force=True))
                        elif attributes.value('if_out') and 'ipv6' in self.parent.acl_type:
                            configurations.append_line(
                                attributes.format('ipv6 traffic-filter {acl_name} out', force=True))

                    return str(configurations)

                def build_unconfig(self, apply=True, attributes=None,
                                   **kwargs):
                    return self.build_config(apply=apply,
                                             attributes=attributes,
                                             unconfig=True, **kwargs)