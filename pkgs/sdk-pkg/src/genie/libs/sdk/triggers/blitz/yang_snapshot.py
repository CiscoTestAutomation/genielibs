import logging
from lxml import etree
from ncclient import xml_
from genie.libs.sdk.triggers.blitz import yangexec, rpcverify,\
                                          netconf_util


log = logging.getLogger(__name__)

FILTER_TAG = '{' + xml_.BASE_NS_1_0 + '}filter'


class YangSnapshot(object):
    '''Remove containers and list instances that are created and left over by
    Yang actions. We do not want to clean up config after every Yang action
    as YangSuite purposely keeps the leaf (or other node type) under test there
    for the next Yang action. It is recommanded to place the yang_snapshot
    action at the begining of a group, and to place yang_snapshot_restore at
    the end of a group.'''

    def __init__(self, device):
        self.testbed = device.testbed if hasattr(device, 'testbed') else None
        self.namespace = {}
        self.xpath = {}
        self.pre_config = {}
        self.server_capabilities = {}
        self.set_datastore(datastore=None, device=device)

    def set_datastore(self, datastore=None, device=None):
        # Set server_capabilities if a device is given
        if (
            device is not None and
            hasattr(device, 'name') and
            device.name in self.server_capabilities
        ):
            server_capabilities = self.server_capabilities[device.name]
        else:
            server_capabilities = []

        if device is not None and hasattr(device, 'server_capabilities'):
            self.server_capabilities[device.name] = device.server_capabilities

        if isinstance(datastore, dict):
            self.datastore = {
                'type': datastore.get('type', 'running'),
                'lock': datastore.get('lock', True),
                'retry': datastore.get('retry', 10),
            }
        elif (
            hasattr(self.testbed, 'testbed') and
            hasattr(self.testbed.testbed, 'custom') and
            hasattr(self.testbed.testbed.custom, 'datastore')
        ):
            self.datastore = self.testbed.testbed.custom.datastore
        else:
            self.datastore = {
                'type': 'running',
                'lock': True,
                'retry': 10,
            }
        rpc_verify = rpcverify.RpcVerify(
            log=log,
            capabilities=server_capabilities,
        )

        # Update self.datastore by calling get_datastore_state()
        self.datastore['type'], self.datastore_state = \
            yangexec.get_datastore_state(
                target=self.datastore['type'],
                device=rpc_verify,
            )
        if self.datastore['type'] in self.datastore_state:
            self.datastore['lock'] = 'lock_ok' in self.datastore_state[
                self.datastore['type']]
        log.debug("Set datastore = {}".format(self.datastore))
        log.debug("Set datastore_state = {}".format(self.datastore_state))

    def register(self, device, connection, protocol, operation, content):
        '''Register one test case. If there is a Yang action that configures
        the device, we collect its Xpaths.

        Parameters
        ----------
        device : `object`
            pyATS device object.

        connection : `str`
            The connection name of the device object. This connection
            correlates with the protocol, by which the snapshot_restore action
            will be performed.

        protocol : `str`
            The protocol name that the snapshot_restore action will be
            performed with.

        operation : `str`
            Operatation of the Yang action.

        content : `dict`
            Operatation infomation organized in a dictionary.

        Returns
        -------
        None
            Nothing returns.
        '''

        if (
            protocol == 'netconf' and
            operation == 'edit-config' and
            device and
            connection and
            content
        ):
            # Update server_capabilities when this is Netconf
            connection_obj = getattr(device, connection)
            if (
                device.name not in self.server_capabilities and
                hasattr(connection_obj, 'server_capabilities')
            ):
                self.server_capabilities[device.name] = \
                    list(connection_obj.server_capabilities)

            new_xpaths = [
                n.get('xpath') for n in content['nodes']
                if n.get('edit-op') in
                ['create', 'merge', 'replace'] and n.get('xpath')
            ]
            if device.name in self.xpath:
                self.xpath[device.name].update(new_xpaths)
            else:
                self.xpath[device.name] = set(new_xpaths)

    def snapshot(self, testcase, device, steps, section):
        '''Execute the yang_snapshot action. Often it is at the begining of a
        group, which is consisted with operation of create, delete, merge,
        replace and remove.

        Parameters
        ----------
        testcase : `object`
            Testcase object.

        device : `object`
            pyATS device object.

        steps : `object`
            pyATS Steps object.

        section : `object`
            pyATS Section object.

        Returns
        -------
        boolean
            Return True when snapshot action was successful, and False
            otherwise.
        '''

        if not (
            hasattr(testcase, 'parent') and
            hasattr(testcase.parent, 'triggers')
        ):
            log.warning("Have trouble to retrieve 'parent.triggers' from "
                        "testcase = {}".format(testcase))
            return False
        data = section.parameters.get('data')
        if data is None:
            log.warning("Have trouble to retrieve 'data' from "
                        "section.parameters = {}"
                        .format(section.parameters))
            return False

        self.xpath = {}
        self.pre_config = {}
        return self.scan_triggers(device, testcase.uid[:-4], section.uid,
                                  steps.index, testcase.parent.triggers)

    def snapshot_restore(self, device, **kwargs):
        '''Execute the yang_snapshot_restore action. It is suggested to put it
        at the end of a group.

        Parameters
        ----------
        device : `object`
            pyATS device object.

        connection : `str`
            The connection name of the device object. This connection
            correlates with the protocol, by which the snapshot_restore action
            will be performed.

        protocol : `str`
            The protocol name that the snapshot_restore action will be
            performed with.

        Returns
        -------
        boolean
            Return True when yang_snapshot_restore action was successful, and
            False when it was unsuccessful. If there is no Xpath to clean up,
            None is returned.
        '''

        connection = kwargs.get('connection')
        protocol = kwargs.get('protocol')
        if not self.pre_config:
            log.warning("There is no snapshot to restore. Please make sure to "
                        "take a yang_snapshot action before this "
                        "yang_snapshot_restore action.")
            return None
        connection_obj = getattr(device, connection)
        self.set_datastore(datastore=kwargs.get('datastore'), device=device)
        if device.name not in self.xpath:
            log.warning("There is no Xpath of device {} that has been "
                        "configured by 'yang' action.".format(device.name))
            return None

        xpath_set = set()
        for xpath in self.xpath[device.name]:
            self.update_remove_xpaths(xpath, xpath_set, device)
        if xpath_set:
            log.info("Removing Xpath:\n{}"
                     .format("\n".join(sorted(list(xpath_set)))))
            if protocol == 'netconf':
                args = self.build_rpc(xpath_set)

                lock_target = self.datastore.get('lock', True)
                target = self.datastore.get('type', 'running')
                lock_running = 'lock_running' in self.datastore_state[target] \
                    if target in self.datastore_state else False
                target_locked = False
                if lock_target:
                    target_locked = netconf_util.try_lock(
                        uut=connection_obj,
                        target=target,
                        timer=self.datastore.get('retry', 10),
                        sleeptime=1,
                    )
                    if not target_locked:
                        return False
                reply = connection_obj.edit_config(**args)
                log.info(etree.tostring(
                    reply._root,
                    encoding='unicode',
                    pretty_print=True,
                ))
                if lock_target and target_locked:
                    connection_obj.unlock(target=target)
                if not reply.ok:
                    return False
                if target == 'candidate':
                    running_locked = False
                    if lock_running:
                        running_locked = netconf_util.try_lock(
                            uut=connection_obj,
                            target='running',
                            timer=self.datastore.get('retry', 10),
                            sleeptime=1,
                        )
                        if not running_locked:
                            return False
                    commit_ret = connection_obj.commit()
                    log.info(etree.tostring(
                        commit_ret._root,
                        encoding='unicode',
                        pretty_print=True,
                    ))
                    if lock_running and running_locked:
                        connection_obj.unlock(target='running')
                    if not commit_ret.ok:
                        connection_obj.discard_changes()
                        return False
                return True
        else:
            log.info("No Xpath to remove on device {}.".format(device.name))
            return None

    def scan_triggers(self, device_obj, testcase_uid, section_uid, step_index,
                      triggers):
        '''Scan Genie triggers to find out Xpaths whose snapshot need to be
        collected, and then collect the snapshot.

        Parameters
        ----------
        device_obj : `object`
            pyATS device object.

        testcase_uid : `str`
            The UID of the current testcase.

        section_uid : `str`
            The UID of the current section.

        step_index : `str`
            The index of the current step.

        triggers : `dict`
            Operatation of the Yang action.

        Returns
        -------
        boolean
            Return True when collecting of pre_config was successful, and False
            otherwise.
        '''

        uids = list(triggers.keys())
        current_index = uids.index(testcase_uid)
        xpaths = {}
        xpaths_tmp = {}
        connections = {}
        hit_next_yang_snapshot = False
        for i in range(current_index, len(uids)):
            if hit_next_yang_snapshot is True:
                break
            testcase = triggers[uids[i]]
            for test_section in testcase.get('test_sections', []):
                if hit_next_yang_snapshot is True:
                    break
                if i == current_index and section_uid in test_section:
                    steps = test_section[section_uid]
                    start_index = int(step_index)
                else:
                    steps = list(test_section.values())[0]
                    start_index = 0
                for step_idx in range(start_index,  len(steps)):
                    step = steps[step_idx]
                    step_actions = list(step.keys())

                    # Stop iteration when hitting the next yang_snapshot
                    if 'yang_snapshot' in step_actions:
                        hit_next_yang_snapshot = True
                        break

                    # Update xpaths when the action is a matching
                    # yang_snapshot_restore
                    if 'yang_snapshot_restore' in step_actions:
                        for device, xpath_set in xpaths_tmp.items():
                            if device in xpaths:
                                xpaths[device].update(xpath_set)
                            else:
                                xpaths[device] = xpath_set
                        xpaths_tmp = {}
                        continue

                    # Update xpaths_tmp when the action is a Netconf
                    # edit-config. This will be extended to other
                    # programmability protocols in the future.
                    if (
                        'yang' in step_actions and
                        step['yang'].get('protocol') == 'netconf' and
                        step['yang'].get('operation') == 'edit-config' and
                        step['yang'].get('content') and
                        step['yang'].get('device') and
                        step['yang'].get('connection')
                    ):
                        content = step['yang'].get('content')
                        device = step['yang'].get('device')
                        device_name = self.get_device_name(device_obj, device)
                        connections[device_name] = \
                            step['yang'].get('connection')
                        for node in content.get('nodes', []):
                            xpath = node.get('xpath')
                            if xpath:
                                if device_name in xpaths_tmp:
                                    xpaths_tmp[device_name].add(xpath)
                                else:
                                    xpaths_tmp[device_name] = set([xpath])
                            namespace = content.get('namespace')
                            if namespace:
                                self.namespace.update(namespace)

        if xpaths:
            log.info("Collecting a snapshot...")
        else:
            log.info("There is no Xpath that will be configured before the "
                     "next one or multiple yang_snapshot_restore actions, so "
                     "this yang_snapshot action is ignored.")
        result = True
        for dev, xpath_set in xpaths.items():
            device = self.testbed.devices[dev]
            connection = getattr(device, connections[dev])
            if connection is None:
                log.warning("Unable to find connection '{}' of device {}."
                            .format(connections[dev], device))
                result = False
            else:
                if not self.collect_pre_config(dev, connection, xpath_set):
                    result = False
        return result

    @staticmethod
    def get_root(xpath):
        '''Find the root of a schema tree.'''

        xpath_list = xpath.split('/')
        if xpath_list[0] == '':
            if len(xpath_list) > 1:
                return xpath_list[1]
        return None

    @staticmethod
    def split_tag(tag):
        '''Given a tag such as ios:native, it returns its prefix and ID.'''

        pieces = tag.split(':')
        if len(pieces) == 2:
            return pieces[0], pieces[1]
        return None, None

    @staticmethod
    def get_device_name(device_obj, device_alias):
        '''Get the real device name when the alias name is provided.'''

        if device_alias in device_obj.testbed.devices:
            device = device_obj.testbed.devices[device_alias]
        else:
            raise Exception("Could not find the device '{d}' "
                            "which was provided in the "
                            "action".format(d=device_alias))
        return device.name

    def collect_pre_config(self, device_name, connection, xpaths):
        '''Collect configuration before Xpaths are manipulated.'''

        self.pre_config[device_name] = {}
        result = True
        for xpath in xpaths:
            root = self.get_root(xpath)
            if root is not None and root not in self.pre_config[device_name]:
                self.pre_config[device_name][root] = self.collect_config(
                    connection, root)
                if self.pre_config[device_name][root] is None:
                    result = False
        return result

    def collect_config(self, connection, root):
        '''Collect configuration by Netconf get-config.'''

        prefix, id = self.split_tag(root)
        if prefix is None or prefix not in self.namespace:
            log.warning("Prefix '{}' is not in self.namespace = {}"
                        .format(prefix, self.namespace))
            return None
        ele_name = "{{{}}}{}".format(self.namespace[prefix], id)
        filter_ele = etree.Element(FILTER_TAG, type='subtree')
        etree.SubElement(filter_ele, ele_name)
        reply = connection.get_config(filter=filter_ele, source='running')
        if reply.ok:
            return etree.ElementTree(reply.data_ele.find(ele_name))
        else:
            log.warning("Received error in reply when collecting '{}'"
                        .format(root))
            return None

    def build_rpc(self, xpath_set):
        '''Build an edit-config to cleanup containers and/or list instances.'''

        operation, rpc_args = yangexec.gen_ncclient_rpc(
            rpc_data={
                'datastore': self.datastore.get('type', 'running'),
                'operation': 'edit-config',
                'namespace': self.namespace,
                'nodes': [
                    {'xpath': x, 'edit-op': 'remove'}
                    for x in xpath_set
                ],
            },
            prefix_type='always',
        )
        return rpc_args

    def update_remove_xpaths(self, modified_xpath, xpath_set, device):
        '''Examine a modified Xpath and determine which container or list
        instance should be removed.'''

        root = self.get_root(modified_xpath)
        if root is None or root not in self.pre_config[device.name]:
            return

        # Make sure modified_xpath is a valid one. Otherwise it is ignored.
        xpath_list = modified_xpath.split('/')
        if xpath_list[0] != '':
            return
        xpath_list_length = len(xpath_list)
        if xpath_list_length < 2:
            return

        for i in range(2, xpath_list_length):
            ancestor_xpath = '/'.join(xpath_list[:i])
            if self.pre_config[device.name][root] is None:
                xpath_set.add(ancestor_xpath)
                return
            try:
                node = self.pre_config[device.name][root].xpath(
                    ancestor_xpath,
                    namespaces=self.namespace,
                )
            except Exception:
                pass
            else:
                if not node:
                    xpath_set.add(ancestor_xpath)
                    return
