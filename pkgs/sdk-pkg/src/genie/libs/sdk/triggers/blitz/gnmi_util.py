from typing import List, Tuple
import logging
import re
import base64
import json
import sys
import pdb
from datetime import datetime
from threading import Thread, Event
import traceback
import time
from abc import ABC
from xml.etree.ElementPath import xpath_tokenizer_re
from google.protobuf import json_format
from six import string_types
from pyats.log.utils import banner
from pyats.utils.secret_strings import to_plaintext
import grpc
from yang.connector import proto
from yang.connector.proto import gnmi_pb2
from yang.connector.gnmi import Gnmi
from .rpcverify import DecodedField, DeletedPath
from copy import deepcopy
from .subscription import Subscription

log = logging.getLogger(__name__)


class GnmiMessageException(Exception):
    pass


class LeafListVal:
    """Class to set a leaf list value"""
    def __init__(self, val):
        self.llvalue = val

    @property
    def llvalue(self):
        return self._llvalue

    @llvalue.setter
    def llvalue(self, val):
        self._llvalue = val


class ForkedPdb(pdb.Pdb):
    """A pdb subclass for debugging GnmiNotification.

    Usage: ForkedPdb().set_trace()
    """
    def interaction(self, *args, **kwargs):
        _stdin = sys.stdin
        try:
            sys.stdin = open('/dev/stdin')
            pdb.Pdb.interaction(self, *args, **kwargs)
        finally:
            sys.stdin = _stdin


