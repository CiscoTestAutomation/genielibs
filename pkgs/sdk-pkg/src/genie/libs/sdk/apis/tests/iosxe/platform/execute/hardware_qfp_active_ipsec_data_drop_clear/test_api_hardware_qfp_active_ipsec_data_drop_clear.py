import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.execute import hardware_qfp_active_ipsec_data_drop_clear


class TestHardwareQfpActiveIpsecDataDropClear(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          GREENDAY:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['GREENDAY']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_hardware_qfp_active_ipsec_data_drop_clear(self):
        result = hardware_qfp_active_ipsec_data_drop_clear(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)
