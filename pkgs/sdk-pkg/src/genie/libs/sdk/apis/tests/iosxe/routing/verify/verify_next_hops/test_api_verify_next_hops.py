import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.routing.verify import verify_next_hops


class TestVerifyNextHops(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          rtr1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iol
            type: iol
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['rtr1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_next_hops(self):
        result = verify_next_hops(self.device, ['2.2.2.2', '3.3.3.3', '31.31.31.31', '141.1.2.0'], '141.1.1.2')
        expected_output = True
        self.assertEqual(result, expected_output)
