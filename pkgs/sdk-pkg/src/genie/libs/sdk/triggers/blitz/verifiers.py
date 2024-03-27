import xmltodict
from logging import Logger
import logging
from typing import Any, List, Tuple, Union
from abc import ABC
import re
from pprint import pformat
import json
from copy import deepcopy
import traceback
from google.protobuf import json_format
from .rpcverify import (RpcVerify,
                        OptFields,
                        OperationalFieldsNode,
                        DecodedResponse,
                        DecodedField,
                        DeletedPath,
                        OPTFIELD_ALLOWED_OPTIONS)
from .gnmi_util import GnmiMessage, GnmiMessageConstructor
from .netconf_util import gen_ncclient_rpc, netconf_send
from genie.conf.base.utils import QDict
from pyats.log.utils import banner
from yang.connector import proto

try:
    import lxml.etree as et
except Exception:
    pass

log = logging.getLogger(__name__)


class BaseVerifier(ABC):
    def __init__(self,
                 device: Any,
                 returns: dict,
                 log: Logger,
                 format: dict = None,
                 steps=None,
                 datastore=None,
                 rpc_data=None,
                 **kwargs):
        super().__init__()
        self.deleted: List = []
        self.returns = returns
        self.steps = steps
        self.datastore = datastore
        self.log = log
        self.format = format
        self.kwargs = kwargs
        self.device = device
        self.rpc_data = rpc_data

    @property
    def validation_on(self) -> bool:
        return self.returns or self.deleted

    def get_config_verify(self,
                          raw_response: Any,
                          *args,
                          **kwargs) -> bool:
        """
        Used Get and Set test cases validation.

        Args:
            raw_response (any): Response received from the device.

        Returns:
            bool: Indicates if test should pass or fail.
        """
        pass

    def subscribe_verify(self,
                         raw_response: Any,
                         sub_mode: str = 'SAMPLE',
                         *args,
                         **kwargs):
        """
        Used for subscription test cases validation.
        Called on every subscription update.

        Args:
            raw_response (Any): Response received from the device.
            sub_mode (str): Gnmi subscription mode. Defaults to 'SAMPLE'.
        """
        pass

    def end_subscription(self,
                         errors: List[Exception],
                         *args,
                         **kwargs) -> bool:
        """
        Method called when subscription is ended. State should be evaluated here.

        Returns:
            bool: Indicates if test should pass or fail.
        """
        pass

    def edit_config_verify(self,
                           raw_response: Any,
                           *args,
                           **kwargs) -> bool:
        """Validation after set-config operation.

        Args:
            raw_response (any): Raw response from device.

        Returns:
            bool: Validation result.
        """
        pass

    class DecodeError(Exception):
        """General decoding error."""
        pass

    class RequestError(Exception):
        """General request error."""
        pass