class GnmiMessage:
    """Class to prepare and return gMNI messages"""

    def __init__(self, message_type, cfg):
        self.msg_type = message_type
        self.cfg = cfg
        self.metadata = None

    @classmethod
    def run_set(self, device, payload):
        """Run gNMI set service.

        Args:
          device (ysdevice.DeviceProfile): Target device.
          user (str): YANG Suite username.
          payload (proto.gnmi_pb2.SetRequest): SetRequest.
        Returns:
          proto.gnmi_pb2.SetResponse
        """
        if isinstance(payload, proto.gnmi_pb2.SetRequest):
            gnmi_string = str(payload)
        else:
            try:
                payload = GnmiMessageConstructor.json_to_gnmi('set', payload)
                gnmi_string = str(payload)
            except Exception:
                log.error(traceback.format_exc())
                raise GnmiMessageException("Invalid payload\n{0}".format(
                    str(payload))
                )
        log.info('gNMI SET\n' + '=' * 8 + '\n{0}'.format(
            gnmi_string
        ))
        try:
            self.metadata = [
                ("username", device.device.credentials.default.get('username', '')),
                ("password", to_plaintext(device.device.credentials.default.get('password', ''))),
            ]
            response = device.gnmi.service.Set(payload, metadata=self.metadata)
            log.info(
                'gNMI SET Response\n' + '=' * 17 + '\n{0}'.format(
                    str(response)
                )
            )
            dt = datetime.fromtimestamp(response.timestamp / 1e9)
            log.info(
                '\ntimestamp decoded: {0}\n\n'.format(
                    dt.strftime('%Y %b %d %H:%M:%S')
                )
            )
            return response
        except Exception as exc:
            log.error(traceback.format_exc())
            if hasattr(exc, 'details'):
                log.error('ERROR: {0}'.format(exc.details()))
            else:
                log.error(str(exc))

    @classmethod
    def run_get(self,
                device: Gnmi,
                payload: str,
                namespace: dict,
                transaction_time: float = 0) -> Tuple[gnmi_pb2.GetResponse, bool]:
        """Run gNMI get service.

        Args:
          device (ysdevice.DeviceProfile): Target device.
          user (str): YANG Suite username.
          payload (proto.gnmi_pb2.GetRequest): GetRequest.
          payload (str): JSON representing a GetRequest.
        Returns:
          proto.gnmi_pb2.GetResponse
        """
        if isinstance(payload, proto.gnmi_pb2.GetRequest):
            gnmi_string = str(payload)
        else:
            try:
                payload = GnmiMessageConstructor.json_to_gnmi('get', payload)
                gnmi_string = str(payload)
                # Fixup namespace for returns processing.
                self.prefix_to_module({'namespace': namespace})
            except Exception:
                log.error(traceback.format_exc())
                raise GnmiMessageException("Invalid payload\n{0}".format(
                    str(payload)
                ))
        log.info('gNMI GET\n' + '=' * 8 + '\n{0}'.format(
            gnmi_string
        ))
        try:
            self.metadata = [
                ("username", device.device.credentials.default.get('username', '')),
                ("password", to_plaintext(device.device.credentials.default.get('password', ''))),
            ]
            if transaction_time:
                start_time = time.time()
                response = device.gnmi.service.Get(
                    payload, metadata=self.metadata)
                response_time = time.time() - start_time
                if response_time > transaction_time:
                    log.info(
                        'gNMI GET Response\n' + '=' * 17 + '\n{0}'.format(
                            str(response)
                        )
                    )
                    log.error(banner(
                        f'Response time: {response_time} seconds exceeded transaction_time {transaction_time}',
                    ))
                    return None
            else:
                response = device.gnmi.service.Get(payload, metadata=self.metadata)
            log.info(
                'gNMI GET Response\n' + '=' * 17 + '\n{0}'.format(
                    str(response)
                )
            )
            if isinstance(response, gnmi_pb2.GetResponse):
                return response
            return None
        except Exception as exc:
            log.error(traceback.format_exc())
            if hasattr(exc, 'details'):
                log.error('ERROR: {0}'.format(exc.details()))
            else:
                log.error(str(exc))
            return None

    @staticmethod
    def get_opfields(val, xpath_str, opfields=[], namespace={}):
        if isinstance(val, dict):
            for name, dict_val in val.items():
                opfields = GnmiMessage.get_opfields(
                    dict_val,
                    xpath_str + '/' + name,
                    opfields,
                    namespace
                )
        elif isinstance(val, list):
            for item in val:
                GnmiMessage.get_opfields(item, xpath_str, opfields, namespace)
        else:
            xpath_list = xpath_str.split('/')
            name = xpath_list.pop()
            for mod in namespace.values():
                name = name.replace(mod + ':', '')
            xpath_str = '/'.join(xpath_list)
            opfields.append((val, xpath_str + '/' + name))

        return opfields

    @staticmethod
    def path_elem_to_xpath(path_elem, prefix='', namespace={}, opfields=[]):
        """Convert a Path structure to an Xpath."""
        elems = path_elem.get('elem', [])
        xpath = []
        for elem in elems:
            name = elem.get('name', '')
            if name:
                for mod in namespace.values():
                    name = name.replace(mod + ':', '')
                xpath.append(name)
            key = elem.get('key', '')
            if key:
                for name, value in key.items():
                    for mod in namespace.values():
                        value = str(value).replace(mod + ':', '')
                    opfields.append((
                        value, prefix + '/' + '/'.join(xpath) + '/' + name))
        if len(xpath):
            return prefix + '/' + '/'.join(xpath)
        else:
            return ''

    @staticmethod
    def decode_update_value(val):
        if 'jsonIetfVal' in val:
            val = val.get('jsonIetfVal', '')
            if not val:
                log.info('"val" has no content')
                return
            json_val = base64.b64decode(val).decode('utf-8')
            json_dict = json.loads(json_val, strict=False)
            return json_dict
        elif 'jsonVal' in val:
            val = val.get('jsonVal', '')
            if not val:
                log.info('"val" has no content')
                return
            json_val = base64.b64decode(val).decode('utf-8')
            json_dict = json.loads(json_val, strict=False)
            return json_dict
        elif 'asciiVal' in val:
            val = val.get('asciiVal', '')
            if not val:
                log.info('"asciiVal" has no content')
                return
            val = val.strip()
            return val
        elif val:
            datatype = next(iter(val))
            value = val[datatype]
            if 'int' in datatype:
                return int(value)
            elif ('float' in datatype or
                    'double' in datatype):
                return float(value)
            elif 'decimal' in datatype:
                return float(value['digits']) / (10 ** value['precision'])
            elif 'bytes' in datatype:
                return bytes(value, encoding='utf8')
            elif 'leaflist' in datatype:
                return GnmiMessage.process_leaf_list_val(value)
            else:
                return value
        else:
            log.info('Update has no value')

    @staticmethod
    def process_update(update, prefix=None, namespace={}, opfields=[]):
        """Convert Update to Xpath, value, and datatype."""
        pre_path = ''
        xpath = ''

        if not isinstance(update, list):
            update = [update]

        if prefix:
            pre_path = GnmiMessage.path_elem_to_xpath(
                prefix, pre_path, namespace, opfields
            )

        for upd in update:
            if 'path' in upd:
                xpath = GnmiMessage.path_elem_to_xpath(
                    upd['path'], pre_path, namespace, opfields
                )
            val = upd.get('val', {})
            decoded_val = GnmiMessage.decode_update_value(val)
            if 'asciiVal' in val:
                opfields.append({
                    'datatype': 'ascii',
                    'value': decoded_val,
                })
            elif decoded_val and isinstance(decoded_val, (list, dict)):
                # Walk the list or dict to get the opfields.
                GnmiMessage.get_opfields(decoded_val, xpath, opfields, namespace)
            else:
                opfields.append((decoded_val, xpath))

        if decoded_val == {}:
            decoded_val = None

        return decoded_val

    @staticmethod
    def process_delete(delete,
                       prefix: str = None,
                       namespace: dict = {},
                       deleted_paths: List[DeletedPath] = []):
        pre_path = ''
        if not isinstance(delete, list):
            delete = [delete]
        if prefix:
            pre_path = GnmiMessage.path_elem_to_xpath(
                prefix, pre_path, namespace, []
            )

        for del_elem in delete:
            path_keys = []
            xpath = GnmiMessage.path_elem_to_xpath(
                del_elem, pre_path, namespace, path_keys)
            deleted_paths.append(DeletedPath(
                xpath, [DecodedField(*field) for field in path_keys]))

    @staticmethod
    def process_leaf_list_val(value):
        """Convert leaf list value to list of values

        Args:
          value (dict): leaf list value

        For proto encoding leaf list value is received as below format:
        val{
           leaflist_val: {
                element: [{'datatype':'value'},{'datatype':'value'}]
           }
        }

        Returns (list): leaf list value convert into list format
                        leaf_list_val = ['value','value']
        """
        leaf_list_val = []
        elements = value['element']
        for elem in elements:
            for datatype, val in elem.items():
                if 'int' in datatype:
                    val = int(val)
                elif ('float' in datatype or
                      'double' in datatype):
                    val = float(val)
                elif 'decimal' in datatype:
                  value = float(value['digits']) / (10 ** value['precision'])
                elif 'bytes' in datatype:
                    val = bytes(value, encoding='utf8')
                leaf_list_val.append(val)

        return leaf_list_val

    @classmethod
    def run_subscribe(self, device: Gnmi, payload: proto.gnmi_pb2.SubscribeRequest, **request) -> Thread:
        """Run gNMI subscribe service.

        Args:
          device (ysdevice.DeviceProfile): Target device.
          payload (proto.gnmi_pb2.SubscribeRequest): SetRequest.
          request (dict): gNMI subscribe settings for thread.
        Returns:
          GnmiSubscription Thread
        """
        if isinstance(payload, proto.gnmi_pb2.SubscribeRequest):
            gnmi_string = str(payload)
        else:
            try:
                payload = GnmiMessageConstructor.json_to_gnmi(
                    'subscribe', payload
                )
                gnmi_string = str(payload)
                # Fixup namespace for returns processing.
                self.prefix_to_module(request)
            except Exception:
                log.error(traceback.format_exc())
                raise GnmiMessageException("Invalid payload\n{0}".format(
                    str(payload)
                ))
        log.info('gNMI SUBSCRIBE\n' + '=' * 14 + '\n{0}'.format(
            gnmi_string
        ))
        try:

            payloads = [payload]
            request['log'] = log
            request_mode = request.get('request_mode', 'ONCE')
            if request_mode == 'ONCE':
                subscribe_thread = GnmiSubscriptionOnce(
                    device, payloads, **request)
            elif request_mode == 'POLL':
                subscribe_thread = GnmiSubscriptionPoll(
                    device, payloads, **request)
            elif request_mode == 'STREAM':
                subscribe_thread = GnmiSubscriptionStream(
                    device, payloads, **request)
            device.active_notifications[device] = subscribe_thread
            subscribe_thread.start()

            # Wait for the thread to complete
            subscribe_thread.join()

            return subscribe_thread
        except Exception as exc:
            log.error(traceback.format_exc())
            if hasattr(exc, 'details'):
                log.error('ERROR: {0}'.format(exc.details()))
            else:
                log.error(str(exc))

    @staticmethod
    def prefix_to_module(request):
        """Convert from prefix-to-namespace to prefix-to-module."""
        if not isinstance(request, dict) or 'namespace' not in request:
            log.error('Reqest must have mapping of prefix-to-namespace')
            return
        if 'namespace_modules' in request:
            request['namespace'] = request['namespace_modules']
            return
        namespace_module = {}
        module = None
        for prefix, nspace in request['namespace'].items():
            if "/Cisco-IOS-" in nspace:
                module = nspace[nspace.rfind("/") + 1:]
            elif "/cisco-nx" in nspace:  # NXOS lowercases namespace
                module = "Cisco-NX-OS-device"
            elif "/openconfig.net" in nspace:
                nspace = nspace.replace('http://openconfig.net/yang/', '')
                nspace = nspace.split('/')
                module = '-'.join(['openconfig'] + nspace)
            elif "urn:ietf:params:xml:ns:yang:" in nspace:
                module = nspace.replace("urn:ietf:params:xml:ns:yang:", "")
            if module:
                namespace_module[prefix] = module
        request['namespace'] = namespace_module
        request['namespace_modules'] = namespace_module

    def get_modules(self, cfg):
        """Helper function for get_entries."""
        return cfg.get('modules', {})

    def get_entries(self, cfg):
        """Helper function for get_messages."""
        entries = []
        modules = self.get_modules(cfg)

        for mod in modules.keys():
            entries.append({
                'module': mod,
                'namespace_modules': modules[mod].get('namespace_modules'),
                'namespace_prefixes': modules[mod].get('namespace_prefixes'),
                'nodes': modules[mod]['configs']
            })
        return entries

    def get_messages(self):
        """Using request, instantiate GnmiMessageConstuctor class.

        Returns:
          list: GnmiMessageConstructor classes.
        """
        gmcs = []
        entries = self.get_entries(self.cfg)
        for entry in entries:
            gmc = GnmiMessageConstructor(self.msg_type, entry, **self.cfg)
            gmcs.append(gmc)
        return gmcs


