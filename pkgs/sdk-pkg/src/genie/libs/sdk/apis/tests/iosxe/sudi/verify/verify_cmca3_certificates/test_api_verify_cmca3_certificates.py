import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.sudi.verify import verify_cmca3_certificates


class TestVerifyCmca3Certificates(unittest.TestCase):

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

    def test_verify_cmca3_certificates(self):
        result = verify_cmca3_certificates(self.device, 15, 5)
        expected_output = True
        self.assertEqual(result, expected_output)
