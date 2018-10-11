
from abc import ABC
import warnings
import contextlib

from genie.conf.base.attributes import UnsupportedAttributeWarning,\
    AttributesHelper
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.config import CliConfig

from genie.libs.conf.interface import BviInterface
from genie.libs.conf.l2vpn.pseudowire import PseudowireNeighbor,\
    PseudowireIPv4Neighbor, PseudowireEviNeighbor


class BridgeDomain(ABC):

    class DeviceAttributes(ABC):

        class InterfaceAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False,
                             **kwargs):
                assert not apply
                assert not kwargs, kwargs
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                # iosxr: l2vpn / bridge group someword (config-l2vpn-bg)
                # iosxr: l2vpn / bridge group someword (config-l2vpn-bg)
                # iosxr: l2vpn / bridge group someword / bridge-domain someword2 (config-l2vpn-bg-bd)

                # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / routed interface BVI1
                # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 (config-l2vpn-bg-bd-ac)
                with configurations.submode_context(
                        attributes.format(
                            'routed interface {interface_name}' if isinstance(self.interface, BviInterface) else 'interface {interface_name}',
                            force=True),
                        exit_cmd='' if isinstance(self.interface, BviInterface) else 'exit',  # routed interface may not be an actual submode
                ):
                    if unconfig and attributes.iswildcard:
                        configurations.submode_unconfig()

                    if isinstance(self.interface, BviInterface):

                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / routed interface BVI1 / split-horizon group core
                        v = attributes.value('split_horizon_group_core')
                        if v is True:
                            configurations.append_line('split-horizon group core')

                        if configurations:
                            # There are configurations... It must be a submode; exit.
                            configurations.append_line('exit', raw=True)
                        else:
                            # There are no configurations... May not be be a submode; Don't exit.
                            pass

                    else:
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / dhcp ipv4 none
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / dhcp ipv4 snoop profile someword3
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / dynamic-arp-inspection (config-l2vpn-bg-bd-ac-dai)
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / dynamic-arp-inspection / address-validation (config-l2vpn-bg-bd-ac-dai-av)
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / dynamic-arp-inspection / address-validation / dst-mac
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / dynamic-arp-inspection / address-validation / dst-mac disable
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / dynamic-arp-inspection / address-validation / ipv4
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / dynamic-arp-inspection / address-validation / ipv4 disable
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / dynamic-arp-inspection / address-validation / src-mac
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / dynamic-arp-inspection / address-validation / src-mac disable
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / dynamic-arp-inspection / disable
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / dynamic-arp-inspection / logging
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / dynamic-arp-inspection / logging disable
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / flooding
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / flooding disable
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / flooding unknown-unicast
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / flooding unknown-unicast disable
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / igmp snooping profile someword3
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / ip-source-guard (config-l2vpn-bg-bd-ac-ipsg)
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / ip-source-guard / disable
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / ip-source-guard / logging
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / ip-source-guard / logging disable

                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / mac (config-l2vpn-bg-bd-ac-mac)
                        sub, attributes2 = attributes.namespace('mac')
                        if sub is not None:
                            configurations.append_block(
                                    sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / mac (config-l2vpn-bg-bd-ac-mac)

                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / mld snooping profile someword3

                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / split-horizon group
                        v = attributes.value('split_horizon_group')
                        if v is True:
                            configurations.append_line('split-horizon group')

                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / static-mac-address aaaa.bbbb.cccc
                        configurations.append_line(attributes.format('static-mac-address {static_mac_address}'))

                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / storm-control broadcast kbps 64
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / storm-control broadcast pps 1
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / storm-control multicast kbps 64
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / storm-control multicast pps 1
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / storm-control unknown-unicast kbps 64
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / storm-control unknown-unicast pps 1

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

            class MacAttributes(ABC):

                def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                    assert not apply
                    assert not kwargs, kwargs
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)

                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / mac (config-l2vpn-bg-bd-ac-mac)
                    with configurations.submode_context('mac', cancel_empty=True):

                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / mac / aging (config-l2vpn-bg-bd-ac-mac-aging)
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / mac / aging / time 300
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / mac / aging / type absolute
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / mac / aging / type inactivity
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / mac / learning
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / mac / learning disable
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / mac / limit (config-l2vpn-bg-bd-ac-mac-limit)
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / mac / limit / action flood
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / mac / limit / action no-flood
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / mac / limit / action none
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / mac / limit / action shutdown
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / mac / limit / maximum 1
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / mac / limit / notification both
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / mac / limit / notification none
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / mac / limit / notification syslog
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / mac / limit / notification trap
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / mac / port-down flush
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / mac / port-down flush disable
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / mac / secure (config-l2vpn-bg-bd-ac-mac-secure)
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / mac / secure / action none
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / mac / secure / action restrict
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / mac / secure / action shutdown
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / mac / secure / disable
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / mac / secure / logging
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 / mac / secure / logging disable

                        pass

                    return str(configurations)

                def build_unconfig(self, apply=True, attributes=None, **kwargs):
                    return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

        class NeighborAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                assert not apply
                assert not kwargs, kwargs
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                nbr_ctx = None
                nbr_is_submode = True
                if isinstance(self.neighbor, PseudowireIPv4Neighbor):
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / neighbor 1.2.3.4 pw-id 1 (config-l2vpn-bg-bd-pw)
                    assert self.ip is not None
                    assert self.pw_id is not None
                    nbr_ctx = attributes.format('neighbor {ip} pw-id {pw_id}', force=True)
                elif isinstance(self.neighbor, PseudowireEviNeighbor):
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / neighbor evpn 1 target 1
                    assert self.evi is not None
                    assert self.ac_id is not None
                    nbr_ctx = attributes.format('neighbor evpn {evi.evi_id} target {ac_id}', force=True)
                    nbr_is_submode = False
                else:
                    raise ValueError(self.neighbor)
                if not nbr_is_submode:
                    configurations.append_line(nbr_ctx)
                else:
                    with configurations.submode_context(nbr_ctx):
                        if unconfig and attributes.iswildcard:
                            configurations.submode_unconfig()

                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / neighbor 1.2.3.4 pw-id 1 / backup neighbor 1.2.3.4 pw-id 1 (config-l2vpn-bg-bd-pw-backup)
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / neighbor 1.2.3.4 pw-id 1 / backup neighbor 1.2.3.4 pw-id 1 / pw-class someword3

                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / neighbor 1.2.3.4 pw-id 1 / dhcp ipv4 none
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / neighbor 1.2.3.4 pw-id 1 / dhcp ipv4 snoop profile someword3
                        v = attributes.value('dhcp_ipv4_snooping_profile')
                        if v is not None:
                            if v is False:
                                configurations.append_line('dhcp ipv4 none')
                            else:
                                configurations.append_line('dhcp ipv4 snoop profile {}'.format(v))

                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / neighbor 1.2.3.4 pw-id 1 / flooding
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / neighbor 1.2.3.4 pw-id 1 / flooding disable
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / neighbor 1.2.3.4 pw-id 1 / flooding unknown-unicast
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / neighbor 1.2.3.4 pw-id 1 / flooding unknown-unicast disable

                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / neighbor 1.2.3.4 pw-id 1 / igmp snooping profile someword3
                        v = attributes.value('igmp_snooping_profile')
                        if v is not None:
                            if v is False:
                                pass
                            else:
                                configurations.append_line('igmp snooping profile {}'.format(v))

                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / neighbor 1.2.3.4 pw-id 1 / mac (config-l2vpn-bg-bd-pw-mac)
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / neighbor 1.2.3.4 pw-id 1 / mac / aging (config-l2vpn-bg-bd-pw-mac-aging)
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / neighbor 1.2.3.4 pw-id 1 / mac / aging / time 300
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / neighbor 1.2.3.4 pw-id 1 / mac / aging / type absolute
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / neighbor 1.2.3.4 pw-id 1 / mac / aging / type inactivity
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / neighbor 1.2.3.4 pw-id 1 / mac / learning
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / neighbor 1.2.3.4 pw-id 1 / mac / learning disable
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / neighbor 1.2.3.4 pw-id 1 / mac / limit (config-l2vpn-bg-bd-pw-mac-limit)
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / neighbor 1.2.3.4 pw-id 1 / mac / limit / action flood
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / neighbor 1.2.3.4 pw-id 1 / mac / limit / action no-flood
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / neighbor 1.2.3.4 pw-id 1 / mac / limit / action none
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / neighbor 1.2.3.4 pw-id 1 / mac / limit / action shutdown
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / neighbor 1.2.3.4 pw-id 1 / mac / limit / maximum 1
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / neighbor 1.2.3.4 pw-id 1 / mac / limit / notification both
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / neighbor 1.2.3.4 pw-id 1 / mac / limit / notification none
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / neighbor 1.2.3.4 pw-id 1 / mac / limit / notification syslog
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / neighbor 1.2.3.4 pw-id 1 / mac / limit / notification trap
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / neighbor 1.2.3.4 pw-id 1 / mac / port-down flush
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / neighbor 1.2.3.4 pw-id 1 / mac / port-down flush disable
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / neighbor 1.2.3.4 pw-id 1 / mac / secure (config-l2vpn-bg-bd-pw-mac-secure)
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / neighbor 1.2.3.4 pw-id 1 / mac / secure / action none
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / neighbor 1.2.3.4 pw-id 1 / mac / secure / action restrict
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / neighbor 1.2.3.4 pw-id 1 / mac / secure / action shutdown
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / neighbor 1.2.3.4 pw-id 1 / mac / secure / disable
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / neighbor 1.2.3.4 pw-id 1 / mac / secure / logging
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / neighbor 1.2.3.4 pw-id 1 / mac / secure / logging disable

                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / neighbor 1.2.3.4 pw-id 1 / mld snooping profile someword3
                        v = attributes.value('mld_snooping_profile')
                        if v is not None:
                            if v is False:
                                pass
                            else:
                                configurations.append_line('mld snooping profile {}'.format(v))

                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / neighbor 1.2.3.4 pw-id 1 / mpls static label local 16 remote 16
                        remote_label = attributes.value('mpls_static_label')
                        if remote_label is not None:
                            local_label = self.parent.neighbor_attr[self.remote_neighbor].mpls_static_label
                            if local_label is None:
                                warnings.warn(
                                    'remote neighbor {!r} mpls_static_label missing'.format(self.remote_neighbor),
                                    UnsupportedAttributeWarning)
                            else:
                                configurations.append_line('mpls static label local {} remote {}'.\
                                                      format(local_label, remote_label))

                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / neighbor 1.2.3.4 pw-id 1 / pw-class someword3
                        v = attributes.value('pw_class')
                        if v is not None:
                            configurations.append_line('pw-class {}'.\
                                                  format(v.device_attr[self.device].name))

                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / neighbor 1.2.3.4 pw-id 1 / split-horizon group
                        if attributes.value('split_horizon'):
                            configurations.append_line('split-horizon group')

                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / neighbor 1.2.3.4 pw-id 1 / static-mac-address aaaa.bbbb.cccc
                        configurations.append_line(attributes.format('static-mac-address {static_mac_address}'))

                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / neighbor 1.2.3.4 pw-id 1 / storm-control broadcast kbps 64
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / neighbor 1.2.3.4 pw-id 1 / storm-control broadcast pps 1
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / neighbor 1.2.3.4 pw-id 1 / storm-control multicast kbps 64
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / neighbor 1.2.3.4 pw-id 1 / storm-control multicast pps 1
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / neighbor 1.2.3.4 pw-id 1 / storm-control unknown-unicast kbps 64
                        # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / neighbor 1.2.3.4 pw-id 1 / storm-control unknown-unicast pps 1

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

        class EviAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False,
                             **kwargs):
                assert not apply
                assert not kwargs, kwargs
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / evi 1 (config-l2vpn-bg-bd-evi)
                with configurations.submode_context(
                        attributes.format('evi {evi_id}', force=True),
                        exit_cmd=''):  # evi is not a sub-mode in all releases.
                    if unconfig and attributes.iswildcard:
                        configurations.submode_unconfig()

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

        class VniAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False,
                             **kwargs):
                assert not apply
                assert not kwargs, kwargs
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                # iosxr: l2vpn / bridge group someword (config-l2vpn-bg)
                # iosxr: l2vpn / bridge group someword / bridge-domain someword2 (config-l2vpn-bg-bd)

                # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / member vni 1 (config-l2vpn-bg-bd-vni)
                with configurations.submode_context(attributes.format('member vni {vni_id}', force=True)):
                    if unconfig and attributes.iswildcard:
                        configurations.submode_unconfig()

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

        class MacAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False,
                             **kwargs):
                assert not apply
                assert not kwargs, kwargs
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / mac (config-l2vpn-bg-bd-mac)
                with configurations.submode_context('mac', cancel_empty=True):

                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / mac / aging (config-l2vpn-bg-bd-mac-aging)
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / mac / aging / time 300
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / mac / aging / type absolute
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / mac / aging / type inactivity
                    with configurations.submode_context('aging',cancel_empty=True):
                        configurations.append_line(attributes.format('time {aging_time}'))

                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / mac / learning
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / mac / learning disable
                    v = attributes.value('learning_disable')
                    if v is True:
                        configurations.append_line('learning disable')
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / mac / limit (config-l2vpn-bg-bd-mac-limit)
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / mac / limit / action flood
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / mac / limit / action no-flood
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / mac / limit / action none
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / mac / limit / action shutdown
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / mac / limit / maximum 1
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / mac / limit / notification both
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / mac / limit / notification none
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / mac / limit / notification syslog
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / mac / limit / notification trap
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / mac / port-down flush
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / mac / port-down flush disable
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / mac / secure (config-l2vpn-bg-bd-mac-secure)
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / mac / secure / action none
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / mac / secure / action restrict
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / mac / secure / action shutdown
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / mac / secure / disable
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / mac / secure / logging
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / mac / secure / logging disable
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / mac / static-address aaaa.bbbb.cccc drop
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / mac / withdraw access-pw disable
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / mac / withdraw disable
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / mac / withdraw optimize
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / mac / withdraw relay
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / mac / withdraw state-down

                    pass

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

        def build_config(self, apply=True, attributes=None, unconfig=False,
                         contained=False, **kwargs):
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            # iosxr: l2vpn (config-l2vpn)
            submode_stack = contextlib.ExitStack()
            if not contained:
                submode_stack.enter_context(
                    configurations.submode_context('l2vpn'))

            # iosxr: l2vpn / bridge group someword (config-l2vpn-bg)
            with configurations.submode_context(attributes.format('bridge group {group_name}', force=True, cancel_empty=True)):

                # iosxr: l2vpn / bridge group someword / bridge-domain someword2 (config-l2vpn-bg-bd)
                with configurations.submode_context(attributes.format('bridge-domain {name}', force=True)):
                    if unconfig and attributes.iswildcard:
                        configurations.submode_unconfig()

                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / coupled-mode
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / dhcp ipv4 snoop profile someword3
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / dynamic-arp-inspection (config-l2vpn-bg-bd-dai)
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / dynamic-arp-inspection / address-validation (config-l2vpn-bg-bd-dai-av)
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / dynamic-arp-inspection / address-validation / dst-mac
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / dynamic-arp-inspection / address-validation / ipv4
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / dynamic-arp-inspection / address-validation / src-mac
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / dynamic-arp-inspection / logging

                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / evi 1 (config-l2vpn-bg-bd-evi)
                    for sub, attributes2 in attributes.mapping_values('evi_attr', keys=self.evis, sort=True):
                        configurations.append_block(
                                sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / flooding disable
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / flooding unknown-unicast disable
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / igmp snooping disable
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / igmp snooping profile someword3

                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / routed interface BVI1
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / interface Bundle-Ether1 (config-l2vpn-bg-bd-ac)
                    for sub, attributes2 in attributes.mapping_values('interface_attr', keys=self.interfaces, sort=True):
                        configurations.append_block(
                            sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / ip-source-guard (config-l2vpn-bg-bd-ipsg)
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / ip-source-guard / logging

                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / mac (config-l2vpn-bg-bd-mac)
                    ns, attributes2 = attributes.namespace('mac')
                    if ns is not None:
                        configurations.append_block(
                                ns.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / member vni 1 (config-l2vpn-bg-bd-vni)
                    for sub, attributes2 in attributes.mapping_values('vni_attr', keys=self.vnis, sort=True):
                        configurations.append_block(
                                sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / mld snooping profile someword3
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / mtu 100

                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / neighbor 1.2.3.4 pw-id 1 (config-l2vpn-bg-bd-pw)
                    for sub, attributes2 in attributes.mapping_values('neighbor_attr', keys=self.pseudowire_neighbors, sort=True):
                        configurations.append_block(
                                sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / neighbor evpn evi 1 target 1
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / neighbor evpn evi 1 target 1 source 1

                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / nv satellite (config-l2vpn-bg-bd-nv)
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / nv satellite / offload ipv4 multicast enable

                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / pbb core (config-l2vpn-bg-bd-pbb-core)
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / pbb core / evi 1 (config-l2vpn-bg-bd-pbb-core-evi)
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / pbb core / mac (config-l2vpn-bg-bd-pbb-core-mac)
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / pbb core / mac / aging (config-l2vpn-bg-bd-pbb-core-mac-aging)
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / pbb core / mac / aging / time 300
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / pbb core / mac / aging / type absolute
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / pbb core / mac / aging / type inactivity
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / pbb core / mac / learning
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / pbb core / mac / learning disable
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / pbb core / mmrp-flood-optimization
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / pbb core / rewrite ingress tag push dot1ad 1 symmetric

                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / pbb edge i-sid 256 core-bridge someword3 (config-l2vpn-bg-bd-pbb-edge)
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / pbb edge i-sid 256 core-bridge someword3 / dhcp ipv4 none
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / pbb edge i-sid 256 core-bridge someword3 / dhcp ipv4 snoop profile someword4
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / pbb edge i-sid 256 core-bridge someword3 / igmp snooping profile someword4
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / pbb edge i-sid 256 core-bridge someword3 / mac (config-l2vpn-bg-bd-pbb-edge-mac)
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / pbb edge i-sid 256 core-bridge someword3 / mac / aging (config-l2vpn-bg-bd-pbb-edge-mac-aging)
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / pbb edge i-sid 256 core-bridge someword3 / mac / aging / time 300
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / pbb edge i-sid 256 core-bridge someword3 / mac / aging / type absolute
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / pbb edge i-sid 256 core-bridge someword3 / mac / aging / type inactivity
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / pbb edge i-sid 256 core-bridge someword3 / mac / learning
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / pbb edge i-sid 256 core-bridge someword3 / mac / learning disable
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / pbb edge i-sid 256 core-bridge someword3 / mac / limit (config-l2vpn-bg-bd-pbb-edge-mac-limit)
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / pbb edge i-sid 256 core-bridge someword3 / mac / limit / action flood
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / pbb edge i-sid 256 core-bridge someword3 / mac / limit / action no-flood
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / pbb edge i-sid 256 core-bridge someword3 / mac / limit / action none
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / pbb edge i-sid 256 core-bridge someword3 / mac / limit / action shutdown
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / pbb edge i-sid 256 core-bridge someword3 / mac / limit / maximum 1
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / pbb edge i-sid 256 core-bridge someword3 / mac / limit / notification both
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / pbb edge i-sid 256 core-bridge someword3 / mac / limit / notification none
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / pbb edge i-sid 256 core-bridge someword3 / mac / limit / notification syslog
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / pbb edge i-sid 256 core-bridge someword3 / mac / limit / notification trap
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / pbb edge i-sid 256 core-bridge someword3 / mac / secure (config-l2vpn-bg-bd-pbb-edge-mac-sec)
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / pbb edge i-sid 256 core-bridge someword3 / mac / secure / accept-shutdown
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / pbb edge i-sid 256 core-bridge someword3 / mac / secure / action none
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / pbb edge i-sid 256 core-bridge someword3 / mac / secure / action restrict
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / pbb edge i-sid 256 core-bridge someword3 / mac / secure / action shutdown
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / pbb edge i-sid 256 core-bridge someword3 / mac / secure / disable
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / pbb edge i-sid 256 core-bridge someword3 / mac / secure / logging
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / pbb edge i-sid 256 core-bridge someword3 / mac / secure / logging disable
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / pbb edge i-sid 256 core-bridge someword3 / split-horizon group vfi disable
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / pbb edge i-sid 256 core-bridge someword3 / static-mac-address aaaa.bbbb.cccc bmac aaaa.bbbb.cccc
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / pbb edge i-sid 256 core-bridge someword3 / unknown-unicast-bmac aaaa.bbbb.cccc

                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / shutdown
                    if attributes.value('shutdown'):
                        configurations.append_line('shutdown')

                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / storm-control broadcast kbps 64
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / storm-control broadcast pps 1
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / storm-control multicast kbps 64
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / storm-control multicast pps 1
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / storm-control unknown-unicast kbps 64
                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / storm-control unknown-unicast pps 1

                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / transport-mode vlan passthrough

                    # iosxr: l2vpn / bridge group someword / bridge-domain someword2 / vfi someword3 (config-l2vpn-bg-bd-vfi)
                    for vfi, attributes2 in attributes.sequence_values('vfis'):
                        configurations.append_block(
                                str(vfi.build_config(apply=False, attributes=attributes2, unconfig=unconfig)))

            submode_stack.close()
            if apply:
                if configurations:
                    self.device.configure(str(configurations), fail_invalid=True)
            else:
                return CliConfig(device=self.device, unconfig=unconfig,
                                 cli_config=configurations, fail_invalid=True)

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

