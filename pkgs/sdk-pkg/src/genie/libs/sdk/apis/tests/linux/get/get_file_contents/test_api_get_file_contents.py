import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.linux.get import get_file_contents


class TestGetFileContents(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          S1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os linux --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: linux
            platform: None
            type: None
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['S1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_file_contents(self):
        result = get_file_contents(self.device, '/users/lgerrior/test_dir/device_key', False)
        expected_output = ('-----BEGIN EC PRIVATE KEY-----\r\n'
 'Proc-Type: 4,ENCRYPTED\r\n'
 'DEK-Info: AES-256-CBC,D738EC42CBE1D776999970BEAE279176\r\n'
 '\r\n'
 'XK9QAj86kgoFuj71zUq8CKNUI9NJqCqbq9WU0PIMT52JWTZZo8J5YcohS2vPqUGP\r\n'
 'FvDmf9SwcAeEmY8wyVlfbv99Cdp0Psuh7OSPy7eleWpcKa8v5VKy6ay5fgRdtBRo\r\n'
 'eS81Ddy6+vBb2fpG7gt8YLud1UCE7P8TAIMVADqQwrcCRvxxG2iTcsZfZMwy3jdS\r\n'
 '1kBeRyqPMGU1w3b4k41i3QTUZyAhkL10Bnzzis9KcMo=\r\n'
 '-----END EC PRIVATE KEY-----')
        self.assertEqual(result, expected_output)
