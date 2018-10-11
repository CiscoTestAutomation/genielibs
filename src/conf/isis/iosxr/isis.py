from abc import ABC
import warnings

from genie.conf.base.attributes import UnsupportedAttributeWarning,\
    AttributesHelper
from genie.conf.base.cli import CliConfigBuilder
from ..isis import Isis as _Isis
from genie.conf.base.config import CliConfig


class Isis(ABC):

    class DeviceAttributes(ABC):

        def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            # iosxr: router isis 100 (config-isis)
            with configurations.submode_context(attributes.format('router isis {pid}', force=True)):
                if unconfig and attributes.iswildcard:
                    configurations.submode_unconfig()

                # iosxr: router isis 100 / distribute bgp-ls
                # iosxr: router isis 100 / distribute bgp-ls instance-id 2
                # iosxr: router isis 100 / distribute bgp-ls instance-id 2 level 1
                # iosxr: router isis 100 / distribute bgp-ls instance-id 2 level 1 throttle 5
                # iosxr: router isis 100 / distribute bgp-ls instance-id 2 throttle 5
                # iosxr: router isis 100 / distribute bgp-ls level 1
                # iosxr: router isis 100 / distribute bgp-ls level 1 throttle 5
                # iosxr: router isis 100 / distribute bgp-ls throttle 5
                # iosxr: router isis 100 / hostname dynamic disable
                # iosxr: router isis 100 / ignore-lsp-errors disable

                # iosxr: router isis 100 / is-type level-1
                # iosxr: router isis 100 / is-type level-1-2
                # iosxr: router isis 100 / is-type level-2-only
                configurations.append_line(attributes.format('is-type {is_type}', transform={
                    _Isis.IsType.level_1: 'level-1',
                    _Isis.IsType.level_1_2: 'level-1-2',
                    _Isis.IsType.level_2: 'level-2-only',
                }))

                # iosxr: router isis 100 / link-group someword (config-isis-link-group)
                # iosxr: router isis 100 / link-group someword / metric-offset 1
                # iosxr: router isis 100 / link-group someword / metric-offset maximum
                # iosxr: router isis 100 / link-group someword / minimum-members 2
                # iosxr: router isis 100 / link-group someword / revert-members 2
                # iosxr: router isis 100 / log adjacency changes
                # iosxr: router isis 100 / log pdu drops
                # iosxr: router isis 100 / lsp-check-interval 10
                # iosxr: router isis 100 / lsp-check-interval 10 level 1
                # iosxr: router isis 100 / lsp-gen-interval initial-wait <0-120000>
                # iosxr: router isis 100 / lsp-gen-interval initial-wait <0-120000> level 1
                # iosxr: router isis 100 / lsp-gen-interval initial-wait <0-120000> maximum-wait <0-120000>
                # iosxr: router isis 100 / lsp-gen-interval initial-wait <0-120000> maximum-wait <0-120000> level 1
                # iosxr: router isis 100 / lsp-gen-interval initial-wait <0-120000> maximum-wait <0-120000> secondary-wait <0-120000>
                # iosxr: router isis 100 / lsp-gen-interval initial-wait <0-120000> maximum-wait <0-120000> secondary-wait <0-120000> level 1
                # iosxr: router isis 100 / lsp-gen-interval initial-wait <0-120000> secondary-wait <0-120000>
                # iosxr: router isis 100 / lsp-gen-interval initial-wait <0-120000> secondary-wait <0-120000> level 1
                # iosxr: router isis 100 / lsp-gen-interval maximum-wait <0-120000>
                # iosxr: router isis 100 / lsp-gen-interval maximum-wait <0-120000> level 1
                # iosxr: router isis 100 / lsp-gen-interval maximum-wait <0-120000> secondary-wait <0-120000>
                # iosxr: router isis 100 / lsp-gen-interval maximum-wait <0-120000> secondary-wait <0-120000> level 1
                # iosxr: router isis 100 / lsp-gen-interval secondary-wait <0-120000>
                # iosxr: router isis 100 / lsp-gen-interval secondary-wait <0-120000> level 1
               
                # iosxr: router isis 100 / lsp-mtu 128
                configurations.append_line(attributes.format('lsp-mtu {lsp_mtu}'))
                
                # iosxr: router isis 100 / lsp-mtu 128 level 1
                # iosxr: router isis 100 / lsp-password accept cisco
                # iosxr: router isis 100 / lsp-password accept cisco level 1
                # iosxr: router isis 100 / lsp-password accept clear cisco
                # iosxr: router isis 100 / lsp-password accept clear cisco level 1
                # iosxr: router isis 100 / lsp-password accept encrypted 060506324F41
                # iosxr: router isis 100 / lsp-password accept encrypted 060506324F41 level 1
                # iosxr: router isis 100 / lsp-password cisco
                # iosxr: router isis 100 / lsp-password cisco level 1
                # iosxr: router isis 100 / lsp-password cisco level 1 send-only
                # iosxr: router isis 100 / lsp-password cisco level 1 send-only snp send-only
                # iosxr: router isis 100 / lsp-password cisco send-only
                # iosxr: router isis 100 / lsp-password cisco send-only snp send-only
                # iosxr: router isis 100 / lsp-password clear cisco
                # iosxr: router isis 100 / lsp-password clear cisco level 1
                # iosxr: router isis 100 / lsp-password clear cisco level 1 send-only
                # iosxr: router isis 100 / lsp-password clear cisco level 1 send-only snp send-only
                # iosxr: router isis 100 / lsp-password clear cisco send-only
                # iosxr: router isis 100 / lsp-password clear cisco send-only snp send-only
                # iosxr: router isis 100 / lsp-password encrypted 060506324F41
                # iosxr: router isis 100 / lsp-password encrypted 060506324F41 level 1
                # iosxr: router isis 100 / lsp-password encrypted 060506324F41 level 1 send-only
                # iosxr: router isis 100 / lsp-password encrypted 060506324F41 level 1 send-only snp send-only
                # iosxr: router isis 100 / lsp-password encrypted 060506324F41 send-only
                # iosxr: router isis 100 / lsp-password encrypted 060506324F41 send-only snp send-only
                # iosxr: router isis 100 / lsp-password hmac-md5 cisco
                # iosxr: router isis 100 / lsp-password hmac-md5 cisco level 1
                # iosxr: router isis 100 / lsp-password hmac-md5 cisco level 1 send-only
                # iosxr: router isis 100 / lsp-password hmac-md5 cisco send-only
                # iosxr: router isis 100 / lsp-password hmac-md5 clear cisco
                # iosxr: router isis 100 / lsp-password hmac-md5 clear cisco level 1
                # iosxr: router isis 100 / lsp-password hmac-md5 clear cisco level 1 send-only
                # iosxr: router isis 100 / lsp-password hmac-md5 clear cisco send-only
                # iosxr: router isis 100 / lsp-password hmac-md5 encrypted 060506324F41
                # iosxr: router isis 100 / lsp-password hmac-md5 encrypted 060506324F41 level 1
                # iosxr: router isis 100 / lsp-password hmac-md5 encrypted 060506324F41 level 1 send-only
                # iosxr: router isis 100 / lsp-password hmac-md5 encrypted 060506324F41 send-only
                # iosxr: router isis 100 / lsp-password keychain cisco
                # iosxr: router isis 100 / lsp-password keychain cisco level 1
                # iosxr: router isis 100 / lsp-password keychain cisco level 1 send-only
                # iosxr: router isis 100 / lsp-password keychain cisco send-only
                # iosxr: router isis 100 / lsp-password text cisco
                # iosxr: router isis 100 / lsp-password text cisco level 1
                # iosxr: router isis 100 / lsp-password text cisco level 1 send-only
                # iosxr: router isis 100 / lsp-password text cisco level 1 send-only snp send-only
                # iosxr: router isis 100 / lsp-password text cisco send-only
                # iosxr: router isis 100 / lsp-password text cisco send-only snp send-only
                # iosxr: router isis 100 / lsp-password text clear cisco
                # iosxr: router isis 100 / lsp-password text clear cisco level 1
                # iosxr: router isis 100 / lsp-password text clear cisco level 1 send-only
                # iosxr: router isis 100 / lsp-password text clear cisco level 1 send-only snp send-only
                # iosxr: router isis 100 / lsp-password text clear cisco send-only
                # iosxr: router isis 100 / lsp-password text clear cisco send-only snp send-only
                # iosxr: router isis 100 / lsp-password text encrypted 060506324F41
                # iosxr: router isis 100 / lsp-password text encrypted 060506324F41 level 1
                # iosxr: router isis 100 / lsp-password text encrypted 060506324F41 level 1 send-only
                # iosxr: router isis 100 / lsp-password text encrypted 060506324F41 level 1 send-only snp send-only
                # iosxr: router isis 100 / lsp-password text encrypted 060506324F41 send-only
                # iosxr: router isis 100 / lsp-password text encrypted 060506324F41 send-only snp send-only
                # iosxr: router isis 100 / lsp-refresh-interval 1
                # iosxr: router isis 100 / lsp-refresh-interval 1 level 1
                # iosxr: router isis 100 / max-link-metric
                # iosxr: router isis 100 / max-link-metric level 1
                # iosxr: router isis 100 / max-lsp-lifetime 1
                # iosxr: router isis 100 / max-lsp-lifetime 1 level 1
                # iosxr: router isis 100 / min-lsp-arrivaltime initial-wait <0-120000>
                # iosxr: router isis 100 / min-lsp-arrivaltime initial-wait <0-120000> level 1
                # iosxr: router isis 100 / min-lsp-arrivaltime initial-wait <0-120000> maximum-wait <0-120000>
                # iosxr: router isis 100 / min-lsp-arrivaltime initial-wait <0-120000> maximum-wait <0-120000> level 1
                # iosxr: router isis 100 / min-lsp-arrivaltime initial-wait <0-120000> maximum-wait <0-120000> secondary-wait <0-120000>
                # iosxr: router isis 100 / min-lsp-arrivaltime initial-wait <0-120000> maximum-wait <0-120000> secondary-wait <0-120000> level 1
                # iosxr: router isis 100 / min-lsp-arrivaltime initial-wait <0-120000> secondary-wait <0-120000>
                # iosxr: router isis 100 / min-lsp-arrivaltime initial-wait <0-120000> secondary-wait <0-120000> level 1
                # iosxr: router isis 100 / min-lsp-arrivaltime maximum-wait <0-120000>
                # iosxr: router isis 100 / min-lsp-arrivaltime maximum-wait <0-120000> level 1
                # iosxr: router isis 100 / min-lsp-arrivaltime maximum-wait <0-120000> secondary-wait <0-120000>
                # iosxr: router isis 100 / min-lsp-arrivaltime maximum-wait <0-120000> secondary-wait <0-120000> level 1
                # iosxr: router isis 100 / min-lsp-arrivaltime secondary-wait <0-120000>
                # iosxr: router isis 100 / min-lsp-arrivaltime secondary-wait <0-120000> level 1
                
                # iosxr: router isis 100 / net 11.0000.0000.0000.0000.00
                for net_id, attributes2 in attributes.sequence_values('net_ids', sort=True):
                    configurations.append_line('net {}'.format(net_id))

                # iosxr: router isis 100 / nsf cisco
                # iosxr: router isis 100 / nsf ietf
                configurations.append_line(attributes.format('nsf {nsf}', transform={
                    _Isis.Nsf.cisco: 'cisco',
                    _Isis.Nsf.ietf: 'ietf',
                }))

                # iosxr: router isis 100 / nsf interface-expires 1
                # iosxr: router isis 100 / nsf interface-timer 1

                # iosxr: router isis 100 / nsf lifetime 5
                configurations.append_line(attributes.format('nsf lifetime {nsf_lifetime}'))

                # iosxr: router isis 100 / nsr
                if attributes.value('nsr'):
                    configurations.append_line(attributes.format('nsr'))

                # iosxr: router isis 100 / segment-routing global-block 16000 16001
                # iosxr: router isis 100 / set-overload-bit
                # iosxr: router isis 100 / set-overload-bit advertise external
                # iosxr: router isis 100 / set-overload-bit advertise external interlevel
                # iosxr: router isis 100 / set-overload-bit advertise interlevel
                # iosxr: router isis 100 / set-overload-bit level 1
                # iosxr: router isis 100 / set-overload-bit level 1 advertise external
                # iosxr: router isis 100 / set-overload-bit level 1 advertise external interlevel
                # iosxr: router isis 100 / set-overload-bit level 1 advertise interlevel
                # iosxr: router isis 100 / set-overload-bit on-startup 5
                # iosxr: router isis 100 / set-overload-bit on-startup 5 advertise external
                # iosxr: router isis 100 / set-overload-bit on-startup 5 advertise external interlevel
                # iosxr: router isis 100 / set-overload-bit on-startup 5 advertise interlevel
                # iosxr: router isis 100 / set-overload-bit on-startup 5 level 1
                # iosxr: router isis 100 / set-overload-bit on-startup 5 level 1 advertise external
                # iosxr: router isis 100 / set-overload-bit on-startup 5 level 1 advertise external interlevel
                # iosxr: router isis 100 / set-overload-bit on-startup 5 level 1 advertise interlevel
                # iosxr: router isis 100 / set-overload-bit on-startup wait-for-bgp
                # iosxr: router isis 100 / set-overload-bit on-startup wait-for-bgp advertise external
                # iosxr: router isis 100 / set-overload-bit on-startup wait-for-bgp advertise external interlevel
                # iosxr: router isis 100 / set-overload-bit on-startup wait-for-bgp advertise interlevel
                # iosxr: router isis 100 / set-overload-bit on-startup wait-for-bgp level 1
                # iosxr: router isis 100 / set-overload-bit on-startup wait-for-bgp level 1 advertise external
                # iosxr: router isis 100 / set-overload-bit on-startup wait-for-bgp level 1 advertise external interlevel
                # iosxr: router isis 100 / set-overload-bit on-startup wait-for-bgp level 1 advertise interlevel
                # iosxr: router isis 100 / trace detailed 1
                # iosxr: router isis 100 / trace detailed 1 hello 1
                # iosxr: router isis 100 / trace detailed 1 hello 1 severe 1
                # iosxr: router isis 100 / trace detailed 1 hello 1 severe 1 standard 1
                # iosxr: router isis 100 / trace detailed 1 hello 1 standard 1
                # iosxr: router isis 100 / trace detailed 1 severe 1
                # iosxr: router isis 100 / trace detailed 1 severe 1 standard 1
                # iosxr: router isis 100 / trace detailed 1 standard 1
                # iosxr: router isis 100 / trace hello 1
                # iosxr: router isis 100 / trace hello 1 severe 1
                # iosxr: router isis 100 / trace hello 1 severe 1 standard 1
                # iosxr: router isis 100 / trace hello 1 standard 1
                # iosxr: router isis 100 / trace mode basic
                # iosxr: router isis 100 / trace mode enhanced
                # iosxr: router isis 100 / trace mode off
                # iosxr: router isis 100 / trace severe 1
                # iosxr: router isis 100 / trace severe 1 standard 1
                # iosxr: router isis 100 / trace standard 1
                # iosxr: router isis 100 / triggers someword

                for sub, attributes2 in attributes.mapping_values('address_family_attr', keys=self.address_families, sort=True):
                    configurations.append_block(
                        sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

                for sub, attributes2 in attributes.mapping_values('interface_attr', keys=self.interfaces, sort=True):
                    configurations.append_block(
                        sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

            if apply:
                if configurations:
                    self.device.configure(configurations, fail_invalid=True)
            else:
                return CliConfig(device=self.device, unconfig=unconfig,
                                 cli_config=configurations, fail_invalid=True)

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

        class AddressFamilyAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                assert not apply
                assert not kwargs, kwargs
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast (config-isis-af)
                with configurations.submode_context(attributes.format('address-family {address_family.value}', force=True)):
                    if unconfig and attributes.iswildcard:
                        configurations.submode_unconfig()

                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / adjacency-check disable
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / advertise passive-only
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / apply-weight ecmp-only
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / apply-weight ucmp-only
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / attached-bit receive ignore
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / attached-bit send always-set
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / attached-bit send never-set
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / default-information originate
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / default-information originate external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / default-information originate external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / default-information originate route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / distance 1
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / distance 1 1.2.3.4/24
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / distance 1 1.2.3.4/24 someword
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / distance 1 1:2::3/128
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / distance 1 1:2::3/128 someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-link priority-limit critical
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-link priority-limit critical level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-link priority-limit high
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-link priority-limit high level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-link priority-limit medium
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-link priority-limit medium level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-link use-candidate-only
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-link use-candidate-only level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-prefix load-sharing disable
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-prefix load-sharing disable level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-prefix priority-limit critical
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-prefix priority-limit critical level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-prefix priority-limit high
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-prefix priority-limit high level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-prefix priority-limit medium
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-prefix priority-limit medium level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-prefix remote-lfa prefix-list someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-prefix remote-lfa prefix-list someword level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-prefix tiebreaker downstream index 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-prefix tiebreaker downstream index 1 level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-prefix tiebreaker lc-disjoint index 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-prefix tiebreaker lc-disjoint index 1 level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-prefix tiebreaker lowest-backup-metric index 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-prefix tiebreaker lowest-backup-metric index 1 level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-prefix tiebreaker node-protecting index 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-prefix tiebreaker node-protecting index 1 level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-prefix tiebreaker primary-path index 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-prefix tiebreaker primary-path index 1 level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-prefix tiebreaker secondary-path index 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-prefix tiebreaker secondary-path index 1 level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-prefix tiebreaker srlg-disjoint index 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-prefix tiebreaker srlg-disjoint index 1 level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-prefix use-candidate-only
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-prefix use-candidate-only level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / ispf
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / ispf level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / maximum-paths 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / maximum-redistributed-prefixes 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / maximum-redistributed-prefixes 1 level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / metric 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / metric 1 level 1

                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / metric-style [narrow|wide] [transition] [level 1]
                    configurations.append_line(attributes.format('metric-style {metric_style.value}'))

                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / microloop avoidance
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / microloop avoidance protected
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / microloop avoidance rib-update-delay 1000
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / monitor-convergence (config-isis-af-rcmd)
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / monitor-convergence / prefix-list someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / monitor-convergence / track-ip-frr
                    # iosxr: router isis 100 / address-family ipv4 unicast / mpls ldp auto-config
                    # iosxr: router isis 100 / address-family ipv4 unicast / mpls traffic-eng igp-intact
                    
                    # iosxr: router isis 100 / address-family ipv4 unicast / mpls traffic-eng level-1
                    # iosxr: router isis 100 / address-family ipv4 unicast / mpls traffic-eng level-1-2
                    # iosxr: router isis 100 / address-family ipv4 unicast / mpls traffic-eng level-2-only
                    configurations.append_line(attributes.format('mpls traffic-eng {mpls_te_level}', transform={
                        _Isis.IsType.level_1: 'level-1',
                        _Isis.IsType.level_1_2: 'level-1-2',
                        _Isis.IsType.level_2: 'level-2-only',
                    }))
                    
                    
                    # iosxr: router isis 100 / address-family ipv4 unicast / mpls traffic-eng multicast-intact                    
                    # iosxr: router isis 100 / address-family ipv4 unicast / mpls traffic-eng router-id 1.2.3.4
                    
                    # iosxr: router isis 100 / address-family ipv4 unicast / mpls traffic-eng router-id <intf>
                    configurations.append_line(attributes.format('mpls traffic-eng router-id {mpls_te_rtrid.name}'))
                   
                    
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / propagate level 1 into level 1 route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-1 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-1 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-1 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-1 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-1 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-1 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-1 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-1 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-1 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-1-2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-1-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-1-2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-1-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-1-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-1-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-1-2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-1-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-1-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-1-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-1-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword level-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute application someword route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-1 metric <0-16777215> metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-1 metric <0-16777215> metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-1 metric <0-16777215> route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-1 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-1 metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-1 metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-1 metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-1 metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-1 route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-1-2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-1-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-1-2 metric <0-16777215> metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-1-2 metric <0-16777215> metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-1-2 metric <0-16777215> route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-1-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-1-2 metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-1-2 metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-1-2 metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-1-2 metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-1-2 route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-2 metric <0-16777215> metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-2 metric <0-16777215> metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-2 metric <0-16777215> route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-2 metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-2 metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-2 metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-2 metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 level-2 route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 metric <0-16777215> metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 metric <0-16777215> metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 metric <0-16777215> route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 1 route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-1 metric <0-16777215> metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-1 metric <0-16777215> metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-1 metric <0-16777215> route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-1 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-1 metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-1 metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-1 metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-1 metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-1 route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-1-2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-1-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-1-2 metric <0-16777215> metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-1-2 metric <0-16777215> metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-1-2 metric <0-16777215> route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-1-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-1-2 metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-1-2 metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-1-2 metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-1-2 metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-1-2 route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-2 metric <0-16777215> metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-2 metric <0-16777215> metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-2 metric <0-16777215> route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-2 metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-2 metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-2 metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-2 metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 level-2 route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 metric <0-16777215> metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 metric <0-16777215> metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 metric <0-16777215> metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 metric <0-16777215> route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 100.200 route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-1 metric <0-16777215> metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-1 metric <0-16777215> metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-1 metric <0-16777215> route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-1 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-1 metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-1 metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-1 metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-1 metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-1 route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-1-2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-1-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-1-2 metric <0-16777215> metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-1-2 metric <0-16777215> metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-1-2 metric <0-16777215> route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-1-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-1-2 metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-1-2 metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-1-2 metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-1-2 metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-1-2 route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-2 metric <0-16777215> metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-2 metric <0-16777215> metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-2 metric <0-16777215> route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-2 metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-2 metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-2 metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-2 metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 level-2 route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 metric <0-16777215> metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 metric <0-16777215> metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 metric <0-16777215> metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 metric <0-16777215> route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute bgp 65536 route-policy someword

                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected
                    if attributes.value('redistribute_connected'):
                        configurations.append_line('redistribute connected')

                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-1 metric <0-16777215> metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-1 metric <0-16777215> metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-1 metric <0-16777215> route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-1 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-1 metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-1 metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-1 metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-1 metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-1 route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-1-2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-1-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-1-2 metric <0-16777215> metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-1-2 metric <0-16777215> metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-1-2 metric <0-16777215> route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-1-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-1-2 metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-1-2 metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-1-2 metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-1-2 metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-1-2 route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-2 metric <0-16777215> metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-2 metric <0-16777215> metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-2 metric <0-16777215> route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-2 metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-2 metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-2 metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-2 metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected level-2 route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected metric <0-16777215> metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected metric <0-16777215> metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected metric <0-16777215> metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected metric <0-16777215> metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected metric <0-16777215> route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute connected route-policy someword

                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-1 metric <0-16777215> metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-1 metric <0-16777215> metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-1 metric <0-16777215> route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-1 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-1 metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-1 metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-1 metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-1 metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-1 route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-1-2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-1-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-1-2 metric <0-16777215> metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-1-2 metric <0-16777215> metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-1-2 metric <0-16777215> route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-1-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-1-2 metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-1-2 metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-1-2 metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-1-2 metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-1-2 route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-2 metric <0-16777215> metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-2 metric <0-16777215> metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-2 metric <0-16777215> route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-2 metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-2 metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-2 metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-2 metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 level-2 route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-1 metric <0-16777215> metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-1 metric <0-16777215> metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-1 metric <0-16777215> route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-1 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-1 metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-1 metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-1 metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-1 metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-1 route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-1-2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-1-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-1-2 metric <0-16777215> metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-1-2 metric <0-16777215> metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-1-2 metric <0-16777215> route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-1-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-1-2 metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-1-2 metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-1-2 metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-1-2 metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-1-2 route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-2 metric <0-16777215> metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-2 metric <0-16777215> metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-2 metric <0-16777215> route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-2 metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-2 metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-2 metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-2 metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external level-2 route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external metric <0-16777215> metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external metric <0-16777215> metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external metric <0-16777215> metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external metric <0-16777215> metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external metric <0-16777215> route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal level-1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal level-1 metric <0-16777215> metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal level-1 metric <0-16777215> route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal level-1 metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal level-1 metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal level-1 metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal level-1 route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal level-1-2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal level-1-2 metric <0-16777215> metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal level-1-2 metric <0-16777215> route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal level-1-2 metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal level-1-2 metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal level-1-2 metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal level-1-2 route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal level-2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal level-2 metric <0-16777215> metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal level-2 metric <0-16777215> route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal level-2 metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal level-2 metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal level-2 metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal level-2 route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal metric <0-16777215> metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal metric <0-16777215> metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal metric <0-16777215> metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal metric <0-16777215> route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 match internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 metric <0-16777215> metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 metric <0-16777215> metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 metric <0-16777215> route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute eigrp 1 route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-1 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-1 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-1 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-1 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-1 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-1 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-1 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-1 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-1 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-1-2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-1-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-1-2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-1-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-1-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-1-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-1-2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-1-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-1-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-1-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-1-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword level-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute isis someword route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-1 metric <0-16777215> metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-1 metric <0-16777215> metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-1 metric <0-16777215> route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-1 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-1 metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-1 metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-1 metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-1 metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-1 route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-1-2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-1-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-1-2 metric <0-16777215> metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-1-2 metric <0-16777215> metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-1-2 metric <0-16777215> route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-1-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-1-2 metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-1-2 metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-1-2 metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-1-2 metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-1-2 route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-2 metric <0-16777215> metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-2 metric <0-16777215> metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-2 metric <0-16777215> route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-2 metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-2 metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-2 metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-2 metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile level-2 route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile metric <0-16777215> metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile metric <0-16777215> metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile metric <0-16777215> metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile metric <0-16777215> metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile metric <0-16777215> route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute mobile route-policy someword
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-1
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-1 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-1 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-1 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-1 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-1 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-1 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-1 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-1 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-1 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-1 route-policy someword2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-1-2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-1-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-1-2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-1-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-1-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-1-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-1-2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-1-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-1-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-1-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-1-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword level-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-1
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-1 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-1 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-1 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-1 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-1 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-1 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-1 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-1 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-1 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-1-2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-1-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-1-2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-1-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-1-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-1-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-1-2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-1-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-1-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-1-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-1-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 level-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 1 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-1
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-1 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-1 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-1 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-1 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-1 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-1 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-1 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-1 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-1 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-1-2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-1-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-1-2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-1-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-1-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-1-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-1-2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-1-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-1-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-1-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-1-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 level-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external 2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-1
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-1 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-1 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-1 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-1 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-1 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-1 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-1 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-1 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-1 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-1-2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-1-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-1-2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-1-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-1-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-1-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-1-2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-1-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-1-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-1-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-1-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external level-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal level-1
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal level-1 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal level-1 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal level-1 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal level-1 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal level-1 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal level-1 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal level-1-2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal level-1-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal level-1-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal level-1-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal level-1-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal level-1-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal level-1-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal level-1-2 route-policy someword2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal level-2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal level-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal level-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal level-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal level-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal level-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal level-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-1
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-1 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-1 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-1 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-1 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-1 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-1 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-1 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-1 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-1 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-1-2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-1-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-1-2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-1-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-1-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-1-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-1-2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-1-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-1-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-1-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-1-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 level-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 1 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-1
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-1 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-1 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-1 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-1 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-1 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-1 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-1 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-1 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-1 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-1-2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-1-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-1-2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-1-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-1-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-1-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-1-2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-1-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-1-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-1-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-1-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 level-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external 2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-1
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-1 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-1 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-1 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-1 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-1 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-1 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-1 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-1 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-1 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-1-2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-1-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-1-2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-1-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-1-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-1-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-1-2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-1-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-1-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-1-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-1-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external level-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword match nssa-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute ospf someword route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-1
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-1 metric <0-16777215> metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-1 metric <0-16777215> metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-1 metric <0-16777215> route-policy someword
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-1 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-1 metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-1 metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-1 metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-1 metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-1 route-policy someword
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-1-2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-1-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-1-2 metric <0-16777215> metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-1-2 metric <0-16777215> metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-1-2 metric <0-16777215> route-policy someword
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-1-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-1-2 metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-1-2 metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-1-2 metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-1-2 metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-1-2 route-policy someword
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-2
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-2 metric <0-16777215> metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-2 metric <0-16777215> metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-2 metric <0-16777215> route-policy someword
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-2 metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-2 metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-2 metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-2 metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip level-2 route-policy someword
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip metric <0-16777215> metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip metric <0-16777215> metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip metric <0-16777215> metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip metric <0-16777215> metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip metric <0-16777215> route-policy someword
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip metric-type external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / redistribute rip route-policy someword
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-1
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-1 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-1 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-1 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-1 metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-1 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-1 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-1 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-1 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-1 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-1-2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-1-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-1-2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-1-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-1-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-1-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-1-2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-1-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-1-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-1-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-1-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword level-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-1
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-1 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-1 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-1 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-1 metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-1 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-1 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-1 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-1 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-1 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-1-2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-1-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-1-2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-1-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-1-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-1-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-1-2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-1-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-1-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-1-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-1-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 level-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 1 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-1
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-1 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-1 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-1 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-1 metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-1 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-1 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-1 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-1 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-1 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-1-2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-1-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-1-2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-1-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-1-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-1-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-1-2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-1-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-1-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-1-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-1-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 level-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external 2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-1
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-1 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-1 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-1 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-1 metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-1 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-1 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-1 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-1 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-1 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-1-2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-1-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-1-2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-1-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-1-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-1-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-1-2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-1-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-1-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-1-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-1-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external level-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal level-1
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal level-1 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal level-1 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal level-1 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal level-1 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal level-1 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal level-1 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal level-1-2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal level-1-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal level-1-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal level-1-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal level-1-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal level-1-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal level-1-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal level-2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal level-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal level-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal level-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal level-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal level-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal level-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-1
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-1 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-1 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-1 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-1 metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-1 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-1 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-1 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-1 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-1 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-1-2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-1-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-1-2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-1-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-1-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-1-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-1-2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-1-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-1-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-1-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-1-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 level-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 1 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-1
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-1 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-1 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-1 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-1 metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-1 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-1 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-1 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-1 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-1 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-1-2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-1-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-1-2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-1-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-1-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-1-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-1-2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-1-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-1-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-1-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-1-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 level-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external 2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-1
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-1 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-1 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-1 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-1 metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-1 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-1 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-1 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-1 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-1 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-1-2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-1-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-1-2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-1-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-1-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-1-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-1-2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-1-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-1-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-1-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-1-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external level-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword match nssa-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword metric-type external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / redistribute ospfv3 someword route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-1 metric <0-16777215> metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-1 metric <0-16777215> metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-1 metric <0-16777215> route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-1 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-1 metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-1 metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-1 metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-1 metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-1 route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-1-2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-1-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-1-2 metric <0-16777215> metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-1-2 metric <0-16777215> metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-1-2 metric <0-16777215> route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-1-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-1-2 metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-1-2 metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-1-2 metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-1-2 metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-1-2 route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-2 metric <0-16777215> metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-2 metric <0-16777215> metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-2 metric <0-16777215> route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-2 metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-2 metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-2 metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-2 metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static level-2 route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static metric <0-16777215> metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static metric <0-16777215> metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static metric <0-16777215> metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static metric <0-16777215> metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static metric <0-16777215> route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute static route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-1 metric <0-16777215> metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-1 metric <0-16777215> metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-1 metric <0-16777215> route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-1 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-1 metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-1 metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-1 metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-1 metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-1 route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-1-2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-1-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-1-2 metric <0-16777215> metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-1-2 metric <0-16777215> metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-1-2 metric <0-16777215> route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-1-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-1-2 metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-1-2 metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-1-2 metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-1-2 metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-1-2 route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-2 metric <0-16777215> metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-2 metric <0-16777215> metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-2 metric <0-16777215> route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-2 metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-2 metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-2 metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-2 metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber level-2 route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber metric <0-16777215> metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber metric <0-16777215> metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber metric <0-16777215> metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber metric <0-16777215> metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber metric <0-16777215> route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber metric-type external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber metric-type internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber metric-type rib-metric-as-external route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber metric-type rib-metric-as-internal route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / redistribute subscriber route-policy someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / route source first-hop

                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast / segment-routing mpls
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast / segment-routing mpls sr-prefer
                    v = attributes.value('segment_routing_mpls')
                    if v:
                        cfg = 'segment-routing mpls'
                        if not unconfig:
                            if attributes.value('segment_routing_mpls_sr_prefer', force=True):
                                cfg += ' sr-prefer'
                        configurations.append_line(cfg)

                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast / segment-routing prefix-sid-map advertise-local
                    v = attributes.value('segment_routing_prefix_sid_map_advertise_local')
                    if v:
                        configurations.append_line('segment-routing prefix-sid-map advertise-local')

                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast / segment-routing prefix-sid-map receive
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast / segment-routing prefix-sid-map receive disable
                    v = attributes.value('segment_routing_prefix_sid_map_receive')
                    if v is not None:
                        if v is True:
                            cfg = 'segment-routing prefix-sid-map receive'
                        else:
                            cfg = 'segment-routing prefix-sid-map receive disable'
                        configurations.append_line(cfg)

                    # iosxr: router isis 100 / address-family ipv6 unicast / single-topology
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / spf periodic disable
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / spf periodic disable level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / spf periodic interval 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / spf periodic interval 1 level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / spf prefix-priority critical someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / spf prefix-priority critical tag 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / spf prefix-priority high someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / spf prefix-priority high tag 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / spf prefix-priority level 1 critical someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / spf prefix-priority level 1 critical tag 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / spf prefix-priority level 1 high someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / spf prefix-priority level 1 high tag 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / spf prefix-priority level 1 medium someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / spf prefix-priority level 1 medium tag 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / spf prefix-priority medium someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / spf prefix-priority medium tag 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / spf-interval initial-wait <0-120000>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / spf-interval initial-wait <0-120000> level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / spf-interval initial-wait <0-120000> maximum-wait <0-120000>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / spf-interval initial-wait <0-120000> maximum-wait <0-120000> level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / spf-interval initial-wait <0-120000> maximum-wait <0-120000> secondary-wait <0-120000>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / spf-interval initial-wait <0-120000> maximum-wait <0-120000> secondary-wait <0-120000> level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / spf-interval initial-wait <0-120000> secondary-wait <0-120000>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / spf-interval initial-wait <0-120000> secondary-wait <0-120000> level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / spf-interval maximum-wait <0-120000>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / spf-interval maximum-wait <0-120000> level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / spf-interval maximum-wait <0-120000> secondary-wait <0-120000>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / spf-interval maximum-wait <0-120000> secondary-wait <0-120000> level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / spf-interval secondary-wait <0-120000>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / spf-interval secondary-wait <0-120000> level 1
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / summary-prefix 1.2.3.0/24
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / summary-prefix 1.2.3.0/24 level 1
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / summary-prefix 1.2.3.0/24 tag 1
                    # iosxr: router isis 100 / address-family ipv4 unicast|multicast / summary-prefix 1.2.3.0/24 tag 1 level 1
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / summary-prefix 1:2::3/128
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / summary-prefix 1:2::3/128 level 1
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / summary-prefix 1:2::3/128 tag 1
                    # iosxr: router isis 100 / address-family ipv6 unicast|multicast / summary-prefix 1:2::3/128 tag 1 level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword (config-isis-af)
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / adjacency-check disable
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / advertise passive-only
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / apply-weight ecmp-only
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / apply-weight ucmp-only
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / attached-bit receive ignore
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / attached-bit send always-set
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / attached-bit send never-set
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / default-information originate
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / default-information originate external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / default-information originate external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / default-information originate route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / distance 1
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / distance 1 1.2.3.4/24
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / distance 1 1.2.3.4/24 someword2
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / distance 1 1:2::3/128
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / distance 1 1:2::3/128 someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-link priority-limit critical
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-link priority-limit critical level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-link priority-limit high
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-link priority-limit high level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-link priority-limit medium
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-link priority-limit medium level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-link use-candidate-only
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-link use-candidate-only level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-prefix load-sharing disable
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-prefix load-sharing disable level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-prefix priority-limit critical
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-prefix priority-limit critical level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-prefix priority-limit high
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-prefix priority-limit high level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-prefix priority-limit medium
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-prefix priority-limit medium level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-prefix remote-lfa prefix-list someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-prefix remote-lfa prefix-list someword2 level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-prefix tiebreaker downstream index 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-prefix tiebreaker downstream index 1 level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-prefix tiebreaker lc-disjoint index 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-prefix tiebreaker lc-disjoint index 1 level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-prefix tiebreaker lowest-backup-metric index 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-prefix tiebreaker lowest-backup-metric index 1 level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-prefix tiebreaker node-protecting index 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-prefix tiebreaker node-protecting index 1 level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-prefix tiebreaker primary-path index 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-prefix tiebreaker primary-path index 1 level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-prefix tiebreaker secondary-path index 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-prefix tiebreaker secondary-path index 1 level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-prefix tiebreaker srlg-disjoint index 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-prefix tiebreaker srlg-disjoint index 1 level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-prefix use-candidate-only
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-prefix use-candidate-only level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / ispf
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / ispf level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / maximum-paths 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / maximum-redistributed-prefixes 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / maximum-redistributed-prefixes 1 level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / metric 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / metric 1 level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / metric-style narrow
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / metric-style narrow level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / metric-style narrow transition
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / metric-style narrow transition level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / metric-style transition
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / metric-style transition level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / metric-style wide
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / metric-style wide level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / metric-style wide transition
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / metric-style wide transition level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / microloop avoidance
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / microloop avoidance protected
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / microloop avoidance rib-update-delay 1000
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / monitor-convergence (config-isis-af-rcmd)
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / monitor-convergence / prefix-list someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / monitor-convergence / track-ip-frr
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / propagate level 1 into level 1 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-1 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-1 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-1 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-1 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-1 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-1 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-1 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-1 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-1 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-1-2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-1-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-1-2 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-1-2 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-1-2 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-1-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-1-2 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-1-2 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-1-2 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-1-2 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-1-2 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-2 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-2 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-2 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-2 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-2 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-2 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-2 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 level-2 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute application someword2 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-1 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-1 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-1 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-1 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-1 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-1 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-1 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-1 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-1 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-1-2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-1-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-1-2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-1-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-1-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-1-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-1-2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-1-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-1-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-1-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-1-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 level-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 1 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-1 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-1 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-1 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-1 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-1 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-1 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-1 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-1 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-1 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-1-2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-1-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-1-2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-1-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-1-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-1-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-1-2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-1-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-1-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-1-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-1-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 level-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 100.200 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-1 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-1 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-1 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-1 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-1 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-1 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-1 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-1 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-1 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-1-2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-1-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-1-2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-1-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-1-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-1-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-1-2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-1-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-1-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-1-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-1-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 level-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute bgp 65536 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-1 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-1 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-1 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-1 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-1 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-1 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-1 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-1 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-1 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-1-2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-1-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-1-2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-1-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-1-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-1-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-1-2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-1-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-1-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-1-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-1-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected level-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute connected route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-1 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-1 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-1 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-1 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-1 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-1 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-1 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-1 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-1 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-1-2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-1-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-1-2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-1-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-1-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-1-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-1-2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-1-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-1-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-1-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-1-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 level-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-1 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-1 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-1 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-1 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-1 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-1 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-1 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-1 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-1 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-1-2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-1-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-1-2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-1-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-1-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-1-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-1-2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-1-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-1-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-1-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-1-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external level-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal level-1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal level-1 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal level-1 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal level-1 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal level-1 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal level-1 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal level-1 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal level-1-2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal level-1-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal level-1-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal level-1-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal level-1-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal level-1-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal level-1-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal level-2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal level-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal level-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal level-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal level-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal level-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal level-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 match internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute eigrp 1 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-1 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-1 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-1 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-1 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-1 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-1 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-1 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-1 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-1 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-1-2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-1-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-1-2 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-1-2 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-1-2 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-1-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-1-2 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-1-2 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-1-2 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-1-2 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-1-2 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-2 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-2 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-2 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-2 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-2 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-2 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-2 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 level-2 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute isis someword2 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-1 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-1 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-1 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-1 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-1 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-1 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-1 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-1 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-1 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-1-2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-1-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-1-2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-1-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-1-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-1-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-1-2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-1-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-1-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-1-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-1-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile level-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute mobile route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-1
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-1 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-1 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-1 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-1 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-1 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-1 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-1 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-1 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-1 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-1-2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-1-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-1-2 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-1-2 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-1-2 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-1-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-1-2 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-1-2 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-1-2 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-1-2 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-1-2 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-2 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-2 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-2 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-2 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-2 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-2 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-2 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 level-2 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-1
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-1 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-1 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-1 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-1 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-1 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-1 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-1 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-1 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-1 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-1-2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-1-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-1-2 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-1-2 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-1-2 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-1-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-1-2 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-1-2 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-1-2 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-1-2 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-1-2 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-2 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-2 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-2 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-2 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-2 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-2 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-2 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 level-2 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 1 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-1
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-1 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-1 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-1 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-1 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-1 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-1 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-1 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-1 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-1 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-1-2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-1-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-1-2 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-1-2 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-1-2 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-1-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-1-2 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-1-2 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-1-2 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-1-2 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-1-2 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-2 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-2 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-2 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-2 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-2 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-2 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-2 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 level-2 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external 2 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-1
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-1 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-1 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-1 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-1 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-1 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-1 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-1 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-1 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-1 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-1-2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-1-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-1-2 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-1-2 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-1-2 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-1-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-1-2 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-1-2 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-1-2 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-1-2 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-1-2 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-2 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-2 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-2 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-2 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-2 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-2 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-2 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external level-2 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal level-1
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal level-1 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal level-1 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal level-1 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal level-1 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal level-1 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal level-1 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal level-1-2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal level-1-2 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal level-1-2 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal level-1-2 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal level-1-2 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal level-1-2 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal level-1-2 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal level-2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal level-2 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal level-2 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal level-2 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal level-2 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal level-2 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal level-2 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-1
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-1 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-1 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-1 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-1 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-1 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-1 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-1 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-1 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-1 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-1-2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-1-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-1-2 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-1-2 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-1-2 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-1-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-1-2 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-1-2 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-1-2 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-1-2 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-1-2 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-2 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-2 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-2 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-2 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-2 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-2 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-2 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 level-2 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 1 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-1
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-1 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-1 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-1 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-1 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-1 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-1 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-1 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-1 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-1 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-1-2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-1-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-1-2 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-1-2 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-1-2 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-1-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-1-2 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-1-2 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-1-2 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-1-2 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-1-2 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-2 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-2 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-2 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-2 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-2 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-2 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-2 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 level-2 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external 2 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-1
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-1 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-1 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-1 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-1 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-1 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-1 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-1 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-1 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-1 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-1-2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-1-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-1-2 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-1-2 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-1-2 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-1-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-1-2 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-1-2 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-1-2 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-1-2 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-1-2 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-2 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-2 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-2 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-2 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-2 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-2 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-2 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external level-2 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 match nssa-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute ospf someword2 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-1
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-1 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-1 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-1 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-1 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-1 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-1 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-1 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-1 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-1 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-1-2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-1-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-1-2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-1-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-1-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-1-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-1-2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-1-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-1-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-1-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-1-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip level-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip metric-type external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip metric-type internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / redistribute rip route-policy someword2
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-1
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-1 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-1 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-1 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-1 metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-1 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-1 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-1 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-1 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-1 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-1-2
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-1-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-1-2 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-1-2 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-1-2 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-1-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-1-2 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-1-2 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-1-2 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-1-2 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-1-2 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-2
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-2 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-2 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-2 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-2 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-2 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-2 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-2 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 level-2 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-1
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-1 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-1 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-1 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-1 metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-1 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-1 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-1 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-1 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-1 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-1-2
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-1-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-1-2 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-1-2 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-1-2 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-1-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-1-2 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-1-2 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-1-2 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-1-2 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-1-2 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-2
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-2 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-2 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-2 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-2 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-2 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-2 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-2 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 level-2 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 1 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-1
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-1 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-1 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-1 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-1 metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-1 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-1 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-1 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-1 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-1 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-1-2
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-1-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-1-2 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-1-2 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-1-2 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-1-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-1-2 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-1-2 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-1-2 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-1-2 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-1-2 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-2
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-2 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-2 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-2 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-2 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-2 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-2 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-2 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 level-2 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external 2 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-1
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-1 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-1 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-1 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-1 metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-1 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-1 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-1 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-1 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-1 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-1-2
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-1-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-1-2 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-1-2 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-1-2 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-1-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-1-2 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-1-2 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-1-2 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-1-2 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-1-2 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-2
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-2 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-2 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-2 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-2 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-2 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-2 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-2 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external level-2 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal level-1
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal level-1 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal level-1 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal level-1 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal level-1 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal level-1 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal level-1 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal level-1-2
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal level-1-2 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal level-1-2 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal level-1-2 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal level-1-2 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal level-1-2 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal level-1-2 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal level-2
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal level-2 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal level-2 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal level-2 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal level-2 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal level-2 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal level-2 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-1
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-1 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-1 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-1 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-1 metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-1 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-1 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-1 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-1 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-1 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-1-2
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-1-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-1-2 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-1-2 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-1-2 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-1-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-1-2 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-1-2 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-1-2 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-1-2 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-1-2 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-2
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-2 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-2 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-2 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-2 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-2 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-2 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-2 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 level-2 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 1 route-policy someword3 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-1
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-1 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-1 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-1 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-1 metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-1 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-1 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-1 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-1 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-1 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-1-2
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-1-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-1-2 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-1-2 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-1-2 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-1-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-1-2 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-1-2 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-1-2 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-1-2 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-1-2 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-2
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-2 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-2 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-2 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-2 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-2 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-2 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-2 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 level-2 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external 2 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-1
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-1 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-1 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-1 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-1 metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-1 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-1 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-1 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-1 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-1 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-1-2
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-1-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-1-2 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-1-2 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-1-2 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-1-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-1-2 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-1-2 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-1-2 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-1-2 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-1-2 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-2
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-2 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-2 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-2 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-2 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-2 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-2 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-2 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external level-2 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 match nssa-external route-policy someword3 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 metric <0-16777215> metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 metric <0-16777215> metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 metric <0-16777215> route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 metric-type external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 metric-type external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 metric-type internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 metric-type rib-metric-as-external route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 metric-type rib-metric-as-internal route-policy someword3
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / redistribute ospfv3 someword2 route-policy someword3
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-1 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-1 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-1 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-1 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-1 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-1 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-1 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-1 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-1 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-1-2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-1-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-1-2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-1-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-1-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-1-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-1-2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-1-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-1-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-1-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-1-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static level-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute static route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-1 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-1 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-1 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-1 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-1 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-1 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-1 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-1 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-1 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-1 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-1 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-1 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-1 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-1 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-1 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-1 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-1 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-1 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-1 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-1-2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-1-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-1-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-1-2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-1-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-1-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-1-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-1-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-1-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-1-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-1-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-1-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-1-2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-1-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-1-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-1-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-1-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-1-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-1-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-1-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-2 metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-2 metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-2 metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-2 metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-2 metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-2 metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-2 metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-2 metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-2 metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-2 metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-2 metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-2 metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-2 metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-2 metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-2 metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-2 metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-2 metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-2 metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber level-2 route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber metric <0-16777215>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber metric <0-16777215> metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber metric <0-16777215> metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber metric <0-16777215> metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber metric <0-16777215> metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber metric <0-16777215> metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber metric <0-16777215> metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber metric <0-16777215> metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber metric <0-16777215> metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber metric <0-16777215> route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber metric-type external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber metric-type external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber metric-type internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber metric-type internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber metric-type rib-metric-as-external
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber metric-type rib-metric-as-external route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber metric-type rib-metric-as-internal
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber metric-type rib-metric-as-internal route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / redistribute subscriber route-policy someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / route source first-hop
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / spf periodic disable
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / spf periodic disable level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / spf periodic interval 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / spf periodic interval 1 level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / spf prefix-priority critical someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / spf prefix-priority critical tag 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / spf prefix-priority high someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / spf prefix-priority high tag 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / spf prefix-priority level 1 critical someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / spf prefix-priority level 1 critical tag 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / spf prefix-priority level 1 high someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / spf prefix-priority level 1 high tag 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / spf prefix-priority level 1 medium someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / spf prefix-priority level 1 medium tag 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / spf prefix-priority medium someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / spf prefix-priority medium tag 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / spf-interval initial-wait <0-120000>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / spf-interval initial-wait <0-120000> level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / spf-interval initial-wait <0-120000> maximum-wait <0-120000>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / spf-interval initial-wait <0-120000> maximum-wait <0-120000> level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / spf-interval initial-wait <0-120000> maximum-wait <0-120000> secondary-wait <0-120000>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / spf-interval initial-wait <0-120000> maximum-wait <0-120000> secondary-wait <0-120000> level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / spf-interval initial-wait <0-120000> secondary-wait <0-120000>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / spf-interval initial-wait <0-120000> secondary-wait <0-120000> level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / spf-interval maximum-wait <0-120000>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / spf-interval maximum-wait <0-120000> level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / spf-interval maximum-wait <0-120000> secondary-wait <0-120000>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / spf-interval maximum-wait <0-120000> secondary-wait <0-120000> level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / spf-interval secondary-wait <0-120000>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / spf-interval secondary-wait <0-120000> level 1
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / summary-prefix 1.2.3.0/24
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / summary-prefix 1.2.3.0/24 level 1
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / summary-prefix 1.2.3.0/24 tag 1
                    # iosxr: router isis 100 / address-family ipv4 multicast / topology someword / summary-prefix 1.2.3.0/24 tag 1 level 1
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / summary-prefix 1:2::3/128
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / summary-prefix 1:2::3/128 level 1
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / summary-prefix 1:2::3/128 tag 1
                    # iosxr: router isis 100 / address-family ipv6 multicast / topology someword / summary-prefix 1:2::3/128 tag 1 level 1
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / topology-id 6
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / ucmp
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / ucmp delay-interval 100
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / ucmp exclude interface <intf>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / ucmp prefix-list someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / ucmp variance 101
                    # iosxr: router isis 100 / address-family ipv4|ipv6 multicast / topology someword / ucmp variance 101 prefix-list someword2
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / ucmp
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / ucmp delay-interval 100
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / ucmp exclude interface <intf>
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / ucmp prefix-list someword
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / ucmp variance 101
                    # iosxr: router isis 100 / address-family ipv4|ipv6 unicast|multicast / ucmp variance 101 prefix-list someword

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

        class InterfaceAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                assert not apply
                assert not kwargs, kwargs
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                # iosxr: router isis 100 / interface <intf> (config-isis-if)
                with configurations.submode_context(attributes.format('interface {interface.name}', force=True)):
                    if unconfig and attributes.iswildcard:
                        configurations.submode_unconfig()

                    # iosxr: router isis 100 / interface <intf> / bfd fast-detect ipv4
                    # iosxr: router isis 100 / interface <intf> / bfd fast-detect ipv6
                    # iosxr: router isis 100 / interface <intf> / bfd minimum-interval 3
                    # iosxr: router isis 100 / interface <intf> / bfd multiplier 2
                    # iosxr: router isis 100 / interface <intf> / circuit-type level-1
                    # iosxr: router isis 100 / interface <intf> / circuit-type level-1-2
                    # iosxr: router isis 100 / interface <intf> / circuit-type level-2-only
                    # iosxr: router isis 100 / interface <intf> / csnp-interval <0-65535>
                    # iosxr: router isis 100 / interface <intf> / csnp-interval <0-65535> level 1
                    # iosxr: router isis 100 / interface <intf> / hello-interval 1
                    # iosxr: router isis 100 / interface <intf> / hello-interval 1 level 1
                    # iosxr: router isis 100 / interface <intf> / hello-multiplier 3
                    # iosxr: router isis 100 / interface <intf> / hello-multiplier 3 level 1
                    # iosxr: router isis 100 / interface <intf> / hello-padding disable
                    # iosxr: router isis 100 / interface <intf> / hello-padding disable level 1
                    # iosxr: router isis 100 / interface <intf> / hello-padding sometimes
                    # iosxr: router isis 100 / interface <intf> / hello-padding sometimes level 1
                    # iosxr: router isis 100 / interface <intf> / hello-password accept cisco
                    # iosxr: router isis 100 / interface <intf> / hello-password accept cisco level 1
                    # iosxr: router isis 100 / interface <intf> / hello-password accept clear cisco
                    # iosxr: router isis 100 / interface <intf> / hello-password accept clear cisco level 1
                    # iosxr: router isis 100 / interface <intf> / hello-password accept encrypted 060506324F41
                    # iosxr: router isis 100 / interface <intf> / hello-password accept encrypted 060506324F41 level 1
                    # iosxr: router isis 100 / interface <intf> / hello-password cisco
                    # iosxr: router isis 100 / interface <intf> / hello-password cisco level 1
                    # iosxr: router isis 100 / interface <intf> / hello-password cisco level 1 send-only
                    # iosxr: router isis 100 / interface <intf> / hello-password cisco send-only
                    # iosxr: router isis 100 / interface <intf> / hello-password clear cisco
                    # iosxr: router isis 100 / interface <intf> / hello-password clear cisco level 1
                    # iosxr: router isis 100 / interface <intf> / hello-password clear cisco level 1 send-only
                    # iosxr: router isis 100 / interface <intf> / hello-password clear cisco send-only
                    # iosxr: router isis 100 / interface <intf> / hello-password encrypted 060506324F41
                    # iosxr: router isis 100 / interface <intf> / hello-password encrypted 060506324F41 level 1
                    # iosxr: router isis 100 / interface <intf> / hello-password encrypted 060506324F41 level 1 send-only
                    # iosxr: router isis 100 / interface <intf> / hello-password encrypted 060506324F41 send-only
                    # iosxr: router isis 100 / interface <intf> / hello-password hmac-md5 cisco
                    # iosxr: router isis 100 / interface <intf> / hello-password hmac-md5 cisco level 1
                    # iosxr: router isis 100 / interface <intf> / hello-password hmac-md5 cisco level 1 send-only
                    # iosxr: router isis 100 / interface <intf> / hello-password hmac-md5 cisco send-only
                    # iosxr: router isis 100 / interface <intf> / hello-password hmac-md5 clear cisco
                    # iosxr: router isis 100 / interface <intf> / hello-password hmac-md5 clear cisco level 1
                    # iosxr: router isis 100 / interface <intf> / hello-password hmac-md5 clear cisco level 1 send-only
                    # iosxr: router isis 100 / interface <intf> / hello-password hmac-md5 clear cisco send-only
                    # iosxr: router isis 100 / interface <intf> / hello-password hmac-md5 encrypted 060506324F41
                    # iosxr: router isis 100 / interface <intf> / hello-password hmac-md5 encrypted 060506324F41 level 1
                    # iosxr: router isis 100 / interface <intf> / hello-password hmac-md5 encrypted 060506324F41 level 1 send-only
                    # iosxr: router isis 100 / interface <intf> / hello-password hmac-md5 encrypted 060506324F41 send-only
                    # iosxr: router isis 100 / interface <intf> / hello-password keychain cisco
                    # iosxr: router isis 100 / interface <intf> / hello-password keychain cisco level 1
                    # iosxr: router isis 100 / interface <intf> / hello-password keychain cisco level 1 send-only
                    # iosxr: router isis 100 / interface <intf> / hello-password keychain cisco send-only
                    # iosxr: router isis 100 / interface <intf> / hello-password text cisco
                    # iosxr: router isis 100 / interface <intf> / hello-password text cisco level 1
                    # iosxr: router isis 100 / interface <intf> / hello-password text cisco level 1 send-only
                    # iosxr: router isis 100 / interface <intf> / hello-password text cisco send-only
                    # iosxr: router isis 100 / interface <intf> / hello-password text clear cisco
                    # iosxr: router isis 100 / interface <intf> / hello-password text clear cisco level 1
                    # iosxr: router isis 100 / interface <intf> / hello-password text clear cisco level 1 send-only
                    # iosxr: router isis 100 / interface <intf> / hello-password text clear cisco send-only
                    # iosxr: router isis 100 / interface <intf> / hello-password text encrypted 060506324F41
                    # iosxr: router isis 100 / interface <intf> / hello-password text encrypted 060506324F41 level 1
                    # iosxr: router isis 100 / interface <intf> / hello-password text encrypted 060506324F41 level 1 send-only
                    # iosxr: router isis 100 / interface <intf> / hello-password text encrypted 060506324F41 send-only
                    # iosxr: router isis 100 / interface <intf> / link-down fast-detect
                    # iosxr: router isis 100 / interface <intf> / lsp fast-flood threshold 1
                    # iosxr: router isis 100 / interface <intf> / lsp fast-flood threshold 1 level 1
                    # iosxr: router isis 100 / interface <intf> / lsp-interval 1
                    # iosxr: router isis 100 / interface <intf> / lsp-interval 1 level 1
                    # iosxr: router isis 100 / interface <intf> / mesh-group 1
                    # iosxr: router isis 100 / interface <intf> / mesh-group blocked

                    # iosxr: router isis 100 / interface <intf> / passive
                    if attributes.value('passive'):
                        configurations.append_line(attributes.format('passive'))

                    # iosxr: router isis 100 / interface <intf> / point-to-point
                    if attributes.value('point_to_point'):
                        configurations.append_line(attributes.format('point-to-point'))

                    # iosxr: router isis 100 / interface <intf> / priority <0-127>
                    # iosxr: router isis 100 / interface <intf> / priority <0-127> level 1
                    # iosxr: router isis 100 / interface <intf> / retransmit-interval <0-65535>
                    # iosxr: router isis 100 / interface <intf> / retransmit-interval <0-65535> level 1
                    # iosxr: router isis 100 / interface <intf> / retransmit-throttle-interval <0-65535>
                    # iosxr: router isis 100 / interface <intf> / retransmit-throttle-interval <0-65535> level 1

                    # iosxr: router isis 100 / interface <intf> / shutdown
                    if attributes.value('shutdown'):
                        configurations.append_line(attributes.format('shutdown'))

                    # iosxr: router isis 100 / interface <intf> / suppressed

                    for sub, attributes2 in attributes.mapping_values('address_family_attr', keys=self.address_families, sort=True):
                        configurations.append_block(
                            sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

            class AddressFamilyAttributes(ABC):

                def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
                    assert not apply
                    assert not kwargs, kwargs
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)

                    # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 unicast|multicast (config-isis-if-af)
                    with configurations.submode_context(attributes.format('address-family {address_family.value}', force=True)):
                        if unconfig and attributes.iswildcard:
                            configurations.submode_unconfig()

                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 unicast|multicast / auto-metric proactive-protect 1
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 unicast|multicast / auto-metric proactive-protect 1 level 1
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 unicast|multicast / disable
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-link
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-link exclude interface <intf>
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-link exclude interface <intf> level 1
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-link level 1
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-link lfa-candidate interface <intf>
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-link lfa-candidate interface <intf> level 1
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-prefix
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-prefix exclude interface <intf>
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-prefix exclude interface <intf> level 1
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-prefix level 1
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-prefix lfa-candidate interface <intf>
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-prefix lfa-candidate interface <intf> level 1
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-prefix remote-lfa maximum-metric 1
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-prefix remote-lfa maximum-metric 1 level 1
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-prefix remote-lfa tunnel mpls-ldp
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-prefix remote-lfa tunnel mpls-ldp level 1
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-prefix ti-lfa
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-prefix ti-lfa level 1
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-prefix tiebreaker default
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-prefix tiebreaker default level 1
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-prefix tiebreaker node-protecting index 1
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-prefix tiebreaker node-protecting index 1 level 1
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-prefix tiebreaker srlg-disjoint index 1
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 unicast|multicast / fast-reroute per-prefix tiebreaker srlg-disjoint index 1 level 1
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 unicast|multicast / link-group someword
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 unicast|multicast / link-group someword level 1

                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 unicast|multicast / metric 1
                        configurations.append_line(attributes.format('metric {metric}'))

                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 unicast|multicast / metric 1 level 1
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 unicast|multicast / metric maximum
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 unicast|multicast / metric maximum level 1
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 unicast / mpls ldp sync
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 unicast / mpls ldp sync level 1

                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 unicast / prefix-sid absolute 16000
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 unicast / prefix-sid absolute 16000 explicit-null
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 unicast / prefix-sid absolute 16000 explicit-null n-flag-clear
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 unicast / prefix-sid absolute 16000 n-flag-clear
                        cfg = attributes.format('prefix-sid absolute {prefix_sid}')
                        if cfg:
                            if attributes.value('prefix_sid_explicit_null', force=True):
                                cfg += ' explicit-null'
                            if attributes.value('prefix_sid_n_flag_clear', force=True):
                                cfg += ' n-flag-clear'
                            configurations.append_line(cfg)

                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 unicast / prefix-sid index <0-65535>
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 unicast / prefix-sid index <0-65535> explicit-null
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 unicast / prefix-sid index <0-65535> explicit-null n-flag-clear
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 unicast / prefix-sid index <0-65535> n-flag-clear
                        cfg = attributes.format('prefix-sid index {prefix_sid_index}')
                        if cfg:
                            if attributes.value('prefix_sid_explicit_null', force=True):
                                cfg += ' explicit-null'
                            if attributes.value('prefix_sid_n_flag_clear', force=True):
                                cfg += ' n-flag-clear'
                            configurations.append_line(cfg)

                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 unicast|multicast / tag 1
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 unicast|multicast / tag 1 level 1
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 multicast / topology someword (config-isis-if-af)
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 multicast / topology someword / auto-metric proactive-protect 1
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 multicast / topology someword / auto-metric proactive-protect 1 level 1
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 multicast / topology someword / disable
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-link
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-link exclude interface <intf>
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-link exclude interface <intf> level 1
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-link level 1
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-link lfa-candidate interface <intf>
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-link lfa-candidate interface <intf> level 1
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-prefix
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-prefix exclude interface <intf>
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-prefix exclude interface <intf> level 1
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-prefix level 1
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-prefix lfa-candidate interface <intf>
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-prefix lfa-candidate interface <intf> level 1
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-prefix remote-lfa maximum-metric 1
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-prefix remote-lfa maximum-metric 1 level 1
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-prefix remote-lfa tunnel mpls-ldp
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-prefix remote-lfa tunnel mpls-ldp level 1
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-prefix ti-lfa
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-prefix ti-lfa level 1
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-prefix tiebreaker default
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-prefix tiebreaker default level 1
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-prefix tiebreaker node-protecting index 1
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-prefix tiebreaker node-protecting index 1 level 1
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-prefix tiebreaker srlg-disjoint index 1
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 multicast / topology someword / fast-reroute per-prefix tiebreaker srlg-disjoint index 1 level 1
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 multicast / topology someword / link-group someword2
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 multicast / topology someword / link-group someword2 level 1
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 multicast / topology someword / metric 1
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 multicast / topology someword / metric 1 level 1
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 multicast / topology someword / metric maximum
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 multicast / topology someword / metric maximum level 1
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 multicast / topology someword / tag 1
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 multicast / topology someword / tag 1 level 1
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 multicast / topology someword / weight 1
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 multicast / topology someword / weight 1 level 1
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 unicast|multicast / weight 1
                        # iosxr: router isis 100 / interface <intf> / address-family ipv4|ipv6 unicast|multicast / weight 1 level 1

                    return str(configurations)

                def build_unconfig(self, apply=True, attributes=None, **kwargs):
                    return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

