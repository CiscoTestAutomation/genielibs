import logging
from time import sleep
from copy import deepcopy
from six import string_types

from pyats.log.utils import banner
from .rpcbuilder import YSNetconfRPCBuilder
from .rpcverify import RpcVerify

log = logging.getLogger(__name__)

try:
    from ncclient.operations import RaiseMode
except Exception:
    pass
try:
    import lxml.etree as et
except Exception:
    pass

lock_retry_errors = ['lock-denied', 'resource-denied', 'in-use']


def try_lock(uut, target, timer=30, sleeptime=1):
    """Tries to lock the datastore to perform edit-config operation.

    Attempts to acquire the lock on the datastore. If exception thrown,
    retries the lock on the datastore till the specified timer expires.

    Helper function to :func:`lock_datastore`.

    Args:
        session (NetconfSession): active session
        target (str): Datastore to be locked
        timer: lock retry counter.
        sleeptime: sleep timer.

    Returns:
        bool: True if datastore was successfully locked, else False.
    """
    for counter in range(1, timer+1):
        ret = uut.lock(target=target)
        if ret.ok:
            return True
        retry = False
        if ret.error.tag in lock_retry_errors:
            retry = True
        if not retry:
            log.error(banner('ERROR - CANNOT ACQUIRE LOCK - {0}'.format(
                ret.error.tag)))
            break
        elif counter < timer:
            log.info("RETRYING LOCK - {0}".format(counter))
            sleep(sleeptime)
        else:
            log.error(
                banner('ERROR - LOCKING FAILED. RETRY TIMER EXCEEDED!!!')
            )
    return False


def netconf_send(uut, rpcs, ds_state, lock=True, lock_retry=40, timeout=30):
    """Handle NETCONF messaging with exceptions caught by pyATS."""
    # TODO: handle edit-data and get-data
    if not uut.connected:
        uut.connect()

    result = []
    target_locked = False
    running_locked = False

    for nc_op, kwargs in rpcs:

        try:
            ret = ''
            commit_ret = ''
            dc_ret = ''

            if nc_op == 'edit-config':
                # default to running datastore
                target_state = ds_state.get(
                    kwargs.get('target', 'running'),
                    []
                )
                if lock and 'lock_ok' in target_state:
                    target_locked = try_lock(
                        uut, kwargs['target'],
                        timer=lock_retry
                    )

                ret = uut.edit_config(**kwargs)
                if ret.ok and 'commit' in target_state:
                    if target_locked and 'lock_running' in target_state:
                        running_locked = try_lock(
                            uut, 'running', timer=lock_retry
                        )
                    commit_ret = uut.commit()
                    if not commit_ret.ok:
                        if commit_ret.error.tag in lock_retry_errors:
                            # writable-running not advertized but running is locked
                            running_locked = try_lock(
                                uut, 'running', timer=lock_retry
                            )
                            commit_ret = uut.commit()
                            if running_locked:
                                uut.unlock(target='running')
                                running_locked = False
                        if not commit_ret.ok:
                            log.error('COMMIT FAILED\n{0}\n'.format(commit_ret))
                            dc_ret = uut.discard_changes()
                            log.info('\n{0}\n'.format(dc_ret))
                        else:
                            log.info(commit_ret)
                    if running_locked:
                        uut.unlock(target='running')
                        running_locked = False
                if target_locked:
                    uut.unlock(target=kwargs['target'])
                    target_locked = False

            elif nc_op == 'commit':
                commit_ret = uut.commit()
                if not commit_ret.ok:
                    log.error(
                            'COMMIT FAILED\n{0}\n'.format(
                                commit_ret
                            )
                        )
                    dc_ret = uut.discard_changes()
                    log.info('\n{0}\n'.format(dc_ret))
                else:
                    log.info(commit_ret)

            elif nc_op == 'get-config':
                ret = uut.get_config(**kwargs)

            elif nc_op == 'get':
                ret = uut.get(**kwargs)

            elif nc_op == 'rpc':
                target = 'running'
                rpc = kwargs.get('rpc')
                if 'edit-config' in rpc and lock:
                    if 'candidate/>' in rpc:
                        target = 'candidate'
                    target_locked = try_lock(uut, target, timer=lock_retry)

                # raw return
                reply = uut.request(rpc)

                if target == 'candidate' and '<rpc-error' not in reply:
                    commit_ret = uut.commit()
                    if not commit_ret.ok:
                        log.error(
                            'COMMIT FAILED\n{0}\n'.format(
                                commit_ret
                            )
                        )
                        dc_ret = uut.discard_changes()
                        log.info('\n{0}\n'.format(dc_ret))
                    else:
                        log.info(commit_ret)

                if target_locked:
                    uut.unlock(target)
                    target_locked = False
                result.append((nc_op, reply))
                continue

            if ret.ok:
                result.append((nc_op, str(ret)))

            else:
                log.error("NETCONF Reply with error(s):")

                for rpcerror in ret.errors:
                    if rpcerror.message:
                        log.error("ERROR MESSAGE - {0}".format(
                            rpcerror.message))

                if hasattr(ret, 'xml') and ret.xml is not None:
                    result.append((nc_op, ret.xml))
        except Exception as exe:
            msg = str(exe)
            e = ''
            if target_locked:
                try:
                    uut.unlock(target=kwargs['target'])
                except Exception as e:
                    msg += '\n' + str(e)
                target_locked = False
            if running_locked:
                try:
                    uut.unlock(target='running')
                except Exception as e:
                    msg += '\n' + str(e)
                running_locked = False
            result.append(('traceback', msg))
            continue

    return result


