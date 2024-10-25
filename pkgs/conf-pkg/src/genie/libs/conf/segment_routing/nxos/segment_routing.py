
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
            # nxos: segment-routing mpls
            with configurations.submode_context('segment-routing'):
                if unconfig and attributes.iswildcard:
                    configurations.submode_unconfig()
                if attributes.value('mpls') is True:
                    configurations.append_line('mpls') 
                    if attributes.value('shutdown') is True:
                        configurations.append_line('shutdown')

                    # nxos: segment-routing / mpls / global-block 16000 16001
                    v = attributes.value('global_block')
                    if v is not None:
                        configurations.append_line('global-block {first} {last}'.format(
                            first=v.start,
                            last=v[-1]+1))
                    v = attributes.value('timers_srgb_cleanup')
                    if v is not None:
                        configurations.append_line('timers srgb cleanup {cleanup_timer}'.format(
                            cleanup_timer=v)) 
                    v = attributes.value('timers_srgb_retry')
                    if v is not None:
                        configurations.append_line('timers srgb retry {retry_timer}'.format(
                            retry_timer=v))  

                    # nxos: segment-routing / mpls / connected-prefix-sid-map
                    if attributes.value('connected_prefix_sid_map'):
                        with configurations.submode_context('connected-prefix-sid-map',cancel_empty=True):

                            for address_family,address_family_sub,address_family_attributes in \
                                attributes.mapping_items('address_family_attr', keys=self.address_families, sort=True):
                                if address_family == AddressFamily.ipv4_unicast:
                                    context_cli = 'address-family ipv4'
                                with configurations.submode_context(context_cli, cancel_empty=True):
                                    for entry,attributes2 in address_family_attributes.sequence_values('connected_prefix_sid_map'):
                                        if attributes2.value('index'):
                                            configurations.append_line(attributes2.format('{prefix} index {index}'))
                                        if attributes2.value('absolute'):
                                            configurations.append_line(attributes2.format('{prefix} absolute {absolute}')) 

            if apply:
                if configurations:
                    self.device.configure(configurations, fail_invalid=True)
            else:
                if configurations:
                    return CliConfig(device=self.device, unconfig=unconfig,
                                    cli_config=configurations, fail_invalid=True)

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

