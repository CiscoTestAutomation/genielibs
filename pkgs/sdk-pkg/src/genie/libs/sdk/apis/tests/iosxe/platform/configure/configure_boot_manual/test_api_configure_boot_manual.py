import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.configure import configure_boot_manual


class TestConfigureBootManual(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          cts_client:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat3k
            type: single_rp
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['cts_client']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_boot_manual(self):
        result = configure_boot_manual(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)