def gen_ncclient_rpc(rpc_data, prefix_type="minimal"):
    """Construct the XML Element(s) needed for the given config dict.

    Helper function to :func:`gen_rpc_api`.

    Creates lxml Element instances specific to what :mod:`ncclient` is looking
    for per netconf protocol operation.

    .. note::
       Unlike :func:`gen_raw_rpc`, the XML generated here will NOT be declared
       to the netconf 1.0 namespace but instead any NETCONF XML elements
       will be left un-namespaced.

       This is so that :mod:`ncclient` can select the appropriate
       namespace (1.0, 1.1, etc.) as needed for the session.

    Args:
       cfgd (dict): Relevant keys - 'proto-op', 'dsstore', 'modules'.
       prefix_namespaces (str): One of "always" (prefer namespace prefixes) or
         "minimal" (prefer unprefixed namespaces)

    Returns:
       list: of lists [protocol operation, kwargs], or None

    Raises:
       ysnetconf.RpcInputError: if cfgd is invalid;
         see :meth:`YSNetconfRPCBuilder.get_payload`.
    """
    if not rpc_data:
        log.warning("No configuration sent for RPC generation")
        return None

    datastore = rpc_data.get('datastore')
    prt_op = rpc_data['operation']
    with_defaults = rpc_data.get('with-defaults', '')

    # Add prefixes for all NETCONF containers
    rpcbuilder = YSNetconfRPCBuilder(prefix_namespaces="always")

    container = None

    if prt_op == 'edit-config':
        container = rpcbuilder.netconf_element('config')
    elif prt_op == 'get-config':
        container = rpcbuilder.netconf_element('filter')
    elif prt_op == 'get':
        container = rpcbuilder.netconf_element('filter')
    elif prt_op == 'action':
        container = rpcbuilder.yang_element('action')
    elif prt_op == 'get-data':
        container = rpcbuilder.get_data('get-data')
    elif prt_op == 'edit-data':
        container = rpcbuilder.edit_data('edit-data')
    else:
        container = rpcbuilder.netconf_element('TEMPORARY')

    # Now create the builder for the payload
    rpcbuilder = YSNetconfRPCBuilder(
        prefix_namespaces=prefix_type,
        nsmap=rpc_data.get('namespace', {}),
        netconf_ns=None
    )
    # XML so all the values must be string or bytes type
    nodes = []
    for node in rpc_data.get('nodes', []):
        if 'value' in node:
            node['value'] = str(node.get('value', ''))
        nodes.append(node)

    rpcbuilder.get_payload(nodes, container)

    kwargs = {}
    if prt_op == "rpc":
        # The outer container is temporary - the child element(s) created
        # should be the actual raw RPC(s), which is what we want to return
        return [[prt_op, {'rpc_command': elem}] for elem in container]

    if prt_op == 'edit-config':
        kwargs['target'] = datastore
        if len(container):
            kwargs['config'] = container
    elif prt_op == 'get-config':
        kwargs['source'] = datastore
        if len(container):
            kwargs['filter'] = container
        if with_defaults:
            kwargs['with_defaults'] = with_defaults
    elif prt_op == 'get':
        if len(container):
            kwargs['filter'] = container
        if with_defaults:
            kwargs['with_defaults'] = with_defaults
    elif prt_op in ['get-data', 'edit-data', 'action']:
        kwargs['rpc_command'] = container

    return prt_op, kwargs


