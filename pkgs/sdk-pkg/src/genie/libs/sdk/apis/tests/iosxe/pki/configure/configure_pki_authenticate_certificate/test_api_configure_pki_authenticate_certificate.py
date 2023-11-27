import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.pki.configure import configure_pki_authenticate_certificate


class TestConfigurePkiAuthenticateCertificate(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Startrek-SVL:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Startrek-SVL']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_pki_authenticate_certificate(self):
        result = configure_pki_authenticate_certificate(self.device, (' MIIDUjCCAjqgAwIBAgIBFDANBgkqhkiG9w0BAQsFADBCMQ0wCwYDVQQDDARTZWxm\n'
 ' MRswGQYJKoZIhvcNAQkCDAxTVkxfOTUwMF80MFgxFDASBgNVBAUTC0ZDVzIxNTBB\n'
 ' MVhKMB4XDTIzMDUxNTA0MTk0MVoXDTMzMDUxNDA0MTk0MVowQjENMAsGA1UEAwwE\n'
 ' U2VsZjEbMBkGCSqGSIb3DQEJAgwMU1ZMXzk1MDBfNDBYMRQwEgYDVQQFEwtGQ1cy\n'
 ' MTUwQTFYSjCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALh6BgATLjtH\n'
 ' 7u5N8Mpyada4wH81HqohQoutTrwgP7/bm8uExvllCutC2vViHT6QkFMTZJhmb7qE\n'
 ' KFrfKxvaKVlSBAWWY3oSrPBYOCv4tc6RR4tv5nA0cDBprlMRffZIQe76FS3SRClu\n'
 ' aSUol3hJ2IPcuySIAKg+ed76OwNSuoNhx0v1wholf12UR5M8sRhObfQ5AV6pjYcc\n'
 ' 4eAllqJNFOiUM5CLtX4brN/HG8sMJLxHbI522+QaD1c4LcAI34EzyyALBxdDLo5w\n'
 ' 6PFL4nSXAyNVS+Vrhk+MXXZKEA8PaLDIBamXL3SAZSCAjaxsz+YtzEw+NPTVugDT\n'
 ' lt/fHiFq2pcCAwEAAaNTMFEwHQYDVR0OBBYEFCLrr/FQ8/iMjMbymk5CJxi03kWz\n'
 ' MB8GA1UdIwQYMBaAFCLrr/FQ8/iMjMbymk5CJxi03kWzMA8GA1UdEwEB/wQFMAMB\n'
 ' Af8wDQYJKoZIhvcNAQELBQADggEBAAhKPV6EBT1pdtSo6RD0wY3kUVe7/wMhmOga\n'
 ' vKIwVvrrJR6tgGEEX8tnN2qPGR2f/ULhbHZ6Y73Sq7kwvd0wbOJOr4vDJSWV7/6N\n'
 ' abNFYmCpaQK9C/3UtCLD1gL2i8FdweQEjmpQ7EC7SPsHiGDUJh59W0bgLoAH+1YW\n'
 ' frw+Jig7mmdW80NMyyxyWQxU7Llvx3cix3Tt9G3r9ZQL19CUXC4uiCj7Z13YLbuA\n'
 ' VmOdnCAmgXl35sdb+UBsZUZlIGDMl+drD2sM/zh+apUYHYOMSefzhd9MYcGkK4GF\n'
 ' qsZIE1fGBj729xrq5dZBhUZob57i1rsmuNoN38InOkeP11jRKXg=\n'), 'Other')
        expected_output = None
        self.assertEqual(result, expected_output)
