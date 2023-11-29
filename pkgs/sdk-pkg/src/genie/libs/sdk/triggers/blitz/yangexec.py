import logging
import json
from time import sleep
from six import string_types
from importlib import import_module
from typing import List, Union
from threading import Thread
from pyats.log.utils import banner

from .rpcverify import RpcVerify
from .verifiers import NetconfDefaultVerifier, GnmiDefaultVerifier, BaseVerifier
from .requestbuilder import RestconfRequestBuilder, NO_BODY_METHODS, WITH_BODY_METHODS
from .yangexec_helper import DictionaryToXML
from .gnmi_util import GnmiMessage, GnmiMessageConstructor
from .netconf_util import (
    gen_ncclient_rpc,
    get_datastore_state,
    netconf_send,
    NetconfSubscription
)
from yang.connector.gnmi import Gnmi


log = logging.getLogger(__name__)

try:
    from ncclient.operations import RaiseMode
except Exception:
    pass
try:
    import lxml.etree as et
except Exception:
    pass


def in_capabilities(caps, returns={}):
    """Find capabilities in expected returns."""
    result = True
    if returns:
        includes = returns.get('includes', [])
        excludes = returns.get('excludes', [])
        if includes and isinstance(includes, (bytes, str)):
            includes = [includes]
        if excludes and isinstance(excludes, (bytes, str)):
            excludes = [excludes]
        include_caps = _included_excluded(caps, includes)
        exclude_caps = _included_excluded(caps, excludes)

        if not include_caps or excludes and exclude_caps:
            result = False
    return result


def _included_excluded(caps, returns=[]):
    result = True
    for item in returns:
        if item not in caps:
            if isinstance(caps, list):
                log.warning("{0} not in capabilities".format(
                    item
                ))
                result = False
                continue
            log.warning("{0} not in capabilities {1}".format(
                item, caps.keys()
            ))
            result = False
        elif isinstance(caps, list):
            log.info("{0} in capabilities".format(
                item
            ))
            continue
        elif isinstance(returns[item], (bytes, str)):
            if returns[item] != caps[item]:
                log.warning("{0} != {1} in capabilities".format(
                    item, returns[item]
                ))
                result = False
            else:
                log.info("{0} == {1} in capabilities".format(
                    item, returns[item]
                ))
        elif isinstance(returns[item], list):
            for value in returns[item]:
                if value in caps[item]:
                    log.info("{0}: {1} in capabilities".format(
                        item, value
                    ))
                else:
                    log.warning("{0}: {1} not in capabilities".format(
                        item, value
                    ))
                    result = False
    return result


def _validate_pause(pause):
    if not pause:
        return 0
    if isinstance(pause, (int, float)):
        return pause
    if isinstance(pause, string_types):
        try:
            pause = float(pause)
            return pause
        except ValueError:
            log.error('Invalid "pause" type {0}'.format(type(pause)))
    return 0


def log_Instructions():
    """Log message for the instruction of returns format to test in sequence"""

    log_msg = " Sequence flag is no longer needed to test in sequence for lists.\n \
    To test lists in the sequence of the keys. Make sure your returns xpath format is as below.\n \
    returns:\n \
        xpath: 'root/container1/list1[key=\"value\"]/container2/list2[key=\"value\"]/property'"

    log.warning(log_msg)


def get_verifier_class(format: dict, protocol: str) -> BaseVerifier:
    """Read data from format, process it and return a verifier class.

    Args:
        device (yang.connector.gnmi.Gnmi): Device object
        format (dict): Testcase format section
        returns (dict): Raw returns passed to init verifier

    Returns:
        BaseVerifier: Verifier class to use for verification
    """
    PROTOCOLS_DEFAULT_VERIFIERS = {
        'netconf': NetconfDefaultVerifier,
        'gnmi': GnmiDefaultVerifier
    }
    verifier = format.get('verifier', {})
    if not verifier:
        log.info("Using default verifier.")
        return PROTOCOLS_DEFAULT_VERIFIERS.get(protocol)

    verifier_class = verifier.get('class', '')
    if verifier_class:
        try:
            module_name, class_name = verifier_class.rsplit('.', 1)
            module = import_module(module_name)
            verifier_class = getattr(module, class_name)
            log.info(
                f"Verifier {class_name} loaded from {module_name}")
            return verifier_class
        except (ModuleNotFoundError, AttributeError):
            log.error('Custom verifier class not found.')
    log.error("Invalid format of custom verifier.")
    return None


