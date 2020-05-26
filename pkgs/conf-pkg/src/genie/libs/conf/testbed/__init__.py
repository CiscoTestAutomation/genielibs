'''genie.libs Testbed class.'''

import collections
from collections import abc
import contextlib
import functools
import types
from copy import copy

# import pcall
import importlib
try:
    pcall = importlib.import_module('pyats.async').pcall
except ImportError:
    from pyats.async_ import pcall
# # import pcall
# from pyats.async import pcall

from genie.conf import Genie
import genie.conf.base.testbed
from genie.conf.base import Device
from genie.conf.base.attributes import AttributesHelper, AttributesHelper2
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.config import Config, YangConfig, CliConfig

def _clean_cfgs_dict(cfgs, *, testbed=None, device=None, add_to_cfgs=None, merge=True):
    '''Clean configurations and return a dictionnary of lists of Config objects
    indexed by device name.

    cfgs can be:
        - A Config object or a string (converted to CliConfig)
        - A Mapping (dict) to recurse upon (indexed by Device object or device
          name);
        - An Iterable (list/tuple) to recurse upon;

    device can be:
        - A string (device name);
        - A device object;
        - A feature object that has a "device" attribute.

    If add_to_cfgs is provided, Config objects are appended instead of creating
    a new dictionnary.
    '''

    cfgs = _clean_cfgs_dict_inner(cfgs=cfgs, testbed=testbed, device=device, add_to_cfgs=add_to_cfgs)

    if merge:
        # Update in place
        cfgs.update({
            device_name: _clean_cfgs_list_merge(device_cfgs)
            for device_name, device_cfgs in cfgs.items()})

    return cfgs


def _clean_cfgs_list_merge(device_cfgs):

    new_device_cfgs = []

    for device_cfg in device_cfgs:
        if isinstance(device_cfg, CliConfig) and not str(device_cfg):
            # Empty, ignore it.
            continue
        if new_device_cfgs and \
                isinstance(device_cfg, CliConfig) \
                and type(device_cfg) is type(new_device_cfgs[-1]) \
                and device_cfg.device is new_device_cfgs[-1].device \
                and device_cfg.unconfig == new_device_cfgs[-1].unconfig \
                and device_cfg.fkwargs == new_device_cfgs[-1].fkwargs:
            # Replace previous with new merged CLI.
            new_device_cfg = type(device_cfg)(
                device=device_cfg.device,
                unconfig=device_cfg.unconfig,
                cli_config='\n'.join([
                    str(new_device_cfgs[-1]),
                    str(device_cfg),
                ]),
                **device_cfg.fkwargs)
            new_device_cfgs[-1] = new_device_cfg
            continue
        new_device_cfgs.append(device_cfg)

    return new_device_cfgs


def _clean_cfgs_dict_inner(cfgs, *, testbed=None, device=None, add_to_cfgs=None):
    if add_to_cfgs is None:
        add_to_cfgs = {}
    if not cfgs:
        return add_to_cfgs

    if isinstance(cfgs, str):
        # Need a device object to instantiate CliConfig
        if device is None:
            raise ValueError(cfgs)
        if isinstance(device, str):
            if not testbed:
                testbed = Genie.testbed
            device = testbed.devices[device]
        elif not isinstance(device, Device):
            # A Feature?
            device = device.device
            assert isinstance(device, Device)
        cfgs = CliConfig(cfgs, device=device)
        # Fallthrough to Config case below...

    elif isinstance(cfgs, abc.Mapping):
        for device, device_cfgs in cfgs.items():
            _clean_cfgs_dict_inner(device_cfgs, testbed=testbed, device=device,
                                   add_to_cfgs=add_to_cfgs)
        return add_to_cfgs

    elif isinstance(cfgs, abc.Iterable):
        for device_cfg in cfgs:
            _clean_cfgs_dict_inner(device_cfg, testbed=testbed, device=device,
                                   add_to_cfgs=add_to_cfgs)
        return add_to_cfgs

    if isinstance(cfgs, Config):
        device = cfgs.device.name
        add_to_cfgs.setdefault(device, []).append(cfgs)
        return add_to_cfgs

    raise ValueError(cfgs)


