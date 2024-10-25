import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_aaa_accounting_connection_default_start_stop_group_tacacs_group


class TestConfigureAaaAccountingConnectionDefaultStartStopGroupTacacsGroup(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          PREG_IFD_CFD_TB2_9500_SA:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: C9500-24Q
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['PREG_IFD_CFD_TB2_9500_SA']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_aaa_accounting_connection_default_start_stop_group_tacacs_group(self):
        result = configure_aaa_accounting_connection_default_start_stop_group_tacacs_group(self.device, 'TACACS-group')
        expected_output = None
        self.assertEqual(result, expected_output)
