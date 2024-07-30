import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.apphosting.execute import install_wcs_enable_guestshell


class TestInstallWcsEnableGuestshell(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          stack3-nyquist-1:
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
        self.device = self.testbed.devices['stack3-nyquist-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_install_wcs_enable_guestshell(self):
        result = install_wcs_enable_guestshell(self.device, 'wcs_docker', 'flash', 'iperf3_signed.tar', 300)
        expected_output = False
        self.assertEqual(result, expected_output)
