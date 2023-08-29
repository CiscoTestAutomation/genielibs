import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.health.health import health_logging


class TestHealthLogging(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          R1_xe:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: csr1000v
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['R1_xe']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_health_logging(self):
        self.maxDiff = None
        result = health_logging(self.device)
        expected_output = {'health_data': {'lines': ['*Feb 14 16:22:43.522: %EVENTLIB-3-CPUHOG: '
                                   'R0/0: smd: undefined: 145ms, '
                                   'Traceback=1#394720775378fb301472d33765b83a70   '
                                   'c:7F41A4489000+37370 c:7F41A4489000+37679 '
                                   'prelib:7F41C9AEE000+777A '
                                   'prelib:7F41C9AEE000+767D '
                                   'c:7F41A4489000+C2ADA c:7F41A4489000+C2BD5 '
                                   'c:7F41A4489000+C99CB c:7F41A4489000+CAC2C '
                                   'btrace:7F41C85FC000+78CD '
                                   'evlib:7F41C92CF000+9145 '
                                   'evlib:7F41C92CF000+9A9C',
                          '*Feb 15 00:01:54.960: %EVENTLIB-3-CPUHOG: '
                                   'R0/0: smd: undefined: 109ms, '
                                   'Traceback=1#394720775378fb301472d33765b83a70   '
                                   'c:7F41A4489000+37370 '
                                   'evlib:7F41C92CF000+55D0 '
                                   'evutil:7F41C83E8000+AC71 '
                                   'evutil:7F41C83E8000+75D6 '
                                   'evutil:7F41C83E8000+6540 '
                                   'evutil:7F41C83E8000+8A22 '
                                   'evutil:7F41C83E8000+8808 '
                                   'uipeer:7F41B2CE5000+3F1B9 '
                                   'uipeer:7F41B2CE5000+1ECB5 '
                                   'evlib:7F41C92CF000+9145 '
                                   'evlib:7F41C92CF000+9A9C',
                          '*Feb 15 00:47:54.973: %EVENTLIB-3-CPUHOG: '
                                   'R0/0: smd: undefined: 140ms, '
                                   'Traceback=1#394720775378fb301472d33765b83a70   '
                                   'c:7F41A4489000+37370 c:7F41A4489000+EA6D5 '
                                   'uipeer:7F41B2CE5000+1D4F6 '
                                   'uipeer:7F41B2CE5000+1EBBE '
                                   'evlib:7F41C92CF000+9145 '
                                   'evlib:7F41C92CF000+9A9C '
                                   'orchestrator_lib:7F41C90AB000+CE31 '
                                   'orchestrator_lib:7F41C90AB000+CDB4 '
                                   'luajit:7F41A4FFB000+7C696 '
                                   'luajit:7F41A4FFB000+35C44 '
                                   'luajit:7F41A4FFB000+BFF9',
                          '*Feb 15 00:47:54.996: %EVENTLIB-3-CPUHOG: '
                                   'R0/0: smd: undefined: 249ms, '
                                   'Traceback=1#394720775378fb301472d33765b83a70   '
                                   'c:7F41A4489000+37370 c:7F41A4489000+EA635 '
                                   'trccfg:7F41AF49E000+285B '
                                   'uipeer:7F41B2CE5000+1EB68 '
                                   'evlib:7F41C92CF000+9145 '
                                   'evlib:7F41C92CF000+9A9C '
                                   'orchestrator_lib:7F41C90AB000+CE31 '
                                   'orchestrator_lib:7F41C90AB000+CDB4 '
                                   'luajit:7F41A4FFB000+7C696 '
                                   'luajit:7F41A4FFB000+35C44 '
                                   'luajit:7F41A4FFB000+BFF9',
                          '*Feb 15 13:20:21.120: %EVENTLIB-3-CPUHOG: '
                                   'R0/0: smd: undefined: 176ms, '
                                   'Traceback=1#394720775378fb301472d33765b83a70   '
                                   'c:7F41A4489000+37370 c:7F41A4489000+37679 '
                                   'prelib:7F41C9AEE000+777A '
                                   'prelib:7F41C9AEE000+767D '
                                   'c:7F41A4489000+C2ADA c:7F41A4489000+C2BD5 '
                                   'c:7F41A4489000+C99CB c:7F41A4489000+CAC2C '
                                   'btrace:7F41C85FC000+78CD '
                                   'evlib:7F41C92CF000+9145 '
                                   'evlib:7F41C92CF000+9A9C',
                          '*Feb 15 15:54:30.013: %EVENTLIB-3-CPUHOG: '
                                   'R0/0: smd: undefined: 112ms, '
                                   'Traceback=1#394720775378fb301472d33765b83a70   '
                                   'c:7F41A4489000+37370 c:7F41A4489000+EFED0 '
                                   'c:7F41A4489000+C2C75 c:7F41A4489000+C99CB '
                                   'c:7F41A4489000+CAC2C '
                                   'btrace:7F41C85FC000+78CD '
                                   'evlib:7F41C92CF000+9145 '
                                   'evlib:7F41C92CF000+9A9C '
                                   'orchestrator_lib:7F41C90AB000+CE31 '
                                   'orchestrator_lib:7F41C90AB000+CDB4 '
                                   'luajit:7F41A4FFB000+7C696',
                          '*Feb 16 10:47:57.702: %EVENTLIB-3-CPUHOG: '
                                   'R0/0: smd: undefined: 121ms, '
                                   'Traceback=1#394720775378fb301472d33765b83a70   '
                                   'c:7F41A4489000+37370 c:7F41A4489000+87E00 '
                                   'evutil:7F41C83E8000+84BC '
                                   'uipeer:7F41B2CE5000+3F1B9 '
                                   'uipeer:7F41B2CE5000+1ECB5 '
                                   'evlib:7F41C92CF000+9145 '
                                   'evlib:7F41C92CF000+9A9C '
                                   'orchestrator_lib:7F41C90AB000+CE31 '
                                   'orchestrator_lib:7F41C90AB000+CDB4 '
                                   'luajit:7F41A4FFB000+7C696 '
                                   'luajit:7F41A4FFB000+35C44'],
                 'num_of_logs': 7}}
        self.assertEqual(result, expected_output)
