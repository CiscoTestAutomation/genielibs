import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import configure_virtual_template


class TestConfigureVirtualTemplate(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          C1113-8P_pkumarmu:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: router
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['C1113-8P_pkumarmu']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_virtual_template(self):
        result = configure_virtual_template(self.device, '100', 'Loopback2', False, None, False, False, 0, 0, '', '', False, False, None, 'ipv6_local_pool')
        expected_output = None
        self.assertEqual(result, expected_output)
