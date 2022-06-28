import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.software_version.get import get_software_version


class TestGetSoftwareVersion(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          A2-9300-3M:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9300
            type: switch
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['A2-9300-3M']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_software_version(self):
        result = get_software_version(self.device)
        expected_output = ('Cisco IOS Software [Dublin], Catalyst L3 Switch Software (CAT9K_IOSXE), '
 'Experimental Version 17.10.20220531:054228 '
 '[BLD_POLARIS_DEV_S2C_20220531_051149:/nobackup/mcpre/s2c-build-ws 101]\n'
 'Copyright (c) 1986-2022 by Cisco Systems, Inc.\n'
 'Compiled Mon 30-May-22 22:42 by mcpre')
        self.assertEqual(result, expected_output)
