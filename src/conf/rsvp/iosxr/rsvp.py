
from abc import ABC
import warnings

from genie.conf.base.attributes import UnsupportedAttributeWarning,\
    AttributesHelper
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.config import CliConfig

from ..rsvp import Rsvp as _Rsvp


def format_bw_unit_percent(bw, unit, percent):
    if bw is None:
        return ''
    s = ' '
    if percent:
        s += '{}'.format(bw)
    elif unit is None:
        s += '{}'.format(bw)
    elif unit is _Rsvp.BwUnit.kbps:
        s += '{} kbps'.format(bw)
    elif unit is _Rsvp.BwUnit.mbps:
        s += '{} mbps'.format(bw // 1000)
    elif unit is _Rsvp.BwUnit.mbps:
        s += '{} gbps'.format(bw // 1000000)
    else:
        raise ValueError(unit)
    return s


class Rsvp(ABC):

    class DeviceAttributes(ABC):

        def build_config(self, links=None, apply=True, attributes=None, unconfig=False, **kwargs):
            '''Device build config'''
            assert not apply
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            # iosxr: rsvp (config-rsvp)
            with configurations.submode_context('rsvp'):
                if unconfig and attributes.iswildcard:
                    configurations.submode_unconfig()

                # iosxr: rsvp / authentication (config-rsvp-auth)
                with configurations.submode_context('authentication', cancel_empty=True):

                    # iosxr: rsvp / authentication / key-source key-chain someword
                    configurations.append_line(attributes.format('key-source key-chain {auth_keysrc_keychain}'))

                    # iosxr: rsvp / authentication / life-time 30
                    configurations.append_line(attributes.format('life-time {auth_lifetime}'))

                    # iosxr: rsvp / authentication / window-size 1
                    configurations.append_line(attributes.format('window-size {auth_window_size}'))

                    # iosxr: rsvp / authentication / retransmit <0-10000>
                    configurations.append_line(attributes.format('retransmit {auth_retransmit}'))

                # iosxr: rsvp / bandwidth rdm percentage max-reservable-bc0 <0-10000>
                # iosxr: rsvp / bandwidth rdm percentage max-reservable-bc0 <0-10000> bc1 <0-10000>
                if self.rdm_bw_percentage:
                    cfg = attributes.format('bandwidth rdm percentage max-reservable-bc0 {rdm_bw_total}')
                    if cfg:
                        cfg += attributes.format(' bc1 {rdm_bw_subpool}', force=True)
                        configurations.append_line(cfg)

                # iosxr: rsvp / bandwidth mam percentage max-reservable <0-10000>
                # iosxr: rsvp / bandwidth mam percentage max-reservable <0-10000> bc0 <0-10000>
                # iosxr: rsvp / bandwidth mam percentage max-reservable <0-10000> bc0 <0-10000> bc1 <0-10000>
                if self.mam_bw_percentage:
                    cfg = attributes.format('bandwidth mam percentage max-reservable {mam_bw_total}')
                    if cfg:
                        if self.mam_bw_bc0 is not None:
                            cfg += attributes.format(' bc0 {mam_bw_bc0}', force=True)
                            cfg += attributes.format(' bc1 {mam_bw_bc1}', force=True)
                        configurations.append_line(cfg)

                # iosxr: rsvp / logging events issu
                if attributes.value('log_events_issu'):
                    configurations.append_line('logging events issu')

                # iosxr: rsvp / logging events nsr
                if attributes.value('log_events_nsr'):
                    configurations.append_line('logging events nsr')

                # iosxr: rsvp / latency threshold <0-180>
                # iosxr: rsvp / ltrace-buffer multiplier 2 all
                # iosxr: rsvp / ltrace-buffer multiplier 2 common
                # iosxr: rsvp / ltrace-buffer multiplier 2 common dbg-err
                # iosxr: rsvp / ltrace-buffer multiplier 2 common dbg-err intf
                # iosxr: rsvp / ltrace-buffer multiplier 2 common dbg-err intf rare
                # iosxr: rsvp / ltrace-buffer multiplier 2 common dbg-err intf rare sig
                # iosxr: rsvp / ltrace-buffer multiplier 2 common dbg-err intf rare sig sig-err
                # iosxr: rsvp / ltrace-buffer multiplier 2 common dbg-err intf rare sig sig-err sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 common dbg-err intf rare sig sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 common dbg-err intf rare sig-err
                # iosxr: rsvp / ltrace-buffer multiplier 2 common dbg-err intf rare sig-err sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 common dbg-err intf rare sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 common dbg-err intf sig
                # iosxr: rsvp / ltrace-buffer multiplier 2 common dbg-err intf sig sig-err
                # iosxr: rsvp / ltrace-buffer multiplier 2 common dbg-err intf sig sig-err sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 common dbg-err intf sig sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 common dbg-err intf sig-err
                # iosxr: rsvp / ltrace-buffer multiplier 2 common dbg-err intf sig-err sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 common dbg-err intf sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 common dbg-err rare
                # iosxr: rsvp / ltrace-buffer multiplier 2 common dbg-err rare sig
                # iosxr: rsvp / ltrace-buffer multiplier 2 common dbg-err rare sig sig-err
                # iosxr: rsvp / ltrace-buffer multiplier 2 common dbg-err rare sig sig-err sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 common dbg-err rare sig sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 common dbg-err rare sig-err
                # iosxr: rsvp / ltrace-buffer multiplier 2 common dbg-err rare sig-err sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 common dbg-err rare sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 common dbg-err sig
                # iosxr: rsvp / ltrace-buffer multiplier 2 common dbg-err sig sig-err
                # iosxr: rsvp / ltrace-buffer multiplier 2 common dbg-err sig sig-err sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 common dbg-err sig sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 common dbg-err sig-err
                # iosxr: rsvp / ltrace-buffer multiplier 2 common dbg-err sig-err sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 common dbg-err sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 common intf
                # iosxr: rsvp / ltrace-buffer multiplier 2 common intf rare
                # iosxr: rsvp / ltrace-buffer multiplier 2 common intf rare sig
                # iosxr: rsvp / ltrace-buffer multiplier 2 common intf rare sig sig-err
                # iosxr: rsvp / ltrace-buffer multiplier 2 common intf rare sig sig-err sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 common intf rare sig sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 common intf rare sig-err
                # iosxr: rsvp / ltrace-buffer multiplier 2 common intf rare sig-err sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 common intf rare sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 common intf sig
                # iosxr: rsvp / ltrace-buffer multiplier 2 common intf sig sig-err
                # iosxr: rsvp / ltrace-buffer multiplier 2 common intf sig sig-err sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 common intf sig sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 common intf sig-err
                # iosxr: rsvp / ltrace-buffer multiplier 2 common intf sig-err sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 common intf sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 common rare
                # iosxr: rsvp / ltrace-buffer multiplier 2 common rare sig
                # iosxr: rsvp / ltrace-buffer multiplier 2 common rare sig sig-err
                # iosxr: rsvp / ltrace-buffer multiplier 2 common rare sig sig-err sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 common rare sig sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 common rare sig-err
                # iosxr: rsvp / ltrace-buffer multiplier 2 common rare sig-err sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 common rare sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 common sig
                # iosxr: rsvp / ltrace-buffer multiplier 2 common sig sig-err
                # iosxr: rsvp / ltrace-buffer multiplier 2 common sig sig-err sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 common sig sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 common sig-err
                # iosxr: rsvp / ltrace-buffer multiplier 2 common sig-err sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 common sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 dbg-err
                # iosxr: rsvp / ltrace-buffer multiplier 2 dbg-err intf
                # iosxr: rsvp / ltrace-buffer multiplier 2 dbg-err intf rare
                # iosxr: rsvp / ltrace-buffer multiplier 2 dbg-err intf rare sig
                # iosxr: rsvp / ltrace-buffer multiplier 2 dbg-err intf rare sig sig-err
                # iosxr: rsvp / ltrace-buffer multiplier 2 dbg-err intf rare sig sig-err sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 dbg-err intf rare sig sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 dbg-err intf rare sig-err
                # iosxr: rsvp / ltrace-buffer multiplier 2 dbg-err intf rare sig-err sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 dbg-err intf rare sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 dbg-err intf sig
                # iosxr: rsvp / ltrace-buffer multiplier 2 dbg-err intf sig sig-err
                # iosxr: rsvp / ltrace-buffer multiplier 2 dbg-err intf sig sig-err sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 dbg-err intf sig sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 dbg-err intf sig-err
                # iosxr: rsvp / ltrace-buffer multiplier 2 dbg-err intf sig-err sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 dbg-err intf sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 dbg-err rare
                # iosxr: rsvp / ltrace-buffer multiplier 2 dbg-err rare sig
                # iosxr: rsvp / ltrace-buffer multiplier 2 dbg-err rare sig sig-err
                # iosxr: rsvp / ltrace-buffer multiplier 2 dbg-err rare sig sig-err sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 dbg-err rare sig sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 dbg-err rare sig-err
                # iosxr: rsvp / ltrace-buffer multiplier 2 dbg-err rare sig-err sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 dbg-err rare sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 dbg-err sig
                # iosxr: rsvp / ltrace-buffer multiplier 2 dbg-err sig sig-err
                # iosxr: rsvp / ltrace-buffer multiplier 2 dbg-err sig sig-err sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 dbg-err sig sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 dbg-err sig-err
                # iosxr: rsvp / ltrace-buffer multiplier 2 dbg-err sig-err sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 dbg-err sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 intf
                # iosxr: rsvp / ltrace-buffer multiplier 2 intf rare
                # iosxr: rsvp / ltrace-buffer multiplier 2 intf rare sig
                # iosxr: rsvp / ltrace-buffer multiplier 2 intf rare sig sig-err
                # iosxr: rsvp / ltrace-buffer multiplier 2 intf rare sig sig-err sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 intf rare sig sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 intf rare sig-err
                # iosxr: rsvp / ltrace-buffer multiplier 2 intf rare sig-err sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 intf rare sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 intf sig
                # iosxr: rsvp / ltrace-buffer multiplier 2 intf sig sig-err
                # iosxr: rsvp / ltrace-buffer multiplier 2 intf sig sig-err sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 intf sig sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 intf sig-err
                # iosxr: rsvp / ltrace-buffer multiplier 2 intf sig-err sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 intf sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 rare
                # iosxr: rsvp / ltrace-buffer multiplier 2 rare sig
                # iosxr: rsvp / ltrace-buffer multiplier 2 rare sig sig-err
                # iosxr: rsvp / ltrace-buffer multiplier 2 rare sig sig-err sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 rare sig sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 rare sig-err
                # iosxr: rsvp / ltrace-buffer multiplier 2 rare sig-err sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 rare sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 sig
                # iosxr: rsvp / ltrace-buffer multiplier 2 sig sig-err
                # iosxr: rsvp / ltrace-buffer multiplier 2 sig sig-err sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 sig sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 sig-err
                # iosxr: rsvp / ltrace-buffer multiplier 2 sig-err sync
                # iosxr: rsvp / ltrace-buffer multiplier 2 sync

                # iosxr: rsvp / signalling checksum disable
                if attributes.value('sig_checksum') is False:
                    configurations.append_line('signalling checksum disable')

                # iosxr: rsvp / signalling event-per-pulse <0-1600>
                configurations.append_line(attributes.format('signalling event-per-pulse {sig_event_per_pulse}'))

                # iosxr: rsvp / signalling graceful-restart
                # iosxr: rsvp / signalling graceful-restart disable
                v = attributes.value('sig_gr')
                if v is not None:
                    if v:
                        configurations.append_line('signalling graceful-restart')
                    else:
                        configurations.append_line('signalling graceful-restart disable')

                # iosxr: rsvp / signalling graceful-restart recovery-time <0-3600>
                configurations.append_line(attributes.format('signalling graceful-restart recovery-time {sig_gr_recov_time}'))

                # iosxr: rsvp / signalling graceful-restart restart-time 60
                configurations.append_line(attributes.format('signalling graceful-restart restart-time {sig_gr_restart_time}'))

                # iosxr: rsvp / signalling hello graceful-restart refresh interval 3000
                configurations.append_line(attributes.format('signalling hello graceful-restart refresh interval {sig_hello_gr_refresh_interval}'))

                # iosxr: rsvp / signalling hello graceful-restart refresh misses 1
                configurations.append_line(attributes.format('signalling hello graceful-restart refresh misses {sig_hello_gr_refresh_misses}'))

                # iosxr: rsvp / signalling message-bundle disable
                if attributes.value('sig_message_bundle') is False:
                    configurations.append_line('signalling message-bundle disable')

                # iosxr: rsvp / signalling out-of-band vrf someword
                configurations.append_line(attributes.format('signalling out-of-band vrf {sig_outofband_vrf.name}'))

                # iosxr: rsvp / signalling patherr state-removal disable
                if attributes.value('sig_patherr_state_removal') is False:
                    configurations.append_line('signalling patherr state-removal disable')

                # iosxr: rsvp / signalling prefix-filtering access-list someword
                configurations.append_line(attributes.format('signalling prefix-filtering access-list {sig_prefixfilt_acl.name}'))

                # iosxr: rsvp / signalling prefix-filtering default-deny-action drop
                configurations.append_line(attributes.format('signalling prefix-filtering default-deny-action {sig_prefixfilt_defdenyaction.value}'))

                # Add per-interface config
                for sub, attributes2 in attributes.mapping_values('interface_attr', keys=self.interfaces, sort=True):
                    configurations.append_block(sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig, **kwargs))

                # Add per-neighbor config
                for sub, attributes2 in attributes.mapping_values('neighbor_attr', keys=self.neighbors, sort=True):
                    configurations.append_block(sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig, **kwargs))

                # Add per-controller config
                for sub, attributes2 in attributes.mapping_values('controller_attr', keys=self.controllers, sort=True):
                    configurations.append_block(sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig, **kwargs))

            return CliConfig(device=self.device, unconfig=unconfig,
                             cli_config=configurations)

        def build_unconfig(self, links=None, apply=True, attributes=None, **kwargs):
            return self.build_config(links=links, apply=apply, attributes=attributes, unconfig=True, **kwargs)

        class InterfaceAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                '''Interface build config'''
                assert not apply
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                # iosxr: rsvp / interface <name> (config-rsvp-if)
                with configurations.submode_context(attributes.format('interface {interface_name}', force=True)):

                    # iosxr: rsvp / interface <name> / authentication (config-rsvp-if-auth)
                    with configurations.submode_context('authentication', cancel_empty=True):

                        # iosxr: rsvp / interface <name> / authentication / key-source key-chain someword
                        configurations.append_line(attributes.format('key-source key-chain {auth_keysrc_keychain}', inherited=False))

                        # iosxr: rsvp / interface <name> / authentication / life-time 30
                        configurations.append_line(attributes.format('life-time {auth_lifetime}', inherited=False))

                        # iosxr: rsvp / interface <name> / authentication / window-size 1
                        configurations.append_line(attributes.format('window-size {auth_window_size}', inherited=False))

                    # iosxr: rsvp / interface <name> / signalling refresh out-of-band interval 180
                    configurations.append_line(attributes.format('signalling refresh out-of-band interval {sig_refresh_outofband_interval}'))

                    # iosxr: rsvp / interface <name> / signalling refresh out-of-band missed 1
                    configurations.append_line(attributes.format('signalling refresh out-of-band missed {sig_refresh_outofband_missed}'))

                    # iosxr: rsvp / interface <name> / signalling dscp <0-63>
                    configurations.append_line(attributes.format('signalling dscp {sig_dscp}'))

                    # iosxr: rsvp / interface <name> / signalling hello graceful-restart interface-based
                    if attributes.value('sig_hello_gr_intfbased'):
                        configurations.append_line('signalling hello graceful-restart interface-based')

                    # iosxr: rsvp / interface <name> / signalling rate-limit
                    # iosxr: rsvp / interface <name> / signalling rate-limit rate 1
                    # iosxr: rsvp / interface <name> / signalling rate-limit rate 1 interval 250
                    v = attributes.value('sig_rate_limit')
                    if v is not None:
                        if v is False:
                            pass
                        else:
                            cfg = 'signalling rate-limit'
                            if v is True:
                                pass
                            else:
                                cfg += ' rate {}'.format(v)
                                cfg += attributes.format(' interval {sig_rate_limit_interval}', force=True)
                            configurations.append_line(cfg)

                    # iosxr: rsvp / interface <name> / signalling refresh interval 10
                    configurations.append_line(attributes.format('signalling refresh interval {sig_refresh_interval}'))

                    # iosxr: rsvp / interface <name> / signalling refresh missed 1
                    configurations.append_line(attributes.format('signalling refresh interval {sig_refresh_missed}'))

                    # iosxr: rsvp / interface <name> / signalling refresh reduction disable
                    if attributes.value('sig_refresh_reduction') is False:
                        configurations.append_line('signalling refresh reduction disable')

                    # iosxr: rsvp / interface <name> / signalling refresh reduction bundle-max-size 512
                    configurations.append_line(attributes.format('signalling refresh reduction bundle-max-size {sig_refresh_reduction_bundle_maxsize}'))

                    # iosxr: rsvp / interface <name> / signalling refresh reduction reliable ack-hold-time 100
                    configurations.append_line(attributes.format('signalling refresh reduction reliable ack-hold-time {sig_refresh_reduction_reliable_ack_holdtime}'))

                    # iosxr: rsvp / interface <name> / signalling refresh reduction reliable ack-max-size 20
                    configurations.append_line(attributes.format('signalling refresh reduction reliable ack-max-size {sig_refresh_reduction_reliable_ack_maxsize}'))

                    # iosxr: rsvp / interface <name> / signalling refresh reduction reliable retransmit-time 100
                    configurations.append_line(attributes.format('signalling refresh reduction reliable retransmit-time {sig_refresh_reduction_reliable_retransmit_time}'))

                    # iosxr: rsvp / interface <name> / signalling refresh reduction reliable summary-refresh
                    if attributes.value('sig_refresh_reduction_reliable_summary_refresh'):
                        configurations.append_line('signalling refresh reduction reliable summary-refresh')

                    # iosxr: rsvp / interface <name> / signalling refresh reduction summary max-size 20
                    configurations.append_line(attributes.format('signalling refresh reduction reliable summary max-size {sig_refresh_reduction_summary_maxsize}'))

                    if not self.rdm_bw_percentage \
                            or not self.isinherited('rdm_bw_percentage') \
                            or not self.isinherited('rdm_bw_total'):
                        if attributes.value('rdm_bw_total') is not None:
                            keywords = ()
                            keywords += ('rdm' if self.rdm_bw_cli_rdm_kw else '',)
                            if self.rdm_bw_cli_style is _Rsvp.RdmBwCliStyle.unnamed_subpool:
                                # iosxr: rsvp / interface <name> / bandwidth [rdm] <0-4294967295> [Kbps|Mbps|Gbps] [<0-4294967295> [Kbps|Mbps|Gbps]] [sub-pool <0-4294967295> [Kbps|Mbps|Gbps]]
                                # iosxr: rsvp / interface <name> / bandwidth [rdm] percentage <0-10000> [<0-10000>] [sub-pool <0-10000>]
                                keywords += ('', 'sub-pool')
                            elif self.rdm_bw_cli_style is _Rsvp.RdmBwCliStyle.bc0_bc1:
                                # iosxr: rsvp / interface <name> / bandwidth [rdm] bc0 <0-4294967295> [<0-4294967295> [Kbps|Mbps|Gbps]] [bc1 <0-4294967295> [Kbps|Mbps|Gbps]]
                                # iosxr: rsvp / interface <name> / bandwidth [rdm] percentage bc0 <0-10000> [<0-10000>] [bc1 <0-10000>]
                                keywords += ('bc0', 'bc1')
                            elif self.rdm_bw_cli_style is _Rsvp.RdmBwCliStyle.global_subpool:
                                # iosxr: rsvp / interface <name> / bandwidth [rdm] global-pool <0-4294967295> [Kbps|Mbps|Gbps] [<0-4294967295> [Kbps|Mbps|Gbps]] [sub-pool <0-4294967295> [Kbps|Mbps|Gbps]]
                                # iosxr: rsvp / interface <name> / bandwidth [rdm] percentage global-pool <0-10000> [<0-10000>] [sub-pool <0-10000>]
                                keywords += ('global-pool', 'sub-pool')
                            else:
                                raise ValueError(self.rdm_bw_cli_style)
                            cfg = 'bandwidth'
                            if self.rdm_bw_percentage:
                                cfg += ' percentage'
                            if keywords[0]:
                                cfg += ' ' + keywords[0]  # rdm
                            if keywords[1]:
                                cfg += ' ' + keywords[1]  # |bc0|global-pool
                            cfg += format_bw_unit_percent(self.rdm_bw_total, self.rdm_bw_total_unit, self.rdm_bw_percentage)
                            cfg += format_bw_unit_percent(self.rdm_bw_largest, self.rdm_bw_largest_unit, self.rdm_bw_percentage)
                            if self.rdm_bw_subpool is not None:
                                if keywords[2]:
                                    cfg += ' ' + keywords[2]  # sub-pool|bc1|sub-pool
                                cfg += format_bw_unit_percent(self.rdm_bw_subpool, self.rdm_bw_subpool_unit, self.rdm_bw_percentage)
                            configurations.append_line(cfg)

                    elif attributes.value('enable_default_bw'):
                        # Effectively overrides rdm config above
                        # iosxr: rsvp / interface <name> / bandwidth
                        configurations.append_line('bandwidth')

                    if not self.mam_bw_percentage \
                            or not self.isinherited('mam_bw_percentage') \
                            or not self.isinherited('mam_bw_total'):
                        if attributes.value('mam_bw_max_reservable') is not None \
                                or attributes.value('mam_bw_total') is not None:
                            # iosxr: rsvp / interface <name> / bandwidth mam [max-reservable-bw] [<0-4294967295> [<0-4294967295> [Kbps|Mbps|Gbps]] [bc0 <0-4294967295> [Kbps|Mbps|Gbps] [bc1 <0-4294967295> [Kbps|Mbps|Gbps]]]]
                            # iosxr: rsvp / interface <name> / bandwidth mam percentage [max-reservable-bw] [<0-10000> [<0-10000>] [bc0 <0-10000> [bc1 <0-10000>]]]
                            cfg = 'bandwidth mam'
                            if self.mam_bw_percentage:
                                cfg += ' percentage'
                            if self.mam_bw_max_reservable:
                                cfg += ' max-reservable-bw'
                            if self.mam_bw_total is not None:
                                cfg += format_bw_unit_percent(self.mam_bw_total, self.mam_bw_total_unit, self.mam_bw_percentage)
                                cfg += format_bw_unit_percent(self.mam_bw_largest, self.mam_bw_largest_unit, self.mam_bw_percentage)
                                if self.mam_bw_bc0 is not None:
                                    cfg += ' bc0'
                                    cfg += format_bw_unit_percent(self.mam_bw_bc0, self.mam_bw_bc0_unit, self.mam_bw_percentage)
                                    if self.mam_bw_bc1 is not None:
                                        cfg += ' bc1'
                                        cfg += format_bw_unit_percent(self.mam_bw_bc1, self.mam_bw_bc1_unit, self.mam_bw_percentage)
                            configurations.append_line(cfg)

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

        class NeighborAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                '''Neighbor build config'''
                assert not apply
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                # iosxr: rsvp / neighbor 1.2.3.4 (config-rsvp-nbr)
                with configurations.submode_context(attributes.format('neighbor {neighbor.ip}', force=True)):

                    # iosxr: rsvp / neighbor 1.2.3.4 / authentication (config-rsvp-nbor-auth)
                    with configurations.submode_context('authentication', cancel_empty=True):

                        # iosxr: rsvp / neighbor 1.2.3.4 / authentication / key-source key-chain someword
                        configurations.append_line(attributes.format('key-source key-chain {auth_keysrc_keychain}', inherited=False))

                        # iosxr: rsvp / neighbor 1.2.3.4 / authentication / life-time 30
                        configurations.append_line(attributes.format('life-time {auth_lifetime}', inherited=False))

                        # iosxr: rsvp / neighbor 1.2.3.4 / authentication / window-size 1
                        configurations.append_line(attributes.format('window-size {auth_window_size}', inherited=False))

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

        class ControllerAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                '''Controller build config'''
                assert not apply
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                # iosxr: rsvp / controller <name> (config-rsvp-cntl)
                with configurations.submode_context(attributes.format('controller {interface_name}', force=True)):

                    # iosxr: rsvp / controller <name> / signalling refresh out-of-band interval 180
                    configurations.append_line(attributes.format('signalling refresh out-of-band interval {sig_refresh_outofband_interval}'))

                    # iosxr: rsvp / controller <name> / signalling refresh out-of-band missed 1
                    configurations.append_line(attributes.format('signalling refresh out-of-band missed {sig_refresh_outofband_missed}'))

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