class GnmiMessageConstructor:
    """Construct a single gNMI message based on request."""
    edit_op = {
        'create': 'update',
        'merge': 'update',
        'replace': 'replace',
        'remove': 'delete',
        'delete': 'delete'
    }

    def __init__(self, message_type, entry, **cfg):
        self.request = entry
        self.cfg = cfg
        self.prefix = cfg.get('prefix')
        self.origin = cfg.get('origin')
        self.encoding = cfg.get('encoding', 'JSON_IETF').upper()
        self.get_type = cfg.get('get_type', 'ALL').upper()
        self.base64 = cfg.get('base64', False)
        self.nodes = None
        self.update = []
        self.replace = []
        self.delete = []
        self.subscribe = []
        self.get = []
        self.json_val = {}
        self.msg_type = message_type
        self.xml_xpath_to_gnmi_xpath()
        self.nodes_to_dict()

    @property
    def msg_type(self):
        return self._msg_type

    @msg_type.setter
    def msg_type(self, msg_type):
        self.payload = None
        self._msg_type = msg_type
        if msg_type == 'set':
            self.payload = proto.gnmi_pb2.SetRequest()
        elif msg_type == 'get':
            self.payload = proto.gnmi_pb2.GetRequest()
            self.payload.type = proto.gnmi_pb2.GetRequest.DataType.Value(
                self.get_type
            )
            self.payload.encoding = proto.gnmi_pb2.Encoding.Value(
                self.encoding
            )
        elif msg_type == 'subscribe':
            self.payload = proto.gnmi_pb2.SubscribeRequest()
        if msg_type != 'subscribe' and self.prefix:
            # TODO: calculate prefix paths
            prefix_path = proto.gnmi_pb2.Path()
            prefix_path.origin = self.origin
            self.payload.prefix.CopyFrom(prefix_path)

    @staticmethod
    def _upd_rpl(upd_rpl, base64_encode):
        updates = []
        for upd in upd_rpl:
            val = None
            if 'val' in upd:
                val = upd.pop('val', {})
            gnmi_update = json_format.ParseDict(
                upd,
                proto.gnmi_pb2.Update()
            )
            if val is not None:
                if 'jsonIetfVal' in val:
                    if base64_encode:
                        jval = bytes(
                            json.dumps(val['jsonIetfVal']), encoding='utf-8'
                        )
                        gnmi_update.val.json_ietf_val = base64.b64encode(jval)
                    else:
                        gnmi_update.val.json_ietf_val = json.dumps(
                            val['jsonIetfVal']
                        ).encode('utf-8')
                elif 'jsonVal' in val:
                    if base64_encode:
                        jval = bytes(
                            json.dumps(val['jsonVal']), encoding='utf-8'
                        )
                        gnmi_update.val.json_val = base64.b64encode(jval)
                    else:
                        gnmi_update.val.json_val = json.dumps(
                            val['jsonVal']
                        ).encode('utf-8')
            updates.append(gnmi_update)
        return updates

    @classmethod
    def split_value_namespaces(self, value: str) -> list:
        try:
            return value.split(':')
        except Exception:
            return []

    @classmethod
    def json_to_gnmi(self, action, payload, **kwargs):
        """Given a JSON payload, convert it to a gNMI message.

        Expected JSON format is similar to a string __repr__ of the
        proto.gnmi_pb2 class with the exception of the "val" member.
        The "val" is passed in normal JSON format in the payload parameter
        but then gets converted to base64 encoding in the returned
        associated proto.gnmi_pb2 class.

        Args:
          action (str): set | get | subscribe.
          payload (str): Properly formated JSON string.
        Raises:
          GnmiMessageException
        Returns:
          gNMI proto.gnmi_pdb2 class
        """
        base64_encode = kwargs.get('base64', False)
        try:
            gnmi_dict = json.loads(payload)
        except Exception as exc:
            log.error(traceback.format_exc())
            raise GnmiMessageException('JSON parse failed: {0}'.format(
                str(exc)
            ))
        try:
            if action == 'set':
                updates = gnmi_dict.pop('update', [])
                replaces = gnmi_dict.pop('replace', [])
                gnmi_pld = json_format.ParseDict(
                    gnmi_dict,
                    proto.gnmi_pb2.SetRequest()
                )
                if updates:
                    gnmi_upd = self._upd_rpl(updates, base64_encode)
                    if gnmi_upd:
                        gnmi_pld.update.extend(gnmi_upd)
                if replaces:
                    gnmi_upd = self._upd_rpl(replaces, base64_encode)
                    if gnmi_upd:
                        gnmi_pld.replace.extend(gnmi_upd)
            elif action == 'get':
                gnmi_pld = json_format.Parse(
                    payload,
                    proto.gnmi_pb2.GetRequest()
                )
            elif action == 'subscribe':
                gnmi_pld = json_format.Parse(
                    payload,
                    proto.gnmi_pb2.SubscribeRequest()
                )
            return gnmi_pld
        except Exception as exc:
            log.error(traceback.format_exc())
            raise GnmiMessageException('Message parse failed: {}'.format(
                str(exc)
            ))

    def _manage_paths(self, path_req, gnmi_req):
        # Get initial gnmi path for gnmi message
        short_xp = self.get_shortest_common_path(path_req)
        gnmi_path = self.parse_xpath_to_gnmi_path(
            short_xp, self.origin
        )

        ext_xpaths = []
        for n in path_req:
            xp = n['xpath']
            n['xpath'] = xp[len(short_xp):]
            ext_xpaths.append(n)

        gnmi_req.path.CopyFrom(gnmi_path)

        return self.get_payload(ext_xpaths)

    def _gnmi_update_request(self, upd_req, gnmi_upd_req):
        # Construct an Update structure for a SetRequest gNMI message.
        json_val = self._manage_paths(upd_req, gnmi_upd_req)
        # Human readable saved for logs

        if self.json_val:
            if not isinstance(self.json_val, list):
                self.json_val = [self.json_val]
            self.json_val.append(json_val)
        else:
            self.json_val = json_val

        json_val = json.dumps(json_val).encode('utf-8')

        if self.base64:
            json_val = base64.b64encode(json_val)

        if self.encoding and self.encoding.lower() == 'json_ietf':
            gnmi_upd_req.val.json_ietf_val = json_val
        else:
            gnmi_upd_req.val.json_val = json_val

        return [gnmi_upd_req]

    def group_nodes(self, update):
        """ Group the nodes based on leaf/list/container level

        Args:
          nodes (list): dicts with xpath in gNMI format, nodetypes, values.
        """
        gnmi_update_paths = []
        update_filter = []
        update_nodes = []
        list_or_cont = False
        parent_xp = ""
        # Group the nodes based on leaf/list/container level
        # Eg nodes: [leaf, leaf, leaf, list, leaf, leaf]
        # leaf level: [leaf], [leaf], [leaf] - Leaf level RPCs
        # will build sepeartely for each leaf node.
        # list level: [list, leaf, leaf]
        for node in update:
            if (node['xpath'].endswith("]") \
            or node['nodetype'] == 'list' \
            or node['nodetype'] == 'container') \
            and (not parent_xp or not parent_xp in node['xpath']):
                parent_xp = node['xpath']
                list_or_cont = True
                if update_filter:
                    update_nodes.append(update_filter)
                update_filter = []
                update_filter.append(node)
            else:
                update_filter.append(node)
                if not list_or_cont:
                    update_nodes.append(update_filter)
                    update_filter = []

        if update_filter:
            update_nodes.append(update_filter)

        return update_nodes

    def nodes_to_dict(self, nodes=None, origin=None):
        """Construct full gNMI request message to be sent through service.

        Args:
          nodes (list): dicts with xpath in gNMI format, nodetypes, values.
          origin (string): gNMI origin for message.
        """
        # TODO: classmethod?
        if not self.nodes:
            self.nodes = nodes
        if origin:
            self.origin = origin

        update = self.nodes.get('update', [])
        replace = self.nodes.get('replace', [])
        delete = self.nodes.get('delete', [])
        get = self.nodes.get('get', [])
        subscribes = self.nodes.get('subscribe', [])

        if update:
            gnmi_update = proto.gnmi_pb2.Update()
            update_nodes = self.group_nodes(update)
            # Send each group for payload building
            for node in update_nodes:
                self.update = self._gnmi_update_request(node, gnmi_update)
                self.payload.update.extend(self.update)

        if replace:
            gnmi_replace = proto.gnmi_pb2.Update()
            replace_nodes = self.group_nodes(replace)
            # Send each group for payload building.
            for node in replace_nodes:
                self.replace = self._gnmi_update_request(node, gnmi_replace)
                self.payload.replace.extend(self.replace)

        if delete:
            gnmi_delete_paths = []
            for xp in delete:
                gnmi_delete_paths.append(
                    self.parse_xpath_to_gnmi_path(xp, self.origin)
                )
            self.payload.delete.extend(gnmi_delete_paths)

        if get:
            gnmi_get_paths = []
            for xp in get:
                self.payload.path.append(
                    self.parse_xpath_to_gnmi_path(xp, self.origin)
                )
            self.payload.path.extend(gnmi_get_paths)

        if subscribes:
            # Create subscribe list.
            subscribe_list = proto.gnmi_pb2.SubscriptionList()
            subscribe_list.updates_only = self.cfg.get('updates_only', False)
            subscribe_list.encoding = proto.gnmi_pb2.Encoding.Value(
                self.encoding
            )
            mode = self.cfg.get('request_mode', 'STREAM')
            subscribe_list.mode = proto.gnmi_pb2.SubscriptionList.Mode.Value(
                mode
            )
            if self.prefix:
                # TODO: calculate prefix paths
                prefix_path = proto.gnmi_pb2.Path()
                prefix_path.origin = self.origin
                subscribe_list.prefix.CopyFrom(prefix_path)

            # Create subscriptions for the list.
            sub_mode = self.cfg.get('sub_mode')
            for subscribe in subscribes:
                subscription = proto.gnmi_pb2.Subscription()
                sample_poll = self.cfg.get(
                    'sample_interval', self.cfg.get('sample_poll'))

                if sub_mode:
                    subscription.mode = proto.gnmi_pb2.SubscriptionMode.Value(
                        sub_mode
                    )
                if sub_mode == 'SAMPLE' and sample_poll:
                    sample_poll = int(1e9) * int(sample_poll)
                    subscription.sample_interval = sample_poll
                gnmi_path = self.parse_xpath_to_gnmi_path(subscribe)
                subscription.path.CopyFrom(gnmi_path)

                # Add the subscription to the list.
                subscribe_list.subscription.extend([subscription])
            # Add list to the subscribe request.
            self.payload.subscribe.CopyFrom(subscribe_list)

        return self.payload

    @classmethod
    def get_subscribe_poll(self):
        """POLL subscribe requires a message to start polling."""
        sub = proto.gnmi_pb2.SubscribeRequest()
        sub.poll.SetInParent()
        return sub

    def _trim_xpaths(self, xpaths, short_xp):
        # Helper function for get_shortest_common_path.
        for xpath in xpaths:
            if short_xp not in xpath:
                if short_xp.endswith(']'):
                    while short_xp.endswith(']'):
                        short_xp = short_xp[:short_xp.rfind('[')]
                    xp = short_xp[:short_xp.rfind('/')]
                else:
                    xp = short_xp[:short_xp.rfind('/')]
                short_xp = self._trim_xpaths(xpaths, xp)
        return short_xp

    def get_shortest_common_path(self, nodes):
        """Find the shortest common path in a collection of nodes.

        Args:
          nodes (list): dicts with xpath in gNMI format, nodetypes, values.

        Return:
          str
        """
        if(len(nodes) == 1):
            return nodes[0]['xpath']
        xpaths = [n['xpath'] for n in nodes]
        short_xp = min(set(xpaths), key=len)
        short_xp = self._trim_xpaths(xpaths, short_xp)
        short_node = [n for n in nodes if n['xpath'] == short_xp]
        if short_node:
            if not short_node[0]['xpath'].endswith("]") \
            and short_node[0]['nodetype'] not in ['list', 'container']:
                while short_xp.endswith(']'):
                    short_xp = short_xp[:short_xp.rfind('[')]
                short_xp = short_xp[:short_xp.rfind('/')]
        return short_xp

    def get_payload(self, update):
        """Construct dict that will be converted to json_val in Update.

        dict will be in format of json {}

        For all list having similar keys but different values, create a list of dictionaries.
        This will allow to store every key value in a single json_val

        Eg: xpath =  common_xpath/x-list[type="t1"]/val
                     common_xpath/x-list[type="t2"]/val

        json_val will be = "{"x-list": [{"type": "t1", "val": 10}, {"type": "t2", "val": 10}]}"

        Args:
          update (list): dicts with xpath in gNMI format, nodetypes, values.

        Returns:
          dict
        """
        if(len(update) == 1 and not update[0]['xpath']):
            return update[0]['value']
        json_val = {}
        processed_xp = []
        list_nodes = []
        for node in update:
            ind = 0
            xp = node['xpath']
            if xp.endswith(']'):
                xp = xp + '/'
            if '[' in xp:
                # child node of list
                # get the name of the list node
                list_xpath = node['xpath']
                while '[' in list_xpath:
                    list_xpath = list_xpath[:list_xpath.rfind('[')]
                    if not list_xpath.endswith(']'):
                        list_node = list_xpath[list_xpath.rfind('/'):]
                        list_node = list_node.strip('/')
                        if not list_node in list_nodes:
                            list_nodes.append(list_node)
            if xp in processed_xp:
                if node['nodetype'] != 'leaf-list':
                    continue
            jval = json_val
            collect_key = False
            key_elem = None
            tokenized = xpath_tokenizer_re.findall(xp)
            if len(tokenized) == 0:
                continue
            for i, seg in enumerate(tokenized, 1):
                token, elem = seg
                if token in ['/', '=']:
                    continue
                if not token and not collect_key and elem:
                    if len(tokenized) == i:
                        # If a node has only one element
                        if len(jval) == 0:
                            if node.get('nodetype', '') == 'leaf-list':
                                if jval.get(elem) is None:
                                    jval[elem] = [LeafListVal(node['value'][0])]
                                else:
                                    jval[elem].append(LeafListVal(node['value'][0]))
                            else:
                                jval[elem] = node['value']
                        else:
                            # Check if jval is pointing to a list or dict to assign values
                            if isinstance(jval, list):
                                if node.get('nodetype', '') == 'leaf-list':
                                    if jval[ind].get(elem) is None:
                                        jval[ind][elem] = [LeafListVal(node['value'][0])]
                                    else:
                                        jval[ind][elem].append(LeafListVal(node['value'][0]))
                                else:
                                    jval[ind][elem] = node['value']
                            else:
                                if node.get('nodetype', '') == 'leaf-list':
                                    if jval.get(elem) is None:
                                        jval[elem] = [LeafListVal(node['value'][0])]
                                    else:
                                        jval[elem].append(LeafListVal(node['value'][0]))
                                else:
                                    jval[elem] = node['value']
                    else:
                        # Create a new list of dictionary / new key in dictionary if elem is not present
                        if elem not in jval:
                            if isinstance(jval, list):
                                if (elem not in jval[ind]):
                                    if (len(jval) == 0 or {} in jval):
                                        ind = 0
                                    jval[ind][elem] = []
                                    jval[ind][elem].append({})
                            else:
                                jval[elem] = []
                                ind = 0
                                jval[elem].append({})

                        # For every interation point jval to the last list created.
                        if isinstance(jval, list):
                            if jval[ind][elem] == "":
                                jval[ind][elem] = []
                                jval[ind][elem].append({})
                            jval = jval[ind][elem]
                            ind = 0
                        else:
                            jval = jval[elem]
                    continue
                if token == '[':
                    collect_key = True
                    continue
                if token == ']':
                    collect_key = False
                    continue
                if key_elem is not None and token:
                    # Store key_elem only if it is not equal to prevous key_elem for the same list.
                    if key_elem in jval[ind]:
                        index=0
                        f=0
                        for j in jval:
                            if j[key_elem] == token.strip('"'):
                                f=1
                                break
                            index = index+1
                        if f==0:
                            ind = len(jval)
                            jval.append({})
                            jval[ind][key_elem] = token.strip('"')
                        else:
                            ind = index
                    else:
                        jval[ind][key_elem] = token.strip('"')
                    key_elem = None
                    continue
                if collect_key and elem:
                    key_elem = elem
                    continue
            processed_xp.append(xp)

        self.format_json_val(json_val)
        self.format_list_nodes(json_val, list_nodes)
        return json_val

    def format_list_nodes(self, json_val, list_nodes):
        # Enclose list entries within square brackets.
        if not isinstance(json_val, dict):
            if isinstance(json_val, list):
                for val in json_val:
                    self.format_list_nodes(val, list_nodes)
            else:
                return
        for val in json_val:
            if val in list_nodes:
                json_val[val] = [json_val[val]]
            if isinstance(val, dict) or isinstance(json_val, list):
                return
            self.format_list_nodes(json_val[val], list_nodes)

    def format_json_val(self,json_val):
        # Convert List of Dictionaries with only 1 one element to Dictionary
        if not isinstance(json_val,dict):
            return
        for j in json_val:
            if isinstance(json_val[j],list) and len(json_val[j]) == 1:
                if isinstance(json_val[j][0], LeafListVal):
                    # leaflist value need to enclosed within brackets
                    # extract the value from Leaflistval object
                    json_val[j][0] = json_val[j][0].llvalue
                    self.format_json_val(json_val[j])
                else:
                    json_val[j] = json_val[j][0]
                    self.format_json_val(json_val[j])
            else:
                if isinstance(json_val[j],list):
                    for ind, i in enumerate(json_val[j]):
                        if isinstance(i, LeafListVal):
                            json_val[j][ind] = i.llvalue
                            self.format_json_val(i.llvalue)
                        else:
                            self.format_json_val(i)

    def _trim_nodes(self, nodes):
        # Prune list nodes if already in other nodes xpath
        if nodes:
            xps = [n['xpath'] for n in nodes]
            long_xp = max(xps, key=len)
        for i in range(len(nodes)):
            if nodes[i]['xpath'] == long_xp:
                continue
            if nodes[i]['xpath']+'/' in long_xp:
                nodes.remove(nodes[i])
                return self._trim_nodes(nodes)
        return nodes

    def xml_xpath_to_gnmi_xpath(self):
        """Convert XML Path Language 1.0 Xpath to gNMI Xpath.

        Input modeled after YANG/NETCONF Xpaths.
        References:
        * https://www.w3.org/TR/1999/REC-xpath-19991116/#location-paths
        * https://www.w3.org/TR/1999/REC-xpath-19991116/#path-abbrev
        * https://tools.ietf.org/html/rfc6020#section-6.4
        * https://tools.ietf.org/html/rfc6020#section-9.13
        * https://tools.ietf.org/html/rfc6241

        Parameters
        ----------
        self.request: dict containing request namespace and nodes to be worked on.
            namespace: dict of <prefix>: <namespace>
            nodes: list of dict
                    <xpath>: Xpath pointing to resource
                    <nodetype>: YANG statement type
                    <value>: value to set resource to
                    <edit-op>: equivelant NETCONF edit-config operation

        Constructs
        ----------
          self.nodes: 4 lists containing possible updates, replaces,
            deletes, or gets derived from input request.
        """
        message = {
            "update": [],
            "replace": [],
            "delete": [],
            "get": [],
            "subscribe": []
        }

        if "nodes" not in self.request:
            # TODO: raw rpc?
            return message

        GnmiMessage.prefix_to_module(self.request)

        nodes = deepcopy(self.request.get("nodes", []))
        if self.msg_type == 'set':
            # Prune key nodes without edit-op assigned.
            nodes = [n for n in nodes if not (
                n['xpath'].endswith(']') and
                not n.get('edit-op')
            )]
        if self.msg_type in ['get', 'subscribe'] and len(nodes) > 1:
            # Prune nodes with xpaths already in other node's xpath.
            nodes = self._trim_nodes(nodes)

        module = self.request.get('module')
        self.namespace_modules = self.request.get("namespace_modules", {})
        parent_edit_op = None
        for node in nodes:
            if "xpath" not in node:
                log.error("Xpath is not in message")
            else:
                xpath = node["xpath"]
                value = node.get("value", "")
                datatype = node.get('datatype', 'string')
                edit_op = node.get("edit-op", "")
                if(xpath.endswith("]")):
                    nodetype = "list"
                else:
                    nodetype = node.get("nodetype","")

                if nodetype in ['list', 'container']:
                    parent_edit_op = edit_op

                # Ready value for proper JSON conversion.
                if datatype == 'boolean':
                    if isinstance(value, string_types):
                        if value.lower() == 'true':
                            value = True
                        elif value.lower() == 'false':
                            value = False
                elif datatype.startswith('int') or \
                        datatype.startswith('uint'):
                    if value:
                        value = int(value)
                elif ('float' in datatype or
                      'double' in datatype):
                    if value:
                        value = float(value)
                elif 'decimal' in datatype:
                    if value:
                        value = float(value['digits']) / \
                            (10 ** value['precision'])

                if xpath.startswith('/'):
                    xp = xpath.split('/')[1:]
                else:
                    node['xpath'] = '/' + xpath
                    xp = xpath.split('/')

                if not module:
                    # First segment of xpath has prefix of module.
                    if ':' in xp[0]:
                        pfx = xp[0].split(':')[0]
                        if pfx not in self.namespace_modules:
                            if pfx in self.namespace_modules.values():
                                # This xpath has a gNMI type prefix
                                module = pfx
                        else:
                            module = self.namespace_modules[pfx]
                    else:
                        module = ''
                    if self.prefix is None:
                        # Should be in format so this is an older test
                        if 'Cisco-IOS-XE' in module:
                            self.prefix = True
                            self.origin = 'rfc7951'
                        elif 'openconfig' in module:
                            self.origin = 'openconfig'
                value_namespaces = self.split_value_namespaces(value)
                # For info about namespaces handling refer to
                # https://datatracker.ietf.org/doc/html/rfc7951#page-5
                for pfx, mod in self.namespace_modules.items():
                    if isinstance(value, string_types) and pfx in value_namespaces:
                        if mod != module:
                            value = value.replace(pfx + ":", mod + ':')
                    elif isinstance(value, list):
                        for ind, i in enumerate(value):
                            list_value_namespaces = self.split_value_namespaces(i)
                            if (pfx in list_value_namespaces) and (mod != module):
                                value[ind] = value[ind].replace(pfx + ":", mod + ":")
                    # rfc7951 origin requires entire module name in path.
                    # Module as origin requires entire module name in path.
                    for i, seg in enumerate(xp):
                        if pfx not in xpath:
                            continue
                        if i == 0 and self.prefix:
                            # Only needed for first path elem.
                            seg = seg.replace(pfx + ":", module + ':')
                            xp[i] = seg
                            continue
                        if mod != module and self.origin == 'rfc7951':
                            # From another module so this is required.
                            seg = seg.replace(pfx + ":", mod + ':')
                        else:
                            seg = seg.replace(pfx + ':', '')
                        xp[i] = seg

                    if not xpath.endswith(']'):
                        node['name'] = xp[-1:][0]
                    else:
                        node['name'] = ''
                    node['xpath'] = '/'.join(xp)

                if nodetype == 'leaf-list':
                    node['value'] = [value]
                else:
                    node['value'] = value

                if self.msg_type == 'set':
                    if not edit_op:
                        if parent_edit_op:
                            edit_op = parent_edit_op
                        else:
                            edit_op = 'merge'

                    if self.edit_op[edit_op] in ["update", "replace"]:
                        if self.edit_op[edit_op] == "replace":
                            message["replace"] += [node]
                        elif self.edit_op[edit_op] == "update":
                            message["update"] += [node]
                    elif self.edit_op[edit_op] in ["delete", 'remove']:
                        message["delete"].append(node['xpath'])

                elif self.msg_type in ['get', 'subscribe']:
                    if not message[self.msg_type]:
                        message[self.msg_type] = [node['xpath']]
                    elif node['xpath'] not in message[self.msg_type]:
                        message[self.msg_type].append(node['xpath'])
                else:
                    log.error('gNMI message type "{0}" is invalid.'.format(
                        str(self.msg_type)
                    ))

        self.nodes = message

    @classmethod
    def parse_xpath_to_gnmi_path(cls, xpath, origin=None):
        """Parses an XPath to proto.gnmi_pb2.Path.

        Effectively wraps the std XML XPath tokenizer and traverses
        the identified groups. Parsing robustness needs to be validated.
        Probably best to formalize as a state machine sometime.
        TODO: Formalize tokenizer traversal via state machine.
        """
        if not isinstance(xpath, string_types):
            raise Exception("xpath must be a string!")
        path = proto.gnmi_pb2.Path()
        if origin:
            if not isinstance(origin, string_types):
                raise Exception("origin must be a string!")
            path.origin = origin
        curr_elem = proto.gnmi_pb2.PathElem()
        in_filter = False
        just_filtered = False
        curr_key = None
        # TODO: Lazy
        xpath = xpath.strip("/")
        xpath_elements = xpath_tokenizer_re.findall(xpath)
        path_elems = []
        for element in xpath_elements:
            # stripped initial /, so this indicates a completed element
            if element[0] == "/":
                if not curr_elem.name:
                    # Trying to append to path without a name.
                    raise Exception(
                        "Current PathElem has no name! Invalid XPath?"
                    )
                path_elems.append(curr_elem)
                curr_elem = proto.gnmi_pb2.PathElem()
                continue
            # We are entering a filter
            elif element[0] == "[":
                in_filter = True
                continue
            # We are exiting a filter
            elif element[0] == "]":
                in_filter = False
                continue
            # If we're not in a filter then we're a PathElem name
            elif not in_filter:
                curr_elem.name = element[1]
            # Skip blank spaces
            elif not any([element[0], element[1]]):
                continue
            # If we're in the filter and just completed a filter expr,
            # "and" as a junction should just be ignored.
            elif in_filter and just_filtered and element[1] == "and":
                just_filtered = False
                continue
            # Otherwise we're in a filter and this term is a key name
            elif curr_key is None:
                curr_key = element[1]
                continue
            # Otherwise we're an operator or the key value
            elif curr_key is not None:
                if element[0] in [">", "<"]:
                    raise Exception("Only = supported as filter operand!")
                if element[0] == "=":
                    continue
                else:
                    # We have a full key here, put it in the map
                    if curr_key in curr_elem.key.keys():
                        raise Exception("Key already in key map!")
                    curr_elem.key[curr_key] = element[0].strip("'\"")
                    curr_key = None
                    just_filtered = True
        # Keys/filters in general should be totally cleaned up at this point.
        if curr_key:
            raise Exception("Hanging key filter! Incomplete XPath?")
        # If we have a dangling element that hasn't been completed due to no
        # / element then let's just append the final element.
        if curr_elem:
            path_elems.append(curr_elem)
            curr_elem = None
        if any([curr_elem, curr_key, in_filter]):
            raise Exception("Unfinished elements in XPath parsing!")

        path.elem.extend(path_elems)
        return path


