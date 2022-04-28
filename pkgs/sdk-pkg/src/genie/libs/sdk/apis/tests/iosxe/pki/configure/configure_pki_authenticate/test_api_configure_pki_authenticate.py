import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.pki.configure import configure_pki_authenticate


class TestConfigurePkiAuthenticate(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          ipsec_reg8_new:
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
        self.device = self.testbed.devices['ipsec_reg8_new']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_pki_authenticate(self):
        result = configure_pki_authenticate(self.device, 'client')
        expected_output = None
        self.assertEqual(result, expected_output)