def run_netconf(operation: str,
                device,
                steps,
                datastore,
                rpc_data: dict,
                returns: List[dict],
                **kwargs):
    """Form NETCONF message and send to testbed."""
    log.debug('NETCONF MESSAGE')
    result = True
    format = kwargs.get('format', {})

    if format.get('sequence', None):
        log_Instructions()
        return False

    try:
        device.raise_mode = RaiseMode.NONE
    except NameError:
        log.error('Make sure you have ncclient installed in your virtual env')
        return False
    try:
        et.iselement('<test>')
    except NameError:
        log.error('The "lxml" library is required for NETCONF testing')
        return False

    negative_test = format.get('negative_test', False)
    verifier: BaseVerifier = get_verifier_class(format, 'netconf')(
        device, returns, log, format, steps, datastore, rpc_data)

    timeout = format.get('timeout', None)
    pause = _validate_pause(format.get('pause', 0))
    if pause:
        sleep(pause)

    if operation == 'capabilities':
        if not returns:
            log.error(banner('No NETCONF data to compare capability.'))
            return False
        else:
            result = in_capabilities(
                list(device.server_capabilities),
                returns
            )
        return negative_test != result

    rpc_verify = RpcVerify(
        log=log,
        capabilities=list(device.server_capabilities)
    )

    if not rpc_data:
        log.error('NETCONF message data not present')
        return False

    if 'explicit' not in rpc_verify.with_defaults and \
            'report-all' in rpc_verify.with_defaults:
        for node in rpc_data.get('nodes', []):
            if node.get('edit-op', '') == 'create' and node.get('default', ''):
                log.info(
                    'Skipping CREATE; RFC 6243 "report-all" and default exists'
                )
                return True

    if not datastore:
        log.warning('"datastore" variables not set so choosing:\n'
                    'datastore:\n  type: running\n  lock: True\n  retry: 10\n')
        datastore = {}

    ds = datastore.get('type', '')
    lock = datastore.get('lock', True)
    retry = datastore.get('retry', 10)

    if timeout:
        if isinstance(timeout, string_types):
            try:
                device.timeout = int(timeout)
            except ValueError:
                try:
                    device.timeout = float(timeout)
                except ValueError:
                    log.error('Invalid "timeout" type {0}'.format(type(timeout)))
        else:
            device.timeout = timeout

    actual_ds, ds_state = get_datastore_state(ds, rpc_verify)
    if not ds:
        log.info('USING DEVICE DATASTORE: {0}'.format(actual_ds))
        ds = actual_ds
    else:
        log.info('USING TEST DATASTORE: {0}'.format(ds))

    rpc_data['datastore'] = ds
    rpc_data['operation'] = operation

    # operation may be raw rpc or well-formed lxml object
    if 'rpc' in rpc_data and operation in ['rpc', 'subscribe']:
        # Custom RPC represented in raw string form so check syntax
        try:
            et.fromstring(rpc_data['rpc'])
        except et.XMLSyntaxError as exc:
            log.error('Custom RPC has invalid XML:\n  {0}:'.format(str(exc)))
            log.error('{0}'.format(str(rpc_data['rpc'])))
            log.error(banner('NETCONF FAILED'))
            return False

        result = netconf_send(
            device,
            [('rpc', {'rpc': rpc_data['rpc']})],
            ds_state,
            lock=lock,
            lock_retry=retry
        )
    else:
        prt_op, kwargs = gen_ncclient_rpc(rpc_data)
        result = netconf_send(
            device,
            [(prt_op, kwargs)],
            ds_state,
            lock=lock,
            lock_retry=retry
        )

    if rpc_data['operation'] == 'edit-config':
        if pause:
            sleep(pause)
        return verifier.edit_config_verify(result, ds_state)
    elif rpc_data['operation'] in ['get', 'get-config']:
        return verifier.get_config_verify(result)
    elif rpc_data['operation'] == 'edit-data':
        # TODO: get-data return may not be relevent depending on datastore
        log.debug('Use "get-data" yang action to verify this "edit-data".')
    elif rpc_data['operation'] == 'subscribe':
        # Activate subscription thread.
        rpc_data.update(format)
        rpc_data['verifier'] = verifier
        rpc_data['returns'] = returns
        return NetconfSubscription.run_subscribe(device, result, **rpc_data)
    else:
        try:
            # Validate error response
            # Because it's negative test result will be negated
            # but in this case we have to negate this negation
            return not verifier.get_config_verify(result)
        except Exception:
            log.error('Wrong operation type')
            return negative_test
    return not negative_test


