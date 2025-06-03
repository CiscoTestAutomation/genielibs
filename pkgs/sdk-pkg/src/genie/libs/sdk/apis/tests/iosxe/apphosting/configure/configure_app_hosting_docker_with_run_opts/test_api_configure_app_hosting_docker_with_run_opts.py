from unittest import TestCase
from genie.libs.sdk.apis.iosxe.apphosting.configure import configure_app_hosting_docker_with_run_opts
from unittest.mock import Mock


class TestConfigureAppHostingDockerWithRunOpts(TestCase):

    def test_configure_app_hosting_docker_with_run_opts(self):
        self.device = Mock()
        result = configure_app_hosting_docker_with_run_opts(self.device, '1keyes', '1', '"--shm-size=256M"')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['app-hosting appid 1keyes', 'app-resource docker', 'no run-opts 1 "--shm-size=256M"', 'prepend-pkg-opts'],)
        )
