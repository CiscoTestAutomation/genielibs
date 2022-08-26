import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.cdp.verify import verify_total_cdp_entries_displayed_interfaces


class TestVerifyTotalCdpEntriesDisplayedInterfaces(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          1783-CMS20DN:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: s5k
            type: switch
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['1783-CMS20DN']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_total_cdp_entries_displayed_interfaces(self):
        result = verify_total_cdp_entries_displayed_interfaces(self.device, '17', 60, 10)
        expected_output = True
        self.assertEqual(result, expected_output)
