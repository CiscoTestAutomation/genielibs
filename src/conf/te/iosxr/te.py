
from abc import ABC
import warnings

from genie.conf.base.attributes import AttributesHelper
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.config import CliConfig

import re

class Te(ABC):

    class DeviceAttributes(ABC):

        def build_config(self, links=None, apply=True, attributes=None, unconfig=False, **kwargs):
            '''Device build config'''
            assert not apply
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            if attributes.value('ipv4_unnum_interfaces'):
                for interface in attributes.value('ipv4_unnum_interfaces'):
                    if interface.device == self.device:
                        configurations.append_line('ipv4 unnumbered mpls traffic-eng {}'.format(interface.name))
            
            with configurations.submode_context(attributes.format('mpls traffic-eng', force=True)):
                if unconfig and attributes.iswildcard:
                    configurations.submode_unconfig()

                # configure / mpls traffic-eng / auto-tunnel backup / affinity ignore
                if attributes.value('auto_tun_backup_affinity_ignore'):
                    configurations.append_line('auto-tunnel backup affinity ignore')
                    
                # configure / mpls traffic-eng / auto-tunnel backup / timers removal unused <0-10080>
                configurations.append_line(attributes.format('auto-tunnel backup timers removal unused {auto_tun_backup_timers_rem_unused}'))

                # configure / mpls traffic-eng / auto-tunnel backup / tunnel-id min <0-65535> max 65535
                configurations.append_line(attributes.format(
                    'auto-tunnel backup tunnel-id min {backup_auto_tun_tunid_min} max {backup_auto_tun_tunid_max}'))
                    
                # configure / mpls traffic-eng / auto-tunnel mesh / tunnel-id min <0-65535> max 65535
                configurations.append_line(attributes.format(
                    'auto-tunnel mesh tunnel-id min {mesh_auto_tun_tunid_min} max {mesh_auto_tun_tunid_max}'))
                # configure / mpls traffic-eng / auto-tunnel p2mp / tunnel-id min <0-65535> max 65535
                configurations.append_line(attributes.format(
                    'auto-tunnel p2mp tunnel-id min {p2mp_auto_tun_tunid_min} max {p2mp_auto_tun_tunid_max}'))
                # configure / mpls traffic-eng / auto-tunnel p2p / tunnel-id min <0-65535> max 65535
                configurations.append_line(attributes.format(
                    'auto-tunnel p2p tunnel-id min {p2p_auto_tun_tunid_min} max {p2p_auto_tun_tunid_max}'))
                # configure / mpls traffic-eng / auto-tunnel pcc / tunnel-id min <0-65535> max 65535
                configurations.append_line(attributes.format(
                    'auto-tunnel pcc tunnel-id min {pcc_auto_tun_tunid_min} max {pcc_auto_tun_tunid_max}'))


                # configure / mpls traffic-eng / logging events all
                if attributes.value('log_events_all'):
                    configurations.append_line('logging events all')
                    
                # configure / mpls traffic-eng / logging events issu
                if attributes.value('log_events_issu'):
                    configurations.append_line('logging events issu')
                    
                # configure / mpls traffic-eng / logging events nsr
                if attributes.value('log_events_nsr'):
                    configurations.append_line('logging events nsr')
                    
                # configure / mpls traffic-eng / logging events preemption
                if attributes.value('log_events_preemption'):
                    configurations.append_line('logging events preemption')
                    
                # configure / mpls traffic-eng / logging events role head
                if attributes.value('log_events_role_head'):
                    configurations.append_line('logging events role head')
                    
                # configure / mpls traffic-eng / logging events role mid
                if attributes.value('log_events_role_mid'):
                    configurations.append_line('logging events role mid')
                    
                # configure / mpls traffic-eng / logging events role tail
                if attributes.value('log_events_role_tail'):
                    configurations.append_line('logging events role tail')
                
                # configure / mpls traffic-eng / logging events frr-protection
                # configure / mpls traffic-eng / logging events frr-protection backup-tunnel
                # configure / mpls traffic-eng / logging events frr-protection primary-lsp
                # configure / mpls traffic-eng / logging events frr-protection primary-lsp active-state
                # configure / mpls traffic-eng / logging events frr-protection primary-lsp ready-state
                #   only one of these three can be set at one time, so one attribute used
                if attributes.value('log_events_frr_protection'):
                    v = attributes.value('log_events_frr_protection_type')
                    if v == 'backup-tunnel':
                        configurations.append_line(attributes.format('logging events frr-protection backup-tunnel'))
                    elif v == 'primary-lsp':
                        v = attributes.value('log_events_frr_protection_primary_lsp_type')
                        if re.search('active-state|ready-state', str(v)):
                            configurations.append_line(attributes.format('logging events frr-protection primary-lsp {log_events_frr_protection_primary_lsp_type}'))
                        else:
                            configurations.append_line(attributes.format('logging events frr-protection primary-lsp'))
                    else:
                        # log_events_frr_protection is "True"
                        configurations.append_line(attributes.format('logging events frr-protection'))

                # configure / mpls traffic-eng / reoptimize <0-604800>
                configurations.append_line(attributes.format('reoptimize {reoptimize_secs}'))

                # configure / mpls traffic-eng / reoptimize timers delay cleanup <0-300>
                configurations.append_line(attributes.format('reoptimize timers delay cleanup {reoptimize_delay_cleanup}'))

                # configure / mpls traffic-eng / reoptimize timers delay installation <0-3600>
                configurations.append_line(attributes.format('reoptimize timers delay installation {reoptimize_delay_install}'))

                # configure / mpls traffic-eng / fast-reroute timers hold-backup <0-604800>
                configurations.append_line(attributes.format('fast-reroute timers hold-backup {frr_timers_hold_backup}'))

                # configure / mpls traffic-eng / fast-reroute timers promotion <0-604800>
                configurations.append_line(attributes.format('fast-reroute timers promotion {frr_timers_promotion}'))

                # configure / mpls traffic-eng / flooding threshold up <0-100> down <0-100>
                configurations.append_line(attributes.format(
                    'flooding threshold up {flooding_threshold_up} down {flooding_threshold_down}'))

                # configure / mpls traffic-eng / affinity-map someword bit-position <0-255>
                dic = attributes.value('affinity_map_bitpos_dict')
                for key in sorted(dic.keys()):
                    configurations.append_line('affinity-map {key} bit-position {val}'.format(key=key, val=dic[key]))                  
                
                # configure / mpls traffic-eng / affinity-map someword 0x1
                dic = attributes.value('affinity_map_val_dict')
                for key in sorted(dic.keys()):
                    configurations.append_line('affinity-map {key} {val}'.format(key=key, val=dic[key]))                  

                # configure / mpls traffic-eng / srlg (config-mpls-te-srlg)
                # configure / mpls traffic-eng / srlg / admin-weight <0-4294967295>
                # configure / mpls traffic-eng / srlg / name someword (config-mpls-te-srlg-name)
                # configure / mpls traffic-eng / srlg / name someword / admin-weight <0-4294967295>
                # configure / mpls traffic-eng / srlg / name someword / static ipv4 address 1.2.3.4 next-hop ipv4 address 1.2.3.4
                # configure / mpls traffic-eng / srlg / value <0-4294967295> (config-mpls-te-srlg-value)
                # configure / mpls traffic-eng / srlg / value <0-4294967295> / admin-weight <0-4294967295>
                # configure / mpls traffic-eng / srlg / value <0-4294967295> / static ipv4 address 1.2.3.4 next-hop ipv4 address 1.2.3.4
                configurations.append_line(attributes.format('srlg admin-weight {srlg_admin_weight}'))

                # configure / mpls traffic-eng / soft-preemption (config-soft-preemption)
                # configure / mpls traffic-eng / soft-preemption / timeout 1
                configurations.append_line(attributes.format('soft-preemption timeout {soft_preempt_timeout}'))

                # configure / mpls traffic-eng / soft-preemption / frr-rewrite
                if attributes.value('soft_preempt_frr_rewrite'):
                    configurations.append_line(attributes.format('soft-preemption frr-rewrite'))




                #TODO: remaining attributes
                
                # configure / mpls traffic-eng / named-tunnels (config-mpls-te-named-tunnels)
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 (config-mpls-te-tunnel-name)
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / affinity 0x0 mask 0x0
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / affinity exclude someword
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / affinity exclude someword someword2
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / affinity exclude someword someword2 someword3
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / affinity exclude someword someword2 someword3 someword4
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / affinity exclude someword someword2 someword3 someword4 someword5
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / affinity exclude someword someword2 someword3 someword4 someword5 someword6
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / affinity exclude someword someword2 someword3 someword4 someword5 someword6 someword7
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / affinity exclude someword someword2 someword3 someword4 someword5 someword6 someword7 someword8
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / affinity exclude someword someword2 someword3 someword4 someword5 someword6 someword7 someword8 someword9
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / affinity exclude someword someword2 someword3 someword4 someword5 someword6 someword7 someword8 someword9 someword10
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / affinity exclude-all
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / affinity ignore
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / affinity include someword
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / affinity include someword someword2
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / affinity include someword someword2 someword3
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / affinity include someword someword2 someword3 someword4
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / affinity include someword someword2 someword3 someword4 someword5
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / affinity include someword someword2 someword3 someword4 someword5 someword6
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / affinity include someword someword2 someword3 someword4 someword5 someword6 someword7
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / affinity include someword someword2 someword3 someword4 someword5 someword6 someword7 someword8
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / affinity include someword someword2 someword3 someword4 someword5 someword6 someword7 someword8 someword9
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / affinity include someword someword2 someword3 someword4 someword5 someword6 someword7 someword8 someword9 someword10
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / affinity include-strict someword
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / affinity include-strict someword someword2
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / affinity include-strict someword someword2 someword3
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / affinity include-strict someword someword2 someword3 someword4
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / affinity include-strict someword someword2 someword3 someword4 someword5
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / affinity include-strict someword someword2 someword3 someword4 someword5 someword6
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / affinity include-strict someword someword2 someword3 someword4 someword5 someword6 someword7
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / affinity include-strict someword someword2 someword3 someword4 someword5 someword6 someword7 someword8
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / affinity include-strict someword someword2 someword3 someword4 someword5 someword6 someword7 someword8 someword9
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / affinity include-strict someword someword2 someword3 someword4 someword5 someword6 someword7 someword8 someword9 someword10
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / auto-bw (config-mpls-te-tun-autobw)
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / auto-bw / adjustment-threshold 1
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / auto-bw / adjustment-threshold 1 min 10
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / auto-bw / application 5
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / auto-bw / bw-limit min <0-4294967295> max 4294967295
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / auto-bw / collect-bw-only
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / auto-bw / overflow threshold 1 limit 1
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / auto-bw / overflow threshold 1 min 10 limit 1
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / auto-bw / underflow threshold 1 limit 1
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / auto-bw / underflow threshold 1 min 10 limit 1
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / autoroute announce (config-mpls-te-tunnel-name-aa)
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / autoroute announce / include-ipv6
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / autoroute announce / metric 1
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / autoroute announce / metric absolute 1
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / autoroute announce / metric relative -10
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / autoroute destination 1.2.3.4
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / autoroute metric 1
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / autoroute metric absolute 1
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / destination 1.2.3.4
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / fast-reroute
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / fast-reroute protect bandwidth
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / fast-reroute protect bandwidth node
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / fast-reroute protect node
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / forward-class 1
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / load-interval <0-600>
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / load-share 1
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / logging events all
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / logging events lsp-status bw-change
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / logging events lsp-status insufficient-bandwidth
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / logging events lsp-status record-route
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / logging events lsp-status reoptimize
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / logging events lsp-status reoptimize-attempts
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / logging events lsp-status reroute
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / logging events lsp-status state
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / logging events lsp-status switchover
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / logging events pcalc-failure
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / path-option someword (config-path-option-name)
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / path-option someword / computation dynamic
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / path-option someword / computation explicit someword2
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / path-option someword / preference <0-4294967295>
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / path-selection (config-mpls-te-tunnel-name-path-sel)
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / path-selection / metric igp
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / path-selection / metric te
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / path-selection / tiebreaker max-fill
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / path-selection / tiebreaker min-fill
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / path-selection / tiebreaker random
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / priority <0-7> <0-7>
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / record-route
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / shutdown
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / signalled-bandwidth <0-4294967295>
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / signalled-bandwidth <0-4294967295> class-type <0-1>
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / signalled-bandwidth sub-pool 1
                # configure / mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / soft-preemption



                # configure / mpls traffic-eng / attribute-set auto-backup someword (config-te-attribute-set)
                # configure / mpls traffic-eng / attribute-set auto-backup someword / affinity 0x0 mask 0x0
                # configure / mpls traffic-eng / attribute-set auto-backup someword / affinity exclude someword2
                # configure / mpls traffic-eng / attribute-set auto-backup someword / affinity exclude someword2 someword3
                # configure / mpls traffic-eng / attribute-set auto-backup someword / affinity exclude someword2 someword3 someword4
                # configure / mpls traffic-eng / attribute-set auto-backup someword / affinity exclude someword2 someword3 someword4 someword5
                # configure / mpls traffic-eng / attribute-set auto-backup someword / affinity exclude someword2 someword3 someword4 someword5 someword6
                # configure / mpls traffic-eng / attribute-set auto-backup someword / affinity exclude someword2 someword3 someword4 someword5 someword6 someword7
                # configure / mpls traffic-eng / attribute-set auto-backup someword / affinity exclude someword2 someword3 someword4 someword5 someword6 someword7 someword8
                # configure / mpls traffic-eng / attribute-set auto-backup someword / affinity exclude someword2 someword3 someword4 someword5 someword6 someword7 someword8 someword9
                # configure / mpls traffic-eng / attribute-set auto-backup someword / affinity exclude someword2 someword3 someword4 someword5 someword6 someword7 someword8 someword9 someword10
                # configure / mpls traffic-eng / attribute-set auto-backup someword / affinity exclude someword2 someword3 someword4 someword5 someword6 someword7 someword8 someword9 someword10 someword11
                # configure / mpls traffic-eng / attribute-set auto-backup someword / affinity exclude-all
                # configure / mpls traffic-eng / attribute-set auto-backup someword / affinity ignore
                # configure / mpls traffic-eng / attribute-set auto-backup someword / affinity include someword2
                # configure / mpls traffic-eng / attribute-set auto-backup someword / affinity include someword2 someword3
                # configure / mpls traffic-eng / attribute-set auto-backup someword / affinity include someword2 someword3 someword4
                # configure / mpls traffic-eng / attribute-set auto-backup someword / affinity include someword2 someword3 someword4 someword5
                # configure / mpls traffic-eng / attribute-set auto-backup someword / affinity include someword2 someword3 someword4 someword5 someword6
                # configure / mpls traffic-eng / attribute-set auto-backup someword / affinity include someword2 someword3 someword4 someword5 someword6 someword7
                # configure / mpls traffic-eng / attribute-set auto-backup someword / affinity include someword2 someword3 someword4 someword5 someword6 someword7 someword8
                # configure / mpls traffic-eng / attribute-set auto-backup someword / affinity include someword2 someword3 someword4 someword5 someword6 someword7 someword8 someword9
                # configure / mpls traffic-eng / attribute-set auto-backup someword / affinity include someword2 someword3 someword4 someword5 someword6 someword7 someword8 someword9 someword10
                # configure / mpls traffic-eng / attribute-set auto-backup someword / affinity include someword2 someword3 someword4 someword5 someword6 someword7 someword8 someword9 someword10 someword11
                # configure / mpls traffic-eng / attribute-set auto-backup someword / affinity include-strict someword2
                # configure / mpls traffic-eng / attribute-set auto-backup someword / affinity include-strict someword2 someword3
                # configure / mpls traffic-eng / attribute-set auto-backup someword / affinity include-strict someword2 someword3 someword4
                # configure / mpls traffic-eng / attribute-set auto-backup someword / affinity include-strict someword2 someword3 someword4 someword5
                # configure / mpls traffic-eng / attribute-set auto-backup someword / affinity include-strict someword2 someword3 someword4 someword5 someword6
                # configure / mpls traffic-eng / attribute-set auto-backup someword / affinity include-strict someword2 someword3 someword4 someword5 someword6 someword7
                # configure / mpls traffic-eng / attribute-set auto-backup someword / affinity include-strict someword2 someword3 someword4 someword5 someword6 someword7 someword8
                # configure / mpls traffic-eng / attribute-set auto-backup someword / affinity include-strict someword2 someword3 someword4 someword5 someword6 someword7 someword8 someword9
                # configure / mpls traffic-eng / attribute-set auto-backup someword / affinity include-strict someword2 someword3 someword4 someword5 someword6 someword7 someword8 someword9 someword10
                # configure / mpls traffic-eng / attribute-set auto-backup someword / affinity include-strict someword2 someword3 someword4 someword5 someword6 someword7 someword8 someword9 someword10 someword11
                # configure / mpls traffic-eng / attribute-set auto-backup someword / logging events lsp-status bw-change
                # configure / mpls traffic-eng / attribute-set auto-backup someword / logging events lsp-status reoptimize
                # configure / mpls traffic-eng / attribute-set auto-backup someword / logging events lsp-status reoptimize-attempts
                # configure / mpls traffic-eng / attribute-set auto-backup someword / logging events lsp-status state
                # configure / mpls traffic-eng / attribute-set auto-backup someword / path-selection (config-te-attrset-path-select)
                # configure / mpls traffic-eng / attribute-set auto-backup someword / policy-class 1
                # configure / mpls traffic-eng / attribute-set auto-backup someword / policy-class 1 1
                # configure / mpls traffic-eng / attribute-set auto-backup someword / policy-class 1 1 1
                # configure / mpls traffic-eng / attribute-set auto-backup someword / policy-class 1 1 1 1
                # configure / mpls traffic-eng / attribute-set auto-backup someword / policy-class 1 1 1 1 1
                # configure / mpls traffic-eng / attribute-set auto-backup someword / policy-class 1 1 1 1 1 1
                # configure / mpls traffic-eng / attribute-set auto-backup someword / policy-class 1 1 1 1 1 1 1
                # configure / mpls traffic-eng / attribute-set auto-backup someword / policy-class default
                # configure / mpls traffic-eng / attribute-set auto-backup someword / priority <0-7> <0-7>
                # configure / mpls traffic-eng / attribute-set auto-backup someword / record-route
                # configure / mpls traffic-eng / attribute-set auto-backup someword / signalled-name someword2
                # configure / mpls traffic-eng / attribute-set auto-backup someword / signalled-name someword2 append merge-point-address
                # configure / mpls traffic-eng / attribute-set auto-backup someword / signalled-name someword2 append merge-point-address protected-link address
                # configure / mpls traffic-eng / attribute-set auto-backup someword / signalled-name someword2 append merge-point-address protected-link address source address
                # configure / mpls traffic-eng / attribute-set auto-backup someword / signalled-name someword2 append merge-point-address protected-link address source name
                # configure / mpls traffic-eng / attribute-set auto-backup someword / signalled-name someword2 append merge-point-address protected-link name
                # configure / mpls traffic-eng / attribute-set auto-backup someword / signalled-name someword2 append merge-point-address protected-link name source name
                # configure / mpls traffic-eng / attribute-set auto-backup someword / signalled-name someword2 append merge-point-address source address
                # configure / mpls traffic-eng / attribute-set auto-backup someword / signalled-name someword2 append merge-point-address source name
                # configure / mpls traffic-eng / attribute-set auto-backup someword / signalled-name someword2 append protected-link address
                # configure / mpls traffic-eng / attribute-set auto-backup someword / signalled-name someword2 append protected-link address source address
                # configure / mpls traffic-eng / attribute-set auto-backup someword / signalled-name someword2 append protected-link address source name
                # configure / mpls traffic-eng / attribute-set auto-backup someword / signalled-name someword2 append protected-link name
                # configure / mpls traffic-eng / attribute-set auto-backup someword / signalled-name someword2 append protected-link name source name
                # configure / mpls traffic-eng / attribute-set auto-backup someword / signalled-name someword2 append source address
                # configure / mpls traffic-eng / attribute-set auto-backup someword / signalled-name someword2 append source name
                # configure / mpls traffic-eng / attribute-set auto-mesh someword (config-te-attribute-set)
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / affinity 0x0 mask 0x0
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / affinity exclude someword2
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / affinity exclude someword2 someword3
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / affinity exclude someword2 someword3 someword4
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / affinity exclude someword2 someword3 someword4 someword5
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / affinity exclude someword2 someword3 someword4 someword5 someword6
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / affinity exclude someword2 someword3 someword4 someword5 someword6 someword7
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / affinity exclude someword2 someword3 someword4 someword5 someword6 someword7 someword8
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / affinity exclude someword2 someword3 someword4 someword5 someword6 someword7 someword8 someword9
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / affinity exclude someword2 someword3 someword4 someword5 someword6 someword7 someword8 someword9 someword10
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / affinity exclude someword2 someword3 someword4 someword5 someword6 someword7 someword8 someword9 someword10 someword11
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / affinity exclude-all
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / affinity ignore
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / affinity include someword2
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / affinity include someword2 someword3
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / affinity include someword2 someword3 someword4
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / affinity include someword2 someword3 someword4 someword5
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / affinity include someword2 someword3 someword4 someword5 someword6
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / affinity include someword2 someword3 someword4 someword5 someword6 someword7
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / affinity include someword2 someword3 someword4 someword5 someword6 someword7 someword8
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / affinity include someword2 someword3 someword4 someword5 someword6 someword7 someword8 someword9
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / affinity include someword2 someword3 someword4 someword5 someword6 someword7 someword8 someword9 someword10
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / affinity include someword2 someword3 someword4 someword5 someword6 someword7 someword8 someword9 someword10 someword11
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / affinity include-strict someword2
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / affinity include-strict someword2 someword3
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / affinity include-strict someword2 someword3 someword4
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / affinity include-strict someword2 someword3 someword4 someword5
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / affinity include-strict someword2 someword3 someword4 someword5 someword6
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / affinity include-strict someword2 someword3 someword4 someword5 someword6 someword7
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / affinity include-strict someword2 someword3 someword4 someword5 someword6 someword7 someword8
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / affinity include-strict someword2 someword3 someword4 someword5 someword6 someword7 someword8 someword9
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / affinity include-strict someword2 someword3 someword4 someword5 someword6 someword7 someword8 someword9 someword10
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / affinity include-strict someword2 someword3 someword4 someword5 someword6 someword7 someword8 someword9 someword10 someword11
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / auto-bw collect-bw-only
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / autoroute announce
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / bandwidth <0-4294967295>
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / fast-reroute
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / fast-reroute protect bandwidth
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / fast-reroute protect bandwidth node
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / fast-reroute protect node
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / forward-class 1
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / load-share 1
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / logging events lsp-status bw-change
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / logging events lsp-status insufficient-bandwidth
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / logging events lsp-status reoptimize
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / logging events lsp-status reoptimize-attempts
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / logging events lsp-status reroute
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / logging events lsp-status state
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / logging events pcalc-failure
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / path-selection (config-te-attrset-path-select)
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / policy-class 1
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / policy-class 1 1
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / policy-class 1 1 1
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / policy-class 1 1 1 1
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / policy-class 1 1 1 1 1
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / policy-class 1 1 1 1 1 1
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / policy-class 1 1 1 1 1 1 1
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / policy-class default
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / priority <0-7> <0-7>
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / record-route
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / signalled-bandwidth <0-4294967295>
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / signalled-bandwidth <0-4294967295> class-type <0-1>
                # configure / mpls traffic-eng / attribute-set auto-mesh someword / soft-preemption
                # configure / mpls traffic-eng / attribute-set p2mp-te someword (config-te-attribute-set)
                # configure / mpls traffic-eng / attribute-set p2mp-te someword / affinity 0x0 mask 0x0
                # configure / mpls traffic-eng / attribute-set p2mp-te someword / affinity exclude someword2
                # configure / mpls traffic-eng / attribute-set p2mp-te someword / affinity exclude someword2 someword3
                # configure / mpls traffic-eng / attribute-set p2mp-te someword / affinity exclude someword2 someword3 someword4
                # configure / mpls traffic-eng / attribute-set p2mp-te someword / affinity exclude someword2 someword3 someword4 someword5
                # configure / mpls traffic-eng / attribute-set p2mp-te someword / affinity exclude someword2 someword3 someword4 someword5 someword6
                # configure / mpls traffic-eng / attribute-set p2mp-te someword / affinity exclude someword2 someword3 someword4 someword5 someword6 someword7
                # configure / mpls traffic-eng / attribute-set p2mp-te someword / affinity exclude someword2 someword3 someword4 someword5 someword6 someword7 someword8
                # configure / mpls traffic-eng / attribute-set p2mp-te someword / affinity exclude someword2 someword3 someword4 someword5 someword6 someword7 someword8 someword9
                # configure / mpls traffic-eng / attribute-set p2mp-te someword / affinity exclude someword2 someword3 someword4 someword5 someword6 someword7 someword8 someword9 someword10
                # configure / mpls traffic-eng / attribute-set p2mp-te someword / affinity exclude someword2 someword3 someword4 someword5 someword6 someword7 someword8 someword9 someword10 someword11
                # configure / mpls traffic-eng / attribute-set p2mp-te someword / affinity exclude-all
                # configure / mpls traffic-eng / attribute-set p2mp-te someword / affinity ignore
                # configure / mpls traffic-eng / attribute-set p2mp-te someword / affinity include someword2
                # configure / mpls traffic-eng / attribute-set p2mp-te someword / affinity include someword2 someword3
                # configure / mpls traffic-eng / attribute-set p2mp-te someword / affinity include someword2 someword3 someword4
                # configure / mpls traffic-eng / attribute-set p2mp-te someword / affinity include someword2 someword3 someword4 someword5
                # configure / mpls traffic-eng / attribute-set p2mp-te someword / affinity include someword2 someword3 someword4 someword5 someword6
                # configure / mpls traffic-eng / attribute-set p2mp-te someword / affinity include someword2 someword3 someword4 someword5 someword6 someword7
                # configure / mpls traffic-eng / attribute-set p2mp-te someword / affinity include someword2 someword3 someword4 someword5 someword6 someword7 someword8
                # configure / mpls traffic-eng / attribute-set p2mp-te someword / affinity include someword2 someword3 someword4 someword5 someword6 someword7 someword8 someword9
                # configure / mpls traffic-eng / attribute-set p2mp-te someword / affinity include someword2 someword3 someword4 someword5 someword6 someword7 someword8 someword9 someword10
                # configure / mpls traffic-eng / attribute-set p2mp-te someword / affinity include someword2 someword3 someword4 someword5 someword6 someword7 someword8 someword9 someword10 someword11
                # configure / mpls traffic-eng / attribute-set p2mp-te someword / affinity include-strict someword2
                # configure / mpls traffic-eng / attribute-set p2mp-te someword / affinity include-strict someword2 someword3
                # configure / mpls traffic-eng / attribute-set p2mp-te someword / affinity include-strict someword2 someword3 someword4
                # configure / mpls traffic-eng / attribute-set p2mp-te someword / affinity include-strict someword2 someword3 someword4 someword5
                # configure / mpls traffic-eng / attribute-set p2mp-te someword / affinity include-strict someword2 someword3 someword4 someword5 someword6
                # configure / mpls traffic-eng / attribute-set p2mp-te someword / affinity include-strict someword2 someword3 someword4 someword5 someword6 someword7
                # configure / mpls traffic-eng / attribute-set p2mp-te someword / affinity include-strict someword2 someword3 someword4 someword5 someword6 someword7 someword8
                # configure / mpls traffic-eng / attribute-set p2mp-te someword / affinity include-strict someword2 someword3 someword4 someword5 someword6 someword7 someword8 someword9
                # configure / mpls traffic-eng / attribute-set p2mp-te someword / affinity include-strict someword2 someword3 someword4 someword5 someword6 someword7 someword8 someword9 someword10
                # configure / mpls traffic-eng / attribute-set p2mp-te someword / affinity include-strict someword2 someword3 someword4 someword5 someword6 someword7 someword8 someword9 someword10 someword11
                # configure / mpls traffic-eng / attribute-set p2mp-te someword / bandwidth <0-4294967295>
                # configure / mpls traffic-eng / attribute-set p2mp-te someword / fast-reroute
                # configure / mpls traffic-eng / attribute-set p2mp-te someword / fast-reroute protect bandwidth
                # configure / mpls traffic-eng / attribute-set p2mp-te someword / logging events lsp-status bw-change
                # configure / mpls traffic-eng / attribute-set p2mp-te someword / logging events lsp-status insufficient-bandwidth
                # configure / mpls traffic-eng / attribute-set p2mp-te someword / logging events lsp-status reoptimize
                # configure / mpls traffic-eng / attribute-set p2mp-te someword / logging events lsp-status reoptimize-attempts
                # configure / mpls traffic-eng / attribute-set p2mp-te someword / logging events lsp-status reroute
                # configure / mpls traffic-eng / attribute-set p2mp-te someword / logging events lsp-status state
                # configure / mpls traffic-eng / attribute-set p2mp-te someword / logging events pcalc-failure
                # configure / mpls traffic-eng / attribute-set p2mp-te someword / logging events sub-lsp-status state
                # configure / mpls traffic-eng / attribute-set p2mp-te someword / path-selection (config-te-attrset-path-select)
                # configure / mpls traffic-eng / attribute-set p2mp-te someword / priority <0-7> <0-7>
                # configure / mpls traffic-eng / attribute-set p2mp-te someword / record-route
                # configure / mpls traffic-eng / attribute-set p2mp-te someword / signalled-bandwidth <0-4294967295>
                # configure / mpls traffic-eng / attribute-set p2mp-te someword / signalled-bandwidth <0-4294967295> class-type <0-1>
                # configure / mpls traffic-eng / attribute-set p2p-te someword (config-te-attribute-set)
                # configure / mpls traffic-eng / attribute-set p2p-te someword / affinity exclude someword2
                # configure / mpls traffic-eng / attribute-set p2p-te someword / affinity exclude someword2 someword3
                # configure / mpls traffic-eng / attribute-set p2p-te someword / affinity exclude someword2 someword3 someword4
                # configure / mpls traffic-eng / attribute-set p2p-te someword / affinity exclude someword2 someword3 someword4 someword5
                # configure / mpls traffic-eng / attribute-set p2p-te someword / affinity exclude someword2 someword3 someword4 someword5 someword6
                # configure / mpls traffic-eng / attribute-set p2p-te someword / affinity exclude someword2 someword3 someword4 someword5 someword6 someword7
                # configure / mpls traffic-eng / attribute-set p2p-te someword / affinity exclude someword2 someword3 someword4 someword5 someword6 someword7 someword8
                # configure / mpls traffic-eng / attribute-set p2p-te someword / affinity exclude someword2 someword3 someword4 someword5 someword6 someword7 someword8 someword9
                # configure / mpls traffic-eng / attribute-set p2p-te someword / affinity exclude someword2 someword3 someword4 someword5 someword6 someword7 someword8 someword9 someword10
                # configure / mpls traffic-eng / attribute-set p2p-te someword / affinity exclude someword2 someword3 someword4 someword5 someword6 someword7 someword8 someword9 someword10 someword11
                # configure / mpls traffic-eng / attribute-set p2p-te someword / logging events all
                # configure / mpls traffic-eng / attribute-set p2p-te someword / logging events lsp-status bw-change
                # configure / mpls traffic-eng / attribute-set p2p-te someword / logging events lsp-status insufficient-bandwidth
                # configure / mpls traffic-eng / attribute-set p2p-te someword / logging events lsp-status reoptimize
                # configure / mpls traffic-eng / attribute-set p2p-te someword / logging events lsp-status reoptimize-attempts
                # configure / mpls traffic-eng / attribute-set p2p-te someword / logging events lsp-status reroute
                # configure / mpls traffic-eng / attribute-set p2p-te someword / logging events lsp-status state
                # configure / mpls traffic-eng / attribute-set p2p-te someword / logging events pcalc-failure
                # configure / mpls traffic-eng / attribute-set p2p-te someword / path-selection (config-te-attrset-path-select)
                # configure / mpls traffic-eng / attribute-set p2p-te someword / path-selection / invalidation <0-60000>
                # configure / mpls traffic-eng / attribute-set p2p-te someword / path-selection / invalidation <0-60000> drop
                # configure / mpls traffic-eng / attribute-set p2p-te someword / path-selection / invalidation <0-60000> tear
                # configure / mpls traffic-eng / attribute-set p2p-te someword / path-selection / invalidation drop
                # configure / mpls traffic-eng / attribute-set p2p-te someword / path-selection / invalidation tear
                # configure / mpls traffic-eng / attribute-set p2p-te someword / path-selection / metric igp
                # configure / mpls traffic-eng / attribute-set p2p-te someword / path-selection / metric te
                # configure / mpls traffic-eng / attribute-set p2p-te someword / path-selection / segment-routing adjacency protected
                # configure / mpls traffic-eng / attribute-set p2p-te someword / path-selection / segment-routing adjacency unprotected
                # configure / mpls traffic-eng / attribute-set p2p-te someword / path-selection / segment-routing prepend (config-te-attrset-prepend)
                # configure / mpls traffic-eng / attribute-set p2p-te someword / path-selection / segment-routing prepend / index 1 bgp-nhop
                # configure / mpls traffic-eng / attribute-set p2p-te someword / path-selection / segment-routing prepend / index 1 next-label <0-1048575>
                # configure / mpls traffic-eng / attribute-set p2p-te someword / pce (config-te-attrset-pce)
                # configure / mpls traffic-eng / attribute-set p2p-te someword / pce / bidirectional source 1.2.3.4 group-id 1
                # configure / mpls traffic-eng / attribute-set p2p-te someword / pce / disjoint-path source 1.2.3.4 type link group-id 1
                # configure / mpls traffic-eng / attribute-set p2p-te someword / pce / disjoint-path source 1.2.3.4 type node group-id 1
                # configure / mpls traffic-eng / attribute-set p2p-te someword / pce / disjoint-path source 1.2.3.4 type srlg group-id 1
                # configure / mpls traffic-eng / attribute-set path-option someword (config-te-attribute-set)
                # configure / mpls traffic-eng / attribute-set path-option someword / affinity 0x0 mask 0x0
                # configure / mpls traffic-eng / attribute-set path-option someword / affinity exclude someword2
                # configure / mpls traffic-eng / attribute-set path-option someword / affinity exclude someword2 someword3
                # configure / mpls traffic-eng / attribute-set path-option someword / affinity exclude someword2 someword3 someword4
                # configure / mpls traffic-eng / attribute-set path-option someword / affinity exclude someword2 someword3 someword4 someword5
                # configure / mpls traffic-eng / attribute-set path-option someword / affinity exclude someword2 someword3 someword4 someword5 someword6
                # configure / mpls traffic-eng / attribute-set path-option someword / affinity exclude someword2 someword3 someword4 someword5 someword6 someword7
                # configure / mpls traffic-eng / attribute-set path-option someword / affinity exclude someword2 someword3 someword4 someword5 someword6 someword7 someword8
                # configure / mpls traffic-eng / attribute-set path-option someword / affinity exclude someword2 someword3 someword4 someword5 someword6 someword7 someword8 someword9
                # configure / mpls traffic-eng / attribute-set path-option someword / affinity exclude someword2 someword3 someword4 someword5 someword6 someword7 someword8 someword9 someword10
                # configure / mpls traffic-eng / attribute-set path-option someword / affinity exclude someword2 someword3 someword4 someword5 someword6 someword7 someword8 someword9 someword10 someword11
                # configure / mpls traffic-eng / attribute-set path-option someword / affinity exclude-all
                # configure / mpls traffic-eng / attribute-set path-option someword / affinity ignore
                # configure / mpls traffic-eng / attribute-set path-option someword / affinity include someword2
                # configure / mpls traffic-eng / attribute-set path-option someword / affinity include someword2 someword3
                # configure / mpls traffic-eng / attribute-set path-option someword / affinity include someword2 someword3 someword4
                # configure / mpls traffic-eng / attribute-set path-option someword / affinity include someword2 someword3 someword4 someword5
                # configure / mpls traffic-eng / attribute-set path-option someword / affinity include someword2 someword3 someword4 someword5 someword6
                # configure / mpls traffic-eng / attribute-set path-option someword / affinity include someword2 someword3 someword4 someword5 someword6 someword7
                # configure / mpls traffic-eng / attribute-set path-option someword / affinity include someword2 someword3 someword4 someword5 someword6 someword7 someword8
                # configure / mpls traffic-eng / attribute-set path-option someword / affinity include someword2 someword3 someword4 someword5 someword6 someword7 someword8 someword9
                # configure / mpls traffic-eng / attribute-set path-option someword / affinity include someword2 someword3 someword4 someword5 someword6 someword7 someword8 someword9 someword10
                # configure / mpls traffic-eng / attribute-set path-option someword / affinity include someword2 someword3 someword4 someword5 someword6 someword7 someword8 someword9 someword10 someword11
                # configure / mpls traffic-eng / attribute-set path-option someword / affinity include-strict someword2
                # configure / mpls traffic-eng / attribute-set path-option someword / affinity include-strict someword2 someword3
                # configure / mpls traffic-eng / attribute-set path-option someword / affinity include-strict someword2 someword3 someword4
                # configure / mpls traffic-eng / attribute-set path-option someword / affinity include-strict someword2 someword3 someword4 someword5
                # configure / mpls traffic-eng / attribute-set path-option someword / affinity include-strict someword2 someword3 someword4 someword5 someword6
                # configure / mpls traffic-eng / attribute-set path-option someword / affinity include-strict someword2 someword3 someword4 someword5 someword6 someword7
                # configure / mpls traffic-eng / attribute-set path-option someword / affinity include-strict someword2 someword3 someword4 someword5 someword6 someword7 someword8
                # configure / mpls traffic-eng / attribute-set path-option someword / affinity include-strict someword2 someword3 someword4 someword5 someword6 someword7 someword8 someword9
                # configure / mpls traffic-eng / attribute-set path-option someword / affinity include-strict someword2 someword3 someword4 someword5 someword6 someword7 someword8 someword9 someword10
                # configure / mpls traffic-eng / attribute-set path-option someword / affinity include-strict someword2 someword3 someword4 someword5 someword6 someword7 someword8 someword9 someword10 someword11
                # configure / mpls traffic-eng / attribute-set path-option someword / bfd-reverse-path binding-label <0-1048575>
                # configure / mpls traffic-eng / attribute-set path-option someword / path-selection (config-te-attrset-path-select)
                # configure / mpls traffic-eng / attribute-set path-option someword / path-selection / cost-limit 1
                # configure / mpls traffic-eng / attribute-set path-option someword / path-selection / exclude someword2
                # configure / mpls traffic-eng / attribute-set path-option someword / path-selection / invalidation <0-60000>
                # configure / mpls traffic-eng / attribute-set path-option someword / path-selection / invalidation <0-60000> drop
                # configure / mpls traffic-eng / attribute-set path-option someword / path-selection / invalidation <0-60000> tear
                # configure / mpls traffic-eng / attribute-set path-option someword / path-selection / invalidation drop
                # configure / mpls traffic-eng / attribute-set path-option someword / path-selection / invalidation tear
                # configure / mpls traffic-eng / attribute-set path-option someword / pce (config-te-attrset-pce)
                # configure / mpls traffic-eng / attribute-set path-option someword / pce / bidirectional source 1.2.3.4 group-id 1
                # configure / mpls traffic-eng / attribute-set path-option someword / pce / disjoint-path source 1.2.3.4 type link group-id 1
                # configure / mpls traffic-eng / attribute-set path-option someword / pce / disjoint-path source 1.2.3.4 type node group-id 1
                # configure / mpls traffic-eng / attribute-set path-option someword / pce / disjoint-path source 1.2.3.4 type srlg group-id 1
                # configure / mpls traffic-eng / attribute-set path-option someword / signalled-bandwidth <0-4294967295>
                # configure / mpls traffic-eng / attribute-set path-option someword / signalled-bandwidth <0-4294967295> class-type <0-1>
                # configure / mpls traffic-eng / attribute-set path-protection-aps someword (config-te-attribute-set)
                # configure / mpls traffic-eng / attribute-set path-protection-aps someword / path-selection (config-te-attrset-path-select)
                # configure / mpls traffic-eng / attribute-set path-protection-aps someword / protection-mode revertive
                # configure / mpls traffic-eng / attribute-set path-protection-aps someword / protection-type BIDIR-APS
                # configure / mpls traffic-eng / attribute-set path-protection-aps someword / protection-type UNIDIR-APS
                # configure / mpls traffic-eng / attribute-set path-protection-aps someword / protection-type UNIDIR-NO-APS
                # configure / mpls traffic-eng / attribute-set path-protection-aps someword / revert-schedule schedule-name someword2 (config-te-attribute-set-rev-sch)
                # configure / mpls traffic-eng / attribute-set path-protection-aps someword / revert-schedule schedule-name someword2 / date 01:02 JAN 1 2015
                # configure / mpls traffic-eng / attribute-set path-protection-aps someword / revert-schedule schedule-name someword2 / date 01:02 FEB 1 2015
                # configure / mpls traffic-eng / attribute-set path-protection-aps someword / revert-schedule schedule-name someword2 / date 01:02 MAR 1 2015
                # configure / mpls traffic-eng / attribute-set path-protection-aps someword / revert-schedule schedule-name someword2 / date 01:02 APR 1 2015
                # configure / mpls traffic-eng / attribute-set path-protection-aps someword / revert-schedule schedule-name someword2 / date 01:02 MAY 1 2015
                # configure / mpls traffic-eng / attribute-set path-protection-aps someword / revert-schedule schedule-name someword2 / date 01:02 JUN 1 2015
                # configure / mpls traffic-eng / attribute-set path-protection-aps someword / revert-schedule schedule-name someword2 / date 01:02 JUL 1 2015
                # configure / mpls traffic-eng / attribute-set path-protection-aps someword / revert-schedule schedule-name someword2 / date 01:02 AUG 1 2015
                # configure / mpls traffic-eng / attribute-set path-protection-aps someword / revert-schedule schedule-name someword2 / date 01:02 SEP 1 2015
                # configure / mpls traffic-eng / attribute-set path-protection-aps someword / revert-schedule schedule-name someword2 / date 01:02 OCT 1 2015
                # configure / mpls traffic-eng / attribute-set path-protection-aps someword / revert-schedule schedule-name someword2 / date 01:02 NOV 1 2015
                # configure / mpls traffic-eng / attribute-set path-protection-aps someword / revert-schedule schedule-name someword2 / date 01:02 DEC 1 2015
                # configure / mpls traffic-eng / attribute-set path-protection-aps someword / revert-schedule schedule-name someword2 / frequency daily
                # configure / mpls traffic-eng / attribute-set path-protection-aps someword / revert-schedule schedule-name someword2 / frequency once
                # configure / mpls traffic-eng / attribute-set path-protection-aps someword / revert-schedule schedule-name someword2 / frequency weekly
                # configure / mpls traffic-eng / attribute-set path-protection-aps someword / revert-schedule schedule-name someword2 / max-tries 1
                # configure / mpls traffic-eng / attribute-set path-protection-aps someword / sub-network connection-mode SNC-I
                # configure / mpls traffic-eng / attribute-set path-protection-aps someword / sub-network connection-mode SNC-N
                # configure / mpls traffic-eng / attribute-set path-protection-aps someword / sub-network connection-mode SNC-S
                # configure / mpls traffic-eng / attribute-set path-protection-aps someword / sub-network connection-mode SNC-S tcm-id 1
                # configure / mpls traffic-eng / attribute-set path-protection-aps someword / timers (config-te-attribute-set-aps-timer)
                # configure / mpls traffic-eng / attribute-set path-protection-aps someword / timers / hold-off 100
                # configure / mpls traffic-eng / attribute-set path-protection-aps someword / timers / wait-to-restore <0-720>
                # configure / mpls traffic-eng / attribute-set xro someword (config-te-attribute-set)
                # configure / mpls traffic-eng / attribute-set xro someword / exclude best-effort lsp source 1.2.3.4 destination 1.2.3.4 tunnel-id <0-65535> extended-tunnel-id 1.2.3.4
                # configure / mpls traffic-eng / attribute-set xro someword / exclude best-effort lsp source 1.2.3.4 destination 1.2.3.4 tunnel-id <0-65535> extended-tunnel-id 1.2.3.4 lsp-id <0-65535>
                # configure / mpls traffic-eng / attribute-set xro someword / exclude best-effort srlg value <0-4294967295>
                # configure / mpls traffic-eng / attribute-set xro someword / exclude strict lsp source 1.2.3.4 destination 1.2.3.4 tunnel-id <0-65535> extended-tunnel-id 1.2.3.4
                # configure / mpls traffic-eng / attribute-set xro someword / exclude strict lsp source 1.2.3.4 destination 1.2.3.4 tunnel-id <0-65535> extended-tunnel-id 1.2.3.4 lsp-id <0-65535>
                # configure / mpls traffic-eng / attribute-set xro someword / exclude strict srlg value <0-4294967295>
                # configure / mpls traffic-eng / attribute-set xro someword / path-selection (config-te-attrset-path-select)
                # configure / mpls traffic-eng / auto-bw collect frequency 1


                # configure / mpls traffic-eng / bfd lsp head down-action reoptimize timeout 120
                # configure / mpls traffic-eng / bfd lsp head down-action resetup
                # configure / mpls traffic-eng / bfd lsp tail minimum-interval 50
                # configure / mpls traffic-eng / bfd lsp tail multiplier 3
                # configure / mpls traffic-eng / bfd minimum-interval 15
                # configure / mpls traffic-eng / bfd multiplier 2
                # configure / mpls traffic-eng / ds-te bc-model mam
                # configure / mpls traffic-eng / ds-te mode ietf
                # configure / mpls traffic-eng / ds-te te-classes (config-te-class)
                # configure / mpls traffic-eng / ds-te te-classes / te-class <0-7> class-type <0-1> priority <0-7>
                # configure / mpls traffic-eng / ds-te te-classes / te-class <0-7> unused
                # configure / mpls traffic-eng / fault-oam
                # configure / mpls traffic-eng / gmpls optical-nni (config-te-gmpls-nni)
                # configure / mpls traffic-eng / gmpls optical-nni / path-selection metric delay
                # configure / mpls traffic-eng / gmpls optical-nni / path-selection metric te-metric
                # configure / mpls traffic-eng / gmpls optical-uni (config-te-gmpls-uni)
                # configure / mpls traffic-eng / gmpls optical-uni / timers path-option holddown 100 200
                # configure / mpls traffic-eng / link-management timers bandwidth-hold 1
                # configure / mpls traffic-eng / link-management timers periodic-flooding <0-3600>
                # configure / mpls traffic-eng / link-management timers preemption-delay bundle-capacity <0-300>
                # configure / mpls traffic-eng / load-share unequal
                # configure / mpls traffic-eng / maxabs destinations 1
                # configure / mpls traffic-eng / maxabs destinations 1 p2mp-tunnels 1
                # configure / mpls traffic-eng / maxabs destinations 1 p2mp-tunnels 1 tunnels 1
                # configure / mpls traffic-eng / maxabs destinations 1 tunnels 1
                # configure / mpls traffic-eng / maxabs p2mp-tunnels 1
                # configure / mpls traffic-eng / maxabs p2mp-tunnels 1 tunnels 1
                # configure / mpls traffic-eng / maxabs tunnels 1
                # configure / mpls traffic-eng / mib midstats disable
                # configure / mpls traffic-eng / path-selection (config-mpls-te-path-sel)
                # configure / mpls traffic-eng / path-selection / cost-limit 1
                # configure / mpls traffic-eng / path-selection / ignore overload
                # configure / mpls traffic-eng / path-selection / ignore overload head
                # configure / mpls traffic-eng / path-selection / ignore overload head mid
                # configure / mpls traffic-eng / path-selection / ignore overload head mid tail
                # configure / mpls traffic-eng / path-selection / ignore overload head tail
                # configure / mpls traffic-eng / path-selection / ignore overload mid
                # configure / mpls traffic-eng / path-selection / ignore overload mid tail
                # configure / mpls traffic-eng / path-selection / ignore overload tail
                # configure / mpls traffic-eng / path-selection / invalidation <0-60000>
                # configure / mpls traffic-eng / path-selection / invalidation <0-60000> drop
                # configure / mpls traffic-eng / path-selection / invalidation <0-60000> tear
                # configure / mpls traffic-eng / path-selection / invalidation drop
                # configure / mpls traffic-eng / path-selection / invalidation tear
                # configure / mpls traffic-eng / path-selection / loose-expansion affinity 0x0 mask 0x0
                # configure / mpls traffic-eng / path-selection / loose-expansion affinity 0x0 mask 0x0 class-type <0-1>
                # configure / mpls traffic-eng / path-selection / loose-expansion domain-match
                # configure / mpls traffic-eng / path-selection / loose-expansion metric igp
                # configure / mpls traffic-eng / path-selection / loose-expansion metric igp class-type <0-1>
                # configure / mpls traffic-eng / path-selection / loose-expansion metric te
                # configure / mpls traffic-eng / path-selection / loose-expansion metric te class-type <0-1>
                # configure / mpls traffic-eng / path-selection / metric igp
                # configure / mpls traffic-eng / path-selection / metric te
                # configure / mpls traffic-eng / path-selection / tiebreaker max-fill
                # configure / mpls traffic-eng / path-selection / tiebreaker min-fill
                # configure / mpls traffic-eng / path-selection / tiebreaker random
                # configure / mpls traffic-eng / pce (config-mpls-te-pce)
                # configure / mpls traffic-eng / pce / address ipv4 1.2.3.4
                # configure / mpls traffic-eng / pce / deadtimer <0-255>
                # configure / mpls traffic-eng / pce / keepalive <0-255>
                # configure / mpls traffic-eng / pce / keychain someword
                # configure / mpls traffic-eng / pce / logging events peer-status
                # configure / mpls traffic-eng / pce / password clear some clear password
                # configure / mpls traffic-eng / pce / password encrypted 060506324F41
                # configure / mpls traffic-eng / pce / peer ipv4 1.2.3.4 (config-mpls-te-pce-peer)
                # configure / mpls traffic-eng / pce / peer ipv4 1.2.3.4 / keychain someword
                # configure / mpls traffic-eng / pce / peer ipv4 1.2.3.4 / password clear some clear password
                # configure / mpls traffic-eng / pce / peer ipv4 1.2.3.4 / password encrypted 060506324F41
                # configure / mpls traffic-eng / pce / peer ipv4 1.2.3.4 / precedence <0-255>
                # configure / mpls traffic-eng / pce / peer source ipv4 1.2.3.4
                # configure / mpls traffic-eng / pce / request-timeout 5
                # configure / mpls traffic-eng / pce / segment-routing
                # configure / mpls traffic-eng / pce / speaker-entity-id someword
                # configure / mpls traffic-eng / pce / stateful-client (config-mpls-te-pce-stateful)
                # configure / mpls traffic-eng / pce / stateful-client / cisco-extension
                # configure / mpls traffic-eng / pce / stateful-client / delegation
                # configure / mpls traffic-eng / pce / stateful-client / fast-repair
                # configure / mpls traffic-eng / pce / stateful-client / instantiation
                # configure / mpls traffic-eng / pce / stateful-client / report
                # configure / mpls traffic-eng / pce / stateful-client / timers redelegation-timeout <0-3600>
                # configure / mpls traffic-eng / pce / stateful-client / timers state-timeout <0-3600>
                # configure / mpls traffic-eng / pce / tolerance keepalive <0-255>
                # configure / mpls traffic-eng / preemption-graceful bw-reduction
                # configure / mpls traffic-eng / reoptimize disable affinity-failure
                # configure / mpls traffic-eng / reoptimize events link-up
                # configure / mpls traffic-eng / reoptimize load-balance
                # configure / mpls traffic-eng / reoptimize timers delay after-affinity-failure 1
                # configure / mpls traffic-eng / reoptimize timers delay after-frr <0-120>
                # configure / mpls traffic-eng / reoptimize timers delay path-protection <0-604800>
                # configure / mpls traffic-eng / route-priority role head backup queue <0-12>
                # configure / mpls traffic-eng / route-priority role head primary queue <0-12>
                # configure / mpls traffic-eng / route-priority role middle queue <0-12>
                # configure / mpls traffic-eng / router-id secondary 1.2.3.4
                # configure / mpls traffic-eng / signalling advertise explicit-null
                # configure / mpls traffic-eng / timers loose-path retry-period 30
                # configure / mpls traffic-eng / topology holddown sigerr <0-300>
                # configure / mpls traffic-eng / tp (config-mpls-te-tp)
                # configure / mpls traffic-eng / tp / alarm (config-mpls-te-tp-alarm)
                # configure / mpls traffic-eng / tp / alarm / soak-time <0-10>
                # configure / mpls traffic-eng / tp / alarm / suppression disable
                # configure / mpls traffic-eng / tp / bfd (config-mpls-te-tp-bfd)
                # configure / mpls traffic-eng / tp / bfd / min-interval 3
                # configure / mpls traffic-eng / tp / bfd / min-interval micro-sec 3000
                # configure / mpls traffic-eng / tp / bfd / min-interval standby 3
                # configure / mpls traffic-eng / tp / bfd / min-interval standby micro-sec 3000
                # configure / mpls traffic-eng / tp / bfd / multiplier 2
                # configure / mpls traffic-eng / tp / bfd / multiplier standby 2
                # configure / mpls traffic-eng / tp / fault (config-mpls-te-tp-fault)
                # configure / mpls traffic-eng / tp / fault / oam interval 1
                # configure / mpls traffic-eng / tp / fault / protection-trigger ais
                # configure / mpls traffic-eng / tp / fault / protection-trigger ldi disable
                # configure / mpls traffic-eng / tp / fault / protection-trigger lkr disable
                # configure / mpls traffic-eng / tp / fault / wait-to-restore interval <0-2147483647>
                # configure / mpls traffic-eng / tp / global-id 1
                # configure / mpls traffic-eng / tp / mid someword (config-mpls-te-tp-mid)
                # configure / mpls traffic-eng / tp / mid someword / destination 1.2.3.4 tunnel-id <0-65535>
                # configure / mpls traffic-eng / tp / mid someword / destination 1.2.3.4 tunnel-id <0-65535> global-id 1
                # configure / mpls traffic-eng / tp / mid someword / fast-protect
                # configure / mpls traffic-eng / tp / mid someword / forward-lsp (config-mpls-te-tp-mid-fwd)
                # configure / mpls traffic-eng / tp / mid someword / forward-lsp / bandwidth <0-4294967295>
                # configure / mpls traffic-eng / tp / mid someword / forward-lsp / in-label 16 out-label 16 out-link 1
                # configure / mpls traffic-eng / tp / mid someword / lsp-number <0-65535>
                # configure / mpls traffic-eng / tp / mid someword / reverse-lsp (config-mpls-te-tp-mid-rev)
                # configure / mpls traffic-eng / tp / mid someword / reverse-lsp / bandwidth <0-4294967295>
                # configure / mpls traffic-eng / tp / mid someword / reverse-lsp / in-label 16 out-label 16 out-link 1
                # configure / mpls traffic-eng / tp / mid someword / source 1.2.3.4 tunnel-id <0-65535>
                # configure / mpls traffic-eng / tp / mid someword / source 1.2.3.4 tunnel-id <0-65535> global-id 1
                # configure / mpls traffic-eng / tp / mid someword / tunnel-name someword2
                # configure / mpls traffic-eng / tp / node-id 1.2.3.4

                # PER CONTROLLER
                # configure / mpls traffic-eng / gmpls optical-uni / controller Loopback0 (config-te-gmpls-cntl)
                # configure / mpls traffic-eng / gmpls optical-uni / controller Loopback0 / announce srlgs
                # configure / mpls traffic-eng / gmpls optical-uni / controller Loopback0 / logging discovered-srlgs
                # configure / mpls traffic-eng / gmpls optical-uni / controller Loopback0 / tunnel-properties (config-te-gmpls-tun)
                # configure / mpls traffic-eng / gmpls optical-uni / controller Loopback0 / tunnel-properties / destination ipv4 unicast 1.2.3.4
                # configure / mpls traffic-eng / gmpls optical-uni / controller Loopback0 / tunnel-properties / logging events lsp-status state
                # configure / mpls traffic-eng / gmpls optical-uni / controller Loopback0 / tunnel-properties / path-option 1 explicit identifier 1 lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller Loopback0 / tunnel-properties / path-option 1 explicit identifier 1 signaled-label dwdm wavelength 1 lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller Loopback0 / tunnel-properties / path-option 1 explicit identifier 1 signaled-label dwdm wavelength 1 xro-attribute-set someword lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller Loopback0 / tunnel-properties / path-option 1 explicit identifier 1 xro-attribute-set someword lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller Loopback0 / tunnel-properties / path-option 1 explicit name someword lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller Loopback0 / tunnel-properties / path-option 1 explicit name someword signaled-label dwdm wavelength 1 lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller Loopback0 / tunnel-properties / path-option 1 explicit name someword signaled-label dwdm wavelength 1 xro-attribute-set someword2 lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller Loopback0 / tunnel-properties / path-option 1 explicit name someword xro-attribute-set someword2 lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller Loopback0 / tunnel-properties / path-option 1 no-ero lockdown
                # configure / mpls traffic-eng / gmpls optical-uni / controller Loopback0 / tunnel-properties / path-option 1 no-ero signaled-label dwdm wavelength 1 lockdown
                # configure / mpls traffic-eng / gmpls optical-uni / controller Loopback0 / tunnel-properties / path-option 1 no-ero signaled-label dwdm wavelength 1 xro-attribute-set someword lockdown
                # configure / mpls traffic-eng / gmpls optical-uni / controller Loopback0 / tunnel-properties / path-option 1 no-ero xro-attribute-set someword lockdown
                # configure / mpls traffic-eng / gmpls optical-uni / controller Loopback0 / tunnel-properties / priority <0-7> <0-7>
                # configure / mpls traffic-eng / gmpls optical-uni / controller Loopback0 / tunnel-properties / record srlg
                # configure / mpls traffic-eng / gmpls optical-uni / controller Loopback0 / tunnel-properties / record-route
                # configure / mpls traffic-eng / gmpls optical-uni / controller Loopback0 / tunnel-properties / signalled-name someword
                # configure / mpls traffic-eng / gmpls optical-uni / controller Loopback0 / tunnel-properties / tunnel-id <0-65535>
                # configure / mpls traffic-eng / gmpls optical-uni / controller CoherentDSP 0/1/0/0 (config-te-gmpls-cntl)
                # configure / mpls traffic-eng / gmpls optical-uni / controller CoherentDSP 0/1/0/0 / announce srlgs
                # configure / mpls traffic-eng / gmpls optical-uni / controller CoherentDSP 0/1/0/0 / logging discovered-srlgs
                # configure / mpls traffic-eng / gmpls optical-uni / controller CoherentDSP 0/1/0/0 / tunnel-properties (config-te-gmpls-tun)
                # configure / mpls traffic-eng / gmpls optical-uni / controller CoherentDSP 0/1/0/0 / tunnel-properties / destination ipv4 unicast 1.2.3.4
                # configure / mpls traffic-eng / gmpls optical-uni / controller CoherentDSP 0/1/0/0 / tunnel-properties / logging events lsp-status state
                # configure / mpls traffic-eng / gmpls optical-uni / controller CoherentDSP 0/1/0/0 / tunnel-properties / path-option 1 explicit identifier 1 lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller CoherentDSP 0/1/0/0 / tunnel-properties / path-option 1 explicit identifier 1 signaled-label dwdm wavelength 1 lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller CoherentDSP 0/1/0/0 / tunnel-properties / path-option 1 explicit identifier 1 signaled-label dwdm wavelength 1 xro-attribute-set someword lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller CoherentDSP 0/1/0/0 / tunnel-properties / path-option 1 explicit identifier 1 xro-attribute-set someword lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller CoherentDSP 0/1/0/0 / tunnel-properties / path-option 1 explicit name someword lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller CoherentDSP 0/1/0/0 / tunnel-properties / path-option 1 explicit name someword signaled-label dwdm wavelength 1 lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller CoherentDSP 0/1/0/0 / tunnel-properties / path-option 1 explicit name someword signaled-label dwdm wavelength 1 xro-attribute-set someword2 lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller CoherentDSP 0/1/0/0 / tunnel-properties / path-option 1 explicit name someword xro-attribute-set someword2 lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller CoherentDSP 0/1/0/0 / tunnel-properties / path-option 1 no-ero lockdown
                # configure / mpls traffic-eng / gmpls optical-uni / controller CoherentDSP 0/1/0/0 / tunnel-properties / path-option 1 no-ero signaled-label dwdm wavelength 1 lockdown
                # configure / mpls traffic-eng / gmpls optical-uni / controller CoherentDSP 0/1/0/0 / tunnel-properties / path-option 1 no-ero signaled-label dwdm wavelength 1 xro-attribute-set someword lockdown
                # configure / mpls traffic-eng / gmpls optical-uni / controller CoherentDSP 0/1/0/0 / tunnel-properties / path-option 1 no-ero xro-attribute-set someword lockdown
                # configure / mpls traffic-eng / gmpls optical-uni / controller CoherentDSP 0/1/0/0 / tunnel-properties / priority <0-7> <0-7>
                # configure / mpls traffic-eng / gmpls optical-uni / controller CoherentDSP 0/1/0/0 / tunnel-properties / record srlg
                # configure / mpls traffic-eng / gmpls optical-uni / controller CoherentDSP 0/1/0/0 / tunnel-properties / record-route
                # configure / mpls traffic-eng / gmpls optical-uni / controller CoherentDSP 0/1/0/0 / tunnel-properties / signalled-name someword
                # configure / mpls traffic-eng / gmpls optical-uni / controller CoherentDSP 0/1/0/0 / tunnel-properties / tunnel-id <0-65535>
                # configure / mpls traffic-eng / gmpls optical-uni / controller GigabitEthernet0/0/0/0 (config-te-gmpls-cntl)
                # configure / mpls traffic-eng / gmpls optical-uni / controller GigabitEthernet0/0/0/0 / announce srlgs
                # configure / mpls traffic-eng / gmpls optical-uni / controller GigabitEthernet0/0/0/0 / logging discovered-srlgs
                # configure / mpls traffic-eng / gmpls optical-uni / controller GigabitEthernet0/0/0/0 / tunnel-properties (config-te-gmpls-tun)
                # configure / mpls traffic-eng / gmpls optical-uni / controller GigabitEthernet0/0/0/0 / tunnel-properties / destination ipv4 unicast 1.2.3.4
                # configure / mpls traffic-eng / gmpls optical-uni / controller GigabitEthernet0/0/0/0 / tunnel-properties / logging events lsp-status state
                # configure / mpls traffic-eng / gmpls optical-uni / controller GigabitEthernet0/0/0/0 / tunnel-properties / path-option 1 explicit identifier 1 lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller GigabitEthernet0/0/0/0 / tunnel-properties / path-option 1 explicit identifier 1 signaled-label dwdm wavelength 1 lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller GigabitEthernet0/0/0/0 / tunnel-properties / path-option 1 explicit identifier 1 signaled-label dwdm wavelength 1 xro-attribute-set someword lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller GigabitEthernet0/0/0/0 / tunnel-properties / path-option 1 explicit identifier 1 xro-attribute-set someword lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller GigabitEthernet0/0/0/0 / tunnel-properties / path-option 1 explicit name someword lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller GigabitEthernet0/0/0/0 / tunnel-properties / path-option 1 explicit name someword signaled-label dwdm wavelength 1 lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller GigabitEthernet0/0/0/0 / tunnel-properties / path-option 1 explicit name someword signaled-label dwdm wavelength 1 xro-attribute-set someword2 lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller GigabitEthernet0/0/0/0 / tunnel-properties / path-option 1 explicit name someword xro-attribute-set someword2 lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller GigabitEthernet0/0/0/0 / tunnel-properties / path-option 1 no-ero lockdown
                # configure / mpls traffic-eng / gmpls optical-uni / controller GigabitEthernet0/0/0/0 / tunnel-properties / path-option 1 no-ero signaled-label dwdm wavelength 1 lockdown
                # configure / mpls traffic-eng / gmpls optical-uni / controller GigabitEthernet0/0/0/0 / tunnel-properties / path-option 1 no-ero signaled-label dwdm wavelength 1 xro-attribute-set someword lockdown
                # configure / mpls traffic-eng / gmpls optical-uni / controller GigabitEthernet0/0/0/0 / tunnel-properties / path-option 1 no-ero xro-attribute-set someword lockdown
                # configure / mpls traffic-eng / gmpls optical-uni / controller GigabitEthernet0/0/0/0 / tunnel-properties / priority <0-7> <0-7>
                # configure / mpls traffic-eng / gmpls optical-uni / controller GigabitEthernet0/0/0/0 / tunnel-properties / record srlg
                # configure / mpls traffic-eng / gmpls optical-uni / controller GigabitEthernet0/0/0/0 / tunnel-properties / record-route
                # configure / mpls traffic-eng / gmpls optical-uni / controller GigabitEthernet0/0/0/0 / tunnel-properties / signalled-name someword
                # configure / mpls traffic-eng / gmpls optical-uni / controller GigabitEthernet0/0/0/0 / tunnel-properties / tunnel-id <0-65535>
                # configure / mpls traffic-eng / gmpls optical-uni / controller ODUC2 0/1/0/0 (config-te-gmpls-cntl)
                # configure / mpls traffic-eng / gmpls optical-uni / controller ODUC2 0/1/0/0 / announce srlgs
                # configure / mpls traffic-eng / gmpls optical-uni / controller ODUC2 0/1/0/0 / logging discovered-srlgs
                # configure / mpls traffic-eng / gmpls optical-uni / controller ODUC2 0/1/0/0 / tunnel-properties (config-te-gmpls-tun)
                # configure / mpls traffic-eng / gmpls optical-uni / controller ODUC2 0/1/0/0 / tunnel-properties / destination ipv4 unicast 1.2.3.4
                # configure / mpls traffic-eng / gmpls optical-uni / controller ODUC2 0/1/0/0 / tunnel-properties / logging events lsp-status state
                # configure / mpls traffic-eng / gmpls optical-uni / controller ODUC2 0/1/0/0 / tunnel-properties / path-option 1 explicit identifier 1 lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller ODUC2 0/1/0/0 / tunnel-properties / path-option 1 explicit identifier 1 signaled-label dwdm wavelength 1 lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller ODUC2 0/1/0/0 / tunnel-properties / path-option 1 explicit identifier 1 signaled-label dwdm wavelength 1 xro-attribute-set someword lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller ODUC2 0/1/0/0 / tunnel-properties / path-option 1 explicit identifier 1 xro-attribute-set someword lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller ODUC2 0/1/0/0 / tunnel-properties / path-option 1 explicit name someword lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller ODUC2 0/1/0/0 / tunnel-properties / path-option 1 explicit name someword signaled-label dwdm wavelength 1 lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller ODUC2 0/1/0/0 / tunnel-properties / path-option 1 explicit name someword signaled-label dwdm wavelength 1 xro-attribute-set someword2 lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller ODUC2 0/1/0/0 / tunnel-properties / path-option 1 explicit name someword xro-attribute-set someword2 lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller ODUC2 0/1/0/0 / tunnel-properties / path-option 1 no-ero lockdown
                # configure / mpls traffic-eng / gmpls optical-uni / controller ODUC2 0/1/0/0 / tunnel-properties / path-option 1 no-ero signaled-label dwdm wavelength 1 lockdown
                # configure / mpls traffic-eng / gmpls optical-uni / controller ODUC2 0/1/0/0 / tunnel-properties / path-option 1 no-ero signaled-label dwdm wavelength 1 xro-attribute-set someword lockdown
                # configure / mpls traffic-eng / gmpls optical-uni / controller ODUC2 0/1/0/0 / tunnel-properties / path-option 1 no-ero xro-attribute-set someword lockdown
                # configure / mpls traffic-eng / gmpls optical-uni / controller ODUC2 0/1/0/0 / tunnel-properties / priority <0-7> <0-7>
                # configure / mpls traffic-eng / gmpls optical-uni / controller ODUC2 0/1/0/0 / tunnel-properties / record srlg
                # configure / mpls traffic-eng / gmpls optical-uni / controller ODUC2 0/1/0/0 / tunnel-properties / record-route
                # configure / mpls traffic-eng / gmpls optical-uni / controller ODUC2 0/1/0/0 / tunnel-properties / signalled-name someword
                # configure / mpls traffic-eng / gmpls optical-uni / controller ODUC2 0/1/0/0 / tunnel-properties / tunnel-id <0-65535>
                # configure / mpls traffic-eng / gmpls optical-uni / controller ODUC4 0/1/0/0 (config-te-gmpls-cntl)
                # configure / mpls traffic-eng / gmpls optical-uni / controller ODUC4 0/1/0/0 / announce srlgs
                # configure / mpls traffic-eng / gmpls optical-uni / controller ODUC4 0/1/0/0 / logging discovered-srlgs
                # configure / mpls traffic-eng / gmpls optical-uni / controller ODUC4 0/1/0/0 / tunnel-properties (config-te-gmpls-tun)
                # configure / mpls traffic-eng / gmpls optical-uni / controller ODUC4 0/1/0/0 / tunnel-properties / destination ipv4 unicast 1.2.3.4
                # configure / mpls traffic-eng / gmpls optical-uni / controller ODUC4 0/1/0/0 / tunnel-properties / logging events lsp-status state
                # configure / mpls traffic-eng / gmpls optical-uni / controller ODUC4 0/1/0/0 / tunnel-properties / path-option 1 explicit identifier 1 lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller ODUC4 0/1/0/0 / tunnel-properties / path-option 1 explicit identifier 1 signaled-label dwdm wavelength 1 lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller ODUC4 0/1/0/0 / tunnel-properties / path-option 1 explicit identifier 1 signaled-label dwdm wavelength 1 xro-attribute-set someword lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller ODUC4 0/1/0/0 / tunnel-properties / path-option 1 explicit identifier 1 xro-attribute-set someword lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller ODUC4 0/1/0/0 / tunnel-properties / path-option 1 explicit name someword lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller ODUC4 0/1/0/0 / tunnel-properties / path-option 1 explicit name someword signaled-label dwdm wavelength 1 lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller ODUC4 0/1/0/0 / tunnel-properties / path-option 1 explicit name someword signaled-label dwdm wavelength 1 xro-attribute-set someword2 lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller ODUC4 0/1/0/0 / tunnel-properties / path-option 1 explicit name someword xro-attribute-set someword2 lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller ODUC4 0/1/0/0 / tunnel-properties / path-option 1 no-ero lockdown
                # configure / mpls traffic-eng / gmpls optical-uni / controller ODUC4 0/1/0/0 / tunnel-properties / path-option 1 no-ero signaled-label dwdm wavelength 1 lockdown
                # configure / mpls traffic-eng / gmpls optical-uni / controller ODUC4 0/1/0/0 / tunnel-properties / path-option 1 no-ero signaled-label dwdm wavelength 1 xro-attribute-set someword lockdown
                # configure / mpls traffic-eng / gmpls optical-uni / controller ODUC4 0/1/0/0 / tunnel-properties / path-option 1 no-ero xro-attribute-set someword lockdown
                # configure / mpls traffic-eng / gmpls optical-uni / controller ODUC4 0/1/0/0 / tunnel-properties / priority <0-7> <0-7>
                # configure / mpls traffic-eng / gmpls optical-uni / controller ODUC4 0/1/0/0 / tunnel-properties / record srlg
                # configure / mpls traffic-eng / gmpls optical-uni / controller ODUC4 0/1/0/0 / tunnel-properties / record-route
                # configure / mpls traffic-eng / gmpls optical-uni / controller ODUC4 0/1/0/0 / tunnel-properties / signalled-name someword
                # configure / mpls traffic-eng / gmpls optical-uni / controller ODUC4 0/1/0/0 / tunnel-properties / tunnel-id <0-65535>
                # configure / mpls traffic-eng / gmpls optical-uni / controller OTUC2 0/1/0/0 (config-te-gmpls-cntl)
                # configure / mpls traffic-eng / gmpls optical-uni / controller OTUC2 0/1/0/0 / announce srlgs
                # configure / mpls traffic-eng / gmpls optical-uni / controller OTUC2 0/1/0/0 / logging discovered-srlgs
                # configure / mpls traffic-eng / gmpls optical-uni / controller OTUC2 0/1/0/0 / tunnel-properties (config-te-gmpls-tun)
                # configure / mpls traffic-eng / gmpls optical-uni / controller OTUC2 0/1/0/0 / tunnel-properties / destination ipv4 unicast 1.2.3.4
                # configure / mpls traffic-eng / gmpls optical-uni / controller OTUC2 0/1/0/0 / tunnel-properties / logging events lsp-status state
                # configure / mpls traffic-eng / gmpls optical-uni / controller OTUC2 0/1/0/0 / tunnel-properties / path-option 1 explicit identifier 1 lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller OTUC2 0/1/0/0 / tunnel-properties / path-option 1 explicit identifier 1 signaled-label dwdm wavelength 1 lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller OTUC2 0/1/0/0 / tunnel-properties / path-option 1 explicit identifier 1 signaled-label dwdm wavelength 1 xro-attribute-set someword lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller OTUC2 0/1/0/0 / tunnel-properties / path-option 1 explicit identifier 1 xro-attribute-set someword lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller OTUC2 0/1/0/0 / tunnel-properties / path-option 1 explicit name someword lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller OTUC2 0/1/0/0 / tunnel-properties / path-option 1 explicit name someword signaled-label dwdm wavelength 1 lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller OTUC2 0/1/0/0 / tunnel-properties / path-option 1 explicit name someword signaled-label dwdm wavelength 1 xro-attribute-set someword2 lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller OTUC2 0/1/0/0 / tunnel-properties / path-option 1 explicit name someword xro-attribute-set someword2 lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller OTUC2 0/1/0/0 / tunnel-properties / path-option 1 no-ero lockdown
                # configure / mpls traffic-eng / gmpls optical-uni / controller OTUC2 0/1/0/0 / tunnel-properties / path-option 1 no-ero signaled-label dwdm wavelength 1 lockdown
                # configure / mpls traffic-eng / gmpls optical-uni / controller OTUC2 0/1/0/0 / tunnel-properties / path-option 1 no-ero signaled-label dwdm wavelength 1 xro-attribute-set someword lockdown
                # configure / mpls traffic-eng / gmpls optical-uni / controller OTUC2 0/1/0/0 / tunnel-properties / path-option 1 no-ero xro-attribute-set someword lockdown
                # configure / mpls traffic-eng / gmpls optical-uni / controller OTUC2 0/1/0/0 / tunnel-properties / priority <0-7> <0-7>
                # configure / mpls traffic-eng / gmpls optical-uni / controller OTUC2 0/1/0/0 / tunnel-properties / record srlg
                # configure / mpls traffic-eng / gmpls optical-uni / controller OTUC2 0/1/0/0 / tunnel-properties / record-route
                # configure / mpls traffic-eng / gmpls optical-uni / controller OTUC2 0/1/0/0 / tunnel-properties / signalled-name someword
                # configure / mpls traffic-eng / gmpls optical-uni / controller OTUC2 0/1/0/0 / tunnel-properties / tunnel-id <0-65535>
                # configure / mpls traffic-eng / gmpls optical-uni / controller OTUC4 0/1/0/0 (config-te-gmpls-cntl)
                # configure / mpls traffic-eng / gmpls optical-uni / controller OTUC4 0/1/0/0 / announce srlgs
                # configure / mpls traffic-eng / gmpls optical-uni / controller OTUC4 0/1/0/0 / logging discovered-srlgs
                # configure / mpls traffic-eng / gmpls optical-uni / controller OTUC4 0/1/0/0 / tunnel-properties (config-te-gmpls-tun)
                # configure / mpls traffic-eng / gmpls optical-uni / controller OTUC4 0/1/0/0 / tunnel-properties / destination ipv4 unicast 1.2.3.4
                # configure / mpls traffic-eng / gmpls optical-uni / controller OTUC4 0/1/0/0 / tunnel-properties / logging events lsp-status state
                # configure / mpls traffic-eng / gmpls optical-uni / controller OTUC4 0/1/0/0 / tunnel-properties / path-option 1 explicit identifier 1 lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller OTUC4 0/1/0/0 / tunnel-properties / path-option 1 explicit identifier 1 signaled-label dwdm wavelength 1 lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller OTUC4 0/1/0/0 / tunnel-properties / path-option 1 explicit identifier 1 signaled-label dwdm wavelength 1 xro-attribute-set someword lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller OTUC4 0/1/0/0 / tunnel-properties / path-option 1 explicit identifier 1 xro-attribute-set someword lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller OTUC4 0/1/0/0 / tunnel-properties / path-option 1 explicit name someword lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller OTUC4 0/1/0/0 / tunnel-properties / path-option 1 explicit name someword signaled-label dwdm wavelength 1 lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller OTUC4 0/1/0/0 / tunnel-properties / path-option 1 explicit name someword signaled-label dwdm wavelength 1 xro-attribute-set someword2 lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller OTUC4 0/1/0/0 / tunnel-properties / path-option 1 explicit name someword xro-attribute-set someword2 lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller OTUC4 0/1/0/0 / tunnel-properties / path-option 1 no-ero lockdown
                # configure / mpls traffic-eng / gmpls optical-uni / controller OTUC4 0/1/0/0 / tunnel-properties / path-option 1 no-ero signaled-label dwdm wavelength 1 lockdown
                # configure / mpls traffic-eng / gmpls optical-uni / controller OTUC4 0/1/0/0 / tunnel-properties / path-option 1 no-ero signaled-label dwdm wavelength 1 xro-attribute-set someword lockdown
                # configure / mpls traffic-eng / gmpls optical-uni / controller OTUC4 0/1/0/0 / tunnel-properties / path-option 1 no-ero xro-attribute-set someword lockdown
                # configure / mpls traffic-eng / gmpls optical-uni / controller OTUC4 0/1/0/0 / tunnel-properties / priority <0-7> <0-7>
                # configure / mpls traffic-eng / gmpls optical-uni / controller OTUC4 0/1/0/0 / tunnel-properties / record srlg
                # configure / mpls traffic-eng / gmpls optical-uni / controller OTUC4 0/1/0/0 / tunnel-properties / record-route
                # configure / mpls traffic-eng / gmpls optical-uni / controller OTUC4 0/1/0/0 / tunnel-properties / signalled-name someword
                # configure / mpls traffic-eng / gmpls optical-uni / controller OTUC4 0/1/0/0 / tunnel-properties / tunnel-id <0-65535>
                # configure / mpls traffic-eng / gmpls optical-uni / controller Ots 0/1/0/0 (config-te-gmpls-cntl)
                # configure / mpls traffic-eng / gmpls optical-uni / controller Ots 0/1/0/0 / announce srlgs
                # configure / mpls traffic-eng / gmpls optical-uni / controller Ots 0/1/0/0 / logging discovered-srlgs
                # configure / mpls traffic-eng / gmpls optical-uni / controller Ots 0/1/0/0 / tunnel-properties (config-te-gmpls-tun)
                # configure / mpls traffic-eng / gmpls optical-uni / controller Ots 0/1/0/0 / tunnel-properties / destination ipv4 unicast 1.2.3.4
                # configure / mpls traffic-eng / gmpls optical-uni / controller Ots 0/1/0/0 / tunnel-properties / logging events lsp-status state
                # configure / mpls traffic-eng / gmpls optical-uni / controller Ots 0/1/0/0 / tunnel-properties / path-option 1 explicit identifier 1 lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller Ots 0/1/0/0 / tunnel-properties / path-option 1 explicit identifier 1 signaled-label dwdm wavelength 1 lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller Ots 0/1/0/0 / tunnel-properties / path-option 1 explicit identifier 1 signaled-label dwdm wavelength 1 xro-attribute-set someword lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller Ots 0/1/0/0 / tunnel-properties / path-option 1 explicit identifier 1 xro-attribute-set someword lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller Ots 0/1/0/0 / tunnel-properties / path-option 1 explicit name someword lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller Ots 0/1/0/0 / tunnel-properties / path-option 1 explicit name someword signaled-label dwdm wavelength 1 lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller Ots 0/1/0/0 / tunnel-properties / path-option 1 explicit name someword signaled-label dwdm wavelength 1 xro-attribute-set someword2 lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller Ots 0/1/0/0 / tunnel-properties / path-option 1 explicit name someword xro-attribute-set someword2 lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller Ots 0/1/0/0 / tunnel-properties / path-option 1 no-ero lockdown
                # configure / mpls traffic-eng / gmpls optical-uni / controller Ots 0/1/0/0 / tunnel-properties / path-option 1 no-ero signaled-label dwdm wavelength 1 lockdown
                # configure / mpls traffic-eng / gmpls optical-uni / controller Ots 0/1/0/0 / tunnel-properties / path-option 1 no-ero signaled-label dwdm wavelength 1 xro-attribute-set someword lockdown
                # configure / mpls traffic-eng / gmpls optical-uni / controller Ots 0/1/0/0 / tunnel-properties / path-option 1 no-ero xro-attribute-set someword lockdown
                # configure / mpls traffic-eng / gmpls optical-uni / controller Ots 0/1/0/0 / tunnel-properties / priority <0-7> <0-7>
                # configure / mpls traffic-eng / gmpls optical-uni / controller Ots 0/1/0/0 / tunnel-properties / record srlg
                # configure / mpls traffic-eng / gmpls optical-uni / controller Ots 0/1/0/0 / tunnel-properties / record-route
                # configure / mpls traffic-eng / gmpls optical-uni / controller Ots 0/1/0/0 / tunnel-properties / signalled-name someword
                # configure / mpls traffic-eng / gmpls optical-uni / controller Ots 0/1/0/0 / tunnel-properties / tunnel-id <0-65535>
                # configure / mpls traffic-eng / gmpls optical-uni / controller Ots-Och 0/1/0/0 (config-te-gmpls-cntl)
                # configure / mpls traffic-eng / gmpls optical-uni / controller Ots-Och 0/1/0/0 / announce srlgs
                # configure / mpls traffic-eng / gmpls optical-uni / controller Ots-Och 0/1/0/0 / logging discovered-srlgs
                # configure / mpls traffic-eng / gmpls optical-uni / controller Ots-Och 0/1/0/0 / tunnel-properties (config-te-gmpls-tun)
                # configure / mpls traffic-eng / gmpls optical-uni / controller Ots-Och 0/1/0/0 / tunnel-properties / destination ipv4 unicast 1.2.3.4
                # configure / mpls traffic-eng / gmpls optical-uni / controller Ots-Och 0/1/0/0 / tunnel-properties / logging events lsp-status state
                # configure / mpls traffic-eng / gmpls optical-uni / controller Ots-Och 0/1/0/0 / tunnel-properties / path-option 1 explicit identifier 1 lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller Ots-Och 0/1/0/0 / tunnel-properties / path-option 1 explicit identifier 1 signaled-label dwdm wavelength 1 lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller Ots-Och 0/1/0/0 / tunnel-properties / path-option 1 explicit identifier 1 signaled-label dwdm wavelength 1 xro-attribute-set someword lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller Ots-Och 0/1/0/0 / tunnel-properties / path-option 1 explicit identifier 1 xro-attribute-set someword lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller Ots-Och 0/1/0/0 / tunnel-properties / path-option 1 explicit name someword lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller Ots-Och 0/1/0/0 / tunnel-properties / path-option 1 explicit name someword signaled-label dwdm wavelength 1 lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller Ots-Och 0/1/0/0 / tunnel-properties / path-option 1 explicit name someword signaled-label dwdm wavelength 1 xro-attribute-set someword2 lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller Ots-Och 0/1/0/0 / tunnel-properties / path-option 1 explicit name someword xro-attribute-set someword2 lockdown verbatim
                # configure / mpls traffic-eng / gmpls optical-uni / controller Ots-Och 0/1/0/0 / tunnel-properties / path-option 1 no-ero lockdown
                # configure / mpls traffic-eng / gmpls optical-uni / controller Ots-Och 0/1/0/0 / tunnel-properties / path-option 1 no-ero signaled-label dwdm wavelength 1 lockdown
                # configure / mpls traffic-eng / gmpls optical-uni / controller Ots-Och 0/1/0/0 / tunnel-properties / path-option 1 no-ero signaled-label dwdm wavelength 1 xro-attribute-set someword lockdown
                # configure / mpls traffic-eng / gmpls optical-uni / controller Ots-Och 0/1/0/0 / tunnel-properties / path-option 1 no-ero xro-attribute-set someword lockdown
                # configure / mpls traffic-eng / gmpls optical-uni / controller Ots-Och 0/1/0/0 / tunnel-properties / priority <0-7> <0-7>
                # configure / mpls traffic-eng / gmpls optical-uni / controller Ots-Och 0/1/0/0 / tunnel-properties / record srlg
                # configure / mpls traffic-eng / gmpls optical-uni / controller Ots-Och 0/1/0/0 / tunnel-properties / record-route
                # configure / mpls traffic-eng / gmpls optical-uni / controller Ots-Och 0/1/0/0 / tunnel-properties / signalled-name someword
                # configure / mpls traffic-eng / gmpls optical-uni / controller Ots-Och 0/1/0/0 / tunnel-properties / tunnel-id <0-65535>

                # PER AREA PER CONTROLLER
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> (config-te-gmpls-nni-ti)
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller Loopback0 (config-te-gmpls-nni-ti-cntl)
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller Loopback0 / admin-weight <0-65535>
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller Loopback0 / delay 1
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller Loopback0 / tti-mode odu-pm
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller Loopback0 / tti-mode odu-tcm 1
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller Loopback0 / tti-mode otu-sm
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller CoherentDSP 0/1/0/0 (config-te-gmpls-nni-ti-cntl)
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller CoherentDSP 0/1/0/0 / admin-weight <0-65535>
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller CoherentDSP 0/1/0/0 / delay 1
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller CoherentDSP 0/1/0/0 / tti-mode odu-pm
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller CoherentDSP 0/1/0/0 / tti-mode odu-tcm 1
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller CoherentDSP 0/1/0/0 / tti-mode otu-sm
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller GigabitEthernet0/0/0/0 (config-te-gmpls-nni-ti-cntl)
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller GigabitEthernet0/0/0/0 / admin-weight <0-65535>
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller GigabitEthernet0/0/0/0 / delay 1
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller GigabitEthernet0/0/0/0 / tti-mode odu-pm
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller GigabitEthernet0/0/0/0 / tti-mode odu-tcm 1
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller GigabitEthernet0/0/0/0 / tti-mode otu-sm
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller ODUC2 0/1/0/0 (config-te-gmpls-nni)
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller ODUC2 0/1/0/0 / admin-weight <0-65535>
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller ODUC2 0/1/0/0 / delay 1
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller ODUC2 0/1/0/0 / tti-mode odu-pm
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller ODUC2 0/1/0/0 / tti-mode odu-tcm 1
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller ODUC2 0/1/0/0 / tti-mode otu-sm
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller ODUC4 0/1/0/0 (config-mpls-te)
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller ODUC4 0/1/0/0 / admin-weight <0-65535>
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller ODUC4 0/1/0/0 / delay 1
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller ODUC4 0/1/0/0 / tti-mode odu-pm
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller ODUC4 0/1/0/0 / tti-mode odu-tcm 1
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller ODUC4 0/1/0/0 / tti-mode otu-sm
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller OTUC2 0/1/0/0 (config-mpls-te)
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller OTUC2 0/1/0/0 / admin-weight <0-65535>
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller OTUC2 0/1/0/0 / delay 1
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller OTUC2 0/1/0/0 / tti-mode odu-pm
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller OTUC2 0/1/0/0 / tti-mode odu-tcm 1
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller OTUC2 0/1/0/0 / tti-mode otu-sm
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller OTUC4 0/1/0/0 (config-mpls-te)
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller OTUC4 0/1/0/0 / admin-weight <0-65535>
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller OTUC4 0/1/0/0 / delay 1
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller OTUC4 0/1/0/0 / tti-mode odu-pm
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller OTUC4 0/1/0/0 / tti-mode odu-tcm 1
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller OTUC4 0/1/0/0 / tti-mode otu-sm
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller Ots 0/1/0/0 (config-mpls-te)
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller Ots 0/1/0/0 / admin-weight <0-65535>
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller Ots 0/1/0/0 / delay 1
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller Ots 0/1/0/0 / tti-mode odu-pm
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller Ots 0/1/0/0 / tti-mode odu-tcm 1
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller Ots 0/1/0/0 / tti-mode otu-sm
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller Ots-Och 0/1/0/0 (config-mpls-te)
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller Ots-Och 0/1/0/0 / admin-weight <0-65535>
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller Ots-Och 0/1/0/0 / delay 1
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller Ots-Och 0/1/0/0 / tti-mode odu-pm
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller Ots-Och 0/1/0/0 / tti-mode odu-tcm 1
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area <0-4294967295> / controller Ots-Och 0/1/0/0 / tti-mode otu-sm
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 (config-te-gmpls-nni-ti)
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller Loopback0 (config-te-gmpls-nni-ti-cntl)
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller Loopback0 / admin-weight <0-65535>
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller Loopback0 / delay 1
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller Loopback0 / tti-mode odu-pm
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller Loopback0 / tti-mode odu-tcm 1
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller Loopback0 / tti-mode otu-sm
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller CoherentDSP 0/1/0/0 (config-mpls-te)
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller CoherentDSP 0/1/0/0 / admin-weight <0-65535>
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller CoherentDSP 0/1/0/0 / delay 1
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller CoherentDSP 0/1/0/0 / tti-mode odu-pm
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller CoherentDSP 0/1/0/0 / tti-mode odu-tcm 1
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller CoherentDSP 0/1/0/0 / tti-mode otu-sm
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller GigabitEthernet0/0/0/0 (config-te-gmpls-nni-ti-cntl)
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller GigabitEthernet0/0/0/0 / admin-weight <0-65535>
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller GigabitEthernet0/0/0/0 / delay 1
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller GigabitEthernet0/0/0/0 / tti-mode odu-pm
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller GigabitEthernet0/0/0/0 / tti-mode odu-tcm 1
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller GigabitEthernet0/0/0/0 / tti-mode otu-sm
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller ODUC2 0/1/0/0 (config-mpls-te)
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller ODUC2 0/1/0/0 / admin-weight <0-65535>
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller ODUC2 0/1/0/0 / delay 1
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller ODUC2 0/1/0/0 / tti-mode odu-pm
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller ODUC2 0/1/0/0 / tti-mode odu-tcm 1
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller ODUC2 0/1/0/0 / tti-mode otu-sm
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller ODUC4 0/1/0/0 (config-mpls-te)
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller ODUC4 0/1/0/0 / admin-weight <0-65535>
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller ODUC4 0/1/0/0 / delay 1
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller ODUC4 0/1/0/0 / tti-mode odu-pm
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller ODUC4 0/1/0/0 / tti-mode odu-tcm 1
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller ODUC4 0/1/0/0 / tti-mode otu-sm
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller OTUC2 0/1/0/0 (config-mpls-te)
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller OTUC2 0/1/0/0 / admin-weight <0-65535>
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller OTUC2 0/1/0/0 / delay 1
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller OTUC2 0/1/0/0 / tti-mode odu-pm
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller OTUC2 0/1/0/0 / tti-mode odu-tcm 1
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller OTUC2 0/1/0/0 / tti-mode otu-sm
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller OTUC4 0/1/0/0 (config-mpls-te)
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller OTUC4 0/1/0/0 / admin-weight <0-65535>
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller OTUC4 0/1/0/0 / delay 1
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller OTUC4 0/1/0/0 / tti-mode odu-pm
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller OTUC4 0/1/0/0 / tti-mode odu-tcm 1
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller OTUC4 0/1/0/0 / tti-mode otu-sm
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller Ots 0/1/0/0 (config-mpls-te)
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller Ots 0/1/0/0 / admin-weight <0-65535>
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller Ots 0/1/0/0 / delay 1
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller Ots 0/1/0/0 / tti-mode odu-pm
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller Ots 0/1/0/0 / tti-mode odu-tcm 1
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller Ots 0/1/0/0 / tti-mode otu-sm
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller Ots-Och 0/1/0/0 (config-mpls-te)
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller Ots-Och 0/1/0/0 / admin-weight <0-65535>
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller Ots-Och 0/1/0/0 / delay 1
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller Ots-Och 0/1/0/0 / tti-mode odu-pm
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller Ots-Och 0/1/0/0 / tti-mode odu-tcm 1
                # configure / mpls traffic-eng / gmpls optical-nni / topology instance ospf someword area 1.2.3.4 / controller Ots-Och 0/1/0/0 / tti-mode otu-sm

                # PER-AUTO TUNNEL MESH GROUP
                # configure / mpls traffic-eng / auto-tunnel mesh / group <0-4294967295> (config-te-mesh-group)
                # configure / mpls traffic-eng / auto-tunnel mesh / group <0-4294967295> / attribute-set someword
                # configure / mpls traffic-eng / auto-tunnel mesh / group <0-4294967295> / destination-list someword
                # configure / mpls traffic-eng / auto-tunnel mesh / group <0-4294967295> / disable
                # configure / mpls traffic-eng / auto-tunnel mesh / group <0-4294967295> / onehop
                # configure / mpls traffic-eng / auto-tunnel mesh / timers removal unused <0-10080>
                
                # Add per-interface config
                for sub, attributes2 in attributes.mapping_values('interface_attr', keys=self.interfaces, sort=True):
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

                with configurations.submode_context(attributes.format('interface {interface_name}', force=True)):
                    # configure / mpls traffic-eng / interface Loopback0 / auto-tunnel backup / attribute-set someword
                    configurations.append_line(attributes.format('auto-tunnel backup attribute-set {auto_tun_backup_attr_set}'))
                    
                    # configure / mpls traffic-eng / interface Loopback0 / auto-tunnel backup / exclude srlg
                    # configure / mpls traffic-eng / interface Loopback0 / auto-tunnel backup / exclude srlg preferred
                    # configure / mpls traffic-eng / interface Loopback0 / auto-tunnel backup / exclude srlg weighted
                    #   only one of these three can be set at one time, so one attribute used
                    if attributes.value('auto_tun_backup_exclude_srlg'):
                        v = attributes.value('auto_tun_backup_exclude_srlg_type')
                        if re.search('preferred|weighted', str(v)):
                            configurations.append_line(attributes.format('auto-tunnel backup exclude srlg {auto_tun_backup_exclude_srlg_type}'))
                        else:
                            # auto_tun_backup_exclude_srlg is "True"
                            configurations.append_line(attributes.format('auto-tunnel backup exclude srlg'))
                                            
                    # configure / mpls traffic-eng / interface Loopback0 / auto-tunnel backup / nhop-only
                    if attributes.value('auto_tun_backup_nhop_only'):
                        configurations.append_line('auto-tunnel backup nhop-only')


                    # configure / mpls traffic-eng / interface Loopback0 / admin-weight <0-4294967295>
                    # configure / mpls traffic-eng / interface Loopback0 / attribute-flags 0x0
                    # configure / mpls traffic-eng / interface Loopback0 / attribute-names index 1 someword
                    # configure / mpls traffic-eng / interface Loopback0 / attribute-names index 1 someword someword2
                    # configure / mpls traffic-eng / interface Loopback0 / attribute-names index 1 someword someword2 someword3
                    # configure / mpls traffic-eng / interface Loopback0 / attribute-names index 1 someword someword2 someword3 someword4
                    # configure / mpls traffic-eng / interface Loopback0 / attribute-names index 1 someword someword2 someword3 someword4 someword5
                    # configure / mpls traffic-eng / interface Loopback0 / attribute-names index 1 someword someword2 someword3 someword4 someword5 someword6
                    # configure / mpls traffic-eng / interface Loopback0 / attribute-names index 1 someword someword2 someword3 someword4 someword5 someword6 someword7
                    # configure / mpls traffic-eng / interface Loopback0 / attribute-names index 1 someword someword2 someword3 someword4 someword5 someword6 someword7 someword8
                    # configure / mpls traffic-eng / interface Loopback0 / attribute-names someword
                    # configure / mpls traffic-eng / interface Loopback0 / attribute-names someword someword2
                    # configure / mpls traffic-eng / interface Loopback0 / attribute-names someword someword2 someword3
                    # configure / mpls traffic-eng / interface Loopback0 / attribute-names someword someword2 someword3 someword4
                    # configure / mpls traffic-eng / interface Loopback0 / attribute-names someword someword2 someword3 someword4 someword5
                    # configure / mpls traffic-eng / interface Loopback0 / attribute-names someword someword2 someword3 someword4 someword5 someword6
                    # configure / mpls traffic-eng / interface Loopback0 / attribute-names someword someword2 someword3 someword4 someword5 someword6 someword7
                    # configure / mpls traffic-eng / interface Loopback0 / attribute-names someword someword2 someword3 someword4 someword5 someword6 someword7 someword8
                    # configure / mpls traffic-eng / interface Loopback0 / attribute-names someword someword2 someword3 someword4 someword5 someword6 someword7 someword8 someword9
                    # configure / mpls traffic-eng / interface Loopback0 / attribute-names someword someword2 someword3 someword4 someword5 someword6 someword7 someword8 someword9 someword10
                    # configure / mpls traffic-eng / interface Loopback0 / bfd fast-detect
                    # configure / mpls traffic-eng / interface Loopback0 / fault-oam lockout
                    # configure / mpls traffic-eng / interface Loopback0 / flooding thresholds down <0-100>
                    # configure / mpls traffic-eng / interface Loopback0 / flooding thresholds down <0-100> <0-100>
                    # configure / mpls traffic-eng / interface Loopback0 / flooding thresholds down <0-100> <0-100> <0-100>
                    # configure / mpls traffic-eng / interface Loopback0 / flooding thresholds down <0-100> <0-100> <0-100> <0-100>
                    # configure / mpls traffic-eng / interface Loopback0 / flooding thresholds down <0-100> <0-100> <0-100> <0-100> <0-100>
                    # configure / mpls traffic-eng / interface Loopback0 / flooding thresholds down <0-100> <0-100> <0-100> <0-100> <0-100> <0-100>
                    # configure / mpls traffic-eng / interface Loopback0 / flooding thresholds down <0-100> <0-100> <0-100> <0-100> <0-100> <0-100> <0-100>
                    # configure / mpls traffic-eng / interface Loopback0 / flooding thresholds down <0-100> <0-100> <0-100> <0-100> <0-100> <0-100> <0-100> <0-100>
                    # configure / mpls traffic-eng / interface Loopback0 / flooding thresholds up <0-100>
                    # configure / mpls traffic-eng / interface Loopback0 / flooding thresholds up <0-100> <0-100>
                    # configure / mpls traffic-eng / interface Loopback0 / flooding thresholds up <0-100> <0-100> <0-100>
                    # configure / mpls traffic-eng / interface Loopback0 / flooding thresholds up <0-100> <0-100> <0-100> <0-100>
                    # configure / mpls traffic-eng / interface Loopback0 / flooding thresholds up <0-100> <0-100> <0-100> <0-100> <0-100>
                    # configure / mpls traffic-eng / interface Loopback0 / flooding thresholds up <0-100> <0-100> <0-100> <0-100> <0-100> <0-100>
                    # configure / mpls traffic-eng / interface Loopback0 / flooding thresholds up <0-100> <0-100> <0-100> <0-100> <0-100> <0-100> <0-100>
                    # configure / mpls traffic-eng / interface Loopback0 / flooding thresholds up <0-100> <0-100> <0-100> <0-100> <0-100> <0-100> <0-100> <0-100>
                    # configure / mpls traffic-eng / interface Loopback0 / flooding thresholds up <0-100> <0-100> <0-100> <0-100> <0-100> <0-100> <0-100> <0-100> <0-100>
                    # configure / mpls traffic-eng / interface Loopback0 / flooding thresholds up <0-100> <0-100> <0-100> <0-100> <0-100> <0-100> <0-100> <0-100> <0-100> <0-100>
                    # configure / mpls traffic-eng / interface Loopback0 / flooding thresholds up <0-100> <0-100> <0-100> <0-100> <0-100> <0-100> <0-100> <0-100> <0-100> <0-100> <0-100>
                    # configure / mpls traffic-eng / interface Loopback0 / flooding thresholds up <0-100> <0-100> <0-100> <0-100> <0-100> <0-100> <0-100> <0-100> <0-100> <0-100> <0-100> <0-100>
                    # configure / mpls traffic-eng / interface Loopback0 / flooding thresholds up <0-100> <0-100> <0-100> <0-100> <0-100> <0-100> <0-100> <0-100> <0-100> <0-100> <0-100> <0-100> <0-100>
                    # configure / mpls traffic-eng / interface Loopback0 / flooding thresholds up <0-100> <0-100> <0-100> <0-100> <0-100> <0-100> <0-100> <0-100> <0-100> <0-100> <0-100> <0-100> <0-100> <0-100>
                    # configure / mpls traffic-eng / interface Loopback0 / tp link 1
                    # configure / mpls traffic-eng / interface Loopback0 / tp link 1 next-hop ipv4 1.2.3.4
                    
                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)


