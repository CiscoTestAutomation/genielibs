import os
from pyats.topology import loader
from unittest import TestCase
from genie.libs.sdk.apis.iosxe.startup_config.verify import \
    verify_show_startup_config_section


class TestVerifyShowStartupConfigSection(TestCase):
    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          DNAC-4:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir
                    {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: router
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['DNAC-4']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_show_startup_config_section(self):
        result = verify_show_startup_config_section(
            self.device,
            section='switchport',
            expect_list=['switchport mode access',
                         'switchport access vlan 100'],
            unexpect_list=['switchport mode trunk']
        )
        self.assertTrue(result)
    def test_verify_show_startup_config_section(self):
        result = verify_show_startup_config_section(
            self.device,
            section='switchport',
            expect_list=['switchport mode trunk',
                         'switchport access vlan 100'],
        )
        self.assertFalse(result)