def get_datastore_state(target, device):
    """Apply datastore rules according to device and desired datastore.

    - If no target is passed in and device has candidate, choose candidate.
    - If candidate is chosen, allow commit.
    - If candidate is chosen and writable-running exists, allow lock on running
      prior to commit.
    - If running, allow lock, no commit.
    - If startup, allow lock, no commit.
    - If intent, no lock, no commit.
    - If operational, no lock, no commit.
    - Default: running

    Args:
      target (str): Target datastore for YANG interaction.
      device (rpcverify.RpcVerify): Class containing runtime capabilities.
    Returns:
      (tuple): Target datastore (str): assigned according to capabilities
               Datastore state (dict):
                 commit - can apply a commit to datastore
                 lock_ok - can apply a lock to datastore
                 lock_running - apply lock to running datastore prior to commit
    """
    target_state = {}

    for store in device.datastore:
        if store == 'candidate':
            if not target:
                target = 'candidate'
            target_state['candidate'] = ['commit', 'lock_ok']
            if 'running' in target_state:
                target_state['candidate'].append('lock_running')
            continue
        if store == 'running':
            if 'candidate' in target_state:
                target_state['candidate'].append('lock_running')
            target_state['running'] = ['lock_ok']
            continue
        if store == 'startup':
            target_state['startup'] = ['lock_ok']
            continue
        if store == 'intent':
            # read only
            target_state['intent'] = []
            continue
        if store == 'operational':
            # read only
            target_state['operational'] = []
            continue

    if not target:
        target = 'running'
    return target, target_state


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