class GnmiSubscription(Subscription):
    """Base class for gNMI Subscription."""
    def __init__(self, device=None, **request):
        super().__init__(device, **request)
        if device is not None:
            self.metadata = [
                ("username", device.device.credentials.default.get('username', '')),
                ("password", to_plaintext(
                    device.device.credentials.default.get('password', ''))),
            ]
        self.log.info(banner('gNMI Subscription reciever started'))

    @classmethod
    def iter_subscribe_request(self,
                               payloads: List[gnmi_pb2.SubscribeRequest],
                               delay: int = 0,
                               sample_poll: int = 0):
        """Generator passed to Subscribe service to handle stream payloads.

        Args:
          payload (list): proto.gnmi_pb2.SubscribeRequest
        """
        for payload in payloads:
            if delay:
                time.sleep(delay)
            if payload.HasField('poll'):
                time.sleep(sample_poll)
                log.info('gNMI SUBSCRIBE POLL\n' + '=' * 19 + '\n{0}'.format(
                    str(payload)
                )
                )
            elif sample_poll:
                log.info('Sample poll ignored for non-poll request')
            yield payload

    def cover_exceptions(func):
        """Decorator to catch exceptions, log them and stop the thread."""

        def inner(self):
            try:
                func(self)
            except grpc.RpcError as exc:
                if exc.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
                    self.log.info("Notification MAX timeout")
                    self.result = self.verifier.end_subscription(self.errors)
                    self.log.info("Terminating notification thread")
                    self.stop()
                else:
                    self.log.error("Unknown error: %s", exc)
                    self.result = False
                    self.errors.append(exc)
            except Exception as exc:
                msg = ''
                if hasattr(exc, 'details'):
                    msg += 'details: ' + exc.details()
                if hasattr(exc, 'debug_error_string'):
                    msg += exc.debug_error_string()
                if not msg:
                    msg = str(exc)
                self.log.error("Unknown error: %s", exc)
                self.errors.append(exc)
            finally:
                if not self.stopped():
                    self.log.error("Error while terminating notification thread")
                    self.result = False
                    self.stop()
        return inner


