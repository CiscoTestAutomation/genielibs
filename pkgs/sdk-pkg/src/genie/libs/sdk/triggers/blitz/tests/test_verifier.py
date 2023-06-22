from genie.libs.sdk.triggers.blitz.verifiers import DefaultVerifier
from typing import Tuple, Any
from google.protobuf import json_format


class CustomVerifier(DefaultVerifier):

    def get_config_verify(self,
                          decoded_response: Tuple[list, list],
                          key: bool = False,
                          sequence: Any = None) -> bool:
        # Do something
        return True

    def end_subscription(self) -> bool:
        return True


class VerifierWithArgs(DefaultVerifier):

    def get_config_verify(self,
                          decoded_response: Tuple[list, list],
                          key: bool = False,
                          sequence: Any = None) -> bool:
        if not self.format['verifier'].get('my_arg1') == 1:
            return False
        if not self.format['verifier'].get('my_arg2') == 'test':
            return False
        return True


class VerifierWithCustomDecoder(DefaultVerifier):
    def gnmi_decoder(self, response, namespace: dict = None, method: str = 'get'):
        return json_format.MessageToDict(response)

    def get_config_verify(self,
                          decoded_response: dict,
                          key: bool = False,
                          sequence: Any = None) -> bool:
        return decoded_response['notification'][0]['update'][0]['path']['elem'][0]['name'] == 'System/igmp-items/inst-items'
