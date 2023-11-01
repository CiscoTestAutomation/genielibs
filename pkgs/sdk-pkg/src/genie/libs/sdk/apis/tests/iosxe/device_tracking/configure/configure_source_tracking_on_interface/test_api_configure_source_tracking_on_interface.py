import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.device_tracking.configure import configure_source_tracking_on_interface


class TestConfigureSourceTrackingOnInterface(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          9404_SVL_UUT2:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: C9400
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['9404_SVL_UUT2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_source_tracking_on_interface(self):
        result = configure_source_tracking_on_interface(self.device, 'GigabitEthernet1/4/0/14', 'tracking')
        expected_output = None
        self.assertEqual(result, expected_output)