class GnmiSubscriptionStream(GnmiSubscription):
    def __init__(self,
                 device=None,
                 payload: List[gnmi_pb2.SubscribeRequest] = None,
                 responses: List[gnmi_pb2.SubscribeResponse] = None,
                 **request):
        super().__init__(device, **request)
        if responses is not None:
            self.responses = responses
        elif device is not None and payload is not None:
            self.responses = device.gnmi.service.Subscribe(
                self.iter_subscribe_request(payload, self.delay),
                timeout=self.stream_max,
                metadata=self.metadata
            )

    @GnmiSubscription.cover_exceptions
    def run(self):
        """Check for inbound notifications."""
        self.log.info('Subscribe notification active')
        for response in self.responses:
            self.subscribe_response = True
            if response.HasField('sync_response'):
                # Don't count sync_response as a response for transaction_time
                self.log.info("Initial updates received")
                continue
            if response.HasField('update') and not self.stopped():
                arrive_time = time.time()
                if self.transaction_time:
                    timestamp = response.update.timestamp / 10 ** 9
                    delta_time = arrive_time - timestamp
                    if delta_time < 0:
                        self.errors.append(
                            self.DevieOutOfSyncWithNtp(timestamp, arrive_time, self.ntp_server))
                    elif delta_time > self.transaction_time:
                        self.errors.append(self.TransactionTimeExceeded(
                            delta_time, self.transaction_time))
                if self.verifier.validation_on:
                    self.log.info('Processing returns...')
                    self.verifier.subscribe_verify(
                        response, 'STREAM', self.namespace)
        self.result = self.verifier.end_subscription(self.errors)
        self.stop()


