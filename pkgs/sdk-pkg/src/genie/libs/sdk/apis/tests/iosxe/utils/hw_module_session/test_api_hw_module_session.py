import os
from pyats.topology import loader
from unittest import TestCase
from unittest.mock import patch, MagicMock
from genie.libs.sdk.apis.iosxe.utils import hw_module_session


class TestHwModuleSession(TestCase):
    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          analog-perf-uut1:
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
        self.device = self.testbed.devices['analog-perf-uut1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_hw_module_session(self):
        # Mock the receive method to work with mock devices
        # The receive() method is used to consume data without pattern matching
        # For mock devices, we need to mock this as it doesn't work natively
        
        # Define the responses for each receive_buffer call
        responses = [
            # First call after hw-module session command
            "analog-perf-uut2#hw-module session 0/1\r\nEstablishing session connect to subslot 0/1\r\nTo exit, type ^a^q\r\n\r\npicocom v3.1\r\n\r\nport is        : /dev/ttyDASH2\r\nflowcontrol    : none\r\nbaudrate is    : 9600\r\nparity is      : none\r\ndatabits are   : 8\r\nstopbits are   : 1\r\nescape is      : C-a\r\nlocal echo is  : no\r\nnoinit is      : no\r\nnoreset is     : no\r\nhangup is      : no\r\nnolock is      : yes\r\nsend_cmd is    : sz -vv\r\nreceive_cmd is : rz -vv -E\r\nimap is        : \r\nomap is        : \r\nemap is        : crcrlf,delbs,\r\nlogfile is     : none\r\ninitstring     : none\r\nexit_after is  : not set\r\nexit is        : no\r\n\r\nType [C-a] [C-h] to see available commands\r\nTerminal ready",
            # Second call after show version command  
            "show version\r\n\r\nPID: NIM-4BRI-NT/TE\r\nVersion 62.3.4, built on Sep  4 2024:13:31:00 from /nobackup/dspbld/workspace/team_uc_jenkins/DSPWare_release_build/62.3.4\r\nNGIO Version ngio@polaris_dev/278\r\n\r\nDM8147>",
            # Third call after Ctrl+A Ctrl+Q exit
            "Terminating...\r\nSkipping tty reset...\r\nThanks for using picocom\r\nanalog-perf-uut2#"
        ]
        
        call_count = [0]
        
        def mock_receive(pattern):
            # Just return None - this is a no-op for mock devices
            print(f"[MOCK] device.receive() called with pattern: {pattern}")
            return None
        
        def mock_receive_buffer():
            result = responses[call_count[0]]
            print(f"[MOCK] device.receive_buffer() call #{call_count[0] + 1}, returning {len(result)} characters")
            print(f"[MOCK] Response preview: {result[:100]}...")
            call_count[0] += 1
            return result
        
        def mock_transmit(data):
            print(f"[MOCK] device.transmit() called with: {repr(data)}")
            return None
        
        # Patch the device methods
        with patch.object(self.device, 'receive', side_effect=mock_receive):
            with patch.object(self.device, 'receive_buffer', side_effect=mock_receive_buffer):
                with patch.object(self.device, 'transmit', side_effect=mock_transmit):
                    print("\n[TEST] Starting hw_module_session API call...")
                    result = hw_module_session(self.device, '0/1', False, True, 'show version', None)
                    print(f"\n[TEST] API returned {len(result)} characters")
                    print(f"[TEST] Result preview: {result[:200]}...")
                    
                    # Expected output should contain all three responses concatenated (after strip())
                    expected_output = responses[0] + "\n" + responses[1] + "\n" + responses[2]
                    self.assertEqual(result, expected_output)
                    print("[TEST] ✓ Test assertion passed!")
