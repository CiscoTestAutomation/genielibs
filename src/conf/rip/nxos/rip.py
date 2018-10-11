
from abc import ABC
import warnings

from genie.conf.base.attributes import UnsupportedAttributeWarning,\
    AttributesHelper
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base import Interface
from genie.conf.base.config import CliConfig

from genie.libs.conf.vrf import VrfSubAttributes


class Rip(ABC):

    class DeviceAttributes(ABC):

        def build_config(self, apply=True, attributes=None, unconfig=False, unconfig_feature=False, **kwargs):
            """method to build the configuration based on attributes

            Api to build the configuration of an `DeviceAttributes` object.
            This configuration depends of the configurable attributes of this
            object.

            Args:
                kwargs (`dict`): Argument to drive configuration

            Return:
                `str`
            """
            assert not apply  # not supported
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            # If enable feature has not been sent to the device yet,
            if unconfig and unconfig_feature:
                # if not self.enabled_feature:
                configurations.append_line('no feature rip', raw=True)
                self.enabled_feature = False
            else:
                if not self.enabled_feature:
                    configurations.append_line('feature rip', raw=True)
                    self.enabled_feature = True

                with configurations.submode_context(attributes.format('router rip {instance_id}', force=True)):
                    if unconfig and attributes.iswildcard:
                        configurations.submode_unconfig()

                    v = attributes.value('shutdown')
                    if v is not None:
                        if v is True:
                            configurations.append_line('shutdown')
                        elif not unconfig:
                            configurations.append_line('no shutdown')  # always configure it

                    for sub, attributes2 in attributes.mapping_values('vrf_attr', keys=self.vrfs, sort=True):
                        configurations.append_block(sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig, **kwargs))

            if apply:
                if configurations:
                    self.device.configure(str(configurations))
            else:
                return CliConfig(device=self.device, unconfig=unconfig,
                                 cli_config=configurations)

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

        class VrfAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                """method to build the configuration based on attributes

                Api to build the configuration of an `VrfAttributes` object.
                This configuration depends of the configurable attributes of
                this object.

                Args:
                    kwargs (`dict`): Argument to drive configuration

                Return:
                    `str`
                """
                assert not apply  # not supported
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                with configurations.submode_context(
                        None if self.vrf_name == 'default' else attributes.format('vrf {vrf_name}', force=True)):
                    if self.vrf_name != 'default' and unconfig and attributes.iswildcard:
                        configurations.submode_unconfig()

                    for sub, attributes2 in attributes.mapping_values('address_family_attr', keys=self.address_families, sort=True):
                        configurations.append_block(sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig, **kwargs))

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

            class AddressFamilyAttributes(ABC):

                def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                    """method to build the configuration based on attributes

                    Api to build the configuration of an `AddressFamilyAttributes` object.
                    This configuration depends of the configurable attributes of
                    this object.

                    Args:
                        kwargs (`dict`): Argument to drive configuration

                    Return:
                        `str`
                    """
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)

                    with configurations.submode_context(attributes.format('address-family {address_family.value}', force=True)):
                        if unconfig and attributes.iswildcard:
                            configurations.submode_unconfig()

                        configurations.append_line(attributes.format('default-metric {default_metric}'))

                        configurations.append_line(attributes.format('distance {distance}'))

                        configurations.append_line(attributes.format('maximum-paths {maximum_paths}'))

                        configurations.append_line(attributes.format('redistribute lisp route-map {redistribute_lisp_rmap}'))

                        configurations.append_line(attributes.format('redistribute direct route-map {redistribute_direct_rmap}'))

                        configurations.append_line(attributes.format('redistribute static route-map {redistribute_static_rmap}'))

                    return str(configurations)

                def build_unconfig(self, apply=True, attributes=None, **kwargs):
                    return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

# -- RIP
# nxos: interface <intf> / ip rip authentication key-chain someword
# nxos: interface <intf> / ip rip authentication mode md5
# nxos: interface <intf> / ip rip authentication mode text
# nxos: interface <intf> / ip rip metric-offset 1
# nxos: interface <intf> / ip rip offset-list 1
# nxos: interface <intf> / ip rip passive-interface
# nxos: interface <intf> / ip rip poison-reverse
# nxos: interface <intf> / ip rip route-filter prefix-list someword in
# nxos: interface <intf> / ip rip route-filter prefix-list someword out
# nxos: interface <intf> / ip rip route-filter route-map rpl1 in
# nxos: interface <intf> / ip rip route-filter route-map rpl1 out
# nxos: interface <intf> / ip rip summary-address 1.2.3.0/24
# nxos: interface <intf> / ip router rip someword
# nxos: interface <intf> / ipv6 rip metric-offset 1
# nxos: interface <intf> / ipv6 rip offset-list 1
# nxos: interface <intf> / ipv6 rip passive-interface
# nxos: interface <intf> / ipv6 rip poison-reverse
# nxos: interface <intf> / ipv6 rip route-filter prefix-list someword in
# nxos: interface <intf> / ipv6 rip route-filter prefix-list someword out
# nxos: interface <intf> / ipv6 rip route-filter route-map rpl1 in
# nxos: interface <intf> / ipv6 rip route-filter route-map rpl1 out
# nxos: interface <intf> / ipv6 rip summary-address 1:2::3/128
# nxos: interface <intf> / ipv6 router rip someword
# nxos: interface <intf> / rip shutdown