class Srlg(ABC):

    class DeviceAttributes(ABC):

        def build_config(self, apply=True, attributes=None, unconfig=False):
            assert not apply
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            # iosxr: srlg (config-srlg)
            with configurations.submode_context(attributes.format('srlg', force=True)):
                if unconfig and attributes.iswildcard:
                    configurations.submode_unconfig()

                # iosxr: srlg / name someword value <0-4294967295>
                dic = attributes.value('name_value_dict')
                for key in sorted(dic.keys()):
                    configurations.append_line('name {key} value {val}'.format(key=key, val=dic[key]))                  

                # iosxr: evpn /  interface PTP0/RSP0/CPU0/0 (config-srlg-if)
                for sub, attributes2 in attributes.mapping_values('interface_attr', sort=True):
                    configurations.append_block(sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

            return CliConfig(device=self.device, unconfig=unconfig,
                             cli_config=configurations)

        def build_unconfig(self, apply=True, attributes=None):
            return self.build_config(apply=apply, attributes=attributes, unconfig=True)

        class InterfaceAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False):
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)
        
                # iosxr: srlg / interface PTP0/RSP0/CPU0/0 (config-srlg-if)
                with configurations.submode_context(attributes.format('interface {interface_name}', force=True)):
                    if unconfig and attributes.iswildcard:
                        configurations.submode_unconfig()

                    # iosxr: evpn  / interface PTP0/RSP0/CPU0/0 / name someword
                    configurations.append_line(attributes.format('name {intf_name}'))

                    # configure / srlg / interface PTP0/RSP0/CPU0/0 / 1 value <0-4294967295>
                    # configure / srlg / interface PTP0/RSP0/CPU0/0 / 1 value <0-4294967295> priority critical
                    # configure / srlg / interface PTP0/RSP0/CPU0/0 / 1 value <0-4294967295> priority high
                    # configure / srlg / interface PTP0/RSP0/CPU0/0 / 1 value <0-4294967295> priority low
                    # configure / srlg / interface PTP0/RSP0/CPU0/0 / 1 value <0-4294967295> priority verylow
                    # configure / srlg / interface PTP0/RSP0/CPU0/0 / group (config-srlg-if-group)
                    # configure / srlg / interface PTP0/RSP0/CPU0/0 / group / 1 someword
                    # configure / srlg / interface PTP0/RSP0/CPU0/0 / include-optical (config-srlg-if-optical)
                    # configure / srlg / interface PTP0/RSP0/CPU0/0 / include-optical / priority critical
                    # configure / srlg / interface PTP0/RSP0/CPU0/0 / include-optical / priority high
                    # configure / srlg / interface PTP0/RSP0/CPU0/0 / include-optical / priority low
                    # configure / srlg / interface PTP0/RSP0/CPU0/0 / include-optical / priority verylow
                    # configure / srlg / interface PTP0/RSP0/CPU0/0 / value <0-4294967295>
                    # configure / srlg / interface PTP0/RSP0/CPU0/0 / value <0-4294967295> priority critical
                    # configure / srlg / interface PTP0/RSP0/CPU0/0 / value <0-4294967295> priority high
                    # configure / srlg / interface PTP0/RSP0/CPU0/0 / value <0-4294967295> priority low
                    # configure / srlg / interface PTP0/RSP0/CPU0/0 / value <0-4294967295> priority verylow

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None):
                return self.build_config(apply=apply, attributes=attributes, unconfig=True)

