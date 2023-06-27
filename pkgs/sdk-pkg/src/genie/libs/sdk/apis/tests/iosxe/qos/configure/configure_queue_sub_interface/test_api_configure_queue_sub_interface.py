import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.qos.configure import configure_queue_sub_interface


class TestConfigureQueueSubInterface(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Prasad_9500X:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Prasad_9500X']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_queue_sub_interface(self):
        result = configure_queue_sub_interface(self.device, 'hundredGigE 1/0/1')
        expected_output = None
        self.assertEqual(result, expected_output)