class DefaultBaseVerifier(BaseVerifier):
    RE_FIND_KEYS = re.compile(r'\[.*?\]')
    RE_CLEAR_KEYS = re.compile(r'[\"\[\]]+')

    def __init__(self,
                 device: Any,
                 returns: dict,
                 log: Logger,
                 format: dict = None,
                 steps=None,
                 datastore=None,
                 rpc_data=None,
                 **kwargs):
        super().__init__(device, returns, log, format,
                         steps, datastore, rpc_data, **kwargs)
        self.rpc_verify = RpcVerify(log=self.log)
        if format is None:
            format = {}
        self.negative_test = format.get('negative_test', False)
        if self.negative_test:
            log.info(banner('NEGATIVE TEST'))

    @property
    def returns(self) -> List[OptFields]:
        return self._returns

    @returns.setter
    def returns(self, returns: Union[List[dict], List[OptFields]]):
        if returns and isinstance(returns[0], dict):
            self._returns = []
            for ret in returns:
                data = {}
                for opt_key, opt_value in ret.items():
                    if opt_key in OPTFIELD_ALLOWED_OPTIONS:
                        data.update({opt_key: opt_value})
                    else:
                        log.warning(f'{opt_key} not allowed as OptField, ignoring')
                self._returns.append(OptFields(**data))
        elif not returns:
            self._returns = []
        else:
            self._returns = returns
        # Move 'deleted' returns to separate list
        returns_no_deletes = []
        for ret in self._returns:
            if ret.op == OptFields._operators['deleted']:
                self.deleted.append(ret)
            else:
                returns_no_deletes.append(ret)
        self._returns = returns_no_deletes

    def verify_common_cases(func) -> bool:
        """Decorator to verify common cases

        Returns:
            bool: Test result
        """

        def inner(self, response, *args, **kwargs):
            # Response will be 'None' when some error is received
            if response is None:
                return False
            # Response will be empty, when no response received,
            # If returns not provided, set result false.
            elif not response and not (self.returns or self.deleted):
                return False
            # Response is received, but user don't want to validate returns
            # set result to True as response is successfully received.
            elif response and not (self.returns or self.deleted):
                return True
            return func(self, response, *args, **kwargs)
        return inner

    class EmptyResponse(BaseVerifier.DecodeError):
        pass


