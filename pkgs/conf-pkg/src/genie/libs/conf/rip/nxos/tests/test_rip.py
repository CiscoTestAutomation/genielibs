#!/usr/bin/env python

# Import unittest module
import unittest
from unittest.mock import Mock

from pyats.datastructures import WeakList

# And import what's needed
from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device, Link, Interface
from genie.conf.base.attributes import SubAttributesDict

from genie.libs.conf.rip import Rip
from genie.libs.conf.vrf import Vrf
from genie.libs.conf.address_family import AddressFamily

class test_rip(TestCase):

    def test_init(self):
        tb = Genie.testbed = Testbed()
        dev = Device(testbed=tb, name='PE1', os='nxos')
        rip = Rip(instance_id=10)
        rip.add_force_vrf(None)
        dev.add_feature(rip)
        vrf = Vrf(name='myVrf')
        dev.add_feature(vrf)
        self.assertEqual(rip.instance_id, 10)
        self.assertTrue(isinstance(rip.device_attr, SubAttributesDict))
        self.assertTrue(isinstance(rip.device_attr['dev1'].vrf_attr[None].address_family_attr,
                                   SubAttributesDict))

        # Let's try multilevel
        rip.mega = 'work'
        rip.device_attr['myDevice'].value = 'success'
        rip.device_attr['myDevice'].vrf_attr[None].address_family_attr['ipv4 unicast'].maximum_paths = 3
        rip.device_attr['myDevice'].vrf_attr['myVrf'].\
            address_family_attr['ipv6 unicast'].distance = 120

        self.assertEqual(rip.device_attr['myDevice'].vrf_attr['myVrf'].\
                         address_family_attr['ipv6 unicast'].distance, 120)

        self.assertEqual(rip.mega, 'work')
        self.assertEqual(rip.device_attr['myDevice'].mega, 'work')
        self.assertEqual(rip.device_attr['fake'].mega, 'work')
        self.assertEqual(
            rip.device_attr['myDevice'].vrf_attr[None].address_family_attr['ipv4 unicast'].mega, 'work')
        self.assertEqual(
            rip.device_attr['myDevice'].vrf_attr[None].address_family_attr['ipv6 unicast'].mega, 'work')

        self.assertEqual(rip.device_attr['myDevice'].value, 'success')
        self.assertEqual(
            rip.device_attr['myDevice'].vrf_attr[None].address_family_attr['ipv4 unicast'].value,
            'success')
        self.assertEqual(
            rip.device_attr['myDevice'].vrf_attr[None].address_family_attr['ipv6 unicast'].value,
            'success')

        self.assertEqual(
            rip.device_attr['myDevice'].vrf_attr[None].address_family_attr['ipv4 unicast'].maximum_paths,
            3)

        with self.assertRaises(AttributeError):
            rip.value

        with self.assertRaises(ValueError):
            rip.device_attr['myDevice'].vrf_attr[None].address_family_attr['ipv8'].value,'success'
        with self.assertRaises(KeyError):
            rip.device_attr['myDevice'].vrf_attr[None].address_family_attr['ipv6 flowspec'].value,'success'

        self.assertEqual(\
                rip.device_attr['myDevice'].vrf_attr[None].address_family_attr['ipv6 unicast'].maximum_paths, None)

        # Test unknown argument which is not defined in rip object or its
        # parent
        with self.assertRaises(AttributeError):
            rip.device_attr['myDevice'].ff



    def test_cfg(self):

        tb = Genie.testbed = Testbed()
        dev = Device(testbed=tb, name='PE1', os='nxos')

        rip = Rip(instance_id=1)
        rip.add_force_vrf(None)
        dev.add_feature(rip)
        rip.device_attr['PE1']

        output = rip.build_config(apply=False)

        self.assertMultiLineDictEqual(output, {'PE1':
            'feature rip\n'
            'router rip 1\n'
            ' address-family ipv4 unicast\n'
            '  exit\n'
            ' exit'
            })

        vrf1 = Vrf('vrf1')
        intf1 = Interface(device=dev, name='Ethernet0/0', vrf=vrf1)
        intf1.add_feature(rip)
        rip.address_families |= {AddressFamily.ipv6_unicast}
        rip.shutdown = False
        rip.device_attr['PE1'].vrf_attr[None].address_family_attr['ipv4 unicast'].maximum_paths = 2
        rip.device_attr['PE1'].vrf_attr[None].address_family_attr['ipv4 unicast'].default_metric = 1
        rip.device_attr['PE1'].vrf_attr[None].address_family_attr['ipv4 unicast'].distance = 120
        rip.device_attr['PE1'].vrf_attr[None].address_family_attr['ipv4 unicast'].redistribute_direct_rmap\
            = 'rmap1'
        rip.device_attr['PE1'].vrf_attr[None].address_family_attr['ipv4 unicast'].redistribute_static_rmap\
            = 'rmap2'
        rip.device_attr['PE1'].vrf_attr[None].address_family_attr['ipv4 unicast'].redistribute_lisp_rmap\
            = 'rmap3'
        rip.device_attr['PE1'].vrf_attr[None].address_family_attr['ipv6 unicast'].maximum_paths = 7
        rip.device_attr['PE1'].vrf_attr[None].address_family_attr['ipv6 unicast'].default_metric = 3
        rip.device_attr['PE1'].vrf_attr[None].address_family_attr['ipv6 unicast'].distance = 120
        rip.device_attr['PE1'].vrf_attr[None].address_family_attr['ipv6 unicast'].redistribute_direct_rmap\
            = 'rmap4'
        rip.device_attr['PE1'].vrf_attr[None].address_family_attr['ipv6 unicast'].redistribute_static_rmap\
            = 'rmap5'
        rip.device_attr['PE1'].vrf_attr[None].address_family_attr['ipv6 unicast'].redistribute_lisp_rmap\
            = 'rmap6'
        rip.device_attr['PE1'].vrf_attr['vrf1'].address_family_attr['ipv6 unicast'].\
            maximum_paths = 10
        rip.device_attr['PE1'].vrf_attr['vrf1'].address_family_attr['ipv6 unicast'].\
            default_metric = 7
        rip.device_attr['PE1'].vrf_attr['vrf1'].address_family_attr['ipv6 unicast'].\
            distance = 127
        rip.device_attr['PE1'].vrf_attr['vrf1'].address_family_attr['ipv6 unicast'].\
            redistribute_direct_rmap = 'rmap14'
        rip.device_attr['PE1'].vrf_attr['vrf1'].address_family_attr['ipv6 unicast'].\
            redistribute_static_rmap = 'rmap15'
        rip.device_attr['PE1'].vrf_attr['vrf1'].address_family_attr['ipv6 unicast'].\
            redistribute_lisp_rmap = 'rmap16'

        # rip.build_config(apply=False)
        output = rip.build_config(apply=False)

        expected_output = {'PE1': '''\
router rip 1
 no shutdown
 address-family ipv4 unicast
  default-metric 1
  distance 120
  maximum-paths 2
  redistribute lisp route-map rmap3
  redistribute direct route-map rmap1
  redistribute static route-map rmap2
  exit
 address-family ipv6 unicast
  default-metric 3
  distance 120
  maximum-paths 7
  redistribute lisp route-map rmap6
  redistribute direct route-map rmap4
  redistribute static route-map rmap5
  exit
 vrf vrf1
  address-family ipv4 unicast
   exit
  address-family ipv6 unicast
   default-metric 7
   distance 127
   maximum-paths 10
   redistribute lisp route-map rmap16
   redistribute direct route-map rmap14
   redistribute static route-map rmap15
   exit
  exit
 exit'''}
        self.maxDiff = None
        self.assertMultiLineDictEqual(output, expected_output)

        # Set a mock
        dev.cli = Mock()
        dev.configure = Mock()
        dev.add_feature(rip)
        # Mock config

        output = rip.build_config(apply=True)


    def test_uncfg(self):

        tb = Genie.testbed = Testbed()
        dev = Device(testbed=tb, name='PE1', os='nxos')

        rip = Rip(instance_id=1)
        rip.add_force_vrf(None)
        # Default configuration, let's make sure it works
        output = rip.build_unconfig(apply=False)
        # There was nothing to unconfigure
        self.assertMultiLineDictEqual(output, {})

        dev.add_feature(rip)
        output = rip.build_unconfig(apply=False)
        self.assertMultiLineDictEqual(output, {'PE1': 'feature rip\nno router rip 1'})

        # Set a mock
        dev.cli = Mock()
        dev.configure = Mock()
        output = rip.build_unconfig(apply=True)

        expected_output = None
        self.assertEqual(output, expected_output)

    def test_disable(self):

        tb = Genie.testbed = Testbed()
        dev = Device(testbed=tb, name='PE1', os='nxos')

        rip = Rip(instance_id=1)
        rip.add_force_vrf(None)
        dev.add_feature(rip)

        # Default configuration, let's make sure it works
        output = rip.build_unconfig(apply=False)
        self.assertMultiLineDictEqual(output, {
            'PE1':
            'feature rip\n'
            'no router rip 1'})
        # Set a mock
        dev.cli = Mock()
        dev.configure = Mock()
        output = rip.build_unconfig(apply=True)

        expected_output = None
        self.assertEqual(output, expected_output)

    def test_disable_no_instance(self):

        tb = Genie.testbed = Testbed()
        dev = Device(testbed=tb, name='PE1', os='nxos')

        rip = Rip(instance_id=1)
        rip.add_force_vrf(None)
        dev.add_feature(rip)

        # Default configuration, let's make sure it works
        output = rip.build_unconfig(unconfig_feature=True, apply=False)
        self.assertMultiLineDictEqual(output, {'PE1': 'no feature rip'})
        # Set a mock
        dev.cli = Mock()
        dev.configure = Mock()
        output = rip.build_unconfig(unconfig_feature=True, apply=True)

        expected_output = None
        self.assertEqual(output, expected_output)

    def test_remove_af(self):
        # Add a device to it
        tb = Genie.testbed = Testbed()
        dev1 = Device(testbed=tb, name='dev1', os='nxos')
        dev2 = Device(testbed=tb, name='dev2', os='nxos')
        rip = Rip(instance_id=5)
        rip.add_force_vrf(None)
        dev1.add_feature(rip)
        dev2.add_feature(rip)

        # Configure rip
        rip.device_attr['dev1'].vrf_attr[None].address_family_attr['ipv4 unicast'].distance = 5

        output = rip.build_config(apply=False)
        self.assertMultiLineDictEqual(output,
{'dev1': 'feature rip\n'
         'router rip 5\n'
         ' address-family ipv4 unicast\n'
         '  distance 5\n'
         '  exit\n'
         ' exit',
'dev2': 'feature rip\n'
         'router rip 5\n'
         ' address-family ipv4 unicast\n'
         '  exit\n'
         ' exit'})

        output = rip.build_unconfig(
            attributes={
                'device_attr': {
                    'dev1': {
                        'vrf_attr': {
                            None: {
                                'address_family_attr': {
                                    'ipv4 unicast': None}}}}}},
            apply=False)
        self.assertMultiLineDictEqual(output,
{'dev1': 'router rip 5\n no address-family ipv4 unicast\n exit'})

    def test_remove_vrf(self):
        # Add a device to it
        tb = Genie.testbed = Testbed()
        dev1 = Device(testbed=tb, name='dev1', os='nxos')
        dev2 = Device(testbed=tb, name='dev2', os='nxos')
        vrf1 = Vrf(name='blue')
        intf1 = Interface(device=dev1, name='Ethernet0/0', vrf=vrf1)
        intf2 = Interface(device=dev2, name='Ethernet0/0', vrf=vrf1)
        rip = Rip(instance_id=5)
        rip.add_force_vrf(None)
        intf1.add_feature(rip)
        intf2.add_feature(rip)

        # Configure rip
        rip.device_attr['dev1'].vrf_attr['blue'].address_family_attr['ipv4 unicast'].distance = 5

        output = rip.build_config(apply=False)
        self.assertMultiLineDictEqual(output,
{'dev1': 'feature rip\n'
         'router rip 5\n'
         ' address-family ipv4 unicast\n'
         '  exit\n'
         ' vrf blue\n'
         '  address-family ipv4 unicast\n'
         '   distance 5\n'
         '   exit\n'
         '  exit\n'
         ' exit',
'dev2': 'feature rip\n'
         'router rip 5\n'
         ' address-family ipv4 unicast\n'
         '  exit\n'
         ' vrf blue\n'
         '  address-family ipv4 unicast\n'
         '   exit\n'
         '  exit\n'
         ' exit'})

        output = rip.build_unconfig(\
                 attributes='device_attr__dev1__vrf_attr__blue',
                 apply=False)

        self.assertMultiLineDictEqual(output,
{'dev1': 'router rip 5\n no vrf blue\n exit'})

    def test_remove_vrf_af(self):
        # Add a device to it
        tb = Genie.testbed = Testbed()
        dev1 = Device(testbed=tb, name='dev1', os='nxos')
        dev2 = Device(testbed=tb, name='dev2', os='nxos')
        vrf1 = Vrf(name='blue')
        intf1 = Interface(device=dev1, name='Ethernet0/0', vrf=vrf1)
        rip = Rip(instance_id=5)
        rip.add_force_vrf(None)
        dev1.add_feature(rip)
        dev2.add_feature(rip)
        intf1.add_feature(rip)

        # Configure rip
        rip.device_attr['dev1'].vrf_attr['blue'].address_family_attr['ipv4 unicast'].distance = 5

        output = rip.build_config(apply=False)
        self.assertMultiLineDictEqual(output,
{'dev1': 'feature rip\n'
         'router rip 5\n'
         ' address-family ipv4 unicast\n'
         '  exit\n'
         ' vrf blue\n'
         '  address-family ipv4 unicast\n'
         '   distance 5\n'
         '   exit\n'
         '  exit\n'
         ' exit',
'dev2': 'feature rip\n'
         'router rip 5\n'
         ' address-family ipv4 unicast\n'
         '  exit\n'
         ' exit'})

        output = rip.build_unconfig(\
                 attributes='device_attr__dev1__vrf_attr__blue__address_family_attr__ipv4 unicast',
                 apply=False)

        self.assertMultiLineDictEqual(output,
{'dev1': 'router rip 5\n'
         ' vrf blue\n'
         '  no address-family ipv4 unicast\n'
         '  exit\n'
         ' exit'})

    def test_deactivate_feature(self):

        tb = Genie.testbed = Testbed()
        dev = Device(testbed=tb, name='PE1', os='nxos')

        rip = Rip(instance_id=1)
        rip.add_force_vrf(None)
        dev.add_feature(rip)

        # Default configuration, let's make sure it works
        output = rip.build_unconfig(apply=False)
        self.assertMultiLineDictEqual(output, {'PE1':
            'feature rip\n'
            'no router rip 1'
            })
        # Set a mock
        dev.cli = Mock()
        dev.configure = Mock()
        output = rip.build_unconfig(apply=True)

        expected_output = None
        self.assertEqual(output, expected_output)

    def test_enable_disable_device1(self):
        tb = Genie.testbed = Testbed()
        dev1 = Device(testbed=tb, name='dev1', os='nxos')
        dev2 = Device(testbed=tb, name='dev2', os='nxos')

        rip = Rip(instance_id=1)
        rip.add_force_vrf(None)
        dev1.add_feature(rip)
        dev2.add_feature(rip)

        # Verify weaklist property
        self.assertEqual(len(rip.devices), 2)
        tb.remove_device(dev1)

        del dev1
        self.assertEqual(len(rip.devices), 1)

    def test_multi_device_configuration(self):
        tb = Genie.testbed = Testbed()
        dev1 = Device(testbed=tb, name='dev1', os='nxos')
        dev2 = Device(testbed=tb, name='dev2', os='nxos')

        rip = Rip(instance_id=1)
        rip.add_force_vrf(None)
        dev1.cli = Mock()
        dev1.configure = Mock()
        dev2.cli = Mock()
        dev2.configure = Mock()
        dev1.add_feature(rip)
        dev2.add_feature(rip)

        # Default configuration, let's make sure it works
        output = rip.build_config(apply=False)
        self.assertMultiLineDictEqual(output, {
            'dev1':
            'feature rip\n'
            'router rip 1\n'
            ' address-family ipv4 unicast\n'
            '  exit\n'
            ' exit',
            'dev2':
            'feature rip\n'
            'router rip 1\n'
            ' address-family ipv4 unicast\n'
            '  exit\n'
            ' exit'})

        rip.address_families |= {AddressFamily.ipv6_unicast}
        rip.shutdown = True
        rip.device_attr['dev1'].vrf_attr[None].address_family_attr['ipv4 unicast'].maximum_paths = 2
        rip.device_attr['dev1'].vrf_attr[None].address_family_attr['ipv4 unicast'].default_metric = 1
        rip.device_attr['dev1'].vrf_attr[None].address_family_attr['ipv4 unicast'].distance = 120
        rip.device_attr['dev1'].vrf_attr[None].address_family_attr['ipv4 unicast'].redistribute_direct_rmap\
            = 'rmap1'
        rip.device_attr['dev1'].vrf_attr[None].address_family_attr['ipv4 unicast'].redistribute_static_rmap\
            = 'rmap2'
        rip.device_attr['dev1'].vrf_attr[None].address_family_attr['ipv4 unicast'].redistribute_lisp_rmap\
            = 'rmap3'
        rip.device_attr['dev1'].vrf_attr[None].address_family_attr['ipv6 unicast'].maximum_paths = 7
        rip.device_attr['dev1'].vrf_attr[None].address_family_attr['ipv6 unicast'].default_metric = 3
        rip.device_attr['dev1'].vrf_attr[None].address_family_attr['ipv6 unicast'].distance = 120
        rip.device_attr['dev1'].vrf_attr[None].address_family_attr['ipv6 unicast'].redistribute_direct_rmap\
            = 'rmap4'
        rip.device_attr['dev1'].vrf_attr[None].address_family_attr['ipv6 unicast'].redistribute_static_rmap\
            = 'rmap5'
        rip.device_attr['dev1'].vrf_attr[None].address_family_attr['ipv6 unicast'].redistribute_lisp_rmap\
            = 'rmap6'

        rip.device_attr['dev2'].vrf_attr[None].address_family_attr['ipv4 unicast'].maximum_paths = 4
        rip.device_attr['dev2'].vrf_attr[None].address_family_attr['ipv4 unicast'].default_metric = 3
        rip.device_attr['dev2'].vrf_attr[None].address_family_attr['ipv4 unicast'].distance = 122
        rip.device_attr['dev2'].vrf_attr[None].address_family_attr['ipv4 unicast'].redistribute_direct_rmap\
            = 'rmap_direct'
        rip.device_attr['dev2'].vrf_attr[None].address_family_attr['ipv4 unicast'].redistribute_static_rmap\
            = 'rmap_static'
        rip.device_attr['dev2'].vrf_attr[None].address_family_attr['ipv4 unicast'].redistribute_lisp_rmap\
            = 'rmap_lisp'
        rip.device_attr['dev2'].vrf_attr[None].address_family_attr['ipv6 unicast'].maximum_paths = 7
        rip.device_attr['dev2'].vrf_attr[None].address_family_attr['ipv6 unicast'].default_metric = 3
        rip.device_attr['dev2'].vrf_attr[None].address_family_attr['ipv6 unicast'].distance = 120
        rip.device_attr['dev2'].vrf_attr[None].address_family_attr['ipv6 unicast'].redistribute_direct_rmap\
            = 'rmap_direct_ipv6'
        rip.device_attr['dev2'].vrf_attr[None].address_family_attr['ipv6 unicast'].redistribute_static_rmap\
            = 'rmap_static_ipv6'
        rip.device_attr['dev2'].vrf_attr[None].address_family_attr['ipv6 unicast'].redistribute_lisp_rmap\
            = 'rmap_lisp_ipv6'

        output = rip.build_config(apply=False)
        expected_output = {'dev1': '''\
router rip 1
 shutdown
 address-family ipv4 unicast
  default-metric 1
  distance 120
  maximum-paths 2
  redistribute lisp route-map rmap3
  redistribute direct route-map rmap1
  redistribute static route-map rmap2
  exit
 address-family ipv6 unicast
  default-metric 3
  distance 120
  maximum-paths 7
  redistribute lisp route-map rmap6
  redistribute direct route-map rmap4
  redistribute static route-map rmap5
  exit
 exit''',
'dev2': '''\
router rip 1
 shutdown
 address-family ipv4 unicast
  default-metric 3
  distance 122
  maximum-paths 4
  redistribute lisp route-map rmap_lisp
  redistribute direct route-map rmap_direct
  redistribute static route-map rmap_static
  exit
 address-family ipv6 unicast
  default-metric 3
  distance 120
  maximum-paths 7
  redistribute lisp route-map rmap_lisp_ipv6
  redistribute direct route-map rmap_direct_ipv6
  redistribute static route-map rmap_static_ipv6
  exit
 exit'''}
        self.maxDiff = None
        self.assertMultiLineDictEqual(output, expected_output)
        output = rip.build_config(apply=True)

    def test_no_device_configuration(self):
        tb = Genie.testbed = Testbed()
        dev1 = Device(testbed=tb, name='dev1', os='nxos')
        dev2 = Device(testbed=tb, name='dev2', os='nxos')

        rip = Rip(instance_id=1)
        rip.add_force_vrf(None)

        # Default configuration, let's make sure it works
        output = rip.build_config(apply=False)
        self.assertMultiLineDictEqual(output, {})

        rip.shutdown = False
        rip.device_attr['dev1'].vrf_attr[None].address_family_attr['ipv4 unicast'].maximum_paths = 2
        rip.device_attr['dev1'].vrf_attr[None].address_family_attr['ipv4 unicast'].default_metric = 1
        rip.device_attr['dev1'].vrf_attr[None].address_family_attr['ipv4 unicast'].distance = 120
        rip.device_attr['dev1'].vrf_attr[None].address_family_attr['ipv4 unicast'].redistribute_direct_rmap\
            = 'rmap1'
        rip.device_attr['dev1'].vrf_attr[None].address_family_attr['ipv4 unicast'].redistribute_static_rmap\
            = 'rmap2'
        rip.device_attr['dev1'].vrf_attr[None].address_family_attr['ipv4 unicast'].redistribute_lisp_rmap\
            = 'rmap3'
        rip.device_attr['dev1'].vrf_attr[None].address_family_attr['ipv6 unicast'].maximum_paths = 7
        rip.device_attr['dev1'].vrf_attr[None].address_family_attr['ipv6 unicast'].default_metric = 3
        rip.device_attr['dev1'].vrf_attr[None].address_family_attr['ipv6 unicast'].distance = 120
        rip.device_attr['dev1'].vrf_attr[None].address_family_attr['ipv6 unicast'].redistribute_direct_rmap\
            = 'rmap4'
        rip.device_attr['dev1'].vrf_attr[None].address_family_attr['ipv6 unicast'].redistribute_static_rmap\
            = 'rmap5'
        rip.device_attr['dev1'].vrf_attr[None].address_family_attr['ipv6 unicast'].redistribute_lisp_rmap\
            = 'rmap6'

        rip.device_attr['dev2'].vrf_attr[None].address_family_attr['ipv4 unicast'].maximum_paths = 4
        rip.device_attr['dev2'].vrf_attr[None].address_family_attr['ipv4 unicast'].default_metric = 3
        rip.device_attr['dev2'].vrf_attr[None].address_family_attr['ipv4 unicast'].distance = 122
        rip.device_attr['dev2'].vrf_attr[None].address_family_attr['ipv4 unicast'].redistribute_direct_rmap\
            = 'rmap_direct'
        rip.device_attr['dev2'].vrf_attr[None].address_family_attr['ipv4 unicast'].redistribute_static_rmap\
            = 'rmap_static'
        rip.device_attr['dev2'].vrf_attr[None].address_family_attr['ipv4 unicast'].redistribute_lisp_rmap\
            = 'rmap_lisp'
        rip.device_attr['dev2'].vrf_attr[None].address_family_attr['ipv6 unicast'].maximum_paths = 7
        rip.device_attr['dev2'].vrf_attr[None].address_family_attr['ipv6 unicast'].default_metric = 3
        rip.device_attr['dev2'].vrf_attr[None].address_family_attr['ipv6 unicast'].distance = 120
        rip.device_attr['dev2'].vrf_attr[None].address_family_attr['ipv6 unicast'].redistribute_direct_rmap\
            = 'rmap_direct_ipv6'
        rip.device_attr['dev2'].vrf_attr[None].address_family_attr['ipv6 unicast'].redistribute_static_rmap\
            = 'rmap_static_ipv6'
        rip.device_attr['dev2'].vrf_attr[None].address_family_attr['ipv6 unicast'].redistribute_lisp_rmap\
            = 'rmap_lisp_ipv6'

        expected_output = rip.build_config(apply=False)
        self.assertMultiLineDictEqual(output, {})

        output = rip.build_config(apply=True)

        expected_output = None
        self.assertEqual(output, expected_output)

    def test_modify_configurations_nothing_configured(self):
        '''Nothing is configured on this rip'''

        rip = Rip(instance_id=1)
        rip.add_force_vrf(None)
        output = rip.build_config(apply=False)

        # Nothing should happen, no device was given
        self.assertMultiLineDictEqual(output, {})

    def test_modify_configuration_first_level(self):

        # Add a device to it
        tb = Genie.testbed = Testbed()
        dev1 = Device(testbed=tb, name='dev1', os='nxos')
        dev2 = Device(testbed=tb, name='dev2', os='nxos')
        rip = Rip(instance_id=5)
        rip.add_force_vrf(None)
        dev1.add_feature(rip)
        dev2.add_feature(rip)

        # Can either confgiure via kwargs, or attributes
        output = rip.build_config(apply=False)
        self.assertMultiLineDictEqual(output, {
            'dev1':
            'feature rip\n'
            'router rip 5\n'
            ' address-family ipv4 unicast\n'
            '  exit\n'
            ' exit',
            'dev2':
            'feature rip\n'
            'router rip 5\n'
            ' address-family ipv4 unicast\n'
            '  exit\n'
            ' exit',
            })

        self.assertEqual(rip.device_attr['dev1'].shutdown, None)
        self.assertEqual(rip.device_attr['dev2'].shutdown, None)

        rip.shutdown = False
        output = rip.build_config(attributes='device_attr__dev1__shutdown', apply=False)
        self.assertMultiLineDictEqual(output, {
            'dev1':
            'router rip 5\n'
            ' no shutdown\n'
            ' exit',
            })

        rip.shutdown = False
        output = rip.build_config(attributes='device_attr__*__shutdown', apply=False)
        self.assertMultiLineDictEqual(output, {
            'dev1':
            'router rip 5\n'
            ' no shutdown\n'
            ' exit',
            'dev2':
            'router rip 5\n'
            ' no shutdown\n'
            ' exit',
            })

        # XXXJST
        # output = rip.build_config(shutdown=False, apply=False)
        # self.assertMultiLineDictEqual(output, {'dev1':'router rip 5\n no shutdown',
        #                           'dev2':'router rip 5\n no shutdown'})
        #
        # self.assertEqual(rip.device_attr['dev1'].shutdown, False)
        # self.assertEqual(rip.device_attr['dev2'].shutdown, False)
        #
        # # Rest are all into a vrf
        # # Let's try without a af , vrf/af
        # output = rip.build_config(maximum_paths=3, apply=False)
        # self.assertMultiLineDictEqual(output, {'dev1':'',
        #                           'dev2':''})
        #
        # # Let's add an af
        # rip.device_attr['dev1'].vrf_attr[None].address_family_attr['ipv4 unicast'].create()
        # rip.device_attr['dev2'].vrf_attr[None].address_family_attr['ipv4 unicast'].create()
        #
        # output = rip.build_config(maximum_paths=3, apply=False)
        # self.assertMultiLineDictEqual(output, {'dev1':'router rip 5\n address-family ipv4 '
        #                                  'unicast\n  maximum-paths 3\n  exit',
        #                           'dev2':'router rip 5\n address-family ipv4 '
        #                                  'unicast\n  maximum-paths 3\n  exit'})
        #
        # # Mix both together
        # output = rip.build_config(maximum_paths=3, shutdown=True, apply=False)
        # self.assertMultiLineDictEqual(output, {'dev1':'router rip 5\n shutdown\n '
        #                                  'address-family ipv4 '
        #                                  'unicast\n  maximum-paths 3\n  exit',
        #                           'dev2':'router rip 5\n shutdown\n '
        #                                  'address-family ipv4 '
        #                                  'unicast\n  maximum-paths 3\n  exit'})
        #
        # # Do the same for vrf now
        # rip.device_attr['dev1'].vrf_attr['blue'].address_family_attr['ipv4 unicast'].create()
        # rip.device_attr['dev2'].vrf_attr['orange'].address_family_attr['ipv4 unicast'].create()
        #
        # output = rip.build_config(maximum_paths=3, shutdown=False, apply=False)
        # self.maxDiff = None
        # self.assertMultiLineDictEqual(output,
        # {'dev1': 'router rip 5\n'
        #          ' no shutdown\n'
        #          ' address-family ipv4 unicast\n'
        #          '  maximum-paths 3\n'
        #          '  exit\n'
        #          ' vrf blue\n'
        #          '  address-family ipv4 unicast\n'
        #          '   maximum-paths 3\n'
        #          '   exit\n'
        #          '  exit',
        #  'dev2': 'router rip 5\n'
        #          ' no shutdown\n'
        #          ' address-family ipv4 unicast\n'
        #          '  maximum-paths 3\n'
        #          '  exit\n'
        #          ' vrf orange\n'
        #          '  address-family ipv4 unicast\n'
        #          '   maximum-paths 3\n'
        #          '   exit\n'
        #          '  exit'})
        #
        # # Now test all the fields
        #
        # output = rip.build_config(maximum_paths=2, default_metric=1,
        #                           distance=120,
        #                           redistribute_direct_rmap='rmap1',
        #                           redistribute_static_rmap='rmap2',
        #                           redistribute_lisp_rmap='rmap3', apply=False)
        # self.assertMultiLineDictEqual(output,
        # {'dev1': 'router rip 5\n'
        #  ' address-family ipv4 unicast\n'
        #  '  default-metric 1\n'
        #  '  distance 120\n'
        #  '  maximum-paths 2\n'
        #  '  redistribute lisp route-map rmap3\n'
        #  '  redistribute direct route-map rmap1\n'
        #  '  redistribute static route-map rmap2\n'
        #  '  exit\n'
        #  ' vrf blue\n'
        #  '  address-family ipv4 unicast\n'
        #  '   default-metric 1\n'
        #  '   distance 120\n'
        #  '   maximum-paths 2\n'
        #  '   redistribute lisp route-map rmap3\n'
        #  '   redistribute direct route-map rmap1\n'
        #  '   redistribute static route-map rmap2\n'
        #  '   exit\n'
        #  '  exit',
        #  'dev2': 'router rip 5\n'
        #  ' address-family ipv4 unicast\n'
        #  '  default-metric 1\n'
        #  '  distance 120\n'
        #  '  maximum-paths 2\n'
        #  '  redistribute lisp route-map rmap3\n'
        #  '  redistribute direct route-map rmap1\n'
        #  '  redistribute static route-map rmap2\n'
        #  '  exit\n'
        #  ' vrf orange\n'
        #  '  address-family ipv4 unicast\n'
        #  '   default-metric 1\n'
        #  '   distance 120\n'
        #  '   maximum-paths 2\n'
        #  '   redistribute lisp route-map rmap3\n'
        #  '   redistribute direct route-map rmap1\n'
        #  '   redistribute static route-map rmap2\n'
        #  '   exit\n'
        #  '  exit'})
        #
        # # Now test all the fields with None
        #
        # output = rip.build_unconfig(maximum_paths=True, default_metric=True,
        #                             distance=True,
        #                             redistribute_direct_rmap=True,
        #                             redistribute_static_rmap=True,
        #                             redistribute_lisp_rmap=True, shutdown=True,
        #                             apply=False)
        # self.assertMultiLineDictEqual(output,
        # {'dev1': 'router rip 5\n'
        #  ' shutdown\n'
        #  ' address-family ipv4 unicast\n'
        #  '  no default-metric\n'
        #  '  no distance\n'
        #  '  no maximum-paths\n'
        #  '  no redistribute lisp route-map rmap3\n'
        #  '  no redistribute direct route-map rmap1\n'
        #  '  no redistribute static route-map rmap2\n'
        #  '  exit\n'
        #  ' vrf blue\n'
        #  '  address-family ipv4 unicast\n'
        #  '   no default-metric\n'
        #  '   no distance\n'
        #  '   no maximum-paths\n'
        #  '   no redistribute lisp route-map rmap3\n'
        #  '   no redistribute direct route-map rmap1\n'
        #  '   no redistribute static route-map rmap2\n'
        #  '   exit\n'
        #  '  exit',
        #  'dev2': 'router rip 5\n'
        #  ' shutdown\n'
        #  ' address-family ipv4 unicast\n'
        #  '  no default-metric\n'
        #  '  no distance\n'
        #  '  no maximum-paths\n'
        #  '  no redistribute lisp route-map rmap3\n'
        #  '  no redistribute direct route-map rmap1\n'
        #  '  no redistribute static route-map rmap2\n'
        #  '  exit\n'
        #  ' vrf orange\n'
        #  '  address-family ipv4 unicast\n'
        #  '   no default-metric\n'
        #  '   no distance\n'
        #  '   no maximum-paths\n'
        #  '   no redistribute lisp route-map rmap3\n'
        #  '   no redistribute direct route-map rmap1\n'
        #  '   no redistribute static route-map rmap2\n'
        #  '   exit\n'
        #  '  exit'})

    # XXXJST
    # def test_modify_configuration_many_level(self):
    #
    #     # Add a device to it
    #     tb = Genie.testbed = Testbed()
    #     dev1 = Device(testbed=tb, name='dev1', os='nxos')
    #     dev2 = Device(testbed=tb, name='dev2', os='nxos')
    #     rip = Rip(instance_id=5)
    #     rip.add_force_vrf(None)
    #     dev1.add_feature(rip)
    #     dev2.add_feature(rip)
    #
    #     output = rip.build_config(device_attr__dev1__shutdown=False,
    #                               apply=False)
    #     self.assertMultiLineDictEqual(output,
    #             {'dev1':'feature rip\nrouter rip 5\n no shutdown',
    #              'dev2':'feature rip\nrouter rip 5'})
    #
    #     # Does not exists
    #     with self.assertRaises(AttributeError):
    #         output = rip.build_config(test__dev1__shutdown=False,
    #                                   apply=False)
    #
    #     self.assertEqual(rip.device_attr['dev1'].shutdown, False)
    #     self.assertFalse(hasattr(rip.device_attr['dev2'],' shutdown'))
    #
    #     # Let's add an af
    #     rip.device_attr['dev1'].vrf_attr[None].address_family_attr['ipv4 unicast'].create()
    #     rip.device_attr['dev1'].vrf_attr[None].address_family_attr['ipv6 unicast'].create()
    #     rip.device_attr['dev2'].vrf_attr[None].address_family_attr['ipv4 unicast'].create()
    #
    #     output = rip.build_config(\
    #             device_attr__dev1__vrf_attr__None__address_family_attr__ipv4__maximum_paths=3,
    #             apply=False)
    #     self.assertMultiLineDictEqual(output,
    #     {'dev1': 'router rip 5\n'
    #      ' address-family ipv4 unicast\n'
    #      '  maximum-paths 3\n'
    #      '  exit',
    #      'dev2': ''})
    #
    #     # Mix both together
    #     output = rip.build_config(\
    #             device_attr__dev1__vrf_attr__None__address_family_attr__ipv4__maximum_paths=3,
    #             shutdown=False, apply=False)
    #
    #     self.assertMultiLineDictEqual(output, {'dev1':'router rip 5\n no shutdown\n '
    #                                      'address-family ipv4 '
    #                                      'unicast\n  maximum-paths 3\n  exit',
    #                               'dev2':'router rip 5\n no shutdown'})
    #
    #     # What if both are the same !
    #
    #     output = rip.build_config(\
    #             device_attr__dev1__vrf_attr__None__address_family_attr__ipv4__maximum_paths=3,
    #             maximum_paths=5, apply=False)
    #     self.assertMultiLineDictEqual(output,
    #     {'dev1': 'router rip 5\n'
    #      ' address-family ipv4 unicast\n'
    #      '  maximum-paths 3\n'
    #      '  exit\n'
    #      ' address-family ipv6 unicast\n'
    #      '  maximum-paths 5\n'
    #      '  exit',
    #      'dev2': 'router rip 5\n'
    #      ' address-family ipv4 unicast\n'
    #      '  maximum-paths 5\n'
    #      '  exit'})
    #
    #     # Do the same for vrf now
    #     rip.device_attr['dev1'].vrf_attr['blue'].address_family_attr['ipv4 unicast'].create()
    #     rip.device_attr['dev2'].vrf_attr['orange'].address_family_attr['ipv4 unicast'].create()
    #
    #     output = rip.build_config(\
    #             device_attr__dev1__vrf_attr__blue__address_family_attr__ipv4__maximum_paths=3,
    #             shutdown=False, apply=False)
    #     self.assertMultiLineDictEqual(output,
    #     {'dev1': 'router rip 5\n'
    #              ' no shutdown\n'
    #              ' vrf blue\n'
    #              '  address-family ipv4 unicast\n'
    #              '   maximum-paths 3\n'
    #              '   exit\n'
    #              '  exit',
    #      'dev2':'router rip 5\n no shutdown'})
    #     output = rip.build_config(\
    #             device_attr__dev1__vrf_attr__blue__address_family_attr__ipv4__maximum_paths=3,
    #             shutdown=False, apply=False, devices=[dev2])
    #     self.assertMultiLineDictEqual(output,
    #     {'dev2':'router rip 5\n no shutdown'})
    #     # Now test all the fields
    #     # Now test all the fields
    #
    #     output = rip.build_config(\
    #             device_attr__dev1__vrf_attr__blue__address_family_attr__ipv4__maximum_paths=2,
    #             device_attr__dev1__vrf_attr__blue__address_family_attr__ipv4__default_metric=1,
    #             device_attr__dev1__vrf_attr__blue__address_family_attr__ipv4__distance=120,
    #             device_attr__dev1__vrf_attr__blue__address_family_attr__ipv4__redistribute_direct_rmap='rmap1',
    #             device_attr__dev1__vrf_attr__blue__address_family_attr__ipv4__redistribute_static_rmap='rmap2',
    #             device_attr__dev1__vrf_attr__blue__address_family_attr__ipv4__redistribute_lisp_rmap='rmap3',
    #             apply=False)
    #     self.assertMultiLineDictEqual(output,
    #     {'dev1': 'router rip 5\n'
    #      ' vrf blue\n'
    #      '  address-family ipv4 unicast\n'
    #      '   default-metric 1\n'
    #      '   distance 120\n'
    #      '   maximum-paths 2\n'
    #      '   redistribute lisp route-map rmap3\n'
    #      '   redistribute direct route-map rmap1\n'
    #      '   redistribute static route-map rmap2\n'
    #      '   exit\n'
    #      '  exit',
    #     'dev2': ''})

if __name__ == '__main__':
    unittest.main()

