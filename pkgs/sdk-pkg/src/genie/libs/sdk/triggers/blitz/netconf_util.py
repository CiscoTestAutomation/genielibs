import logging
import time
from typing import List
from collections import deque
import lxml.etree as et
from pyats.log.utils import banner
from yang.connector import Netconf
from .rpcbuilder import YSNetconfRPCBuilder
from .subscription import Subscription

log = logging.getLogger(__name__)
lock_retry_errors = ['lock-denied', 'resource-denied', 'in-use']


class NetconfSubscription(Subscription):
    """Base Subscription class for all NETCONF notifications."""
    subscription_queue = {}

    def __init__(self, device, payload, **request):
        super().__init__(device, **request)
        op, response = payload[0]
        self._result = []
        sub_id = self.get_subscribe_id(response)
        if not sub_id:
            log.warning('NO SUBSCRIPTION ID FOUND')
        self.subscription_id = sub_id
        self.device = device
        self.payload = payload
        if self.sub_mode:
            self.log.info(f'Subscription sub mode: {self.sub_mode}')

    def cover_exceptions(func):
        """Decorator to catch exceptions and log them."""
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                self.errors.append(e)
                self.result = self.verifier.end_subscription(self.errors)
                self.stop()
        return wrapper

    def _trim_xml_header(self, xml):
        # Trim off encoding (<?xml version="1.0" encoding="UTF-8"?>)
        if xml and xml.lstrip().startswith('<?xml'):
            xml = xml[xml.find('>')+1:]
        return xml.strip()

    def get_subscribe_id(self, payload):
        """Get the subscription ID from the payload.

        Args:
            payload (str): The payload to parse.
        Returns:
            str: The subscription ID if found in payload or None.
        """
        payload = self._trim_xml_header(payload)
        if payload:
            xml_ele = et.fromstring(payload)
            for el in xml_ele.iter():
                if et.QName(el).localname == 'rpc-error':
                    self.log.error('SUBSCRIBE FAILED')
                    self.result = False
                    return ''
                if et.QName(el).localname == 'subscription-id':
                    if el.text:
                        return el.text.strip()
                    return None
        return None

    @classmethod
    def validate_subscribe_response(cls, payload):
        """Validate the subscribe response.

        Args:
            payload (list): Tuple of (operation, response).
        Returns:
            bool: True if valid, else False.
        """
        _, response = payload[0]
        payload = cls._trim_xml_header(cls, response)
        if payload:
            xml_ele = et.fromstring(payload)
            for el in xml_ele.iter():
                if et.QName(el).localname == 'rpc-error':
                    # Details of error should already be in log.
                    return False
            return True
        return False

    @property
    def result(self):
        if not self._result:
            return False
        return all(self._result)

    @result.setter
    def result(self, value):
        self._result.append(value)

    @classmethod
    def run_subscribe(cls, device, payload, **request):
        """Instantiate the correct subscription class.

        Args:
            device (Netconf): The device to subscribe to.
            payload (list): Tuple of (operation, response).
            **request: The request dictionary.
        Returns:
            NetconfSubscription: The subscription class.
        """
        if cls.validate_subscribe_response(payload) is False:
            log.error('SUBSCRIBE FAILED')
            return False

        request['log'] = log
        request_mode = request.get('request_mode')
        if not request_mode:
            log.error('No request_mode specified; setting to "ONCE"')
            request_mode = 'ONCE'
        if request_mode == 'ONCE':
            subscribe_thread = NetconfSubscriptionOnce(
                device, payload, **request)
        elif request_mode == 'POLL':
            subscribe_thread = NetconfSubscriptionPoll(
                device, payload, **request)
        elif request_mode == 'STREAM':
            subscribe_thread = NetconfSubscriptionStream(
                device, payload, **request)
        else:
            log.error(f'Unknown request_mode: {request_mode}')
            return False

        subscribe_thread.start()
        log.info(banner('NETCONF Subscription reciever started'))
        cls.subscription_queue[
            subscribe_thread.subscription_id] = deque()
        return subscribe_thread


