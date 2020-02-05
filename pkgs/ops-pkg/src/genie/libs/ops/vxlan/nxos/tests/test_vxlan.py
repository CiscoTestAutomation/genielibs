# Python
import unittest

# Ats
from pyats.topology import Device
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
                                   ShowFabricMulticastGlobals,\
                                   ShowFabricMulticastIpSaAdRoute,\
                                   ShowFabricMulticastIpL2Mroute,\
                                   ShowNveVniIngressReplication

from genie.libs.parser.nxos.show_feature import ShowFeature
from genie.libs.parser.nxos.show_bgp import ShowBgpL2vpnEvpnSummary,\
                                   ShowBgpL2vpnEvpnRouteType,\
                                   ShowBgpL2vpnEvpnNeighbors,\
                                   ShowBgpIpMvpnRouteType, \
                                   ShowBgpIpMvpnSaadDetail

from genie.libs.parser.nxos.show_mcast import ShowForwardingDistributionMulticastRoute

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

        ####   TRM  ###############
        f.maker.outputs[ShowFabricMulticastGlobals] = {'': VxlanOutput.showFabricMulticastGlobals}
        f.maker.outputs[ShowFabricMulticastIpL2Mroute] = {"{'vni':'all'}": VxlanOutput.showFabricMulticastIpL2Mroute}
        f.maker.outputs[ShowFabricMulticastIpSaAdRoute] = {"{'vrf':'all'}": VxlanOutput.showFabricMulticastIpSaAdRoute}

        f.maker.outputs[ShowForwardingDistributionMulticastRoute] = \
            {"{'vrf':'all'}":VxlanOutput.showForwardingDistributionMulticastRoute}

        bgp_mvpn_route_1 = {"{'route_type':'1','vrf':'all'}": VxlanOutput.showBgpIpMvpnRouteType_1}
        bgp_mvpn_route_2 = {"{'route_type':'2','vrf':'all'}": VxlanOutput.showBgpIpMvpnRouteType_2}
        bgp_mvpn_route_3 = {"{'route_type':'3','vrf':'all'}": VxlanOutput.showBgpIpMvpnRouteType_3}
        bgp_mvpn_route_4 = {"{'route_type':'4','vrf':'all'}": VxlanOutput.showBgpIpMvpnRouteType_4}
        bgp_mvpn_route_5 = {"{'route_type':'5','vrf':'all'}": VxlanOutput.showBgpIpMvpnRouteType_5}
        bgp_mvpn_route_6 = {"{'route_type':'6','vrf':'all'}": VxlanOutput.showBgpIpMvpnRouteType_6}
        bgp_mvpn_route_7 = {"{'route_type':'7','vrf':'all'}": VxlanOutput.showBgpIpMvpnRouteType_7}

        bgp_mvpn_route_type = bgp_mvpn_route_1.copy()
        bgp_mvpn_route_type.update(bgp_mvpn_route_2)
        bgp_mvpn_route_type.update(bgp_mvpn_route_3)
        bgp_mvpn_route_type.update(bgp_mvpn_route_4)
        bgp_mvpn_route_type.update(bgp_mvpn_route_5)
        bgp_mvpn_route_type.update(bgp_mvpn_route_6)
        bgp_mvpn_route_type.update(bgp_mvpn_route_7)
        f.maker.outputs[ShowBgpIpMvpnRouteType] = bgp_mvpn_route_type

        f.maker.outputs[ShowBgpIpMvpnSaadDetail] = {"{'vrf':'all'}": VxlanOutput.showBgpIpMvpnSaadDetail}

        self.device.execute = Mock()
        # Learn the feature
        f.learn()

        self.maxDiff = None
        self.assertEqual(f.nve, VxlanOutput.vxlanVniOpsOutput)
        self.assertEqual(f.l2route, VxlanOutput.vxlanL2routeOpsOutput)
        self.assertEqual(f.bgp_l2vpn_evpn, VxlanOutput.vxlanBgpL2vpnEvpnOpsOutput)
        self.assertEqual(f.fabric, VxlanOutput.fabricOpsOutput)
        self.assertEqual(f.forwarding, VxlanOutput.forwardingOpsOutput)
        self.assertEqual(f.bgp_mvpn, VxlanOutput.bgpMvpnOpsOutput)

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

        ####   TRM  ###############
        f.maker.outputs[ShowFabricMulticastGlobals] = {'': VxlanOutput.showFabricMulticastGlobals}
        f.maker.outputs[ShowFabricMulticastIpL2Mroute] = {"{'vni':'all'}": VxlanOutput.showFabricMulticastIpL2Mroute}
        f.maker.outputs[ShowFabricMulticastIpSaAdRoute] = {"{'vrf':'all'}": VxlanOutput.showFabricMulticastIpSaAdRoute}

        f.maker.outputs[ShowForwardingDistributionMulticastRoute] = \
            {"{'vrf':'all'}": VxlanOutput.showForwardingDistributionMulticastRoute}

        bgp_mvpn_route_1 = {"{'route_type':'1','vrf':'all'}": VxlanOutput.showBgpIpMvpnRouteType_1}
        bgp_mvpn_route_2 = {"{'route_type':'2','vrf':'all'}": VxlanOutput.showBgpIpMvpnRouteType_2}
        bgp_mvpn_route_3 = {"{'route_type':'3','vrf':'all'}": VxlanOutput.showBgpIpMvpnRouteType_3}
        bgp_mvpn_route_4 = {"{'route_type':'4','vrf':'all'}": VxlanOutput.showBgpIpMvpnRouteType_4}
        bgp_mvpn_route_5 = {"{'route_type':'5','vrf':'all'}": VxlanOutput.showBgpIpMvpnRouteType_5}
        bgp_mvpn_route_6 = {"{'route_type':'6','vrf':'all'}": VxlanOutput.showBgpIpMvpnRouteType_6}
        bgp_mvpn_route_7 = {"{'route_type':'7','vrf':'all'}": VxlanOutput.showBgpIpMvpnRouteType_7}

        bgp_mvpn_route_type = bgp_mvpn_route_1.copy()
        bgp_mvpn_route_type.update(bgp_mvpn_route_2)
        bgp_mvpn_route_type.update(bgp_mvpn_route_3)
        bgp_mvpn_route_type.update(bgp_mvpn_route_4)
        bgp_mvpn_route_type.update(bgp_mvpn_route_5)
        bgp_mvpn_route_type.update(bgp_mvpn_route_6)
        bgp_mvpn_route_type.update(bgp_mvpn_route_7)
        f.maker.outputs[ShowBgpIpMvpnRouteType] = bgp_mvpn_route_type

        f.maker.outputs[ShowBgpIpMvpnSaadDetail] = {"{'vrf':'all'}": VxlanOutput.showBgpIpMvpnSaadDetail}

        # Learn the feature
        f.learn()
        # Check match

        self.assertEqual('0300.0000.0001.2c00.0309', f.l2route['evpn']['ethernet_segment'][1]['ethernet_segment'])
        self.assertEqual(4, f.bgp_l2vpn_evpn['instance']['default']['vrf']['default']['address_family']\
            ['l2vpn evpn']['neighbor']['172.16.205.8']['version'])
        self.assertEqual('up',f.nve['nve1']['peer_ip']['192.168.16.1']['peer_state'])

        self.assertNotEqual('0300.0000.0309.1265', f.l2route['evpn']['ethernet_segment'][1]['ethernet_segment'])
        self.assertNotEqual(5, f.bgp_l2vpn_evpn['instance']['default']['vrf']['default']['address_family'] \
            ['l2vpn evpn']['neighbor']['172.16.205.8']['version'])
        self.assertNotEqual('down', f.nve['nve1']['peer_ip']['192.168.16.1']['peer_state'])

        self.assertNotEqual('50', f.fabric['multicast']['vrf']['vni_10100']['address_family']['ipv4']\
            ['sa_ad_routes']['gaddr']['238.8.4.101/32'])

        self.assertNotEqual('PC', f.forwarding['distribution']['multicast']['route']['vrf']['default']['address_family']['ipv4']\
            ['gaddr']['224.0.0.0/4']['saddr']['*']['flags'])

        self.assertNotEqual(False,
                            f.bgp_mvpn['instance']['default']['vrf']['default']['address_family'][
                                'ipv4 mvpn'] \
                                ['rd']['10.16.2.2:3']['prefix']['[1][10.111.1.3][238.8.4.101]/64']['on_xmitlist'])

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

        ####   TRM  ###############
        f.maker.outputs[ShowFabricMulticastGlobals] = {'': {}}
        f.maker.outputs[ShowFabricMulticastIpL2Mroute] = {"{'vni':'all'}": {}}
        f.maker.outputs[ShowFabricMulticastIpSaAdRoute] = {"{'vrf':'all'}":{}}

        f.maker.outputs[ShowForwardingDistributionMulticastRoute] = \
            {"{'vrf':'all'}": {}}

        bgp_mvpn_route_1 = {"{'route_type':'1','vrf':'all'}": {}}
        bgp_mvpn_route_2 = {"{'route_type':'2','vrf':'all'}": {}}
        bgp_mvpn_route_3 = {"{'route_type':'3','vrf':'all'}": {}}
        bgp_mvpn_route_4 = {"{'route_type':'4','vrf':'all'}": {}}
        bgp_mvpn_route_5 = {"{'route_type':'5','vrf':'all'}": {}}
        bgp_mvpn_route_6 = {"{'route_type':'6','vrf':'all'}": {}}
        bgp_mvpn_route_7 = {"{'route_type':'7','vrf':'all'}": {}}

        bgp_mvpn_route_type = bgp_mvpn_route_1.copy()
        bgp_mvpn_route_type.update(bgp_mvpn_route_2)
        bgp_mvpn_route_type.update(bgp_mvpn_route_3)
        bgp_mvpn_route_type.update(bgp_mvpn_route_4)
        bgp_mvpn_route_type.update(bgp_mvpn_route_5)
        bgp_mvpn_route_type.update(bgp_mvpn_route_6)
        bgp_mvpn_route_type.update(bgp_mvpn_route_7)
        f.maker.outputs[ShowBgpIpMvpnRouteType] = bgp_mvpn_route_type

        f.maker.outputs[ShowBgpIpMvpnSaadDetail] = {"{'vrf':'all'}": {}}

        # Learn the feature
        f.learn()

        # Check no attribute not found
        with self.assertRaises(AttributeError):
            f.nve['instance']
            f.bgp_l2vpn_evpn['instance']
            f.bgp_mvpn['instance']
            f.forwarding['distribution']
            f.fabric['multicast']


if __name__ == '__main__':
    unittest.main()
