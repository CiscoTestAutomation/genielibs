from unittest import TestCase
from genie.libs.sdk.apis.iosxe.apphosting.configure import configure_app_hosting_docker
from unittest.mock import Mock


class TestConfigureAppHostingDocker(TestCase):

    def test_configure_app_hosting_docker(self):
        self.device = Mock()
        result = configure_app_hosting_docker(self.device, '1keyes', '12345678', 'cisco-teye-USB', '1g')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['app-hosting appid 1keyes', 'app-resource docker', 'prepend-pkg-opts', 'run-opts 1 "-e TEAGENT_ACCOUNT_TOKEN=12345678"', 'run-opts 2 "--hostname=cisco-teye-USB --memory=1g"'],)
        )
