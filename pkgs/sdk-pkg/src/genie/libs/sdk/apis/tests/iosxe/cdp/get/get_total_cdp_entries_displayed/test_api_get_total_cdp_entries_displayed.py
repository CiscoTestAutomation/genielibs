import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.cdp.get import get_total_cdp_entries_displayed


class TestGetTotalCdpEntriesDisplayed(unittest.TestCase):

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

    def test_get_total_cdp_entries_displayed(self):
        result = get_total_cdp_entries_displayed(self.device)
        expected_output = 17
        self.assertEqual(result, expected_output)