def run_netconf(operation, device, steps, datastore, rpc_data, returns, **kwargs):
    """Form NETCONF message and send to testbed."""
    log.debug('NETCONF MESSAGE')
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

    if operation == 'capabilities':
        if not returns:
            log.error(banner('No NETCONF data to compare capability.'))
            return False
        return in_capabilities(
            list(device.server_capabilities),
            returns
        )

    rpc_verify = RpcVerify(
        log=log,
        capabilities=list(device.server_capabilities)
    )

    if not rpc_data:
        log.error('NETCONF message data not present')
        return False

    if not datastore:
        log.warning('"datastore" variables not set so choosing:\n'
                    'datastore:\n  type: running\n  lock: True\n  retry: 10\n')
        datastore = {}

    ds = datastore.get('type', '')
    lock = datastore.get('lock', True)
    retry = datastore.get('retry', 10)
    format = kwargs.get('format', {})
    auto_validate = format.get('auto-validate', True)
    negative_test = format.get('negative-test', False)
    timeout = format.get('timeout', None)
    pause = format.get('pause', 0)

    if pause:
        if isinstance(pause, string_types):
            try:
                sleep(int(pause))
            except ValueError:
                try:
                    pause = sleep(float(pause))
                except ValueError:
                    log.error('Invalid "pause" type {0}'.format(type(pause)))
        else:
            sleep(pause)

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

    if operation == 'rpc':
        # Custom RPC represented in raw string form
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

    try:
        for op, reply in result:
            log.info(
                et.tostring(
                    et.fromstring(
                        reply.encode('utf-8'),
                        parser=et.XMLParser(
                            recover=True,
                            encoding='utf-8')
                    ),
                    pretty_print=True
                ).decode('utf-8')
            )
    except Exception as exc:
        log.info('Pretty print failed: {0}'.format(str(exc)))

    # rpc-reply should show up in NETCONF log
    if not result:
        log.error(banner('NETCONF rpc-reply NOT RECIEVED'))
        return False

    errors = []
    for op, res in result:
        if '<rpc-error>' in res:
            errors.append(res)
        elif op == 'traceback':
            errors.append(res)

    if errors:
        log.error(banner('NETCONF MESSAGE ERRORED'))
        if not negative_test:
            return False

    if rpc_data['operation'] == 'edit-config' and auto_validate:
        # Verify the get-config TODO: what do we do with custom rpc's?
        rpc_clone = deepcopy(rpc_data)
        rpc_clone['operation'] = 'get-config'
        rpc_clone['datastore'] = 'running'

        for node in rpc_clone.get('nodes'):
            node.pop('value', '')
            node.pop('edit-op', '')
        prt_op, kwargs = gen_ncclient_rpc(rpc_clone)
        resp_xml = netconf_send(
            device,
            [(prt_op, kwargs)],
            ds_state,
            lock=False
        )
        resp_elements = rpc_verify.process_rpc_reply(resp_xml)
        return rpc_verify.verify_rpc_data_reply(resp_elements, rpc_data)
    elif rpc_data['operation'] in ['get', 'get-config']:
        if not returns:
            log.error(banner('No NETCONF data to compare rpc-reply to.'))
            return False
        # should be just one result
        if len(result) >= 1:
            op, resp_xml = result[0]
            resp_elements = rpc_verify.process_rpc_reply(resp_xml)
            return rpc_verify.process_operational_state(
                resp_elements, returns
            )
        else:
            log.error(banner('NO XML RESPONSE'))
            return False
    elif rpc_data['operation'] == 'edit-data':
        # TODO: get-data return may not be relevent depending on datastore
        log.debug('Use "get-data" yang action to verify this "edit-data".')
    elif rpc_data['operation'] == 'subscribe':
        log.info(banner('Subscribed to {0}'.format('TODO: device name')))

    return True


def run_gnmi(operation, device, steps,
             datastore, rpc_data, returns, **kwargs):
    """Form gNMI message and send to testbed."""
    log.debug('gNMI MESSAGE')
    result = True
    rpc_verify = RpcVerify(log=log, capabilities=[])

    if operation == 'edit-config':
        result = device.set(rpc_data)
    elif operation == 'get':
        if not returns:
            log.error(banner('No gNMI data to compare to GET'))
            return False
        response = device.get(rpc_data)
        if not response:
            return False
        for resp in response:
            update = resp.get('update')
            if not update:
                result = False
                continue
            if not rpc_verify.process_operational_state(update, returns):
                result = False
        return result
    elif operation == 'get-config':
        response = device.get_config(rpc_data)
        deletes = False
        updates = False
        result = True
        for resp in response:
            if 'update' in resp:
                updates = True
                if not rpc_verify.process_operational_state(
                        resp['update'], returns):
                    result = False
            if 'delete' in resp:
                deletes = True
        if not updates and deletes:
            log.info('All configs were deleted')
            return True
        return result
    elif operation == 'subscribe':
        format = kwargs.get('format', {})
        rpc_data['format'] = format
        if format.get('request_mode', 'STREAM') == 'ONCE':
            response = device.subscribe(rpc_data)
        else:
            rpc_data['returns'] = returns
            rpc_data['verifier'] = rpc_verify.process_operational_state
            return device.subscribe(rpc_data)
    elif operation == 'capabilities':
        if not returns:
            log.error(banner('No gNMI data to compare to GET'))
            return False
        resp = device.capabilities()
        result = in_capabilities(resp, returns)
    else:
        log.warning(banner('OPERATION: {0} not allowed'.format(operation)))
    return result


def notify_wait(steps, device):
    if hasattr(device, 'notify_wait'):
        return device.notify_wait(steps)
