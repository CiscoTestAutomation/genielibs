#!/usr/bin/env python

#python
import unittest
from unittest.mock import Mock

from genie.conf import Genie
from genie.conf.base import Testbed, Device, Link, Interface
from genie.conf.base.attributes import SubAttributes, \
                                       SubAttributesDict, \
                                       AttributesHelper, \
                                       KeyedSubAttributes

from genie.libs.conf.vlan import Vlan

try:
    from ydk.models.ydkmodels import Cisco_IOS_XR_ifmgr_cfg as xr_ifmgr_cfg
    from ydk.services import CodecService
    from ydk.providers import CodecServiceProvider
    from ydk.types import DELETE, Empty
    from ydk.services import CRUDService

    # patch a netconf provider
    from ydk.providers import NetconfServiceProvider as _NetconfServiceProvider
    from ydk.providers._provider_plugin import _ClientSPPlugin
except:
    pass


class NetconfConnectionInfo(object):
    def __init__(self):
        self.ip = '1.1.1.1'
        self.port = 830
        self.username = 'admin'
        self.password = 'lab'


class test_vlan(unittest.TestCase):

    def test_vlan_interface_configuration(self):
        testbed = Genie.testbed = Testbed()
        dev1 = Device(testbed=testbed, name='PE1', os='iosxr', context='yang')
        dev2 = Device(testbed=testbed, name='PE2', os='iosxr', context='yang')
        intf1 = Interface(name='GigabitEthernet0/0/1',device=dev1, context='yang')
        intf2 = Interface(name='GigabitEthernet0/0/2',device=dev2, context='yang')
        intf3 = Interface(name='GigabitEthernet0/0/3',device=dev1, context='yang')
        link = Link(name='1_2_1',testbed=testbed)
        link.connect_interface(interface=intf1)
        link.connect_interface(interface=intf2)
        vlan = Vlan()

        for dev in testbed.devices:
            dev.connections=Mock()
            dev.connections={'netconf':NetconfConnectionInfo()}

        link.add_feature(vlan)

        vlan.device_attr[dev1]
        vlan.device_attr[dev2]
        vlan.device_attr[dev1].interface_attr[intf1]
        vlan.device_attr[dev1].interface_attr[intf1].eth_encap_type1 = 'dot1q'
        vlan.device_attr[dev1].interface_attr[intf1].eth_encap_val1 = 2
        vlan.device_attr[dev1].interface_attr[intf1].eth_encap_type2 = 'second-dot1q'
        vlan.device_attr[dev1].interface_attr[intf1].eth_encap_val2 = 5

        # Testing can't be done at the moment due to XR models lack on the device.
        # cfg1 = vlan.build_config(apply=False)
        # self.assertCountEqual(cfg1.keys(), ['PE1', 'PE2'])

        # compare = ""
        # for i in cfg1['PE1']: 
        #     compare+=str(i)

        # self.assertMultiLineEqual(compare, '\n'.join([]))

if __name__ == '__main__':
    unittest.main()
