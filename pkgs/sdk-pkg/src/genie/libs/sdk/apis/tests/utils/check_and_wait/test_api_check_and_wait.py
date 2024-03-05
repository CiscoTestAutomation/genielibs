import os
import unittest
import re
from pyats.topology import loader
from genie.libs.sdk.apis.utils import check_and_wait


class TestCheckAndWait(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Organ:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: router
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Organ']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_check_and_wait(self):
        result = check_and_wait('True', '60', '10', None)
        self.assertIsInstance(result, object)
