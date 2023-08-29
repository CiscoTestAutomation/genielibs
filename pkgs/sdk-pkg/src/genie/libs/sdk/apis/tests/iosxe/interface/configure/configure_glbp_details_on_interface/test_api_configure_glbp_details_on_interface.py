import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import configure_glbp_details_on_interface


class TestConfigureGlbpDetailsOnInterface(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          P-R1:
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
        self.device = self.testbed.devices['P-R1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_glbp_details_on_interface(self):
        result = configure_glbp_details_on_interface(self.device, 'vlan10', 0, '10.1.0.3', None, '150', '0', '1', '4')
        expected_output = None
        self.assertEqual(result, expected_output)
