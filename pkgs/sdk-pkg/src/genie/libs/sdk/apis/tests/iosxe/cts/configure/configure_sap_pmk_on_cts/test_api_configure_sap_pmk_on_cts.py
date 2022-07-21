import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.cts.configure import configure_sap_pmk_on_cts


class TestConfigureSapPmkOnCts(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          9500H_SVL_W0607:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9500
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['9500H_SVL_W0607']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_sap_pmk_on_cts(self):
        result = configure_sap_pmk_on_cts(self.device, 'HundredGigE1/0/23', '0000000000000000000000000000000000000000000000000000000012345678', 'gcm-encrypt null gmac no-encap')
        expected_output = None
        self.assertEqual(result, expected_output)
