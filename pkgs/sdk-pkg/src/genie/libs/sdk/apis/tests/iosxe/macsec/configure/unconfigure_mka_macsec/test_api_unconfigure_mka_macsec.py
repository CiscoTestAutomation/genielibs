import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.macsec.configure import unconfigure_mka_macsec


class TestUnconfigureMkaMacsec(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          FUGAZI:
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
        self.device = self.testbed.devices['FUGAZI']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_mka_macsec(self):
        result = unconfigure_mka_macsec(self.device, 'Te0/1/1', 'K1', 'POLICY')
        expected_output = None
        self.assertEqual(result, expected_output)