def run_gnmi(operation: str,
             device: Gnmi,
             steps,
             datastore,
             rpc_data: dict,
             returns: List[dict], **kwargs) -> Union[bool, Thread]:
    """Form gNMI message and send to testbed.

    Args:
        operation (str): 'get-config', 'edit-config', 'subscribe'
        device (Gnmi): GNMI device
        steps (_type_): _description_
        datastore (_type_): _description_
        rpc_data (dict): _description_
        returns (List[dict]): Expected returns

    Returns:
        Union[bool, Thread]: For subscribe, returns a thread object for others returns a bool
    """
    log.debug('gNMI MESSAGE')
    result = True
    payload = None
    namespace_modules = {}
    format = kwargs.get('format', {})

    # To check the sequence
    if format.get('sequence', None):
        log_Instructions()
        return False

    if format:
        pause = _validate_pause(format.get('pause', 0))
        if pause:
            sleep(pause)
        negative_test = format.get('negative_test', False)
    else:
        negative_test = False

    transaction_time = format.get('transaction_time', 0)
    verifier: BaseVerifier = get_verifier_class(format, 'gnmi')(
        device, returns, log, format, steps, datastore, rpc_data)
    if verifier is None:
        return False

    if operation == 'edit-config':
        if 'rpc' in rpc_data:
            # Assume we have a well-formed dict representing gNMI set
            payload = json.dumps(rpc_data.get('rpc', {}), indent=2)
        else:
            gmc = GnmiMessageConstructor('set', rpc_data, **format)
            payload = gmc.payload
        resp = GnmiMessage.run_set(device, payload)
        return verifier.edit_config_verify(resp)
    elif operation in ['get', 'get-config']:
        if 'rpc' in rpc_data:
            # Assume we have a well-formed dict representing gNMI get
            payload = json.dumps(rpc_data.get('rpc', {}), indent=2)
            namespace_modules = rpc_data
        else:
            gmc = GnmiMessageConstructor('get', rpc_data, **format)
            payload = gmc.payload
            namespace_modules = gmc.namespace_modules
        response = GnmiMessage.run_get(
            device, payload, namespace_modules,
            transaction_time=transaction_time
        )
        return verifier.get_config_verify(response, namespace_modules)
    elif operation == 'subscribe':
        rpc_data.update(format)
        rpc_data['returns'] = returns
        rpc_data['verifier'] = verifier
        if 'rpc' in rpc_data:
            # Assume we have a well-formed dict representing gNMI subscribe
            payload = json.dumps(rpc_data.get('rpc', {}), indent=2)
        else:
            gmc = GnmiMessageConstructor('subscribe', rpc_data, **format)
            payload = gmc.payload
        # Returns subscribe thread and results are handled by caller
        return GnmiMessage.run_subscribe(device, payload, **rpc_data)
    elif operation == 'capabilities':
        if not returns:
            log.error(banner('No gNMI data to compare to GET'))
            return False
        resp = device.capabilities()
        result = in_capabilities(resp, returns)
    else:
        log.warning(banner('OPERATION: {0} not allowed'.format(operation)))
    return negative_test != result


def run_restconf(operation, device, steps, datastore, rpc_data, returns, **kwargs):
    result = False
    request_successful = False
    request_senders = {
        'PATCH': device.patch,
        'POST': device.post,
        'PUT': device.put,
        'DELETE': device.delete,
        'GET': device.get,
    }

    format = kwargs.get('format', {})
    if 'auto_validate' in format:
        auto_validate = format.get('auto_validate')
    else:
        auto_validate = format.get('auto-validate', True)
    if 'negative_test' in format:
        negative_test = format.get('negative_test')
    else:
        negative_test = format.get('negative-test', False)

    if negative_test:
        log.info(banner('NEGATIVE TEST'))

    # Get URL and request body
    request_builder = RestconfRequestBuilder(request_data=rpc_data, returns=returns)
    url = request_builder.url
    body = request_builder.json_body
    content_type = request_builder.content_type
    http_method = request_builder.http_method
    # Translate HTTP method to a function present in device to execute request(s)
    send_request = request_senders[http_method]

    # Print HTTP method
    log.info(f'Using HTTP method: {http_method}')
    # Print request URL
    log.info(f'Using request URL: {url}')

    # Send request
    if http_method in NO_BODY_METHODS:
        request = send_request(url, content_type)
    elif http_method in WITH_BODY_METHODS:
        # Print request body
        log.info(f'Using request body:\n{body}')
        request = send_request(url, body, content_type)

    status_code = request.status_code
    content = json.loads(request.content.decode('utf-8')) if len(request.content) else None

    if status_code >= 200 and status_code <= 299:
        # Request was successful
        log.info(banner(f'Request successful! Request status code: {status_code}'))
        request_successful = True
    elif status_code >= 400 and status_code <= 499:
        # Client error occured
        log.error(banner(f'Client error occured! Request status code: {status_code}'))
    elif status_code >= 500 and status_code <= 599:
        # Server error occured
        log.error(banner(f'Server error occured! Request status code: {status_code}'))
    # Pretty print server response
    log.info(f'Server response:\n{json.dumps(content or {}, indent=2)}')

    if request_successful:
        if content and returns:
            log.info(banner('Server response and returns exist'))
            # If the response has a body, convert body to xml, process body, and verify body
            rpc_verify = RpcVerify(log=log)
            resp_xml = DictionaryToXML(content).xml_str
            resp_elements = rpc_verify.process_rpc_reply(resp_xml)
            # Remove namespaces from returns' XPaths
            formatted_returns = []
            for item in returns:
                xpath = item.get('xpath', '')
                item['xpath'] = RestconfRequestBuilder.replace_or_delete_namespaces(xpath, rpc_data, 'delete')
                formatted_returns.append(item)
            result = rpc_verify.process_operational_state(resp_elements, formatted_returns)
        elif content and not returns:
            log.info(banner('Server response exist, returns does not exist'))
            result = True
        elif not content and returns:
            log.error(banner(f'Server response does not exist, returns does exist, no response to compare'))
        elif not content and not returns:
            log.info(banner('Server response and returns does not exist'))
            result = True

        return negative_test != result

    return False