class GnmiSubscriptionOnce(GnmiSubscription):
    def __init__(self,
                 device=None,
                 payload: List[gnmi_pb2.SubscribeRequest] = None,
                 responses: List[gnmi_pb2.SubscribeResponse] = None,
                 ** request):
        super().__init__(device, **request)
        if responses is not None:
            self.responses = responses
        elif device is not None and payload is not None:
            self.responses = device.gnmi.service.Subscribe(
                self.iter_subscribe_request(payload, self.delay),
                metadata=self.metadata
            )

    @GnmiSubscription.cover_exceptions
    def run(self):
        """Check for inbound notifications."""
        self.log.info('Subscribe notification active')
        stop_receiver = False
        t = time.time()
        for response in self.responses:
            delta_time = time.time() - t
            # Subscribe response ends here
            if response.HasField('sync_response'):
                self.log.info('Subscribe sync_response')
                self.result = self.verifier.end_subscription(self.errors)
                self.log.info('Subscribe ONCE processed')
                self.stop()
                break

            elif self.transaction_time and delta_time > self.transaction_time:
                self.errors.append(self.TransactionTimeExceeded(
                    delta_time, self.transaction_time))

            if response.HasField('update') and not self.stopped():
                self.log.info(
                    "gNMI SUBSCRIBE Response\n" + "=" * 23 + "\n{}"
                        .format(response)
                )
                if self.verifier.validation_on:
                    self.log.info('Processing returns...')
                    self.verifier.subscribe_verify(
                        response, 'ONCE', self.namespace)

            if self.stopped():
                self.log.info("Notification stream stopped has been stopped")
                break

        self.result = self.verifier.end_subscription(self.errors)
        self.log.info('Subscribe ONCE processed')
        self.stop()


