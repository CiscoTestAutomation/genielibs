import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_aaa_accounting_update_periodic


class TestConfigureAaaAccountingUpdatePeriodic(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          stack-12m:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9300
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['stack-12m']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_aaa_accounting_update_periodic(self):
        result = configure_aaa_accounting_update_periodic(self.device, '2880')
        expected_output = None
        self.assertEqual(result, expected_output)
