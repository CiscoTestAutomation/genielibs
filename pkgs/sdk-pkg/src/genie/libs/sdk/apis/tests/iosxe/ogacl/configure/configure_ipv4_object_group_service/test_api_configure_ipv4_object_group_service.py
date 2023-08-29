import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.ogacl.configure import configure_ipv4_object_group_service


class TestConfigureIpv4ObjectGroupService(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          P-R1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: C9400
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['P-R1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_ipv4_object_group_service(self):
        result = configure_ipv4_object_group_service(self.device, 'ogacl_service', 'services', ['ospf', 'icmp echo', 'icmp echo-reply', 'tcp source range 5000 6000'])
        expected_output = None
        self.assertEqual(result, expected_output)
