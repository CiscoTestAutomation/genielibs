import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.aaa.configure import unconfigure_aaa_accounting_dot1x_default_start_stop_group


class TestUnconfigureAaaAccountingDot1xDefaultStartStopGroup(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          T6_C9200L_STK:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: svl
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['T6_C9200L_STK']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_aaa_accounting_dot1x_default_start_stop_group(self):
        result = unconfigure_aaa_accounting_dot1x_default_start_stop_group(self.device, 'srvgrp')
        expected_output = None
        self.assertEqual(result, expected_output)