class GnmiDefaultVerifier(DefaultBaseVerifier):

    def get_config_verify(self,
                          raw_response: proto.gnmi_pb2.GetResponse,
                          namespace: dict = None) -> bool:
        try:
            decoded_response = self.decode(raw_response, namespace)
        except (self.DecodeError, self.EmptyResponse):
            return self.negative_test
        if not decoded_response.updates:
            decoded_response.updates.append((None, "/"))
        result = self._deletes_verify(decoded_response.deletes)
        if self.returns:
            result = self._validate_get_response(decoded_response) and result
        return self.negative_test != result

    def subscribe_verify(self,
                         raw_response: proto.gnmi_pb2.SubscribeResponse,
                         sub_type: str = 'ONCE',
                         namespace: dict = None):
        """Decode response and verify result.

        Decoder callback returns desired format of response.
        Verify callback returns verification of expected results.
        """
        try:
            decoded_response = self.decode(
                raw_response, namespace, 'subscribe')
            decoded_updates = decoded_response.updates
            returns_found: List[OptFields] = []

            for field in decoded_updates:
                for ret in self.returns:
                    if ((self._find_xpath(ret.xpath, field[1], decoded_updates)) and
                            (ret not in returns_found)):
                        returns_found.append(ret)
                        break

            self._deletes_verify(decoded_response.deletes)
            if decoded_updates and returns_found:
                if self.log.level == logging.DEBUG:
                    msg = 'Xpath/Value\n' + '=' * 11 + \
                        '\n' + pformat(decoded_updates)
                    self.log.debug(msg)

                result = self.rpc_verify.process_operational_state(
                    decoded_updates, returns_found)
                if result:
                    self.returns = [
                        r for r in self.returns if r not in returns_found]
        except Exception as exc:
            self.log.error(str(exc))
            raise

    def end_subscription(self, errors: List[Exception]) -> bool:
        if errors:
            return self.negative_test is not False
        result = True
        for ret in self.returns:
            xp, val = ret.xpath, ret.value
            self.log.error(
                'ERROR: "{0} value: {1}" Not found.'.format(xp, str(val)))
            result = False
        for delete in self.deleted:
            self.log.error(f"ERROR: {delete.xpath} not deleted.")
            result = False
        return result

    def edit_config_verify(self, response: Any) -> bool:
        if not response:
            return self.negative_test

        if 'returns' in self.rpc_data:
            self.returns = self.rpc_data['returns']
            return self._validate_get_response(response)

        auto_validate = self.format.get(
            'auto_validate', self.format.get('auto-validate', True))
        if auto_validate:
            self.log.info(banner('AUTO-VALIDATION'))
            self.format['get_type'] = 'CONFIG'
            gmc = GnmiMessageConstructor('get', self.rpc_data, **self.format)
            payload = gmc.payload
            namespace_modules = gmc.namespace_modules
            response = GnmiMessage.run_get(
                self.device, payload, namespace_modules
            )
            for node in self.rpc_data.get('nodes'):
                node.pop('edit-op', '')
            return self.negative_test != self._auto_validation(response, namespace_modules)
        return True

    def decode(self,
               response: Any,
               namespace: dict = None,
               method: str = 'get') -> DecodedResponse:
        """Process get response and convert into dict

        Args:
          response : Raw gNMI get response.
          namespace (dict): Can be used if verifier is implemented.

        Returns:
          List[OptFields]: List of OptFields
        """
        self.log.info(str(response))
        if response is None:
            raise self.EmptyResponse()
        if namespace is None:
            namespace = {}
        decoded_response = DecodedResponse()
        notification = json_format.MessageToDict(response)
        self.log.info(f"NOTIFICATION: {notification} \n\n")

        if 'notification' not in notification and 'update' not in notification:
            raise Exception('No notification in Response')
        if method == 'get':
            notifications = notification['notification']
        elif method == 'subscribe':
            notifications = [notification['update']]
        else:
            notifications = []

        for notification in notifications:
            if 'update' not in notification and 'delete' not in notification:
                raise Exception(
                    f'No update or delete in {method.capitalize()}Response')
            prefix = notification.get('prefix')
            if 'update' in notification:
                for updates in notification['update']:
                    decoded_response.json_dicts.append(GnmiMessage.process_update(
                        updates,
                        prefix,
                        namespace,
                        decoded_response.updates
                    ))
            if 'delete' in notification:
                for deletes in notification['delete']:
                    GnmiMessage.process_delete(
                        deletes,
                        prefix,
                        namespace,
                        decoded_response.deletes)

        self.log.info(
            f'{method.capitalize()}Response JSON value decoded\n' +
            '=' * 31 + '\n'
        )
        if decoded_response.json_dicts:
            try:
                for result in decoded_response.json_dicts:
                    try:
                        msg = json.dumps(result, indent=2)
                        self.log.info(msg)
                    except Exception:
                        self.log.error(str(result))
            except TypeError:
                self.log.error(str(decoded_response.json_dicts))
        if decoded_response.deletes:
            self.log.info(
                f"Deleted paths: {[str(d) for d in decoded_response.deletes]}")
        return decoded_response

    @DefaultBaseVerifier.verify_common_cases
    def _validate_get_response(self,
                               decoded_response: DecodedResponse,
                               key: bool = False) -> bool:
        return self.rpc_verify.process_operational_state(
            decoded_response.updates, self.returns, key=key)

    def _auto_validation(self, response: Any, namespace_modules: dict) -> bool:
        try:
            decoded_response = self.decode(
                response, namespace=namespace_modules, method='get')
        except self.EmptyResponse:
            return False
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

        for node in self.rpc_data.get('nodes', []):
            # original xpath with key/value required to validate
            # key values with multilist entries in response
            xpath_original = re.sub(
                self.rpc_verify.RE_FIND_PREFIXES, '/', node.get('xpath', ''))

            # Find missing prefixes and log warning
            matches = re.findall(self.rpc_verify.RE_FIND_KEY_PREFIX, xpath_original)
            if matches:
                for m in matches:
                    prefix = m[0]
                    name = m[1]
                    if not prefix:
                        self.log.warning(f'RPC reply key "{name}" is missing prefix in {xpath_original}')

            xpath_original = re.sub(
                self.rpc_verify.RE_FIND_KEY_PREFIX, r'[\g<name>', xpath_original)

            # xpath with keys and namespace prefix stripped.
            xpath = re.sub(self.rpc_verify.RE_FIND_KEYS,
                           '', node.get('xpath', ''))
            xpath = re.sub(
                self.rpc_verify.RE_FIND_PREFIXES, '/', xpath)
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
            value = node.get('value', None)
            if value is None:
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
                self.rpc_verify.add_key_nodes(
                    node.get('xpath', ''), list_keys)
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
        if not decoded_response.updates and not nodes and \
                edit_op in ['delete', 'remove']:
            self.log.info('NO DATA RETURNED')
            return True
        elif decoded_response.updates and not nodes and \
                edit_op in ['delete', 'remove']:
            # Check if node is removed in the response
            if isinstance(decoded_response.updates[0], tuple):
                decoded_response.updates = [decoded_response.updates]
                for resp in decoded_response.updates:
                    for reply, reply_path in resp:
                        if xpath == reply_path:
                            # node xpath still exists in the response
                            self.log.error(
                                "Config not removed. {0} operation failed".format(edit_op))
                            return False
        for node in nodes:
            self.returns = [node.opfields]
            if not self._validate_get_response(decoded_response):
                if node.edit_op in ['delete', 'remove'] and not node.default_value:
                    continue
                result = False
        for node in list_keys:
            self.returns = [node]
            if not self._validate_get_response(decoded_response, key=True):
                result = False
        return result

    def _find_keys_in_opfield(self, xpath, opfields):
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
                try:
                    # gNMI opfield values can be integers but Xpath has keys as strings
                    key_val = int(key_val)
                except ValueError:
                    log.error(f'Key "{key_val}" not found at Xpath {key_path}')
                    return False
                if not (key_val, key_path) in opfields:
                    log.error(f'Key "{key_val}" not found at Xpath {key_path}')
                    return False
        return True

    def _find_xpath(self,
                    ret_xpath: str,
                    response_xpath: str,
                    decoded_response: List[Union[Tuple, DecodedField]]) -> bool:
        """Find xpath from returns in decoded response
        Args:
            ret_xpath (str): Xpath from returns
            response_xpath (str): Xpath from response
            decoded_response (List[Union[Tuple, DecodedField]]): Decoded response as a list of
            DecodedField for delete validation or list of tuples for update validation

        Returns:
            bool: _description_
        """
        if ret_xpath == response_xpath:
            return True
        if '[' in ret_xpath:
            # if list keys are found in the returns field['xpath']
            # Eg: returns['xpath'] = /Sys/List[key=value]/leaf
            # if above xpath with no keys '/Sys/List/leaf'
            # is in the opfield that means this might be the
            # possible returns to select, but we need check
            # keys in opfields as well.
            xp_no_keys = re.sub(self.RE_FIND_KEYS,
                                '', ret_xpath)
            if xp_no_keys == response_xpath:
                # To make sure that this is the correct returns to select
                # we need to check that all the keys mentioned in the xpath
                # are in opfield or not.
                all_keys_in_opfield = self._find_keys_in_opfield(
                    ret_xpath, decoded_response)
                return all_keys_in_opfield
        return False

    def _deletes_verify(self, decoded_response: List[DeletedPath]) -> bool:
        """Verify delete section from response against expected returns deletes

        Args:
            decoded_response (List[DeletedPath]): Decoded response containing deleted paths
            Found elements will be removed from self.deleted
        Returns:
            bool: Verification result
        """
        if not decoded_response:
            return True
        for delete_resp in decoded_response:
            for delete_returns in deepcopy(self.deleted):
                if self._find_xpath(delete_returns.xpath, delete_resp.xpath, delete_resp.keys):
                    try:
                        self.deleted.remove(delete_returns)
                        self.log.info(f"Found deleted path: {delete_returns.xpath}")
                    finally:
                        break
        return not self.deleted


