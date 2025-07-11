from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.apphosting.configure import configure_app_hosting_appid_docker


class TestConfigureAppHostingAppidDocker(TestCase):

    def test_configure_app_hosting_appid_docker(self):
        self.device = Mock()
        configure_app_hosting_appid_docker(self.device, '1key', True, [{'index': 3,
        'string': '-e TEAGENT_ACCOUNT_TOKEN=r3d29srpebr4j845lvnamwhswlori2xs'},
      {'index': 5, 'string': '-e TEAGENT_PROXY_TYPE=STATIC'},
      {'index': 7, 'string': '-e TEAGENT_PROXY_BYPASS_LIST=*.cisco.com'}])
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['app-hosting appid 1key', 'app-resource docker','prepend-pkg-opts',
              'run-opts 3 "-e TEAGENT_ACCOUNT_TOKEN=r3d29srpebr4j845lvnamwhswlori2xs"',
              'run-opts 5 "-e TEAGENT_PROXY_TYPE=STATIC"','run-opts 7 "-e TEAGENT_PROXY_BYPASS_LIST=*.cisco.com"'] ,)
        )

    def test_configure_app_hosting_appid_docker_1(self):
        self.device = Mock()
        configure_app_hosting_appid_docker(self.device, '1key1', False, [{'index': 3,
          'string': '-e TEAGENT_ACCOUNT_TOKEN=r3d29srpebr4j845lvnamwhswlori2xs'},
        {'index': 5, 'string': '-e TEAGENT_PROXY_TYPE=STATIC'},
        {'index': 7, 'string': '-e TEAGENT_PROXY_BYPASS_LIST=*.cisco.com'}])
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['app-hosting appid 1key1','app-resource docker',
              'run-opts 3 "-e TEAGENT_ACCOUNT_TOKEN=r3d29srpebr4j845lvnamwhswlori2xs"',
              'run-opts 5 "-e TEAGENT_PROXY_TYPE=STATIC"','run-opts 7 "-e TEAGENT_PROXY_BYPASS_LIST=*.cisco.com"'] ,)
        )

    def test_configure_app_hosting_appid_docker_2(self):
        self.device = Mock()
        configure_app_hosting_appid_docker(self.device, '1key2', True, [])
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['app-hosting appid 1key2', 'app-resource docker', 'prepend-pkg-opts'],)
        )
