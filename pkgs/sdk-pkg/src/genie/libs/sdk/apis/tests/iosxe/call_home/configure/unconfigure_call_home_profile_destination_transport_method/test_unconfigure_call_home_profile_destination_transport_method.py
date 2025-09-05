from unittest import TestCase
from genie.libs.sdk.apis.iosxe.call_home.configure import unconfigure_call_home_profile_destination_transport_method
from unittest.mock import Mock

class TestUnconfigureCallHomeProfileDestinationTransportMethod(TestCase):

    def test_unconfigure_call_home_profile_destination_transport_method(self):
        device = Mock()
        profile = "MY_PROFILE"
        address = "http"

        unconfigure_call_home_profile_destination_transport_method(device, profile, address)

        device.configure.assert_called_once_with([
            "call-home",
            f"profile {profile}",
            f"no destination transport-method {address}",
        ])