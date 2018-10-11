# Python
import unittest

# Ats
from ats.topology import Device
from unittest.mock import Mock

from genie.libs.ops.vxlan.nxos.vxlan import Vxlan
from genie.libs.ops.vxlan.nxos.tests.vxlan_output import VxlanOutput

from genie.libs.parser.nxos.show_vxlan import ShowNvePeers,\
                                   ShowNveInterfaceDetail,\
                                   ShowNveEthernetSegment,\
                                   ShowNveVni,\
                                   ShowNveVniSummary,\
                                   ShowNveMultisiteDciLinks,\
                                   ShowNveMultisiteFabricLinks, \
                                   ShowL2routeEvpnEternetSegmentAll, \
                                   ShowL2routeTopologyDetail, \
                                   ShowL2routeMacAllDetail, \
                                   ShowL2routeMacIpAllDetail, \
                                   ShowL2routeSummary,\
                                   ShowL2routeFlAll,\
                                   ShowRunningConfigNvOverlay,\
                                   ShowNveVniIngressReplication

from genie.libs.parser.nxos.show_feature import ShowFeature
from genie.libs.parser.nxos.show_bgp import ShowBgpL2vpnEvpnSummary,\
                                   ShowBgpL2vpnEvpnRouteType,\
                                   ShowBgpL2vpnEvpnNeighbors

