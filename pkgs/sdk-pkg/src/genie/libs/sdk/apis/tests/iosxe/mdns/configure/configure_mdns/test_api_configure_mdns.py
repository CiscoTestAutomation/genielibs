import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mdns.configure import configure_mdns


class TestConfigureMdns(TestCase):

    def test_configure_mdns(self):
        device = Mock()
        device.configure.return_value = None

        result = configure_mdns(
            device,
            "custom22",
            ["policie31", "policie32", "policie33", "policie34"],
            ["IN", "OUT", "OUT", "IN"],
            {
                "Policy41": ["policie31", "IN"],
                "Policy42": [
                    "policie32",
                    "OUT",
                    "policie33",
                    "OUT",
                    "policie34",
                    "IN",
                ],
            },
            "policie55",
            "IN",
            "query",
            "policie66",
            "OUT",
            "filter8",
            {"Policy43": ["policie55", "IN", "policie66", "OUT"]},
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                "mdns-sd gateway",
                "mdns-sd service-definition custom22",
                "service-type _airplay._tcp.local",
                "service-type _raop._tcp.local",
                "service-type _ipp._tcp.local",
                "service-type _afpovertcp._tcp.local",
                "service-type _nfs._tcp.local",
                "service-type _ssh._tcp.local",
                "service-type _dpap._tcp.local",
                "service-type _daap._tcp.local",
                "service-type _ichat._tcp.local",
                "service-type _presence._tcp.local",
                "service-type _http._tcp.local",
                "service-type _ipps._tcp.local",
                "service-type _printer._tcp.local",
                "service-type _smb._tcp.local",
                "service-type _ftp._tcp.local",
                "mdns-sd service-list policie31 IN",
                "match custom22",
                "mdns-sd service-list policie32 OUT",
                "match custom22",
                "mdns-sd service-list policie33 OUT",
                "match custom22",
                "mdns-sd service-list policie34 IN",
                "match custom22",
                "mdns-sd service-policy Policy41",
                "service-list policie31 IN",
                "mdns-sd service-policy Policy42",
                "service-list policie32 OUT",
                "service-list policie33 OUT",
                "service-list policie34 IN",
                "mdns-sd service-list policie55 IN",
                "match custom22 message-type query",
                "mdns-sd service-list policie66 OUT",
                "match custom22 location-filter filter8",
                "mdns-sd service-policy Policy43",
                "service-list policie55 IN",
                "service-list policie66 OUT",
            ]
        )


if __name__ == "__main__":
    unittest.main()
