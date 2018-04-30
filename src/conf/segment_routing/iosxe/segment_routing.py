
from abc import ABC
import warnings

from genie.conf.base.attributes import UnsupportedAttributeWarning,\
    AttributesHelper
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.config import CliConfig
from genie.libs.conf.address_family import AddressFamily, AddressFamilySubAttributes


class SegmentRouting(ABC):

    class DeviceAttributes(ABC):

        def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            # iosxe: segment-routing mpls
            with configurations.submode_context('segment-routing mpls'):
                if unconfig and attributes.iswildcard:
                    configurations.submode_unconfig()

                if attributes.value('shutdown'):
                    configurations.append_line('shutdown')

                # iosxe: segment-routing mpls / set-attributes
                with configurations.submode_context('set-attributes',cancel_empty=True):
                    for address_family,address_family_sub,address_family_attributes in \
                        attributes.mapping_items('address_family_attr', keys=self.address_families, sort=True):

                        if address_family == AddressFamily.ipv4_unicast:
                            context_cli = 'address-family ipv4'
                        else:
                            context_cli = address_family_attributes.format('address-family {address_family.value}', force = True)

                        with configurations.submode_context(context_cli,cancel_empty=True):

                            if address_family_attributes.value('sr_label_preferred'):
                                configurations.append_line('sr-label-preferred')

                            if address_family_attributes.value('explicit_null'):
                                configurations.append_line('explicit-null')

                # iosxe: segment-routing mpls / global-block 16000 16001
                v = attributes.value('global_block')
                if v is not None:
                    configurations.append_line('global-block {first} {last}'.format(
                        first=v.start,
                        last=v[-1]))

                # iosxe: segment-routing mpls / connected-prefix-sid-map
                with configurations.submode_context('connected-prefix-sid-map',cancel_empty=True):

                    for address_family,address_family_sub,address_family_attributes in \
                        attributes.mapping_items('address_family_attr', keys=self.address_families, sort=True):

                        if address_family == AddressFamily.ipv4_unicast:
                            context_cli = 'address-family ipv4'
                        else:
                            context_cli = address_family_attributes.format('address-family {address_family.value}', force = True)

                        with configurations.submode_context(context_cli,cancel_empty=True):

                            for entry,attributes2 in address_family_attributes.sequence_values('connected_prefix_sid_map'):
                                configurations.append_line(attributes2.format('{prefix} index {index} range {range}'))

                # iosxe: segment-routing mpls / mapping-server / prefix-sid-map
                if attributes.value('mapping_server'):
                    with configurations.submode_context('mapping server'):
                        with configurations.submode_context('prefix-sid-map',cancel_empty=True):

                            for address_family,address_family_sub,address_family_attributes in \
                                attributes.mapping_items('address_family_attr', keys=self.address_families, sort=True):

                                if address_family == AddressFamily.ipv4_unicast:
                                    context_cli = 'address-family ipv4'
                                else:
                                    context_cli = address_family_attributes.format('address-family {address_family.value}', force = True)

                                with configurations.submode_context(context_cli,cancel_empty=True):

                                    for entry,attributes2 in address_family_attributes.sequence_values('prefix_sid_map'):
                                        if attributes2.value('attach'):
                                            configurations.append_line(attributes2.format('{prefix} index {index} range {range} attach'))
                                        else:
                                            configurations.append_line(attributes2.format('{prefix} index {index} range {range}'))

            if apply:
                if configurations:
                    self.device.configure(configurations, fail_invalid=True)
            else:
                #return str(configurations)
                return CliConfig(device=self.device, unconfig=unconfig,
                                 cli_config=configurations, fail_invalid=True)

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

