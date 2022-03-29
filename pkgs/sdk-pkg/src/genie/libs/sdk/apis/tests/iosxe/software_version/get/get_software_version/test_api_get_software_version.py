import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.software_version.get import get_software_version


class TestGetSoftwareVersion(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          9600_Switch:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['9600_Switch']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_software_version(self):
        result = get_software_version(self.device)
        expected_output = ('Cisco IOS Software Cupertino, Catalyst L3 Switch Software (CAT9K_IOSXE), '
 'Experimental Version 17.8.20211216:071212 '
 '[BLD_POLARIS_DEV_S2C_20211216_061759:/nobackup/mcpre/s2c-build-ws 101]\n'
 'Copyright (c) 1986-2021 by Cisco Systems, Inc.\n'
 'Compiled Wed 15-Dec-21 23:12 by mcpre')
        self.assertEqual(result, expected_output)
