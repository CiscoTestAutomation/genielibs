import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.FedIgmpSnooping.verify import verify_Software_Fed_Igmp_Snooping


class TestVerifySoftwareFedIgmpSnooping(unittest.TestCase):

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

    def test_verify_Software_Fed_Igmp_Snooping(self):
        result = verify_Software_Fed_Igmp_Snooping(self.device, 'active', 10, 'mroute_port', 'None')
        expected_output = False
        self.assertEqual(result, expected_output)
