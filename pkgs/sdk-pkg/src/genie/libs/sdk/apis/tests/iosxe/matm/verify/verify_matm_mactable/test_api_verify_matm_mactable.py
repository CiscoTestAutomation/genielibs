import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.matm.verify import verify_matm_mactable


class TestVerifyMatmMactable(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          SF1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: '9500'
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['SF1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_matm_mactable(self):
        result = verify_matm_mactable(self.device, 'active', '10', '0000.1111.aaaa', 'VTEP 10.10.10.10 adj_id 1065')
        expected_output = False
        self.assertEqual(result, expected_output)
