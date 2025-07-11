from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.apphosting.configure import configure_thousand_eyes_application


class TestConfigureThousandEyesApplication(TestCase):

    def test_configure_thousand_eyes_application(self):
        self.device = Mock()
        configure_thousand_eyes_application(self.device, '1500', '1.1.1.2', '1.1.1.1', '255.255.255.0', 'dsadscasdc325423erwgwe', 'abc.com', '2.2.2.2')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no app-hosting appid 1keyes', 'app-hosting appid 1keyes', 'app-vnic AppGigabitEthernet trunk',
              'vlan 1500 guest-interface 0', 'guest-ipaddress 1.1.1.2 netmask 255.255.255.0', 'app-default-gateway 1.1.1.1 guest-interface 0',
              'app-resource docker', 'prepend-pkg-opts', 'run-opts 1 "-e TEAGENT_ACCOUNT_TOKEN=dsadscasdc325423erwgwe"', 
              'run-opts 3 "-e TEAGENT_PROXY_TYPE=STATIC"', 'run-opts 4 "-e TEAGENT_PROXY_LOCATION=abc.com"', 'name-server0 2.2.2.2', 'start'] ,)
        )