class GnmiSubscriptionPoll(GnmiSubscription):
    def __init__(self,
                 device=None,
                 payload: List[gnmi_pb2.SubscribeRequest] = None,
                 responses: List[gnmi_pb2.SubscribeResponse] = None,
                 **request):
        super().__init__(device, **request)
        if responses is not None:
            self.responses = responses
        elif device is not None and payload is not None:
            polls_number = self.stream_max // self.sample_poll

            for _ in range(polls_number):
                payload.append(GnmiMessageConstructor.get_subscribe_poll())
            self.responses = device.gnmi.service.Subscribe(
                self.iter_subscribe_request(
                    payload, sample_poll=self.sample_poll),
                timeout=self.stream_max,
                metadata=self.metadata
            )

    @GnmiSubscription.cover_exceptions
    def run(self):
        """Check for inbound notifications."""
        self.log.info('Subscribe notification active')
        t = time.time()
        for (i, response) in enumerate(self.responses):
            if (i == 0):
                delta_time = time.time() - t
            else:
                delta_time = time.time() - t - self.sample_poll
            if (self.transaction_time and t and delta_time > self.transaction_time):
                self.errors.append(self.TransactionTimeExceeded(
                    delta_time, self.transaction_time))
            if response.HasField('sync_response'):
                self.log.info('Subscribe sync_response')

            if response.HasField('update') and not self.stopped():
                self.log.info(
                    "gNMI SUBSCRIBE Response\n" + "=" * 23 + "\n{}"
                        .format(response)
                )
                if self.verifier.validation_on:
                    self.log.info('Processing returns...')
                    self.verifier.subscribe_verify(
                        response, 'POLL', self.namespace)
            t = time.time()
        self.result = self.verifier.end_subscription(self.errors)
        self.stop()
