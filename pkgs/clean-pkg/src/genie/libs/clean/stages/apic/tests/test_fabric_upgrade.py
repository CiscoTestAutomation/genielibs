import os
import unittest
from unittest.mock import Mock, call

from pyats.datastructures import AttrDict
from pyats.aetest.steps import Steps
from pyats.aetest.base import TestItem
from pyats.aetest.signals import AEtestPassedSignal

from pyats.kleenex.engine import KleenexEngine
from pyats.kleenex.loader import KleenexFileLoader

from genie.testbed import load
from genie.libs.clean.stages.apic.stages import fabric_upgrade

import sys
import logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


test_path = os.path.dirname(os.path.abspath(__file__))


class PositiveStages(unittest.TestCase):

    def setUp(self):
        self.tb = load(test_path+'/mock_testbed.yaml')
        self.clean_config = KleenexFileLoader(testbed=self.tb,
                                              invoke_clean=True).\
                                              load(test_path+'/mock_clean.yaml')
        KleenexEngine.update_testbed(self.tb, **self.clean_config['devices'])
        self.steps = Steps()
        self.section = TestItem(uid='test', description='', parameters={})

    def test_fabric_upgrade(self):
        self.section.history = {'fabric_upgrade': AttrDict({'parameters': {}})}

        def mock_parse(cmd, *args, **kwargs):
            output = {'show version': {
                    "pod": {
                        1: {
                            "node": {
                                1: {
                                    "name": "ifc1",
                                    "node": 1,
                                    "pod": 1,
                                    "role": "controller",
                                    "version": "5.1(2e)"
                                },
                                101: {
                                    "name": "leaf1",
                                    "node": 101,
                                    "pod": 1,
                                    "role": "leaf",
                                    "version": "n9000-15.1(2e)"
                                },
                                201: {
                                    "name": "spine1",
                                    "node": 201,
                                    "pod": 1,
                                    "role": "spine",
                                    "version": "n9000-15.1(2e)"
                                },
                                202: {
                                    "name": "spine2",
                                    "node": 202,
                                    "pod": 1,
                                    "role": "spine",
                                    "version": "n9000-14.2(2e)"
                                }
                            }
                        }
                    }
                }
            }

            return output.get(cmd)

        device = Mock()
        device.name = 'ifc1'
        device.testbed = self.tb
        device.api = Mock()
        device.api.get_firmware_repository_images_by_polling = Mock(return_value=['/root/aci-apic-dk9.5.1.2e.iso'])
        device.api.get_firmware_version_from_image_name = Mock(return_value='5.1(2e)')
        device.os = 'apic'
        device.clean = Mock()
        device.clean.fabric_upgrade = {
            'controller_image': ['aci-apic-dk9.5.1.2e.iso'],
            'switch_image': ['aci-n9000-dk9.15.1.2e.bin'],
            'switch_group_nodes': ['Spine1', 'Spine2', 'Leaf1'],
            'timeouts': {
                'controller_upgrade': 3000,
                'controller_reconnect': 1200,
                'controller_upgrade_after_reconnect': 600,
                'switch_upgrade': 3000
            }
        }
        device.parse = Mock(side_effect=mock_parse)
        device.configure = Mock(return_value="")
        device.destroy = Mock(return_value="")
        device.connect = Mock(return_value="")
        device.execute = Mock(return_value="")
        device.copy = Mock(return_value="")

        # Execute stage: apply_configuration
        with self.assertRaises(AEtestPassedSignal):
            fabric_upgrade(self.section, self.steps, device,
                           **device.clean.fabric_upgrade)

        device.parse.assert_has_calls([call('show version')])
        device.execute.assert_has_calls([
            call('firmware repository add aci-n9000-dk9.15.1.2e.bin', timeout=300, error_pattern=['.*Command execution failed.*'])
        ])
        device.api.get_firmware_repository_images_by_polling.assert_has_calls([
            call(image_type='switch', max_time=300)
        ])
        device.api.get_firmware_version_from_image_name.assert_has_calls([call('aci-apic-dk9.5.1.2e.iso')])

    def test_fabric_upgrade_show_version_empty(self):
        self.section.history = {'fabric_upgrade': AttrDict({'parameters': {}})}

        def mock_parse(cmd, *args, **kwargs):
            output = {'show version': {
                    "pod": {
                        1: {
                            "node": {
                                101: {
                                    "name": "leaf1",
                                    "node": 101,
                                    "pod": 1,
                                    "role": "leaf",
                                    "version": "n9000-15.1(2e)"
                                },
                                201: {
                                    "name": "spine1",
                                    "node": 201,
                                    "pod": 1,
                                    "role": "spine",
                                    "version": "n9000-15.1(2e)"
                                },
                            }
                        }
                    }
                }}

            return output.get(cmd)

        device = Mock()
        device.name = 'ifc1'
        device.testbed = self.tb
        device.api = Mock()
        device.api.get_firmware_repository_images_by_polling = Mock(return_value=[
            '/root/aci-apic-dk9.5.1.2e.iso',
            '/root/aci-n9000-dk9.15.1.2e.bin'
            ])
        device.api.get_firmware_version_from_image_name = Mock(return_value='5.1(2e)')
        device.os = 'apic'
        device.clean = Mock()
        device.clean.fabric_upgrade = {
            'controller_image': ['aci-apic-dk9.5.1.2e.iso'],
            'switch_image': ['aci-n9000-dk9.15.1.2e.bin'],
            'switch_group_nodes': ['Spine1', 'Leaf1'],
            'timeouts': {
                'controller_upgrade': 3000,
                'controller_reconnect': 1200,
                'controller_upgrade_after_reconnect': 600,
                'switch_upgrade': 3000
            }
        }
        device.parse = Mock(side_effect=mock_parse)
        device.configure = Mock(return_value="")
        device.destroy = Mock(return_value="")
        device.connect = Mock(return_value="")
        device.execute = Mock(return_value="")
        device.copy = Mock(return_value="")

        # Execute stage: apply_configuration
        with self.assertRaises(AEtestPassedSignal):
            fabric_upgrade(self.section, self.steps, device,
                           **device.clean.fabric_upgrade)

        device.parse.assert_has_calls([call('show version')])
        device.execute.assert_has_calls([
            call('firmware repository add aci-apic-dk9.5.1.2e.iso', timeout=300, error_pattern=['.*Command execution failed.*']),
            call('firmware repository add aci-n9000-dk9.15.1.2e.bin', timeout=300, error_pattern=['.*Command execution failed.*'])
        ])
        device.api.get_firmware_repository_images_by_polling.assert_has_calls([
            call(image_type='controller', max_time=300),
            call(image_type='switch', max_time=300)
        ])
        device.api.get_firmware_version_from_image_name.assert_has_calls([call('aci-apic-dk9.5.1.2e.iso')])


if __name__ == "__main__":
    unittest.main()