class NetconfSubscriptionStream(NetconfSubscription):
    """NETCONF Subscription class for STREAM mode."""
    def __init__(self,
                 device: Netconf = None,
                 payload: List = None,
                 **request):
        super().__init__(device, payload, **request)

    @NetconfSubscription.cover_exceptions
    def run(self):
        """Check for inbound notifications."""
        self.log.info('Subscribe STREAM notification active')
        t = time.time()
        time_delta = 0.0
        self.log.info(f"Maximum stream time: {self.stream_max} seconds.")

        while time_delta < self.stream_max:
            time_delta = time.time() - t
            self.log.info(f"Delta: {time_delta} seconds.")
            if self.transaction_time and self.ntp_server:
                if time_delta > self.transaction_time:
                    self.log.error('Transaction time exceeded')
                    self.result.append(False)
                    break
            if self.stopped():
                time_delta = self.stream_max
                self.log.info("Terminating notification early.")
                break
            self.log.info('Check for incoming notifications.')
            notif = self.device.take_notification(timeout=self.stream_max)
            if hasattr(notif, "notification_xml"):
                # Add to global queue (this might not be for this subscription)
                sub_id = self.get_subscribe_id(notif.notification_xml)
                if sub_id is None:
                    self.log.warning('NO SUBSCRIPTION ID FOUND')
                self.log.info(f'Adding notification ID:{sub_id} to queue.')
                if sub_id not in self.subscription_queue:
                    self.subscription_queue[sub_id] = deque()
                self.subscription_queue[sub_id].append(
                    notif.notification_xml)
            self.log.info(f'Check queue for ID:{self.subscription_id} notifications.')
            if self.subscription_id not in self.subscription_queue:
                self.log.warning(f'No notifications for {self.subscription_id}')
                continue
            while len(self.subscription_queue[self.subscription_id]):
                notif_xml = self.subscription_queue[self.subscription_id].popleft()
                if notif_xml:
                    self.log.info(f'Verifying notification {self.subscription_id}')
                    self.result = self.verifier.subscribe_verify(notif_xml)
        self.stop()


class NetconfSubscriptionOnce(NetconfSubscription):
    """NETCONF Subscription class for ONCE mode."""
    def __init__(self,
                 device: Netconf = None,
                 payload: List = None,
                 ** request):
        super().__init__(device, payload, **request)

    @NetconfSubscription.cover_exceptions
    def run(self):
        """Check for inbound notifications."""
        self.log.info('Subscribe ONCE notification active')
        t = time.time()
        time_delta = 0.0
        self.log.info(f"Maximum stream time: {self.stream_max} seconds.")

        while time_delta < self.stream_max:
            time_delta = time.time() - t
            self.log.info(f"Delta: {time_delta} seconds.")
            if self.transaction_time and self.ntp_server:
                if time_delta > self.transaction_time:
                    self.log.error('Transaction time exceeded')
                    self.result.append(False)
                    break
            if self.stopped():
                time_delta = self.stream_max
                self.log.info("Terminating notification early.")
                break
            self.log.info('Check for incoming notifications.')
            notif = self.device.take_notification(timeout=self.stream_max)
            if hasattr(notif, "notification_xml"):
                # Add to global queue (this might not be for this subscription)
                sub_id = self.get_subscribe_id(notif.notification_xml)
                if sub_id is None:
                    self.log.warning('NO SUBSCRIPTION ID FOUND')
                self.log.info(f'Adding notification ID:{sub_id} to queue.')
                if sub_id not in self.subscription_queue:
                    self.subscription_queue[sub_id] = deque()
                self.subscription_queue[sub_id].append(
                    notif.notification_xml)
            self.log.info(f'Check queue for {self.subscription_id} notifications.')
            if self.subscription_id not in self.subscription_queue:
                self.log.warning(f'No notifications for {self.subscription_id}')
                continue
            while len(self.subscription_queue[self.subscription_id]):
                notif_xml = self.subscription_queue[self.subscription_id].popleft()
                if notif_xml:
                    self.log.info(f'Verifying notification {self.subscription_id}')
                    self.result = self.verifier.subscribe_verify(notif_xml)
                    break
        self.stop()