class test_vxlan_all(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'nxos'
        self.device.mapping={}
        self.device.mapping['cli']='cli'
        self.device.connectionmgr.connections['cli'] = '5'

    def test_full_vni_vxlan(self):
        f = Vxlan(device=self.device)

        f.maker.outputs[ShowFeature] = {'': VxlanOutput.showFeature}
        f.maker.outputs[ShowBgpL2vpnEvpnSummary] = {'': VxlanOutput.showBgpL2vpnEvpnSummary}
        f.maker.outputs[ShowNveVniSummary] = {'': VxlanOutput.showNveVniSummary}
        f.maker.outputs[ShowNveInterfaceDetail] = {"{'intf':'nve1'}": VxlanOutput.showNveInterfaceDetail}
        f.maker.outputs[ShowNvePeers] = {'': VxlanOutput.showNvePeers}
        f.maker.outputs[ShowNveEthernetSegment] = {'': VxlanOutput.showNveEthernetSegment}
        f.maker.outputs[ShowNveVni] = {'': VxlanOutput.showNveVni}
        f.maker.outputs[ShowNveMultisiteDciLinks] = {'': VxlanOutput.showNveMultisiteDciLinks}
        f.maker.outputs[ShowNveMultisiteFabricLinks] = {'': VxlanOutput.showNveMultisiteFabricLinks}
        f.maker.outputs[ShowRunningConfigNvOverlay] = {'': VxlanOutput.showRunningConfigNvOverlay}
        f.maker.outputs[ShowNveVniIngressReplication] = {'': VxlanOutput.showNveVniIngressReplication}

        f.maker.outputs[ShowL2routeEvpnEternetSegmentAll] = {'': VxlanOutput.showL2routeEvpnEternetSegmentAll}
        f.maker.outputs[ShowL2routeFlAll] = {'': VxlanOutput.showL2routeFlAll}
        f.maker.outputs[ShowL2routeTopologyDetail] = {'': VxlanOutput.showL2routeTopologyDetail}
        f.maker.outputs[ShowL2routeMacAllDetail] = {'': VxlanOutput.showL2routeMacAllDetail}
        f.maker.outputs[ShowL2routeMacIpAllDetail] = {'': VxlanOutput.showL2routeMacIpAllDetail}
        f.maker.outputs[ShowL2routeSummary] = {'': VxlanOutput.showL2routeSummary}


        f.maker.outputs[ShowBgpL2vpnEvpnNeighbors] = {'': VxlanOutput.showBgpL2vpnEvpnNeighbors}

        route_1 = {"{'route_type':'1'}": VxlanOutput.showBgpL2vpnEvpnRouteType_1}
        route_2 = {"{'route_type':'2'}": VxlanOutput.showBgpL2vpnEvpnRouteType_2}
        route_3 = {"{'route_type':'3'}": VxlanOutput.showBgpL2vpnEvpnRouteType_3}
        route_4 = {"{'route_type':'4'}": VxlanOutput.showBgpL2vpnEvpnRouteType_4}

        route_type = route_1.copy()
        route_type.update(route_2)
        route_type.update(route_3)
        route_type.update(route_4)
        f.maker.outputs[ShowBgpL2vpnEvpnRouteType] = route_type

        self.device.execute = Mock()
        # Learn the feature
        f.learn()

        self.maxDiff = None
        self.assertEqual(f.nve, VxlanOutput.vxlanVniOpsOutput)
        self.assertEqual(f.l2route, VxlanOutput.vxlanL2routeOpsOutput)
        self.assertEqual(f.bgp_l2vpn_evpn, VxlanOutput.vxlanBgpL2vpnEvpnOpsOutput)


    def test_selective_attribute_vxlan(self):
        f = Vxlan(device=self.device)
        f.maker.outputs[ShowFeature] = {'': VxlanOutput.showFeature}
        f.maker.outputs[ShowNveVniSummary] = {'': VxlanOutput.showNveVniSummary}
        f.maker.outputs[ShowNveInterfaceDetail] = {"{'intf':'nve1'}": VxlanOutput.showNveInterfaceDetail}
        f.maker.outputs[ShowNvePeers] = {'': VxlanOutput.showNvePeers}
        f.maker.outputs[ShowNveEthernetSegment] = {'': VxlanOutput.showNveEthernetSegment}
        f.maker.outputs[ShowNveVni] = {'': VxlanOutput.showNveVni}
        f.maker.outputs[ShowNveMultisiteDciLinks] = {'': VxlanOutput.showNveMultisiteDciLinks}
        f.maker.outputs[ShowNveMultisiteFabricLinks] = {'': VxlanOutput.showNveMultisiteFabricLinks}
        f.maker.outputs[ShowRunningConfigNvOverlay] = {'': VxlanOutput.showRunningConfigNvOverlay}
        f.maker.outputs[ShowNveVniIngressReplication] = {'': VxlanOutput.showNveVniIngressReplication}

        f.maker.outputs[ShowL2routeEvpnEternetSegmentAll] = {'': VxlanOutput.showL2routeEvpnEternetSegmentAll}
        f.maker.outputs[ShowL2routeFlAll] = {'': VxlanOutput.showL2routeFlAll}
        f.maker.outputs[ShowL2routeTopologyDetail] = {'': VxlanOutput.showL2routeTopologyDetail}
        f.maker.outputs[ShowL2routeMacAllDetail] = {'': VxlanOutput.showL2routeMacAllDetail}
        f.maker.outputs[ShowL2routeMacIpAllDetail] = {'': VxlanOutput.showL2routeMacIpAllDetail}
        f.maker.outputs[ShowL2routeSummary] = {'': VxlanOutput.showL2routeSummary}

        f.maker.outputs[ShowBgpL2vpnEvpnSummary] = {'': VxlanOutput.showBgpL2vpnEvpnSummary}
        f.maker.outputs[ShowBgpL2vpnEvpnNeighbors] = {'': VxlanOutput.showBgpL2vpnEvpnNeighbors}

        route_1 = {"{'route_type':'1'}": VxlanOutput.showBgpL2vpnEvpnRouteType_1}
        route_2 = {"{'route_type':'2'}": VxlanOutput.showBgpL2vpnEvpnRouteType_2}
        route_3 = {"{'route_type':'3'}": VxlanOutput.showBgpL2vpnEvpnRouteType_3}
        route_4 = {"{'route_type':'4'}": VxlanOutput.showBgpL2vpnEvpnRouteType_4}

        route_type = route_1.copy()
        route_type.update(route_2)
        route_type.update(route_3)
        route_type.update(route_4)
        f.maker.outputs[ShowBgpL2vpnEvpnRouteType] = route_type
        # Learn the feature
        f.learn()
        # Check match

        self.assertEqual('0300.0000.0001.2c00.0309', f.l2route['evpn']['ethernet_segment'][1]['ethernet_segment'])
        self.assertEqual(4, f.bgp_l2vpn_evpn['instance']['default']['vrf']['default']['address_family']\
            ['l2vpn evpn']['neighbor']['191.13.1.8']['version'])
        self.assertEqual('up',f.nve['nve1']['peer_ip']['201.202.1.1']['peer_state'])

        self.assertNotEqual('0300.0000.0309.1265', f.l2route['evpn']['ethernet_segment'][1]['ethernet_segment'])
        self.assertNotEqual(5, f.bgp_l2vpn_evpn['instance']['default']['vrf']['default']['address_family'] \
            ['l2vpn evpn']['neighbor']['191.13.1.8']['version'])
        self.assertNotEqual('down', f.nve['nve1']['peer_ip']['201.202.1.1']['peer_state'])

    def test_empty_output_vxlan(self):
        self.maxDiff = None
        f = Vxlan(device=self.device)

        # Get outputs
        f.maker.outputs[ShowFeature] = {'': {}}
        f.maker.outputs[ShowNveVniSummary] = {'':{}}
        f.maker.outputs[ShowNveInterfaceDetail] = {"{'intf':'nve1'}": {}}
        f.maker.outputs[ShowNvePeers] = {'': {}}
        f.maker.outputs[ShowNveEthernetSegment] = {'': {}}
        f.maker.outputs[ShowNveVni] = {'': {}}
        f.maker.outputs[ShowNveMultisiteDciLinks] = {'': {}}
        f.maker.outputs[ShowNveMultisiteFabricLinks] = {'':{}}
        f.maker.outputs[ShowRunningConfigNvOverlay] = {'': {}}
        f.maker.outputs[ShowNveVniIngressReplication] = {'': {}}

        f.maker.outputs[ShowL2routeEvpnEternetSegmentAll] = {'': {}}
        f.maker.outputs[ShowL2routeFlAll] = {'': {}}
        f.maker.outputs[ShowL2routeTopologyDetail] = {'': {}}
        f.maker.outputs[ShowL2routeMacAllDetail] = {'': {}}
        f.maker.outputs[ShowL2routeMacIpAllDetail] = {'': {}}
        f.maker.outputs[ShowL2routeSummary] = {'': {}}

        f.maker.outputs[ShowBgpL2vpnEvpnSummary] = {'': {}}
        f.maker.outputs[ShowBgpL2vpnEvpnNeighbors] = {'': {}}
        route_1 = {"{'route_type':'1'}": {}}
        route_2 = {"{'route_type':'2'}": {}}
        route_3 = {"{'route_type':'3'}": {}}
        route_4 = {"{'route_type':'4'}": {}}

        route_type = route_1.copy()
        route_type.update(route_2)
        route_type.update(route_3)
        route_type.update(route_4)
        f.maker.outputs[ShowBgpL2vpnEvpnRouteType] = route_type
        # Learn the feature
        f.learn()

        # Check no attribute not found
        with self.assertRaises(AttributeError):
            f.nve['instance']
            f.bgp_l2vpn_evpn['instance']

if __name__ == '__main__':
    unittest.main()
