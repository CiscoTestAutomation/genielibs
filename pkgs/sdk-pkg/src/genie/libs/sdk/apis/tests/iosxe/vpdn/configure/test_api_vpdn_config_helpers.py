import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vpdn.configure import (
    configure_vpdn_group_l2tp_tunnel_busy_timeout,
    configure_vpdn_group_local_name,
    configure_vpdn_group_session_limit,
    configure_vpdn_logging_dead_cache,
    configure_vpdn_session_limit,
    unconfigure_vpdn_group_l2tp_tunnel_busy_timeout,
    unconfigure_vpdn_group_session_limit,
    unconfigure_vpdn_logging_dead_cache,
    unconfigure_vpdn_session_limit,
)


class TestConfigureVpdnLoggingDeadCache(unittest.TestCase):

    def test_configure_when_missing(self):
        device = Mock()
        device.api.get_running_config_dict.return_value = {}

        result = configure_vpdn_logging_dead_cache(device)

        self.assertIsNone(result)
        device.api.get_running_config_dict.assert_called_once_with()
        device.configure.assert_called_once_with("vpdn logging dead-cache")

    def test_skip_when_present(self):
        device = Mock()
        device.api.get_running_config_dict.return_value = {
            "vpdn logging dead-cache": {}
        }

        result = configure_vpdn_logging_dead_cache(device)

        self.assertIsNone(result)
        device.configure.assert_not_called()


class TestUnconfigureVpdnLoggingDeadCache(unittest.TestCase):

    def test_unconfigure_when_present(self):
        device = Mock()
        device.api.get_running_config_dict.return_value = {
            "vpdn logging dead-cache": {}
        }

        result = unconfigure_vpdn_logging_dead_cache(device)

        self.assertIsNone(result)
        device.configure.assert_called_once_with("no vpdn logging dead-cache")

    def test_skip_when_missing(self):
        device = Mock()
        device.api.get_running_config_dict.return_value = {}

        result = unconfigure_vpdn_logging_dead_cache(device)

        self.assertIsNone(result)
        device.configure.assert_not_called()


class TestConfigureVpdnSessionLimit(unittest.TestCase):

    def test_configure_when_missing(self):
        device = Mock()
        device.api.get_running_config_dict.return_value = {}

        result = configure_vpdn_session_limit(device, 16)

        self.assertIsNone(result)
        device.api.get_running_config_dict.assert_called_once_with()
        device.configure.assert_called_once_with("vpdn session-limit 16")

    def test_skip_when_present(self):
        device = Mock()
        device.api.get_running_config_dict.return_value = {
            "vpdn session-limit 16": {}
        }

        result = configure_vpdn_session_limit(device, 16)

        self.assertIsNone(result)
        device.configure.assert_not_called()


class TestUnconfigureVpdnSessionLimit(unittest.TestCase):

    def test_unconfigure_when_present(self):
        device = Mock()
        device.api.get_running_config_dict.return_value = {
            "vpdn session-limit 16": {}
        }

        result = unconfigure_vpdn_session_limit(device, 16)

        self.assertIsNone(result)
        device.configure.assert_called_once_with("no vpdn session-limit 16")

    def test_skip_when_missing(self):
        device = Mock()
        device.api.get_running_config_dict.return_value = {}

        result = unconfigure_vpdn_session_limit(device, 16)

        self.assertIsNone(result)
        device.configure.assert_not_called()


class TestConfigureVpdnGroupSessionLimit(unittest.TestCase):

    def test_configure_when_missing(self):
        device = Mock()
        device.api.get_running_config_dict.return_value = {
            "vpdn-group 11": {
                "protocol l2tp": {},
            }
        }

        result = configure_vpdn_group_session_limit(device, "11", 2)

        self.assertIsNone(result)
        device.api.get_running_config_dict.assert_called_once_with()
        device.configure.assert_called_once_with(["vpdn-group 11", "session-limit 2"])

    def test_skip_when_present(self):
        device = Mock()
        device.api.get_running_config_dict.return_value = {
            "vpdn-group 11": {
                "session-limit 2": {},
            }
        }

        result = configure_vpdn_group_session_limit(device, "11", 2)

        self.assertIsNone(result)
        device.configure.assert_not_called()


class TestConfigureVpdnGroupLocalName(unittest.TestCase):

    def test_configure_when_missing(self):
        device = Mock()
        device.api.get_running_config_dict.return_value = {
            "vpdn-group 11": {
                "accept-dialin": {},
            }
        }

        result = configure_vpdn_group_local_name(device, "11", "UUT1")

        self.assertIsNone(result)
        device.api.get_running_config_dict.assert_called_once_with()
        device.configure.assert_called_once_with(["vpdn-group 11", "local name UUT1"])

    def test_skip_when_present(self):
        device = Mock()
        device.api.get_running_config_dict.return_value = {
            "vpdn-group 11": {
                "local name UUT1": {},
            }
        }

        result = configure_vpdn_group_local_name(device, "11", "UUT1")

        self.assertIsNone(result)
        device.configure.assert_not_called()


class TestConfigureVpdnGroupL2tpTunnelBusyTimeout(unittest.TestCase):

    def test_configure_when_missing(self):
        device = Mock()
        device.api.get_running_config_dict.return_value = {
            "vpdn-group 11": {
                "accept-dialin": {},
            }
        }

        result = configure_vpdn_group_l2tp_tunnel_busy_timeout(device, "11", 60)

        self.assertIsNone(result)
        device.api.get_running_config_dict.assert_called_once_with()
        device.configure.assert_called_once_with(
            ["vpdn-group 11", "l2tp tunnel busy timeout 60"]
        )

    def test_skip_when_present(self):
        device = Mock()
        device.api.get_running_config_dict.return_value = {
            "vpdn-group 11": {
                "l2tp tunnel busy timeout 60": {},
            }
        }

        result = configure_vpdn_group_l2tp_tunnel_busy_timeout(device, "11", 60)

        self.assertIsNone(result)
        device.configure.assert_not_called()


class TestUnconfigureVpdnGroupSessionLimit(unittest.TestCase):

    def test_unconfigure_when_present(self):
        device = Mock()
        device.api.get_running_config_dict.return_value = {
            "vpdn-group 11": {
                "session-limit 2": {},
            }
        }

        result = unconfigure_vpdn_group_session_limit(device, "11", 2)

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            ["vpdn-group 11", "no session-limit 2"]
        )

    def test_skip_when_missing(self):
        device = Mock()
        device.api.get_running_config_dict.return_value = {
            "vpdn-group 11": {
                "protocol l2tp": {},
            }
        }

        result = unconfigure_vpdn_group_session_limit(device, "11", 2)

        self.assertIsNone(result)
        device.configure.assert_not_called()


class TestUnconfigureVpdnGroupL2tpTunnelBusyTimeout(unittest.TestCase):

    def test_unconfigure_when_present(self):
        device = Mock()
        device.api.get_running_config_dict.return_value = {
            "vpdn-group 11": {
                "l2tp tunnel busy timeout 60": {},
            }
        }

        result = unconfigure_vpdn_group_l2tp_tunnel_busy_timeout(device, "11", 60)

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            ["vpdn-group 11", "no l2tp tunnel busy timeout 60"]
        )

    def test_skip_when_missing(self):
        device = Mock()
        device.api.get_running_config_dict.return_value = {
            "vpdn-group 11": {
                "accept-dialin": {},
            }
        }

        result = unconfigure_vpdn_group_l2tp_tunnel_busy_timeout(device, "11", 60)

        self.assertIsNone(result)
        device.configure.assert_not_called()


if __name__ == "__main__":
    unittest.main()
