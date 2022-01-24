import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.sudi.verify import verify_sudi_pki


class TestVerifySudiPki(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          Switch:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: Switch
            type: Switch
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Switch']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_sudi_pki(self):
        result = verify_sudi_pki(self.device, 'Enabled', 15, 5)
        expected_output = True
        self.assertEqual(result, expected_output)
