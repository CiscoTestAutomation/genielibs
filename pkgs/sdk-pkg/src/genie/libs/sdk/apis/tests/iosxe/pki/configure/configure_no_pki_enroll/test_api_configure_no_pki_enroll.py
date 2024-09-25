import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.pki.configure import configure_no_pki_enroll


class TestConfigureNoPkiEnroll(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          dut1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c8000v
            type: c8000v
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['dut1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_no_pki_enroll(self):
        result = configure_no_pki_enroll(self.device, 'tp_wo_pass_enc')
        expected_output = None
        self.assertEqual(result, expected_output)
