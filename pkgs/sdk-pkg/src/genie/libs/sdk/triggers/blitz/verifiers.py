from logging import Logger
import logging
from typing import Any, List, Tuple
from abc import ABC
import re
from pprint import pformat
import json
from google.protobuf import json_format
from .rpcverify import RpcVerify, OptFields, OperationalFieldsNode
from .gnmi_util import GnmiMessage


class BaseVerifier(ABC):
    def __init__(self,
                 device: Any,
                 returns: dict,
                 log: Logger,
                 format: dict = None,
                 steps=None,
                 datastore=None,
                 **kwargs):
        super().__init__()
        self.returns = returns
        self.steps = steps
        self.datastore = datastore
        self.log = log
        self.format = format
        self.kwargs = kwargs
        self.device = device

    def get_config_verify(self,
                          decoded_response: Any,
                          key: bool = False,
                          sequence: Any = None) -> bool:
        """
        Used by GNMI and Netconf Get and Set test cases validation.
        Called when a GetResponse is received.

        Args:
            decoded_response (any): Response received from the device and decoded
            by using the decoder method.
            key (bool, optional): Indicates if the response is a key. Defaults to False.

        Returns:
            bool: Indicates if test should pass or fail.
        """
        pass

    def gnmi_decoder(self, response: Any,
                     namespace: dict = None,
                     method: str = 'get') -> Any:
        """
        Used by GNMI to decode response before passing it to verifier.

        Args:
            response (gnmi_pb2.GetResponse | gnmi_pb2.SubscribeResponse): Response received from the device.
            method (str): Gnmi method. Defaults to 'get'.
        Returns:
            Any: Decoded response.
        """
        pass

    def netconf_decoder(self, response: Any,
                        namespace: dict = None,
                        method: str = 'get-config') -> Any:
        """
        Used by Netconf to decode response before passing it to verifier.

        Args:
            response (Any): Response received from the device.
            method (str): Netconf method. Defaults to 'get-config'.
        Returns:
            Any: Decoded response.
        """
        pass

    def restconf_decoder(self, response: Any,
                         namespace: dict = None,
                         method='') -> Any:
        """
        Used by Restconf to decode response before passing it to verifier.

        Args:
            response (gnmi_pb2.GetResponse | gnmi_pb2.SubscribeResponse): Response received from the device.
            method (str): Gnmi method. Defaults to 'get'.
        Returns:
            Any: Decoded response.
        """
        pass

    def subscribe_verify(self, decoded_response: Any, sub_mode: str = 'SAMPLE'):
        """
        Used by GNMI Subscription test cases validation.
        Called on every subscription update.

        Args:
            response (gnmi_pb2.SubscribeResponse): Response received from the device.
            sub_mode (str): Gnmi subscription mode. Defaults to 'SAMPLE'.
        """
        pass

    def end_subscription(self, errors: List[Exception]) -> bool:
        """
        Used by GNMI Subscription test cases validation.
        Method called when subscription is ended. State should be evaluated here.

        Returns:
            bool: Indicates if test should pass or fail.
        """
        pass

    def edit_config_auto_validate(self, response: any, rpc_data: dict, namespace_modules: dict) -> bool:
        """Auto-validaton after set-config operation for netconf and gnmi

        Args:
            response (any): _description_
            rpc_data (dict): _description_
            namespace_modules (dict): _description_

        Returns:
            bool: Validation result
        """
        pass

    def verify_common_cases(func) -> bool:
        """Decorator to verify common cases

        Returns:
            bool: Test result
        """

        def inner(self, response):
            # Response will be 'None' when some error is received
            if response is None:
                return False
            # Response will be empty, when no response received,
            # If returns not provided, set result false.
            elif not response and not self.returns:
                return False
            # Response is received, but user don't want to validate returns
            # set result to True as response is successfully received.
            elif response and not self.returns:
                return True
            return func(self, response)
        return inner


