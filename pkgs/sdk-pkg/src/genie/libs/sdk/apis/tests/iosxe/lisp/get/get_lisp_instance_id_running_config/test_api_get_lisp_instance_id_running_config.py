import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.lisp.get import get_lisp_instance_id_running_config


class TestGetLispInstanceIdRunningConfig(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          AMZ-9500-Dist3:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9500
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['AMZ-9500-Dist3']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_lisp_instance_id_running_config(self):
        result = get_lisp_instance_id_running_config(self.device, '699')
        expected_output = {'instance_id': 699, 'multicast_address': '239.0.0.7'}
        self.assertEqual(result, expected_output)
