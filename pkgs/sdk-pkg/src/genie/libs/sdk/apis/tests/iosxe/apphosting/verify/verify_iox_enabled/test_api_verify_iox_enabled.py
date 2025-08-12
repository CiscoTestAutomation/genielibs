import os
from pyats.topology import loader
from unittest import TestCase
from genie.libs.sdk.apis.iosxe.apphosting.verify import verify_iox_enabled


class TestVerifyIoxEnabled(TestCase):
    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Q11-2042_1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: NG9K
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Q11-2042_1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_iox_enabled(self):
        services = ['caf_service', 'ioxman_service', 'libvirtd','dockerd']
        result = verify_iox_enabled(self.device,services=services)
        expected_output = True
        self.assertEqual(result, expected_output)
