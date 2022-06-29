import logging
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.acl.clear import clear_ip_reflexive_list


class TestClearIpReflexiveList(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          Cat9600-SVL_CGW:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
                # ip: 10.126.109.21 
                # port: 2013
            os: iosxe
            platform: C9600
            type: C9600
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Cat9600-SVL_CGW']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )
    def test_clear_ip_reflexive_list(self):
        result = clear_ip_reflexive_list(self.device,'REF1')
        expected_output = None
        logging.info(result)
        self.assertEqual(result, expected_output)

    def test_clear_ip_reflexive_list_1(self):
        result = clear_ip_reflexive_list(self.device,'*')
        expected_output = None
        logging.info(result)
        self.assertEqual(result, expected_output)
