"""
"""

# Python
import time
import logging

# ATS
from pyats.log.utils import banner
from pyats.results import Passed, Failed, Skipped, Passx

# Genie
from genie.harness.libs.prepostprocessor.processors import report

# OSPF
from genie.libs.sdk.apis.iosxe.ospf.get import get_ospf_session_count

# MPLS
from genie.libs.sdk.apis.iosxe.mpls.get import get_mpls_ldp_session_count

# Arp
from genie.libs.sdk.apis.iosxe.arp.get import get_arp_table_count

# Bridge Domain
from genie.libs.sdk.apis.iosxe.bridge_domain.get import (
    get_bridge_domain_bridge_domain_mac_count,
)

# Routing
from genie.libs.sdk.apis.iosxe.routing.get import (
    get_routing_route_count_all_vrf,
)

# BGP
from genie.libs.sdk.apis.iosxe.bgp.get import (
    get_bgp_session_count,
    get_bgp_external_internal_neighbor_count,
)

# Logger
log = logging.getLogger(__name__)


# ==============================================================================
# processor: verify_state
# ==============================================================================


@report
def verify_state(
    section,
    iteration=5,
    interval=60,
    arp_entry_count=10,
    bgp_route_count=1000,
    ldp_neighbor_count=2,
    mac_entry_count=10,
    ospf_neighbor_count=2,
):

    """Trigger Pre-Processor:
        * verify state:
    """

    log.info(banner("processor: 'verify_state'"))

    # Find uut and TGN devices
    dev_name = section.parameters["uut"].name
    uut = section.parameters["testbed"].devices[dev_name]
    tgn_devices = section.parameters["testbed"].find_devices(type="tgn")

    if not tgn_devices:
        log.error("Traffic generator devices not found in testbed YAML")
        section.result = verify_state.result = Failed
        # section.failed(goto=['common_cleanup'])
        return

    for i in range(iteration):
        log.info(
            "Verifying state: attempt {} out of {}".format(i + 1, iteration)
        )

        # Start all protocols
        for dev in tgn_devices:
            try:
                if not dev.is_connected():
                    dev.connect(via="tgn")
                dev.start_all_protocols(wait_time=10)
            except Exception as e:
                section.result = Failed
                log.error(e)
                log.error(
                    "Error while starting all protocols on traffic generator "
                    "device '{}'".format(dev.name)
                )
                log.info(
                    "Verify state failed: sleeping {} seconds before "
                    "retrying.".format(interval)
                )
                time.sleep(interval)
                continue

        # Get count for protocals
        try:
            # Getting BGP session count
            count_bgp = get_bgp_session_count(device=uut)

            # Getting number of internal and external BGP neighbors
            ibgp_neighbor_count, ebgp_neighbor_count = get_bgp_external_internal_neighbor_count(
                device=uut
            )

            # Getting OSPF session count
            count_ospf = get_ospf_session_count(device=uut)

            # Getting LDP neighbor count
            count_mpls = get_mpls_ldp_session_count(device=uut)

            # Getting route count for all vrf
            count_route = get_routing_route_count_all_vrf(uut)

            # Getting MAC count
            count_mac = get_bridge_domain_bridge_domain_mac_count(device=uut)

            # Getting ARP table count
            count_arp = get_arp_table_count(device=uut)
        except Exception as e:
            section.result = Failed
            log.error(e)
            log.info(
                "Verify state failed: sleeping {} seconds before "
                "retrying.".format(interval)
            )
            time.sleep(interval)
            continue

        log.info(
            "Verify BGP session is greater than number of "
            "External BGP neighbors or Internal BGP neighbors"
        )

        if count_bgp < ebgp_neighbor_count or count_bgp < ibgp_neighbor_count:
            section.result = Failed
            log.error(
                "Failed: BGP session count is {} and it is smaller "
                "than the number of external BGP neighbors {} and "
                "internal BGP neighbors {}".format(
                    count_bgp, ebgp_neighbor_count, ibgp_neighbor_count
                )
            )

            log.info(
                "Verify state failed: sleeping {} seconds before "
                "retrying.".format(interval)
            )
            time.sleep(interval)
            continue
        else:
            log.info(
                "Passed: BGP session count is {} and it is greater than "
                "the number of external BGP neighbors {} or "
                "internal BGP neighbors {}".format(
                    count_bgp, ebgp_neighbor_count, ibgp_neighbor_count
                )
            )

        log.info(
            "Verify OSPF session is greater than {}".format(
                ospf_neighbor_count
            )
        )

        if count_ospf < ospf_neighbor_count:
            section.result = Failed
            log.error(
                "Failed: OSPF session count is {} and it is smaller "
                "than minimal {}".format(count_ospf, ospf_neighbor_count)
            )
            log.info(
                "Verify state failed: sleeping {} seconds before "
                "retrying.".format(interval)
            )
            time.sleep(interval)
            continue
        else:
            log.info(
                "Passed: OSPF session count is {} and it is greater than "
                "minimal {}".format(count_ospf, ospf_neighbor_count)
            )

        log.info(
            "Verify LDP session is greater than {}".format(ldp_neighbor_count)
        )

        if count_mpls < ldp_neighbor_count:
            section.result = Failed
            log.error(
                "Failed: LDP session count is {} and it is smaller "
                "than minimal {}".format(count_mpls, ldp_neighbor_count)
            )
            log.info(
                "Verify state failed: sleeping {} seconds before "
                "retrying.".format(interval)
            )
            time.sleep(interval)
            continue
        else:
            log.info(
                "Passed: LDP session count is {} and it is greater than "
                "minimal {}".format(count_mpls, ldp_neighbor_count)
            )

        log.info(
            "Verify route count is greater than {}".format(bgp_route_count)
        )

        if count_route < bgp_route_count:
            section.result = Failed
            log.error(
                "Failed: Route count is {} and it is smaller than "
                "minimal {}".format(count_route, bgp_route_count)
            )
            log.info(
                "Verify state failed: sleeping {} seconds before "
                "retrying.".format(interval)
            )
            time.sleep(interval)
            continue
        else:
            log.info(
                "Passed: Route count is {} and it is greater than "
                "minimal {}".format(count_route, bgp_route_count)
            )

        log.info("Verify MAC count is greater than {}".format(mac_entry_count))

        if count_mac < mac_entry_count:
            section.result = Failed
            log.error(
                "Failed: MAC count is {} and it is smaller than "
                "minimal {}".format(count_mac, mac_entry_count)
            )
            log.info(
                "Verify state failed: sleeping {} seconds before "
                "retrying.".format(interval)
            )
            time.sleep(interval)
            continue
        else:
            log.info(
                "Passed: MAC count is {} and it is greater than minimal {}".format(
                    count_mac, mac_entry_count
                )
            )

        log.info(
            "Verify ARP table count is greater than {}".format(arp_entry_count)
        )

        if count_arp < arp_entry_count:
            section.result = Failed
            log.error(
                "Failed: ARP count is {} and it is smaller than "
                "minimal {}".format(count_arp, arp_entry_count)
            )
            log.info(
                "Verify state failed: sleeping {} seconds before "
                "retrying.".format(interval)
            )
            time.sleep(interval)
            continue
        else:
            log.info(
                "Passed: ARP count is {} and it is greater than minimal {}".format(
                    count_arp, arp_entry_count
                )
            )

        section.result = Passed
        break

    if not section.result:
        verify_state.result = section.result
        # section.failed(goto=['common_cleanup'])