class Testbed(genie.conf.base.testbed.Testbed):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_build_objects(self, *, devices=None, links=None, interfaces=None):

        bo = types.SimpleNamespace()

        # Get all the iterables
        bo.devices = set(self.find_devices() if devices is None else devices.values())
        bo.interfaces = set(self.find_interfaces(device=lambda x: x in bo.devices) if interfaces is None else interfaces)
        bo.links = set(
            self.find_links(
                interfaces=lambda x: set(x) <= bo.interfaces)
            if links is None
            else links)

        from genie.libs.conf.device.tgen import Device as TgenDevice
        bo.tgen_devices = {device
                           for device in bo.devices
                           if isinstance(device, TgenDevice)}
        from genie.libs.conf.device import EmulatedDevice
        bo.emulated_devices = {device
                               for device in bo.devices
                               if isinstance(device, EmulatedDevice)}

        bo.active_interfaces = copy(bo.interfaces)
        bo.active_devices = {interface.device
                             for interface in bo.active_interfaces}

        bo.inactive_interfaces = {interface
                                  for device in bo.active_devices
                                  for interface in device.interfaces.values()
                                  if interface.obj_state == 'inactive'}

        # Activate dependent parent interfaces
        for interface in bo.active_interfaces:
            while True:
                parent_interface = interface.parent_interface
                if parent_interface is None \
                        or parent_interface not in bo.inactive_interfaces:
                    break
                parent_interface.obj_state = 'active'
                bo.active_interfaces.add(parent_interface)
                bo.inactive_interfaces.remove(parent_interface)
                interface = parent_interface  # recurse

        bo.active_links = copy(bo.links)

        bo.physical_interfaces = copy(bo.active_interfaces)

        bo.physical_tgen_interfaces = {interface
                                       for interface in bo.physical_interfaces
                                       if interface.device in bo.tgen_devices}
        bo.physical_interfaces -= bo.physical_tgen_interfaces

        from genie.libs.conf.interface import LoopbackInterface
        bo.loopback_interfaces = {interface
                                  for interface in bo.physical_interfaces
                                  if isinstance(interface, LoopbackInterface)}
        bo.physical_interfaces -= bo.loopback_interfaces

        from genie.libs.conf.interface import AggregatedInterface
        bo.bundle_interfaces = {interface
                                for interface in bo.physical_interfaces
                                if isinstance(interface, AggregatedInterface)}
        bo.physical_interfaces -= bo.bundle_interfaces

        from genie.libs.conf.interface import TunnelInterface
        bo.tunnel_interfaces = {interface
                                for interface in bo.physical_interfaces
                                if isinstance(interface, TunnelInterface)}
        bo.physical_interfaces -= bo.tunnel_interfaces

        from genie.libs.conf.interface import VniInterface
        bo.vni_interfaces = {interface
                             for interface in bo.physical_interfaces
                             if isinstance(interface, VniInterface)}
        bo.physical_interfaces -= bo.vni_interfaces

        from genie.libs.conf.interface import SubInterface
        bo.sub_interfaces = {interface
                             for interface in bo.physical_interfaces
                             if isinstance(interface, SubInterface)}
        bo.physical_interfaces -= bo.sub_interfaces

        bo.breakout_interfaces = {
            interface
            for interface in bo.physical_interfaces
            if getattr(interface, 'breakout', None) is not None}
        bo.physical_interfaces -= bo.breakout_interfaces
        # Add inactive breakout interfaces/controllers from active devices that
        # are used to define active physical interfaces.
        # These are kept inactive.
        for inactive_breakout_interface in {
                interface
                for device in bo.active_devices
                for interface in device.interfaces.values()
                if interface.obj_state == 'inactive' \
                and getattr(interface, 'breakout', None) is not None}:
            number_pattern = '{}/'.format(
                inactive_breakout_interface.parse_interface_name().number)
            if any(
                    interface.device is inactive_breakout_interface.device \
                    and (interface.parse_interface_name().number \
                         or '').startswith(number_pattern)
                    for interface in bo.physical_interfaces):
                bo.breakout_interfaces.add(inactive_breakout_interface)
        bo.inactive_interfaces -= bo.breakout_interfaces

        bo.physical_other_interfaces = copy(bo.physical_interfaces)
        from genie.libs.conf.interface import Controller
        bo.physical_controllers = {
            interface
            for interface in bo.physical_other_interfaces
            if isinstance(interface, Controller)}
        bo.physical_other_interfaces -= bo.physical_controllers
        from genie.libs.conf.interface import OpticsController
        bo.physical_optics_controllers = {
            interface
            for interface in bo.physical_controllers
            if isinstance(interface, OpticsController)}
        bo.physical_controllers -= bo.physical_optics_controllers

        from genie.libs.conf.interface import Controller
        bo.breakout_controllers = {interface
                                   for interface in bo.breakout_interfaces
                                   if isinstance(interface, Controller)}
        bo.breakout_interfaces -= bo.breakout_controllers

        from genie.libs.conf.interface import ManagementInterface
        bo.physical_other_interfaces_no_mgmt = {
            interface
            for interface in bo.physical_other_interfaces
            if not isinstance(interface, ManagementInterface)}

        # Drop inactive interfaces who's parent is also inactive
        # This avoids interacting with interfaces that may not be accessible.
        bo.dropped_inactive_interfaces = set()
        for interface in bo.inactive_interfaces:
            parent_interface = interface.parent_interface
            if parent_interface is not None \
                    and parent_interface in bo.inactive_interfaces:
                bo.dropped_inactive_interfaces.add(interface)
        bo.inactive_interfaces -= bo.dropped_inactive_interfaces

        return bo

    def build_config(self, *, devices=None, links=None, interfaces=None,
                     attributes=None, apply=True):
        """method to build the configuration of the whole testbed

        Loops through each testbed, link and configure the whole testbed
        A Dictionary will be returned with devices as keys

        Args:
            None

        Return:
            `dict`

        Examples:
            >>> from genie.conf import Genie
            >>> genie_tb = Genie.init(tb=yaml)
            ....
            >>> configuration = genie_tb.build_config()
            >>> genie_tb.apply_config(configuration)


            # Assuming Genie was already initiated at earlier time
            >>> configuration = Genie.testbed.build_config()
            >>> genie_tb.apply_config(configuration)
        """
        cfgs = {}

        bo = self.get_build_objects(devices=devices or self.devices,
                                    links=links or self.links,
                                    interfaces=interfaces or self.interfaces)

        scale_optimize = True

        exit_stack = contextlib.ExitStack()
        tgen_apply_exit_stack = contextlib.ExitStack()
        exit_stack.enter_context(tgen_apply_exit_stack)
        with exit_stack:

            def config_features(features, unconfig=False, fkwargs=None):
                features = set(features)  # Finalize iterable; We need to pop.
                in_fkwargs = fkwargs
                feature_cfgs = {}
                for feature in features:
                    fkwargs = in_fkwargs
                    if fkwargs is None:
                        fkwargs = feature_kwargs.pop(feature, {})
                    if unconfig:
                        cfg = feature.build_unconfig(apply=False, **fkwargs)
                    else:
                        cfg = feature.build_config(apply=False, **fkwargs)
                    _clean_cfgs_dict(cfg, testbed=self, device=feature,
                                     add_to_cfgs=feature_cfgs, merge=False)
                feature_cfgs = {
                    device: sorted(device_cfgs)
                    for device, device_cfgs in feature_cfgs.items()}
                _clean_cfgs_dict(feature_cfgs, add_to_cfgs=cfgs)

            def unconfig_features(features, **kwargs):
                return config_features(features, unconfig=True, **kwargs)

            def flush_cfgs():
                if apply:
                    self.config_on_devices(cfgs, fail_invalid=True)
                    cfgs.clear()

            feature_kwargs = collections.defaultdict(
                functools.partial(collections.defaultdict, set))
            for device in bo.active_devices:
                for feature in device.features:
                    feature_kwargs[feature]['devices'].add(device)
            for link in bo.active_links:
                for feature in link.features:
                    feature_kwargs[feature]['links'].add(link)
                    feature_kwargs[feature]['interfaces'].update(link.interfaces)
                    feature_kwargs[feature]['devices'].update(link.devices)
            for interface in bo.active_interfaces:
                for feature in interface.features:
                    feature_kwargs[feature]['interfaces'].add(interface)
                    feature_kwargs[feature]['devices'].add(interface.device)

            # tgen - emulation control (stop)
            for tgen_device in bo.tgen_devices:
                tgen_device.stop_emulation()

            # tgen - enable optimizations
            if scale_optimize:
                for tgen_device in bo.tgen_devices:
                    tgen_apply_exit_stack.enter_context(
                        tgen_device.defer_apply_context())

            config_features(bo.active_devices - bo.emulated_devices)
            flush_cfgs()

            config_features(bo.physical_tgen_interfaces)
            config_features(bo.active_devices & bo.emulated_devices)
            flush_cfgs()

            # with steps.start('System configuration'):
            # config - system -- See Device.build_config

            # with steps.start('Clock configuration'):
            # TODO
            # not enxr
            # set s_clock [clock format [clock seconds] -format "%T %d %B %Y" -gmt 0]
            # if { [OK] != [enaExecCLI $router "clock set $s_clock"] } {
            #     enaLogVerify -fail "Unable to set clock on router $router"
            # }

            # with steps.start('Management interfaces configuration'):
            # TODO
            # set lvMgmtIntfs [enaTbGetMgmtInterface $lActiveRouters -create false -all true]
            # if { [enaPatternListSearch $proc_params(config) mgmt] != -1 } {
            #     _enaTbConfigureTestbed_eval_custom_calls before config mgmt
            #
            #     aetest::log -diag [enaFrame "Step [incr step]: Management interfaces configuration"]
            #     if { [OK] == [enaVerify "management interfaces configuration" \
            #                 {enaTbConfigureInterface $lvMgmtIntfs} \
            #                 [OK] -format ena_return_code -eval true] } {
            #         set lAsyncIds {}
            #         set lvUpMgmtIntfs {}
            #         foreach vIntf $lvMgmtIntfs {
            #             if { [enaTbGetInterfaceParam $vIntf -shutdown] } { continue }
            #             lappend lvUpMgmtIntfs $vIntf
            #         }
            #         foreach router [enaTbGetRoutersFromInterfaces $lvUpMgmtIntfs] {
            #             lappend lAsyncIds [enaAsyncStart -router $router -command {
            #                     set ret [OK]
            #
            #                     foreach vIntf [enaTbFindInterface -router $router -free-list $lvUpMgmtIntfs -objState * -all] {
            #
            #                         set route_args {}
            #                         enaGetTftpServerInfo arr_tftp_info -router $router
            #                         if { [info exists arr_tftp_info(tftp_addr)] } {
            #                             set tftp_svr_net $arr_tftp_info(tftp_addr)
            #                             if { [info exists ::tb_tftp_server_subnet($::env(TESTBED))] } {
            #                                 set tftp_svr_mask $::tb_tftp_server_subnet($::env(TESTBED))
            #                             } else {
            #                                 set tftp_svr_mask [enaIpPrefixLengthToNetmask [enaIpAddressDefaultPrefixLength $tftp_svr_net]]
            #                             }
            #                             set tftp_svr_net [enaIpNetmaskToNetwork $tftp_svr_net $tftp_svr_mask]
            #                         } else {
            #                             set tftp_svr_net  223.255.254.0
            #                             set tftp_svr_mask 255.255.255.0
            #                         }
            #                         lappend route_args \
            #                             -destn-addr $tftp_svr_net \
            #                             -destn-mask $tftp_svr_mask
            #
            #                         if { [info exists ::tb_gateway_addr($::env(TESTBED),$router)] } {
            #                             lappend route_args \
            #                                 -fwd_to $::tb_gateway_addr($::env(TESTBED),$router)
            #                         } elseif { [info exists ::tb_gateway_addr($::env(TESTBED))] } {
            #                             lappend route_args \
            #                                 -fwd_to $::tb_gateway_addr($::env(TESTBED))
            #                         }
            #
            #                         # XXXJST Forcing -vrf because static routing object
            #                         # would not be able to find the management interface in
            #                         # the main interface object list.
            #                         lappend route_args \
            #                             -vrf [enaTbGetInterfaceParam $vIntf -vrf]
            #
            #                         set vMgmtRtng [enaRtngNewRouting static \
            #                                 -interface $vIntf $route_args]
            #                         if { [OK] == [enaVerify "static routing configuration" \
            #                                     {enaRtngConfigureRouting $vMgmtRtng -interfaces $vIntf} \
            #                                     [OK] -format ena_return_code -eval true \
            #                                     -prefix [enaTbFormatInterface $vIntf]] } {
            #                             enaAsyncParentEval [list enaEnableTftpConfigCLI $router]
            #                         }
            #
            #                         # No need in async: enaRtngDeleteRouting $vMgmtRtng
            #
            #                         break ;# No need to loop on all interfaces
            #                     }
            #
            #                     return $ret
            #             }]
            #         }
            #         enaVerify "result of asynchronous processing" [enaAsyncWait $lAsyncIds] [OK] -format ena_return_code -log false
            #     }
            #
            #     _enaTbConfigureTestbed_eval_custom_calls after config mgmt
            # } else {
            #     foreach vIntf $lvMgmtIntfs {
            #         if { [enaTbGetInterfaceParam $vIntf -shutdown] } { continue }
            #         enaEnableTftpConfigCLI [enaTbGetInterfaceParam $vIntf -router]
            #     }
            # }

            from genie.libs.conf.community_set import CommunitySet
            config_features(feature
                            for feature in feature_kwargs
                            if isinstance(feature, CommunitySet))

            from genie.libs.conf.route_policy import RoutePolicy
            config_features(feature
                            for feature in feature_kwargs
                            if isinstance(feature, RoutePolicy))

            from genie.libs.conf.vrf import Vrf
            config_features(feature
                            for feature in feature_kwargs
                            if isinstance(feature, Vrf))
            flush_cfgs()

            from genie.libs.conf.vlan import Vlan
            config_features(feature
                            for feature in feature_kwargs
                            if isinstance(feature, Vlan))
            flush_cfgs()

            # config - ip (lo/bundle/breakout/phy/sub)
            config_features(bo.loopback_interfaces)  # TODO late-shutdown
            flush_cfgs()
            config_features(bo.bundle_interfaces)  # TODO late-shutdown
            flush_cfgs()
            config_features(bo.physical_optics_controllers)  # TODO late-shutdown
            flush_cfgs()
            config_features(bo.breakout_controllers)
            flush_cfgs()
            config_features(bo.physical_controllers)  # TODO late-shutdown
            flush_cfgs()
            config_features(bo.breakout_interfaces)
            flush_cfgs()
            config_features(bo.physical_other_interfaces)  # TODO late-shutdown
            flush_cfgs()
            config_features(bo.vni_interfaces)  # TODO late-shutdown
            flush_cfgs()
            config_features(bo.sub_interfaces)  # TODO late-shutdown
            flush_cfgs()

            inactive_interfaces_to_unconfig = set()
            # TODO
            # foreach vIntf $inactive_interfaces {
            #     if {
            #         [enaTbGetInterfaceParam $vIntf -iftype] ne "physical" &&
            #         [lcontain {ios nxos} [enaTbGetInterfaceParam $vIntf -router -image-type]]
            #     } {
            #         set l_ignored {}
            #         if { [OK] != [enaExecCLI \
            #                     [enaTbGetInterfaceParam $vIntf -router] \
            #                     "show run interface [enaTbGetInterfaceParam $vIntf -interface]" \
            #                     -ignore * -save-ignored l_ignored -array arr_out] } {
            #             set ret [ERROR]
            #             continue
            #         }
            #         if { [llength $l_ignored] || [regexp "Invalid range" $arr_out(rtr_output)] } {
            #             aetest::log -debug "[enaTbFormatInterface $vIntf] does not exist; Skip unconfig."
            #             continue
            #         }
            #     }
            #     lappend inactive_interfaces_to_unconfig $vIntf
            # }
            unconfig_features(inactive_interfaces_to_unconfig, fkwargs={})
            flush_cfgs()

            # TODO Srlg

            from genie.libs.conf.l2vpn import IccpGroup
            config_features(feature
                            for feature in feature_kwargs
                            if isinstance(feature, IccpGroup))
            flush_cfgs()

            # TODO Bfd

            from genie.libs.conf.base import Routing
            from genie.libs.conf.static_routing import StaticRouting
            config_features(feature
                            for feature in feature_kwargs
                            if isinstance(feature, Routing) \
                            and not isinstance(feature, StaticRouting))
            flush_cfgs()

            # TODO AS
            # TODO MPLS STATIC
            # TODO MPLS LMP

            from genie.libs.conf.ldp import Ldp
            from genie.libs.conf.rsvp import Rsvp
            from genie.libs.conf.te import Te
            config_features(feature
                            for feature in feature_kwargs
                            if isinstance(feature, (
                                    Ldp,
                                    Rsvp,
                                    Te,
                            )))
            flush_cfgs()

            # TODO Tunnel Template

            config_features(bo.tunnel_interfaces)
            flush_cfgs()

            from genie.libs.conf.l2vpn import L2vpn
            from genie.libs.conf.l2vpn import PseudowireClass
            #from genie.libs.conf.l2tp import L2tpClass
            config_features(feature
                            for feature in feature_kwargs
                            if isinstance(feature, (
                                    L2vpn,
                                    PseudowireClass,
                                    # TODO L2tpClass,
                            )))
            flush_cfgs()

            from genie.libs.conf.l2vpn import Xconnect
            from genie.libs.conf.l2vpn import BridgeDomain
            config_features(feature
                            for feature in feature_kwargs
                            if isinstance(feature, (
                                    Xconnect,
                                    BridgeDomain,
                            )))
            flush_cfgs()

            # TODO - TCAM carving

            from genie.libs.conf.evpn import Evpn
            config_features(feature
                            for feature in feature_kwargs
                            if isinstance(feature, (
                                    Evpn,
                            )))
            flush_cfgs()

            # TODO MPLS OAM

            from genie.libs.conf.mcast import Mcast
            config_features(feature
                            for feature in feature_kwargs
                            if isinstance(feature, (
                                    Mcast,
                            )))
            flush_cfgs()

            from genie.libs.conf.mcast import Mcast
            config_features(feature
                            for feature in feature_kwargs
                            if isinstance(feature, (
                                    Mcast,
                            )))
            flush_cfgs()

            # TODO MulticastGroupJoin

            from genie.libs.conf.static_routing import StaticRouting
            config_features(feature
                            for feature in feature_kwargs
                            if isinstance(feature, StaticRouting))
            flush_cfgs()

            # Rest
            config_features(feature_kwargs)
            flush_cfgs()

            config_features(sorted(set().union(
                *(device.find_streams()
                  for device in bo.tgen_devices))))
            flush_cfgs()

            tgen_apply_exit_stack.close()

            # tgen - emulation control (start)
            for tgen_device in bo.tgen_devices:
                tgen_device.start_emulation()

            # tgen - traffic control (start)
            for tgen_device in bo.tgen_devices:
                if tgen_device.find_streams():
                    tgen_device.start_traffic()

            # TODO late shutdown

        # check added features and add to configurations per device
        if devices is None:
            devices = self.devices
        for device, device_obj in devices.items():
            if device_obj.features:
                cfgs[device] = CliConfigBuilder()
                for feature in device_obj.features:
                    # check if feature in attributes
                    feature_name = feature.__class__.__name__.lower()
                    if isinstance(attributes, dict):
                        if feature_name in attributes:
                            attr = AttributesHelper2(feature, attributes[feature_name])
                            for _, sub, attributes2 in attr.mapping_items(
                                'device_attr',
                                keys=set([device_obj]), sort=True):
                                cfgs[device].append_block(sub.build_config(apply=False, attributes=attributes2))
                    else:
                        attr = AttributesHelper2(feature, attributes)
                        for _, sub, attributes2 in attr.mapping_items(
                            'device_attr',
                            keys=set([device_obj]), sort=True):
                            cfgs[device].append_block(sub.build_config(apply=False, attributes=attributes2))

        if apply:
            flush_cfgs()  # Should be no-op
        else:
            # Return configuration
            return cfgs

    def build_unconfig(self, devices=None, links=None, interfaces=None,
                       clean=False, attributes=None, apply=True):
        """method to build the configuration of the whole testbed

        Loops through each testbed, link and configure the whole testbed
        A Dictionary will be returned with devices as keys

        Args:
            None

        Return:
            `dict`

        Examples:
            >>> from genie.conf import Genie
            >>> genie_tb = Genie.init(tb=yaml)
            ....
            >>> configuration = genie_tb.build_config()
            >>> genie_tb.apply_config(configuration)


            # Assuming Genie was already initiated at earlier time
            >>> configuration = Genie.testbed.build_config()
            >>> genie_tb.apply_config(configuration)
        """
        cfgs = {}

        bo = self.get_build_objects(devices=devices or self.devices,
                                    links=links or self.links,
                                    interfaces=interfaces or self.interfaces)

        scale_optimize = True

        exit_stack = contextlib.ExitStack()
        tgen_apply_exit_stack = contextlib.ExitStack()
        exit_stack.enter_context(tgen_apply_exit_stack)
        with exit_stack:

            def config_features(features, unconfig=False, fkwargs=None):
                features = set(features)  # Finalize iterable; We need to pop.
                in_fkwargs = fkwargs
                feature_cfgs = {}
                for feature in features:
                    fkwargs = in_fkwargs
                    if fkwargs is None:
                        fkwargs = feature_kwargs.pop(feature, {})
                    if unconfig:
                        cfg = feature.build_unconfig(apply=False, **fkwargs)
                    else:
                        cfg = feature.build_config(apply=False, **fkwargs)
                    _clean_cfgs_dict(cfg, testbed=self, device=feature,
                                     add_to_cfgs=feature_cfgs)
                feature_cfgs = {
                    device: sorted(device_cfgs)
                    for device, device_cfgs in feature_cfgs.items()}
                _clean_cfgs_dict(feature_cfgs, add_to_cfgs=cfgs)

            def unconfig_features(features, **kwargs):
                return config_features(features, unconfig=True, **kwargs)

            def flush_cfgs():
                if apply:
                    self.config_on_devices(cfgs, fail_invalid=True)
                    cfgs.clear()

            feature_kwargs = collections.defaultdict(
                functools.partial(collections.defaultdict, set))
            if not clean:
                for device in bo.active_devices:
                    for feature in device.features:
                        feature_kwargs[feature]['devices'].add(device)
                for link in bo.active_links:
                    for feature in link.features:
                        feature_kwargs[feature]['links'].add(link)
                        feature_kwargs[feature]['interfaces'].update(link.interfaces)
                        feature_kwargs[feature]['devices'].update(link.devices)
                for interface in bo.active_interfaces:
                    for feature in interface.features:
                        feature_kwargs[feature]['interfaces'].add(interface)
                        feature_kwargs[feature]['devices'].add(interface.device)

            # tgen - traffic control (stop)
            for tgen_device in bo.tgen_devices:
                if tgen_device.find_streams():
                    tgen_device.stop_traffic()

            # tgen - emulation control (stop)
            for tgen_device in bo.tgen_devices:
                tgen_device.stop_emulation()

            # tgen - enable optimizations
            if scale_optimize:
                for tgen_device in bo.tgen_devices:
                    tgen_apply_exit_stack.enter_context(
                        tgen_device.defer_apply_context())

            unconfig_features(sorted(set().union(
                *(device.find_streams()
                  for device in bo.tgen_devices))))
            flush_cfgs()

            from genie.libs.conf.static_routing import StaticRouting
            unconfig_features(feature
                              for feature in feature_kwargs
                              if isinstance(feature, StaticRouting))
            flush_cfgs()

            # TODO MulticastGroupJoin

            #from genie.libs.conf.mcast import MulticastGroup
            #unconfig_features(feature
            #                  for feature in feature_kwargs
            #                  if isinstance(feature, (
            #                          MulticastGroup,
            #                  )))
            #flush_cfgs()

            from genie.libs.conf.mcast import Mcast
            unconfig_features(feature
                              for feature in feature_kwargs
                              if isinstance(feature, (
                                      Mcast,
                              )))
            flush_cfgs()

            # TODO MPLS OAM

            from genie.libs.conf.l2vpn import Xconnect
            from genie.libs.conf.l2vpn import BridgeDomain
            unconfig_features(feature
                              for feature in feature_kwargs
                              if isinstance(feature, (
                                      Xconnect,
                                      BridgeDomain,
                              )))
            flush_cfgs()

            from genie.libs.conf.evpn import Evpn
            unconfig_features(feature
                              for feature in feature_kwargs
                              if isinstance(feature, (
                                      Evpn,
                              )))
            flush_cfgs()

            from genie.libs.conf.l2vpn import PseudowireClass
            #from genie.libs.conf.l2tp import L2tpClass
            unconfig_features(feature
                              for feature in feature_kwargs
                              if isinstance(feature, (
                                      PseudowireClass,
                                      # TODO L2tpClass,
                              )))
            flush_cfgs()

            unconfig_features(bo.tunnel_interfaces)
            flush_cfgs()

            # TODO Tunnel Template

            from genie.libs.conf.ldp import Ldp
            from genie.libs.conf.rsvp import Rsvp
            from genie.libs.conf.te import Te
            unconfig_features(feature
                              for feature in feature_kwargs
                              if isinstance(feature, (
                                      Ldp,
                                      Rsvp,
                                      Te,
                              )))
            flush_cfgs()

            # TODO MPLS LMP
            # TODO MPLS STATIC

            from genie.libs.conf.base import Routing
            unconfig_features(feature
                              for feature in feature_kwargs
                              if isinstance(feature, Routing))
            flush_cfgs()

            # TODO AS

            # TODO Bfd

            from genie.libs.conf.l2vpn import IccpGroup
            from genie.libs.conf.l2vpn import L2vpn
            unconfig_features(feature
                              for feature in feature_kwargs
                              if isinstance(feature, (
                                      IccpGroup,
                              )))
            # Unconfigure top-level L2vpn last in group
            unconfig_features(feature
                              for feature in feature_kwargs
                              if isinstance(feature, (
                                      L2vpn,
                              )))
            flush_cfgs()

            # TODO Srlg

            unconfig_features(bo.sub_interfaces)
            flush_cfgs()
            unconfig_features(bo.vni_interfaces)
            flush_cfgs()

            # unconfig_features(bo.physical_other_interfaces)
            # CSCup63786 - need to remove bundle ids from interfaces before shutting down
            CSCup63786_interfaces = {
                interface
                for interface in bo.physical_other_interfaces_no_mgmt
                if getattr(interface, 'bundle', None) is not None}
            unconfig_features(CSCup63786_interfaces,
                              fkwargs=dict(
                                  attributes='bundle',
                              ))
            flush_cfgs()
            unconfig_features(bo.physical_other_interfaces_no_mgmt)
            flush_cfgs()

            # XXXJST For now, breakout unconfiguration is a no-op
            # unconfig_features(bo.breakout_interfaces)
            # flush_cfgs()
            unconfig_features(bo.physical_controllers)
            flush_cfgs()
            unconfig_features(bo.breakout_controllers)
            flush_cfgs()
            unconfig_features(bo.physical_optics_controllers)
            flush_cfgs()
            unconfig_features(bo.bundle_interfaces)
            flush_cfgs()
            unconfig_features(bo.loopback_interfaces)
            flush_cfgs()

            from genie.libs.conf.vlan import Vlan
            unconfig_features(feature
                              for feature in feature_kwargs
                              if isinstance(feature, Vlan))
            flush_cfgs()

            # TODO also exclude unconfiguring management VRFs?!?
            from genie.libs.conf.vrf import Vrf
            unconfig_features(feature
                              for feature in feature_kwargs
                              if isinstance(feature, Vrf))
            flush_cfgs()

            from genie.libs.conf.route_policy import RoutePolicy
            unconfig_features(feature
                              for feature in feature_kwargs
                              if isinstance(feature, RoutePolicy))

            from genie.libs.conf.community_set import CommunitySet
            unconfig_features(feature
                              for feature in feature_kwargs
                              if isinstance(feature, CommunitySet))

            # Rest
            unconfig_features(feature_kwargs)
            flush_cfgs()

            if clean:
                for device in bo.active_devices:
                    feature_kwargs[device]['clean'] = True

            unconfig_features(bo.active_devices & bo.emulated_devices)
            unconfig_features(bo.physical_tgen_interfaces)
            flush_cfgs()

            unconfig_features(bo.active_devices - bo.emulated_devices)
            flush_cfgs()

            tgen_apply_exit_stack.close()

        # check added features and add to configurations per device
        if devices is None:
            devices = self.devices
        for device, device_obj in devices.items():
            if device_obj.features:
                cfgs[device] = CliConfigBuilder()
                for feature in device_obj.features:
                    # check if feature in attributes
                    feature_name = feature.__class__.__name__.lower()
                    if isinstance(attributes, dict):
                        if feature_name in attributes:
                            attr = AttributesHelper2(feature, attributes[feature_name])
                            for _, sub, attributes2 in attr.mapping_items(
                                'device_attr',
                                keys=set([device_obj]), sort=True):
                                cfgs[device].append_block(sub.build_unconfig(apply=False, attributes=attributes2))
                    else:
                        attr = AttributesHelper2(feature, attributes)
                        for _, sub, attributes2 in attr.mapping_items(
                            'device_attr',
                            keys=set([device_obj]), sort=True):
                            cfgs[device].append_block(sub.build_unconfig(apply=False, attributes=attributes2))

        if apply:
            flush_cfgs()  # Should be no-op
        else:
            # Return configuration
            return cfgs

    def config_on_device(self, device, configs, **kwargs):
        if isinstance(device, str):
            device = self.devices[device]

        cfgs = _clean_cfgs_dict(configs, testbed=self, device=device)
        if not cfgs:
            # Empty, do nothing.
            return
        if len(cfgs) != 1:
            # Multiple devices, use config_on_devices!
            raise ValueError(configs)
        configs, = cfgs.values()

        for cfg in configs:
            assert cfg.device is device
            cfg.apply(**kwargs)

    def config_on_devices(self, cfgs, **kwargs):

        cfgs = _clean_cfgs_dict(cfgs, testbed=self)

        fg_device_names = set(cfgs.keys())
        bg_device_names = set()

        if False:  # Change to False to disable pcall altogether
            if len(fg_device_names) < 2:
                # Run in foreground only
                pass
            else:
                # Move devices with compatible configurations to background
                for device_name in list(fg_device_names):
                    # YangConfig is incompatible with pcall, keep in foreground
                    if any(
                            isinstance(cfg, YangConfig)
                            for cfg in cfgs[device_name]):
                        continue
                    # Move to background
                    fg_device_names.remove(device_name)
                    bg_device_names.add(device_name)

        p = None
        try:
            if bg_device_names:
                # Apply background configurations in parallel
                p = Pcall(self.config_on_device,
                          device=[self.devices[device_name]
                                  for device_name in sorted(bg_device_names)],
                          configs=[cfgs[device_name]
                                   for device_name in sorted(bg_device_names)],
                          ckwargs=kwargs,
                          )
                p.start()

            # Apply foreground configurations serially
            for device_name in sorted(fg_device_names):
                self.config_on_device(
                    device=self.devices[device_name],
                    configs=cfgs[device_name],
                    **kwargs)

        finally:
            if p:
                p.join()