class NetconfDefaultVerifier(DefaultBaseVerifier):

    class ErroredResponse(Exception):
        def __init__(self, response):
            self.response = response

    def get_config_verify(self,
                          raw_response: Any) -> bool:
        """
        Used by Netconf to verify response.

        Args:
            response (Any): Response received from the device.
            method (str): Netconf method. Defaults to 'get-config'.
        Returns:
            bool: True if verification passes else False.
        """
        try:
            decoded_response = self.decode(raw_response)
        except self.ErroredResponse as e:
            if not self.returns:
                return self.negative_test
            # Validate expected error
            return self.rpc_verify.process_operational_state(
                e.response, self.returns)
        except self.DecodeError:
            return self.negative_test

        if not self.returns:
            # To convert xml to dict
            if len(raw_response) >= 1:
                op, resp_xml = raw_response[0]
                xml_to_dict = QDict(dict(xmltodict.parse(resp_xml)))
                return xml_to_dict
            else:
                self.log.error(
                    banner('No NETCONF data to compare rpc-reply to.'))
                return False

        # should be just one result
        if len(raw_response) >= 1:
            return self.negative_test != self.rpc_verify.process_operational_state(
                decoded_response, self.returns
            )
        else:
            self.log.error(banner('NO XML RESPONSE'))
            return self.negative_test

    def edit_config_verify(self,
                           raw_response: Any = None,
                           ds_state: Any = None):
        try:
            decoded_response = self.decode(raw_response)
        except self.ErroredResponse as e:
            if not self.returns:
                return self.negative_test
                # Validate expected error
            return self.rpc_verify.process_operational_state(
                e.response, self.returns)
        except self.DecodeError:
            return self.negative_test

        auto_validate = self.format.get(
            'auto_validate', self.format.get('auto-validate', True))
        if auto_validate:
            self.log.info(banner('AUTO-VALIDATION'))
            rpc_clone = deepcopy(self.rpc_data)
            rpc_clone['operation'] = 'get-config'
            rpc_clone['datastore'] = 'running'

            for node in rpc_clone.get('nodes'):
                node.pop('value', '')
                node.pop('edit-op', '')
            prt_op, kwargs = gen_ncclient_rpc(rpc_clone)
            resp_xml = netconf_send(
                self.device,
                [(prt_op, kwargs)],
                ds_state,
                lock=False
            )
            decoded_response = self.decode(resp_xml)
            return (self.negative_test !=
                    self.rpc_verify.verify_rpc_data_reply(decoded_response, self.rpc_data))

        return not self.negative_test

    def decode(self,
               response: list = None) -> List[Tuple[et._Element, str]]:
        """
        Used by Netconf to decode response before passing it to verifier.

        Args:
            response (Any): Response received from the device.
            method (str): Netconf method. Defaults to 'get-config'.
        Returns:
            Any: Decoded response.
        """
        # rpc-reply should show up in NETCONF log
        if not response:
            self.log.error(banner('NETCONF rpc-reply NOT RECIEVED'))
            raise self.EmptyResponse()

        errors = []
        for op, res in response:
            if '<rpc-error>' in res:
                self.log.error(
                    et.tostring(
                        et.fromstring(
                            res.encode('utf-8'),
                            parser=et.XMLParser(
                                recover=True,
                                encoding='utf-8')
                        ),
                        pretty_print=True
                    ).decode('utf-8')
                )
                errors.append(res)
            elif op == 'traceback':
                self.log.error('TRACEBACK: {0}'.format(str(res)))
                errors.append(res)

        if errors:
            if self.negative_test:
                op, resp_xml = response[0]
                if op == 'traceback':
                    self.log.error('TRACEBACK: {0}'.format(str(resp_xml)))
                    raise self.DecodeError()
                raise self.ErroredResponse(
                    self.rpc_verify.process_rpc_reply(response))
            else:
                raise self.DecodeError()
        return self.rpc_verify.process_rpc_reply(response)

    def end_subscription(self, errors: List[Exception]) -> bool:
        if errors:
            for err in errors:
                self.log.error(traceback.format_exc())
            return self.negative_test is not False
        return True

    def subscribe_verify(self, raw_response: Any):
        result = self.get_config_verify([('subscribe', raw_response)])
        return result
