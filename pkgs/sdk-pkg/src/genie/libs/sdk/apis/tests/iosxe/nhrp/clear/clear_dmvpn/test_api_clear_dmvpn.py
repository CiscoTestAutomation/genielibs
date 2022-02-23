import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.nhrp.clear import clear_dmvpn


class TestClearDmvpn(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          TLS_Mad1:
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
        self.device = self.testbed.devices['TLS_Mad1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_clear_dmvpn(self):
        result = clear_dmvpn(self.device, None, True, None, 30)
        expected_output = None
        self.assertEqual(result, expected_output)
