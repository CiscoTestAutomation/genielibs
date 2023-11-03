from genie.libs.sdk.triggers.blitz.verifiers import DefaultBaseVerifier
from typing import Tuple, Any
from google.protobuf import json_format


class CustomVerifier(DefaultBaseVerifier):

    def get_config_verify(self,
                          raw_response: Any,
                          key: bool = False,
                          sequence: Any = None) -> bool:
        # Do something
        return True

    def end_subscription(self) -> bool:
        return True


class VerifierWithArgs(DefaultBaseVerifier):

    def get_config_verify(self,
                          raw_response: any,
                          key: bool = False,
                          sequence: Any = None) -> bool:
        if not self.format['verifier'].get('my_arg1') == 1:
            return False
        if not self.format['verifier'].get('my_arg2') == 'test':
            return False
        return True


class VerifierWithCustomDecoder(DefaultBaseVerifier):
    def decode(self, response, namespace: dict = None, method: str = 'get'):
        return json_format.MessageToDict(response)

    def get_config_verify(self,
                          raw_response: any,
                          key: bool = False,
                          sequence: Any = None) -> bool:
        decoded_response = self.decode(raw_response)
        return decoded_response['notification'][0]['update'][0]['path']['elem'][0]['name'] == 'System/igmp-items/inst-items'