class NetconfSubscriptionPoll(NetconfSubscription):
    """NETCONF Subscription class for POLL mode."""
    def __init__(self,
                 device: Netconf = None,
                 payload: List = None,
                 **request):
        super().__init__(device, payload, **request)

    @NetconfSubscription.cover_exceptions
    def run(self):
        """Check for inbound notifications."""
        self.log.info('Subscribe POLL notification active')
        t = time.time()
        time_delta = 0.0
        self.log.info(f"Maximum stream time: {self.stream_max} seconds.")

        while time_delta < self.stream_max:
            time_delta = time.time() - t
            self.log.info(f"Delta: {time_delta} seconds.")
            if self.stopped():
                self.time_delta = self.stream_max
                self.log.info("Terminating notification early.")
                break
            self.log.info('Check for incoming notifications.')
            notif = self.device.take_notification(timeout=self.stream_max)
            if hasattr(notif, "notification_xml"):
                # Add to global queue (this might not be for this subscription)
                sub_id = self.get_subscribe_id(notif.notification_xml)
                if sub_id is None:
                    self.log.warning('NO SUBSCRIPTION ID FOUND')
                self.log.info(f'Adding {sub_id} notification to queue.')
                if sub_id not in self.subscription_queue:
                    self.subscription_queue[sub_id] = deque()
                self.subscription_queue[sub_id].append(
                    notif.notification_xml)
            self.log.info(f'Check queue for {self.subscription_id} notifications.')
            if self.subscription_id not in self.subscription_queue:
                self.log.warning(f'No notifications for {self.subscription_id}')
                continue
            while len(self.subscription_queue[self.subscription_id]):
                notif_xml = self.subscription_queue[self.subscription_id].popleft()
                if notif_xml:
                    self.log.info(f'Verifying notification {self.subscription_id}')
                    self.result = self.verifier.subscribe_verify(notif_xml)
                time.sleep(self.sample_poll)
            result = netconf_send(
                self.device,
                [('rpc', {'rpc': self.request['rpc']})],
                {},
                lock='',
                lock_retry=0
            )
            if self.validate_subscribe_response(result) is False:
                self.result = False
                break
            _, response = result[0]
            sub_id = self.get_subscribe_id(response)
            if sub_id is None:
                self.log.error('NO POLL SUBSCRIPTION ID FOUND')
            self.subscription_id = sub_id
        self.stop()


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

    if prt_op in ['rpc', 'subscribe']:
        # The outer container is temporary - the child element(s) created
        # should be the actual raw RPC(s), which is what we want to return
        child_elements = [(prt_op, {'rpc_command': elem})
                          for elem in container]
        if child_elements:
            return child_elements[0]

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


def netconf_send(uut, rpcs, ds_state, lock=True, lock_retry=40, timeout=30):
    """Handle NETCONF messaging with exceptions caught by pyATS."""
    # TODO: handle edit-data and get-data
    # Below is the temp fix for Netconf connection.
    # Needs to be handled in a better way to check whether the connection is alive
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
                            log.error(
                                'COMMIT FAILED\n{0}\n'.format(commit_ret))
                            dc_ret = uut.discard_changes()
                            ret = commit_ret
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
                    ret = commit_ret
                    dc_ret = uut.discard_changes()
                    log.info('\n{0}\n'.format(dc_ret))
                else:
                    log.info(commit_ret)

            elif nc_op == 'get-config':
                ret = uut.get_config(**kwargs)

            elif nc_op == 'get':
                ret = uut.get(**kwargs)
            elif nc_op == 'subscribe':
                ret = uut.dispatch(**kwargs)
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
                        ret = commit_ret
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
            time.sleep(sleeptime)
        else:
            log.error(
                banner('ERROR - LOCKING FAILED. RETRY TIMER EXCEEDED!!!')
            )
    return False
