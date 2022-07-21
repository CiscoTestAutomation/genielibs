import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.routing.verify import verify_num_routes_equal_before_and_after_clear


class TestVerifyNumRoutesEqualBeforeAndAfterClear(unittest.TestCase):

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

    def test_verify_num_routes_equal_before_and_after_clear(self):
        result = verify_num_routes_equal_before_and_after_clear(self.device, 'show ip route', 'clear ip route *')
        expected_output = True
        self.assertEqual(result, expected_output)
