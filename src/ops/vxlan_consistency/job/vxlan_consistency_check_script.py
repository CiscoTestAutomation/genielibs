#!/bin/env python
###############################################################################
# vxlan_consistency_check.py : A very simple test script example which include:
#     common_setup
#     Tescases
#     common_cleanup
# The purpose of this test script is to verify the Vxlan Consistency as per the
# user instructions.
###############################################################################

# To get a logger for the script
import logging

# To build the table at the end
from tabulate import tabulate

# Needed for aetest script
from ats import aetest

# Import ConnectionPool
from ats.connections.pool import ConnectionPool

from unicon import Unicon
# Genie Imports
# Pre-processor to set Genie harness information.
from genie.harness.standalone import genie_parameters
from genie.conf import Genie

# Genie.libs.ops
from genie.libs.ops.vxlan_consistency.nxos.vxlan_consistency import VxlanConsistency

# Get your logger for your script
log = logging.getLogger(__name__)


###################################################################
###                  COMMON SETUP SECTION                       ###
###################################################################

class common_setup(aetest.CommonSetup):
    """ Common Setup section """

    @aetest.subsection
    def connect(self, testbed, MAX_POOL_SIZE = 31):
        genie_testbed = Genie.init(testbed)
        self.parent.parameters['testbed'] = genie_testbed
        uut = genie_testbed.devices['uut']

        # Create a connection pool
        if hasattr(testbed, 'custom') and hasattr(testbed.custom, 'MAX_POOL_SIZE'):
            MAX_POOL_SIZE = testbed.custom.MAX_POOL_SIZE

        uut.start_pool(alias='pool',size=MAX_POOL_SIZE)

        # A Connection pool workers need to have genie attributes to be able to
        # call ops
        for worker in uut.pool.workers:
            worker.mapping = {}
            worker.mapping['cli'] = 'vty'
            worker.cli = worker

        # Pass 'uut' to testcases
        self.parent.parameters.update(dev=uut)

###################################################################
###                     TESTCASES SECTION                       ###
###################################################################

