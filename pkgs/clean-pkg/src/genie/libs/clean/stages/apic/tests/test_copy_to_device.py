import unittest
from unittest.mock import Mock, call

from pyats.datastructures import AttrDict
from pyats.aetest.steps import Steps
from pyats.aetest.base import TestItem
from pyats.aetest.signals import AEtestPassedSignal
from genie.libs.clean.stages.apic.stages import copy_to_device


class PositiveStages(unittest.TestCase):

    def setUp(self):
        self.steps = Steps()
        self.section = TestItem(uid='test', description='', parameters={})

    def test_copy_to_device(self):
        self.section.history = {'copy_to_device': AttrDict({'parameters': {}})}

        def mock_parse(cmd, *args, **kwargs):
            output = {'show version': {
                    "pod": {
                        1: {
                            "node": {
                                1: {
                                    "name": "msl-ifav205-ifc1",
                                    "node": 1,
                                    "pod": 1,
                                    "role": "controller",
                                    "version": "5.1(2e)"
                                },
                                101: {
                                    "name": "msl-ifav205-leaf1",
                                    "node": 101,
                                    "pod": 1,
                                    "role": "leaf",
                                    "version": "n9000-15.1(2e)"
                                },
                                201: {
                                    "name": "msl-ifav205-spine1",
                                    "node": 201,
                                    "pod": 1,
                                    "role": "spine",
                                    "version": "n9000-15.1(2e)"
                                },
                                202: {
                                    "name": "msl-ifav205-spine2",
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

        class file_exists_class:
            """ Mock helper class
            Return False on the firsts call,
            True on the second call
            """

            def __init__(self, *args, **kwargs):
                self.exists = True

            def __call__(self, *args, **kwargs):
                self.exists = not(self.exists)
                return self.exists

        file_exists = file_exists_class()

        device = Mock()
        device.api = Mock()
        device.api.get_file_size_from_server = Mock(return_value=100)
        device.api.verify_file_exists = Mock(side_effect=file_exists)
        device.os = 'apic'
        device.clean = Mock()
        device.clean.copy_to_device = {
            'origin': {
                'hostname': '10.22.54.133',
                'files': [
                    '/root/aci-apic-dk9.5.1.2e.iso',
                    '/root/aci-n9000-dk9.15.1.2e.bin'
                ]
            },
            'destination': {'directory': '/home/admin'},
            'protocol': 'sftp',
            'skip_deletion': False,
            'timeout': 3600,
            'verify_num_images': False,
            'min_free_space_percent': 70
        }
        device.parse = Mock(side_effect=mock_parse)
        device.configure = Mock(return_value="")
        device.destroy = Mock(return_value="")
        device.connect = Mock(return_value="")
        device.execute = Mock(return_value="")
        device.copy = Mock(return_value="")

        # Execute stage: apply_configuration
        with self.assertRaises(AEtestPassedSignal):
            copy_to_device(self.section, self.steps, device,
                           **device.clean.copy_to_device)


if __name__ == "__main__":
    unittest.main()