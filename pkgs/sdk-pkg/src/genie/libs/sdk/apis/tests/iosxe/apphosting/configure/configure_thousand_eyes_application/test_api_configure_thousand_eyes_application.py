import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.apphosting.configure import configure_thousand_eyes_application


class TestConfigureThousandEyesApplication(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          dut1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['dut1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_thousand_eyes_application(self):
        result = configure_thousand_eyes_application(self.device, '1500', '1.1.1.2', '1.1.1.1', '255.255.255.0', 'dsadscasdc325423erwgwe', 'abc.com', '2.2.2.2')
        expected_output = None
        self.assertEqual(result, expected_output)
