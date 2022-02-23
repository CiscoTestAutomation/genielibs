import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.nxos.bootmode.verify import verify_boot_mode_lxc_config


class TestVerifyBootModeLxcConfig(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          EX_uut2_53:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os nxos --mock_data_dir mock_data --state connect
                protocol: unknown
            os: nxos
            platform: Nexus 9000
            type: Nexus 9000
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['EX_uut2_53']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_boot_mode_lxc_config(self):
        result = verify_boot_mode_lxc_config(self.device)
        expected_output = True
        self.assertEqual(result, expected_output)