class DefaultVerifier(BaseVerifier):
    RE_FIND_KEYS = re.compile(r'\[.*?\]')
    RE_CLEAR_KEYS = re.compile(r'[\"\[\]]+')

    def __init__(self,
                 device: Any,
                 returns: dict,
                 log: Logger,
                 format: dict = None,
                 steps=None,
                 datastore=None,
                 **kwargs):
        super().__init__(device, returns, log, format, steps, datastore, **kwargs)
        self.rpc_verify = RpcVerify(log=self.log)

    @property
    def returns(self) -> List[OptFields]:
        return self._returns

    @returns.setter
    def returns(self, returns: List[dict]):
        if returns and isinstance(returns[0], dict):
            self._returns = [OptFields(**r) for r in returns]
        elif not returns:
            self._returns = []
        else:
            self._returns = returns

    def gnmi_decoder(self, response: Any,
                     namespace: dict = None,
                     method: str = 'get') -> List[OptFields]:
        """Process get response and convert into dict

        Args:
          response : raw gNMI get response.
          namespace (dict): Can be used if verifier is implemented.

        Returns:
          List[OptFields]: List of OptFields
        """
        json_dicts = []
        opfields = []
        notification = json_format.MessageToDict(response)
        if 'notification' not in notification and 'update' not in notification:
            raise Exception('No notification in Response')
        if method == 'get':
            notifications = notification['notification']
        elif method == 'subscribe':
            notifications = [notification['update']]
        for notification in notifications:
            if 'update' not in notification:
                raise Exception(f'No update in {method.capitalize()}Response')
            prefix = notification.get('prefix')
            for updates in notification['update']:
                json_dicts.append(GnmiMessage.process_update(
                    updates,
                    prefix,
                    namespace,
                    opfields
                ))
        self.log.info(
            f'{method.capitalize()}Response JSON value decoded\n' +
            '=' * 31 + '\n'
        )
        if json_dicts:
            try:
                for result in json_dicts:
                    try:
                        msg = json.dumps(result, indent=2)
                        self.log.info(msg)
                    except Exception:
                        self.log.error(str(result))
            except TypeError:
                self.log.error(str(json_dicts))
        return json_dicts, opfields

    @BaseVerifier.verify_common_cases
    def get_config_verify(self,
                          decoded_response: Tuple[list, list],
                          key: bool = False,
                          sequence: Any = None) -> bool:
        decoded_response = decoded_response[1]
        if not decoded_response:
            decoded_response.append((None, "/"))
        return self.rpc_verify.process_operational_state(decoded_response, self.returns, key=key, sequence=sequence)

    def subscribe_verify(self, decoded_response: Tuple[list, list], sub_type: str = 'ONCE'):
        """Decode response and verify result.

        Decoder callback returns desired format of response.
        Verify callback returns verification of expected results.

        Args:
          response (proto.gnmi_pb2.Notification): Contains updates that
              have changes since last timestamp.
        """
        # whole_response = (sub_type == 'ONCE')
        try:
            opfields = decoded_response[1]
            # Split returns on the basis of paths,
            # received in opfields
            returns_found: List[OptFields] = []
            for field in opfields:
                field_xp = field[1]
                for ret in self.returns:
                    xp = ret.xpath
                    if xp == field_xp and ret not in returns_found:
                        returns_found.append(ret)
                        break
                    elif '[' in xp:
                        # if list keys are found in the returns field['xpath']
                        # Eg: returns['xpath'] = /Sys/List[key=value]/leaf
                        # if above xpath with no keys '/Sys/List/leaf'
                        # is in the opfield that means this might be the
                        # possible returns to select, but we need check
                        # keys in opfields as well.
                        xp_no_keys = re.sub(self.RE_FIND_KEYS, '', xp)
                        if xp_no_keys == field_xp:
                            # To make sure that this is the correct returns to select
                            # we need to check that all the keys mentioned in the xpath
                            # are in opfield or not.
                            all_keys_in_opfield = self.find_keys_in_opfield(
                                xp, opfields)
                            # If all keys are present in opfield, then take this returns for validation.
                            if all_keys_in_opfield and ret not in returns_found:
                                returns_found.append(ret)
                                break

            if opfields and returns_found:
                if self.log.level == logging.DEBUG:
                    msg = 'Xpath/Value\n' + '=' * 11 + \
                        '\n' + pformat(opfields)
                    self.log.debug(msg)
                result = self.rpc_verify.process_operational_state(
                    opfields, returns_found)
                if result:
                    self.returns = [
                        r for r in self.returns if r not in returns_found]
        except Exception as exc:
            self.log.error(str(exc))
            raise

    def end_subscription(self, errors: List[Exception]) -> bool:
        if errors:
            return False
        result = True
        for ret in self.returns:
            xp = ret.xpath
            val = ret.value
            self.log.error(
                'ERROR: "{0} value: {1}" Not found.'.format(xp, str(val)))
            result = False
        return result

    def edit_config_auto_validate(self, response: any, rpc_data: dict, namespace_modules: dict) -> bool:
        decoded_response = self.gnmi_get_config_decoder(
            response, namespace=namespace_modules)
        result = True
        nodes: List[OperationalFieldsNode] = []
        list_keys: List[OptFields] = []
        par_xp = ''
        del_parent = False
        if 'explicit' in self.rpc_verify.with_defaults:
            # RFC 6243 - Only tags set by client sould be in reply
            self.log.info('WITH DEFAULTS - EXPLICIT MODE')
        elif 'report-all' in self.rpc_verify.with_defaults:
            # RFC 6243 - if value is default it should match
            self.log.info('WITH DEFAULTS - REPORT-ALL MODE')
        else:
            # RFC 6243 not supported
            self.log.info('WITH DEFAULTS - NOT REPORTED')

        for node in rpc_data.get('nodes', []):
            # original xpath with key/value required to validate
            # key values with multilist entries in response
            xpath_original = re.sub(
                self.rpc_verify.RE_FIND_PREFIXES, '/', node.get('xpath', ''))
            xpath_original = re.sub(
                self.rpc_verify.RE_FIND_KEY_PREFIX, '[', xpath_original)
            # xpath with keys and namespace prefix stripped.
            xpath = re.sub(self.rpc_verify.RE_FIND_KEYS,
                           '', node.get('xpath', ''))
            xpath = re.sub(self.rpc_verify.RE_FIND_PREFIXES, '/', xpath)
            if del_parent:
                # Check to see if parent and child have same xpath,
                # so "not boundary" will be True hence continue.
                # If boundary does not starts with '/' then xpath is not a child.
                # Ex: /xpath/foo/foobar is not a child of /xpath/foobar/foo
                if par_xp and par_xp in xpath:
                    boundary = xpath[len(par_xp):]
                    if not boundary or \
                            boundary.startswith('/'):
                        continue
            edit_op = node.get('edit-op')
            default = node.get('default')
            value = node.get('value', '')
            if not value:
                value = 'empty'

            if node.get('nodetype', '') == 'list':
                if edit_op in ['delete', 'remove']:
                    del_parent = True
                    par_xp = xpath
                    continue
                # get-config on empty list returns no entry data but need
                # to check the parent xpath for any key/values
                list_xpath = node.get('xpath', '')
                parent_path = list_xpath[:list_xpath.rfind('/')]
                self.rpc_verify.add_key_nodes(parent_path, list_keys)

            if node.get('nodetype', '') == 'container':
                if edit_op in ['delete', 'remove']:
                    # presence container
                    par_xp = xpath
                    del_parent = True
                    continue
                self.rpc_verify.add_key_nodes(node.get('xpath', ''), list_keys)
                continue

            if 'explicit' not in self.rpc_verify.with_defaults and \
                    'report-all' in self.rpc_verify.with_defaults:
                # RFC 6243 - if value is default it should match
                if edit_op in ['delete', 'remove']:
                    nodes.append(OperationalFieldsNode(
                        name=xpath.split('/')[-1],
                        value=default,
                        xpath=xpath_original,
                        selected=True,
                        operator='==',
                        default_value=True,
                        edit_op=edit_op
                    ))
                    continue
            nodes.append(OperationalFieldsNode(
                name=xpath.split('/')[-1],
                value=value,
                xpath=xpath_original,
                selected=True,
                operator='==',
                default_value=False,
                edit_op=edit_op
            ))

        if not decoded_response and not nodes and \
                edit_op in ['delete', 'remove']:
            self.log.info('NO DATA RETURNED')
            return True
        elif decoded_response and not nodes and \
                edit_op in ['delete', 'remove']:
            # Check if node is removed in the response
            if isinstance(decoded_response[0], tuple):
                decoded_response = [decoded_response]
                for resp in decoded_response:
                    for reply, reply_path in resp:
                        if xpath == reply_path:
                            # node xpath still exists in the response
                            self.log.error(
                                "Config not removed. {0} operation failed".format(edit_op))
                            return False
        for node in nodes:
            if not self.get_config_verify(decoded_response, [node.opfields]):
                if node.edit_op in ['delete', 'remove'] and not node.default_value:
                    continue
                result = False
        for node in list_keys:
            if not self.get_config_verify(decoded_response, [node], key=True):
                result = False
        return result

    def find_keys_in_opfield(self, xpath, opfields):
        """Check if all keys in xpath present in opfields or not

        Args:
            xpath (Returns['xpath']): xpath with list keys in it
            xpath = /Sys/List[key=key_value]/leaf
            opfields (Decoded gNMI response): List of tuples(val, xpath)
        Return true if (key_value, /Sys/List/Key) is in opfield, else False  
        """
        for match in re.finditer(self.RE_FIND_KEYS, xpath):
            key = match.group()
            cleared_key = re.sub(self.RE_CLEAR_KEYS, '', key, count=4)
            key_name, key_val = cleared_key.split('=')
            key_path = xpath.split(key)[0] + '/' + key_name
            key_path = re.sub(self.RE_FIND_KEYS, '', key_path)

            # create (key_val, key_path) field to check in opfield
            if not (key_val, key_path) in opfields:
                return False
        return True