# Testcase name : vxlan_consistency_check
class vxlan_consistency_check(aetest.Testcase):
    """ This is user Testcases section """

    # First test section
    @ aetest.test
    def learn_ops(self):
        """ Sample test section. Only print """

        log.info("Instantiate the Ops object")

        # Instantiate the Ops object and learn it
        # Has to pass the workers since uut.pool is not available
        self.parameters['Vxlan_ops'] = VxlanConsistency(
            device=self.parent.parameters['dev'].pool)

        log.info("Learn the ops object")
        self.parameters['Vxlan_ops'].learn(intf='nve1')
        log.info("Here is the built Ops object;")
        log.info(self.parameters['Vxlan_ops'].info)

    # Second test section
    @ aetest.test
    def check_consistency_remote(self):
        """ Sample test section. Only print """

        log.info("Print the learnt output")
        mega_tabular = []
        tabular = []
        passed = 0
        failed = 0
        for vni in self.parameters['Vxlan_ops'].info['interface']['nve1']['member_vni']:

            # Append the Vni row to the mega_tabular to be tabulated at the end
            if tabular:
                mega_tabular.append(tabular)

            # Need to clear the list before appending second vni
            tabular = []
            tabular.append(vni)
            if 'remote' in self.parameters['Vxlan_ops'].info['interface']\
                ['nve1']['member_vni'][vni]:
                for mac in self.parameters['Vxlan_ops'].info['interface']\
                    ['nve1']['member_vni'][vni]['remote']['mac_address']:
                    if not len(tabular) == 1:
                        # Case of same Vni member and different mac address,
                        # we need to create a new result entry(row)
                        mega_tabular.append(tabular)
                        tabular = []
                        tabular.append(vni)
                    tabular.append(mac)
                    for topo in self.parameters['Vxlan_ops'].info['interface']\
                        ['nve1']['member_vni'][vni]['remote']['mac_address']\
                        [mac]['topology']:
                        next_hop = self.parameters['Vxlan_ops'].info['interface']\
                            ['nve1']['member_vni'][vni]['remote']['mac_address']\
                            [mac]['topology'][topo]['next_hop']
                        prod = self.parameters['Vxlan_ops'].info['interface']\
                            ['nve1']['member_vni'][vni]['remote']['mac_address']\
                            [mac]['topology'][topo]['prod']
                        tabular.append(next_hop)
                        tabular.append(prod)

                    if 'verified_structure' in self.parameters['Vxlan_ops'].info['interface']\
                        ['nve1']['member_vni'][vni]['remote']:
                        verified_next_hop = self.parameters['Vxlan_ops'].info['interface']\
                            ['nve1']['member_vni'][vni]['remote']['verified_structure']\
                            ['mac_address'][mac]['next_hop']
                        received_label = self.parameters['Vxlan_ops'].info['interface']\
                            ['nve1']['member_vni'][vni]['remote']['verified_structure']\
                            ['mac_address'][mac]['received_label']
                        tabular.append(verified_next_hop)
                        tabular.append(received_label)

                        if verified_next_hop == next_hop and received_label == vni:
                            tabular.append('Passed')
                            passed += 1
                        else:
                            tabular.append('Failed')
                            failed += 1
                    else:
                        # Vni member doesn't have any host
                        verified_next_hop = 'N/A'
                        tabular.append(verified_next_hop)
                        received_label = 'N/A'
                        tabular.append(received_label)
                        tabular.append("VxLAN checker N/A")

            if len(tabular) == 1:
                # Case where there is no 'remote' built for that vni member in the ops
                mac = 'N/A'
                tabular.append(mac)
                next_hop = 'N/A'
                tabular.append(next_hop)
                prod = 'N/A'
                tabular.append(prod)
                verified_next_hop = 'N/A'
                tabular.append(verified_next_hop)
                received_label = 'N/A'
                tabular.append(received_label)
                tabular.append("VxLAN checker N/A")

        # Append last item in the for loop
        mega_tabular.append(tabular)

        # Statisitics
        try:
            total = passed + failed
            percentage = (passed*100) / total
        except:
            percentage = 0

        mega_tabular.append(['','','','','','Total pass percentage',percentage])

        # Show the Vxlan consistency check in a table
        log.info('Here is the Remote Vxlan Consistency Check table;')
        log.info(tabulate(mega_tabular,
            headers=['VNI', 'MAC Address', 'Next Hop (L2RIB)', 'Prod',
                     'Next Hop (BGP EVPN) ', 'Received Label (BGP EVPN)', 'Verified (Passed %)'],
            tablefmt='orgtbl'))

    # Second test section
    @ aetest.test
    def check_consistency_local(self):
        """ Sample test section. Only print """

        log.info("Print the learnt output")
        mega_tabular = []
        tabular = []
        passed = 0
        failed = 0
        for vni in self.parameters['Vxlan_ops'].info['interface']['nve1']['member_vni']:

            # Append the Vni row to the mega_tabular to be tabulated at the end
            if tabular:
                mega_tabular.append(tabular)

            # Need to clear the list before appending second vni
            tabular = []
            tabular.append(vni)
            if 'local' in self.parameters['Vxlan_ops'].info['interface']\
                ['nve1']['member_vni'][vni]:
                for mac in self.parameters['Vxlan_ops'].info['interface']\
                    ['nve1']['member_vni'][vni]['local']['mac_address']:
                    if not len(tabular) == 1:
                        # Case of same Vni member and different mac address,
                        # we need to create a new result entry(row)
                        mega_tabular.append(tabular)
                        tabular = []
                        tabular.append(vni)
                    tabular.append(mac)
                    next_hop_mac_table = self.parameters['Vxlan_ops'].info['interface']\
                        ['nve1']['member_vni'][vni]['local']['mac_address']\
                        [mac]['next_hop']
                    tabular.append(next_hop_mac_table)
                    if 'topology' in self.parameters['Vxlan_ops'].info['interface']\
                        ['nve1']['member_vni'][vni]['local']['mac_address']\
                        [mac]:

                        for topo in self.parameters['Vxlan_ops'].info['interface']\
                            ['nve1']['member_vni'][vni]['local']['mac_address']\
                            [mac]['topology']:
                            next_hop_l2rib = self.parameters['Vxlan_ops'].info['interface']\
                                ['nve1']['member_vni'][vni]['local']['mac_address']\
                                [mac]['topology'][topo]['next_hop']
                            prod_l2rib = self.parameters['Vxlan_ops'].info['interface']\
                                ['nve1']['member_vni'][vni]['local']['mac_address']\
                                [mac]['topology'][topo]['prod']
                            tabular.append(next_hop_l2rib)
                            tabular.append(prod_l2rib)

                        for intf in self.parameters['Vxlan_ops'].info['interface']['nve1']['member_vni']\
                            [vni]['local']['verified_structure']['source_interface'].keys():
                            primary = self.parameters['Vxlan_ops'].info['interface']['nve1']['member_vni']\
                                [vni]['local']['verified_structure']['source_interface'][intf]['primary']
                            secondary = self.parameters['Vxlan_ops'].info['interface']['nve1']['member_vni']\
                                [vni]['local']['verified_structure']['source_interface'][intf]['secondary']

                        for vpc in self.parameters['Vxlan_ops'].info['interface']['nve1']['member_vni']\
                            [vni]['local']['verified_structure']['vpc_capability'].keys():
                            notified = self.parameters['Vxlan_ops'].info['interface']['nve1']['member_vni']\
                                [vni]['local']['verified_structure']['vpc_capability'][vpc]['notified']

                            if notified == True:
                                NVE_Source_IP = secondary
                            else:
                                NVE_Source_IP = primary

                        tabular.append(NVE_Source_IP)

                        next_hop_bgp_evpn = self.parameters['Vxlan_ops'].info['interface']\
                            ['nve1']['member_vni'][vni]['local']['verified_structure']\
                            ['mac_address'][mac]['next_hop']
                        received_label = self.parameters['Vxlan_ops'].info['interface']\
                            ['nve1']['member_vni'][vni]['local']['verified_structure']\
                            ['mac_address'][mac]['received_label']
                        tabular.append(next_hop_bgp_evpn)
                        tabular.append(received_label)

                        if next_hop_mac_table == next_hop_l2rib and prod_l2rib == 'Local' and \
                            received_label == vni and NVE_Source_IP == next_hop_bgp_evpn:
                            tabular.append('Passed')
                            passed += 1
                        else:
                            tabular.append('Failed')
                            failed += 1
                    else:
                        # Vni member doesn't have any host
                        next_hop_mac_table = 'N/A'
                        tabular.append(next_hop_mac_table)
                        next_hop_l2rib = 'N/A'
                        tabular.append(next_hop_l2rib)
                        prod_l2rib = 'N/A'
                        tabular.append(prod_l2rib)
                        NVE_Source_IP = 'N/A'
                        tabular.append(NVE_Source_IP)
                        next_hop_bgp_evpn = 'N/A'
                        tabular.append(next_hop_bgp_evpn)
                        received_label = 'N/A'
                        tabular.append(received_label)
                        tabular.append("Checker N/A")

            if len(tabular) == 1:
                # Case where there is no 'remote' built for that vni member in the ops
                mac = 'N/A'
                tabular.append(mac)
                next_hop_mac_table = 'N/A'
                tabular.append(next_hop_mac_table)
                next_hop_l2rib = 'N/A'
                tabular.append(next_hop_l2rib)
                prod_l2rib = 'N/A'
                tabular.append(prod_l2rib)
                NVE_Source_IP = 'N/A'
                tabular.append(NVE_Source_IP)
                next_hop_bgp_evpn = 'N/A'
                tabular.append(next_hop_bgp_evpn)
                received_label = 'N/A'
                tabular.append(received_label)
                tabular.append("Checker N/A")

        # Append last item in the for loop
        mega_tabular.append(tabular)

        # Statisitics
        try:
            total = passed + failed
            percentage = (passed*100) / total
        except:
            percentage = 0
            print('Passed = {}'.format(passed))
            print('Failed = {}'.format(failed))
            print('Total = {}'.format(total))

        mega_tabular.append(['','','','','','','','Total pass percentage',percentage])

        # Show the Vxlan consistency check in a table
        log.info('Here is the Local Vxlan Consistency Check table;')
        log.info(tabulate(mega_tabular,
            headers=['VNI', 'MAC Address', 'NextHop(MAC_table)', 'NextHop(L2RIB)', 'Prod(L2RIB)', 'NVE Source IP',
                     'NextHop(BGP EVPN) ', 'Rcvd Label(BGP EVPN)', 'Verified(Pass%)'],
            tablefmt='orgtbl'))

# #####################################################################
# ####                       COMMON CLEANUP SECTION                 ###
# #####################################################################

class common_cleanup(aetest.CommonCleanup):
    """ Common Cleanup for Sample Test """

    @aetest.subsection
    def clean_everything(self):
        """ Common Cleanup Subsection """
        log.info("Aetest Common Cleanup ")

if __name__ == '__main__': # pragma: no cover
    aetest.main()
