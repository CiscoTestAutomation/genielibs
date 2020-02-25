import logging
import traceback
from time import sleep
from copy import deepcopy

from pyats.log.utils import banner
from .rpcbuilder import YSNetconfRPCBuilder
from .rpcverify import RpcVerify

log = logging.getLogger(__name__)

try:
    from ncclient.operations import RaiseMode
except Exception:
    log.error(
        banner('Make sure you have ncclient installed in your virtual env')
    )


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
            log.debug("RETRYING LOCK - {0}".format(counter))
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
                    ret = uut.commit()
                    if not ret.ok and ret.error.tag in lock_retry_errors:
                        # writable-running not advertized but running is locked
                        running_locked = try_lock(
                            uut, 'running', timer=lock_retry
                        )
                        ret = uut.commit()
                        if running_locked:
                            uut.unlock(target='running')
                            running_locked = False
                    if running_locked:
                        uut.unlock(target='running')
                        running_locked = False
                if target_locked:
                    uut.unlock(target=kwargs['target'])
                    target_locked = False

            elif nc_op == 'commit':
                ret = uut.commit()

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
            e = ''
            if target_locked:
                try:
                    uut.unlock(target=kwargs['target'])
                except Exception as e:
                    pass
                target_locked = False
            if running_locked:
                try:
                    uut.unlock(target='running')
                except Exception as e:
                    pass
                running_locked = False
            # log.error(traceback.format_exc())
            msg = str(exe)
            msg += '\n' + str(e)
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
            node['value'] = str(node['value'])
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

def run_netconf(operation, device, steps, datastore, rpc_data, returns):
    """Form NETCONF message and send to testbed."""
    log.debug('NETCONF MESSAGE')
    try:
        device.raise_mode = RaiseMode.NONE
    except NameError:
        log.error(
            banner('Make sure you have ncclient installed in your virtual env')
        )
        return

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
        log.error(
            banner('NETCONF MESSAGE ERRORED\n{0}'.format('\n'.join(errors)))
        )
        return False

    if rpc_data['operation'] == 'edit-config':
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

    return True


def run_gnmi(operation, device, steps, datastore, rpc_data, returns):
    """Form gNMI message and send to testbed."""
    result = True
    log.warning('gNMI protocol not implemented!')
    return result
