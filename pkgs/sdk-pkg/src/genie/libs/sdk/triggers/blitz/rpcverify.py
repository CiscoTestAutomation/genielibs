#! /usr/bin/env python
import re
import logging
from six import string_types
from pyats.log.utils import banner
import dataclasses
from dataclasses import dataclass, field
from typing import Union, Callable, List, Tuple, Any, ClassVar
import operator as o
from copy import deepcopy

log = logging.getLogger(__name__)


def range_op(range: str, value: Any, datatype: str = '') -> bool:
    """Check if value is in range."""
    r1 = r2 = None
    if len(range.split(',')) == 2:
        rng = range.split(',')
        r1 = rng[0]
        r2 = rng[1]
    elif len(range.split()) == 2:
        rng = range.split()
        r1 = rng[0]
        r2 = rng[1]
    elif range.count('-') == 1:
        rng = range.split('-')
        r1 = rng[0]
        r2 = rng[1]
    elif '-' in range.split():
        rng = range.split()
        r1 = rng[0]
        r2 = rng[2]
    try:
        if datatype:
            if datatype.startswith('int') or \
                    datatype.startswith('uint'):
                r1 = int(r1)
                r2 = int(r2)
                if r2 < r1:
                    r1, r2 = (r2, r1)
                # change value to int type for subsequent compare operation
                value = int(value)
            else:
                r1 = float(r1)
                r2 = float(r2)
                if r2 < r1:
                    r1, r2 = (r2, r1)
                # change value to float type for subsequent compare operation
                value = float(value)
    except TypeError:
        raise OptFields.InvalidRangeType
    else:
        r1 = float(r1)
        r2 = float(r2)
        if r2 < r1:
            r1, r2 = (r2, r1)
        # change value to float type for subsequent compare operation
        value = float(value)
    if value >= r1 and value <= r2:
        return True
    return False


@dataclass
class OptFields:
    """Data class for opfields and metadata default value, edit operation."""
    name: str = ''
    value: Union[str, list] = ''
    xpath: str = ''
    op: Union[str, Callable] = '=='
    default: str = ''
    selected: bool = True
    id: str = ''
    datatype: str = ''
    sequence: int = 0
    default_xpath: str = ''
    nodetype: str = ''
    key: bool = False
    _operators: ClassVar[dict] = {
        '==': o.eq,
        '!=': o.ne,
        '>': o.gt,
        '>=': o.ge,
        '<': o.lt,
        '<=': o.le,
        'range': range_op,
        'any': lambda x, y: True,
        'deleted': 'deleted'
    }

    def __post_init__(self):
        if not isinstance(self.datatype, str):
            log.warning(f'Datatype must be a string got: {type(self.datatype).__name__}')
        elif 'decimal' in self.datatype:
            try:
                self.value = float(
                    self.value['digits']) / (10 ** self.value['precision'])
            except TypeError:
                self.value = float(self.value)

    class OperatorsException(Exception):
        pass

    class InvalidRangeType(OperatorsException):
        pass

    def __eq__(self, other):
        if self.op != self._operators['deleted']:
            super().__eq__(other)
        return self.xpath == other.xpath

OPTFIELD_ALLOWED_OPTIONS = [f.name for f in dataclasses.fields(OptFields)]


class OperationalFieldsNode:
    """Data class for opfields and metadata default value, edit operation."""

    def __init__(self, name, value, xpath, selected, operator, default_value, edit_op):
        """
        Args:
            name (str): Name of a node.
            value (str): Value of a node.
            xpath (str): Xpath to a node.
            selected (bool): Select this node to be used in processing operational state.
            op (str): Logifieldselfcal operator used to compare state.
        Metadata:
            default_value (bool): Default node value used.
            edit_op (str): Edit operation used.
        """
        self.opfields = OptFields(
            name=name,
            value=value,
            xpath=xpath,
            selected=selected,
            op=operator
        )
        self.default_value = default_value
        self.edit_op = edit_op


@dataclass
class DecodedField:
    """Dataclass to hold decoded field data."""
    value: any
    xpath: str

    def __eq__(self, other):
        if isinstance(other, DecodedField):
            return self.value == other.value and self.xpath == other.xpath
        elif isinstance(other, tuple):
            return self.value == other[0] and self.xpath == other[1]


@dataclass
class DeletedPath:
    """Dataclass to hold single deleted path."""
    xpath: str
    keys: List[DecodedField] = field(default_factory=list)

    def __str__(self) -> str:
        return self.xpath


@dataclass
class DecodedResponse:
    """Dataclass to hold decoded response data."""
    json_dicts: List[dict] = field(default_factory=list)
    updates: List[DecodedField] = field(default_factory=list)
    deletes: List[DeletedPath] = field(default_factory=list)
    errors: List[any] = field(default_factory=list)


class EvalDatatype:
    """Evaluate opfields that contain "datatype" definition."""

    integer_limits = {
        'int8': (-128, 127),
        'uint8': (0, 255),
        'int16': (-32768, 32767),
        'uint16': (0, 65535),
        'int32': (-2147483648, 2147483647),
        'uint32': (0, 4294967295),
        'int64': (-9223372036854775808, 9223372036854775807),
        'uint64': (0, 18446744073709551615)
    }

    def __init__(self, value: Any, field: OptFields):
        """Usage: EvalDatatype(opfield).evalute()"""
        self.min_max_failed = False
        self.bool_failed = False
        self.value = value
        self.field = field

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        if isinstance(val, string_types):
            try:
                self._value = int(val)
            except ValueError:
                try:
                    self._value = float(val)
                except ValueError:
                    self._value = val
        else:
            self._value = val

    @property
    def field(self):
        return self._field

    @field.setter
    def field(self, field: OptFields):
        self._field = field
        datatype = field.datatype
        self.datatype = datatype
        if datatype.startswith('int') or datatype.startswith('uint'):
            self.fval = int(field.value)
            if datatype not in self.integer_limits:
                raise TypeError('Invalid datatype')
            self.min, self.max = self.integer_limits[datatype]
            if self.value < self.min or self.value > self.max:
                self.min_max_failed = True
        elif datatype in ['float', 'double', 'decimal64']:
            self.fval = float(field.value)
            self.min, self.max = self.integer_limits['int64']
            if self.value < self.min or self.value > self.max:
                self.min_max_failed = True
        elif datatype == 'boolean':
            if field.op not in ['==', '!=', 'any']:
                self.bool_failed = True
            if self.value in [1, '1', 'true']:
                self.value = 'true'
            elif self.value in [0, '0', 'false']:
                self.value = 'false'
            else:
                self.bool_failed = True
            if str(field.value).lower() in ['1', 'true']:
                self.fval = 'true'
            elif str(field.value).lower() in ['0', 'false']:
                self.fval = 'false'
            else:
                self.bool_failed = True
        elif datatype == 'identityref':
            # TODO: basetype is string so might not get identityref.
            # strip prefix from values
            val = field.value
            self.fval = val[val.find(':') + 1:]
            val = self.value
            self.value = val[val.find(':') + 1:]
        else:
            self.fval = field.value
        self.op = OptFields._operators[field.op]
        self.fname = field.name if field.name else 'unknown field'

    def evaluate(self):
        if not self.datatype:
            log.error('Datatype not defined for value check of {0}'.format(
                self.fname
            ))
            return False
        if self.min_max_failed:
            return False
        if self.bool_failed:
            return False
        if self.datatype == 'pattern':
            self.value = re.findall(self.fval, self.value)
            if self.value:
                self.fval = self.value
        result = self.op(self.value, self.fval)
        if isinstance(self.value, string_types) and not result:
            if self.value != self.fval:
                # Check if values have prefix
                if self.value.count(':') == 1 and \
                        self.fval.count(':') == 1:
                    # Strip the prefix from values
                    self.value = self.value.split(':')[1]
                    self.fval = self.fval.split(':')[1]
            return self.op(self.value, self.fval)
        return result


class RpcVerify():
    """Verification of NETCONF rpc and rpc-reply messages.

    In this example, we will send an rpc-reply that has tags we expected
    would be deleted from the device's YANG datastore but they were not.

    >>> response = \
        '''<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"
    ...      message-id="urn:uuid:d177b38c-bbc7-440f-be0d-487b2e3c3861">
    ...     <data>
    ...         <System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
    ...             <lldp-items>
    ...                 <name>genericstring</name>
    ...             </lldp-items>
    ...         </System>
    ...     </data>
    ... </rpc-reply>
    ... '''
    >>> expected = \
        '''<System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
    ... -  <lldp-items>
    ... -    <name>genericstring</name>
    ... -  </lldp-items>
    ... </System>
    ... '''
    >>>
    >>> rpcv = RpcVerify(rpc_reply=response, rpc_verify=expected, log=log)
    >>> rpcv.capabilities = [':with-defaults:basic-mode=report-all']
    >>> result = rpcv.parse_rpc_expected(rpcv.rpc_reply, rpcv.rpc_verify)
    >>> print(result)
    False
    """

    NETCONF_NAMESPACE = "urn:ietf:params:xml:ns:netconf:base:1.0"

    # Pattern to detect keys in an xpath
    RE_FIND_KEYS = re.compile(r'\[.*?\]')
    RE_FIND_PREFIXES = re.compile(r'/[-a-zA-Z0-9]+:')

    # pattern to detect prefix in the key name, prefix is optional
    # e.g.
    # /native/route-map[name="set-community-list"]/route-map-seq[ios-route-map:ordering-seq="10"]
    # becomes (note `name` does not have a prefix, but `ordering-seq` has):
    # /native/route-map[name="set-community-list"]/route-map-seq[ordering-seq="10"]
    RE_FIND_KEY_PREFIX = r'\[(?P<prefix>[-\w]+:)?(?P<name>[-\w]+)'

    # Pattern to match value and ignore leading and trailing whitespace
    # e.g. for whitespace:
    # /native/router/bgp[id="6"]/neighbor[id=" 100.5.6.6 "]/remote-as
    # becomes
    # /native/router/bgp[id="6"]/neighbor[id="100.5.6.6"]/remote-as
    RE_FIND_QUOTED_VALUE = r'[\'"]\s*(?P<value>.*?)\s*[\'"]'

    def __init__(self, log=log, rpc_reply=None,
                 rpc_verify=None, capabilities=[]):
        """Instantiate with optional reply and verify.

        User has the option to instantiate a series of RpcVerify instances
        with each containing a different set of reply/verify messages to
        execute depending on needs.  Each instance can use a different
        log to record actions.

        Args:
          log (logging.Logger): Logs internal operations
                                (default, log from module).
          rpc_reply (str): NETCONF rpc-reply (default None).
          rpc_verify (str): NETCONF rpc-reply to compare with rpc_reply
                            (default None).
          capabilities (list): List of NETCONF capabilities from device
                               (default, empty list)
        """
        try:
            import lxml.etree as et
            self.et = et
        except ImportError as e:
            log.error('Make sure you have lxml installed in your virtual env')
            raise (e)
        self.rpc_reply = rpc_reply
        self.rpc_verify = rpc_verify
        self.capabilities = capabilities

    @property
    def with_defaults(self):
        """List of NETCONF "with-defaults" device capabilities.

        Used to apply RFC 6243 logic to determine "get-config" validity.
        """
        return self._with_defaults

    @property
    def datastore(self):
        """Device datastore capabilities."""
        return self._datastore

    @property
    def capabilities(self):
        """List of device NETCONF capabilities."""
        return self._capabilities

    @capabilities.setter
    def capabilities(self, caps=[]):
        self._capabilities = caps
        self._with_defaults = []
        self._datastore = []
        for cap in caps:
            if ':yang-library:1.1' in cap:
                # TODO: figure out how to get datastores for nmda
                pass
            if ':netconf:capability:' not in cap:
                continue
            if ':with-defaults:' in cap:
                self._with_defaults = cap[cap.find('=') + 1:].split(
                    '&also-supported='
                )
                log.info('WITH DEFAULTS SUPPORTED:{0}'.format(
                    self._with_defaults
                ))
            elif ':candidate:' in cap:
                self._datastore.append('candidate')
            elif ':writable-running' in cap:
                self._datastore.append('running')

    def _process_values(self, reply, expect):
        """Determine the variable state of the tag values.

        Reply tags and expected tags are evaluated to determine their state.

        * no_values
          * Both reply and expected tags have no values assigned
        * match
          * Reply value matches expected value

        Returns:
          dict:
            * State (no_values, match)
            * reply value prefixes (if any)
            * expect value prefixes (if any)
            * reply value (if any)
            * expect value (if any)
        """
        result = {}
        expect_val = reply_val = None

        if self.et.iselement(expect) and expect.text and expect.text.strip():
            expect_val = expect.text.strip()
            result['expect_val'] = expect_val

        if self.et.iselement(reply) and reply.text and reply.text.strip():
            reply_val = reply.text.strip()
            result['reply_val'] = reply_val

        if not reply_val and not expect_val:
            result['no_values'] = True
        elif reply_val and expect_val and reply_val != expect_val:
            # check if values have prefixes and are they correct?
            if reply_val.count(':') == 1 and expect_val.count(':') == 1:
                reply_pfx = reply_val.split(':')[0]
                if reply_pfx in reply.nsmap.keys():
                    result['reply_val'] = reply_val.split(':')[1]
                    result['reply_prefix'] = reply_pfx
                    result['expect_prefix'] = expect_val.split(':')[0]
                    result['expect_val'] = expect_val.split(':')[1]
                    # check values without their prefixes
                    if result['reply_val'] == result['expect_val']:
                        result['match'] = True
        else:
            result['match'] = True

        return result

    def _get_resp_xml(self, resp):
        """Remove XML encoding tag if it is there.

        Args:
          resp (list) or (str) or (bytes): rpc-reply returned from ncclient.
        Returns:
          str: rpc-reply in string form.
        """
        if isinstance(resp, list):
            if isinstance(resp[0], tuple):
                op, resp_xml = resp[0]
        elif isinstance(resp, (str, bytes)):
            resp_xml = str(resp)
        else:
            return ''

        if resp_xml.strip().startswith('<?xml'):
            return resp_xml[resp_xml.find('>') + 1:].strip()

        return resp_xml

    def process_expect_reply(self, response, expected):
        """Parse expected response and actual response before comparing.

        * A NETCONF rpc-reply tag is required for all responses so add
          it to expected XML if it is missing for consistency.
        * A NETCONF data tag is not required but if the response has it,
          add it to expected XML for consistency.
        * If a user has added indicators in the expected XML that identifies
          tags expected NOT to be in the response, check the response to make
          sure they do not exist.
        * Check that all tags are in the expected order.

        Args:
          response (list): List of reply lxml.etree.Elements.
          expected (list): List of expected lxml.etree.Elements.
        Returns:
          tuple: bool - True if successfully processed objects.
                 list of expected lxml.etree.Elements.
                 list of reply lxml.etree.Elements.
        """
        result = True
        should_be_missing = ''
        unexpected = []
        expect = []
        # user put "-" (minus) in front of tags they expect to be missing
        for elem, xpath in expected:
            # minus was converted to "expected" attribute earlier
            if elem.attrib.get('expected') == 'false':
                unexpected.append((elem, xpath))
            else:
                expect.append((elem, xpath))
        expected = expect

        for reply, xpath in response:
            for unexpect, unexpect_xpath in unexpected:
                if reply.tag == unexpect.tag and xpath == unexpect_xpath:
                    value_state = self._process_values(reply, unexpect)
                    if 'explicit' in self.with_defaults:
                        # Only tags set by client sould be in reply
                        should_be_missing += reply.tag + ' '
                        should_be_missing += value_state.get('reply_val', '')
                        should_be_missing += '\n'
                        result = False
                        break
                    elif 'report-all' in self.with_defaults:
                        if 'match' not in value_state:
                            continue
                        # TODO: RFC6243 - if value is default it should match
                        should_be_missing += reply.tag + ' '
                        should_be_missing += value_state.get('reply_val', '')
                        should_be_missing += '\n'
                        result = False
                        break
                    elif 'match' in value_state or 'no_values' in value_state:
                        should_be_missing += reply.tag
                        should_be_missing += '\n'
                        result = False

        if should_be_missing:
            log.error(
                "{0} Following tags should be missing:\n\n{1}"
                .format('OPERATIONAL-VERIFY FAILED:', should_be_missing)
            )

        return (result, expected, response)

    @classmethod
    def check_opfield(self, value: Any, field: OptFields):
        """Reply value is logically evaluated according to user expectations.

        User has the flexibility to apply logic to a reply's value.  If the
        logic does not return "True", the test failed.

        Logicial operators for successful value test;

        * "==" - Reply value must be equal to expect value.
        * "!=" - Reply value must not be equal to expect value.
        * ">=" - Reply value must be equal to or greater than expect value.
        * "<=" - Reply value must be equal to or less than expect value.
        * ">"  - Reply value must be greater than expect value.
        * "<"  - Reply value must be less than expect value.
        * "range" - Reply value must be withn a value range.
        * "any" - Verify existence and datatype regardless of value.

        Args:
          value (str): The XML tag value from replay
          field (dict):
            * Name of tag
            * Sequence number signifying where value will appear in reply
            * Logical operation to apply to replay value
            * Value to use when applying logic to replay value
        Returns:
          Tuple: bool: Pass | Fail, str: log message
        """
        log_msg = 'None'

        if field.default_xpath:
            xpath = field.default_xpath
        else:
            xpath = field.xpath
        try:
            # set this to operation in case we get an exception
            op_name, op_method = field.op, OptFields._operators[field.op]
            eval_text = op_name
            datatype = field.datatype

            log.debug(f'Checking xpath {xpath} value "{value}" {op_name} "{field.value}"')

            if op_name == 'range':
                try:
                    if not datatype:
                        value = float(value)
                except ValueError:
                    log_msg = 'OPERATION VALUE {0}: {1} invalid for range {2}{3}'.format(
                        xpath,
                        str(value),
                        str(field.value),
                        ' FAILED'
                    )
                    return (False, log_msg)

                try:
                    result = op_method(field.value, value, datatype)
                except OptFields.InvalidRangeType:
                    log_msg = 'OPERATION VALUE {0}: range datatype "{1}" {2}{3}'.format(
                        xpath,
                        datatype,
                        str(field.value),
                        ' FAILED'
                    )
                    return (False, log_msg)
                if result:
                    log_msg = 'OPERATION VALUE {0}: {1} in range {2} SUCCESS'.format(
                        xpath, str(value), str(field.value)
                    )
                else:
                    log_msg = 'OPERATION VALUE {0}: {1} out of range {2}{3}'.format(
                        xpath,
                        str(value),
                        str(field.value),
                        ' FAILED'
                    )
                    return (False, log_msg)
            else:
                if not datatype:
                    value = str(value)
                    if value.lower() in ['true', 'false']:
                        value = value.lower()
                    fval = str(field.value)
                    if fval.lower() in ['true', 'false']:
                        fval = fval.lower()

                    if (value.isnumeric() and not fval.isnumeric()) or \
                            (fval.isnumeric() and not value.isnumeric()):
                        # the eval_text will show the issue
                        eval_text = '"' + value + '" ' + op_name
                        eval_text += ' "' + fval + '"'
                        log_msg = 'OPERATION VALUE {0}: {1} FAILED'.format(
                            xpath, eval_text
                        )
                        return (False, log_msg)
                    if value.isnumeric():
                        result = op_method(value, fval)
                        eval_text = value + ' ' + op_name + ' '
                        eval_text += fval
                    else:
                        try:
                            # See if we are dealing with floats
                            v1 = float(value)
                            v2 = float(fval)
                            eval_text = str(v1) + ' ' + op_name + ' '
                            eval_text += str(v2)
                            result = op_method(v1, v2)
                        except (TypeError, ValueError):
                            if value.startswith('"') and value.endswith('"'):
                                eval_text = value + ' ' + op_name
                            else:
                                eval_text = '"' + value + '" ' + op_name
                            if fval.startswith('"') and fval.endswith('"'):
                                eval_text += ' ' + fval
                            else:
                                eval_text += ' "' + fval + '"'
                            result = op_method(value, fval)
                    if result:
                        log_msg = 'OPERATION VALUE {0}: {1} SUCCESS'.format(
                            xpath, eval_text
                        )
                    # check if values have prefixes
                    elif value.count(':') == 1 and fval.count(':') == 1:
                        value = value.split(':')[1]
                        fval = fval.split(':')[1]
                        eval_text = f'"{value}" {op_name} "{fval}"'
                        if op_method(value, fval):
                            log_msg = 'OPERATION VALUE {0}: {1} SUCCESS'.format(
                                xpath, eval_text
                            )
                        else:
                            log_msg = 'OPERATION VALUE {0}: {1} FAILED'.format(
                                xpath, eval_text
                            )
                            return (False, log_msg)
                    else:
                        log_msg = 'OPERATION VALUE {0}: {1} FAILED'.format(
                            xpath, eval_text
                        )
                        return (False, log_msg)
                else:
                    log_tmp = 'OPERATION VALUE {0}: {1} {2} {3} {4}'
                    failed_type = 'FAILED'
                    evaldt = EvalDatatype(value, field)
                    if evaldt.evaluate():
                        log_msg = log_tmp.format(
                            xpath, str(value),
                            op_name, str(field.value),
                            'SUCCESS'
                        )
                    else:
                        if evaldt.min_max_failed:
                            failed_type = '"{0}" MIN-MAX FAILED'.format(
                                evaldt.datatype
                            )
                        elif evaldt.bool_failed:
                            failed_type = 'BOOLEAN FAILED'
                        log_msg = log_tmp.format(
                            xpath, str(value),
                            op_name, str(field.value),
                            failed_type
                        )
                        return (False, log_msg)

        except Exception as e:
            log_msg = 'OPERATION VALUE {0}: {1} {2} FAILED\n{3}'.format(
                xpath, str(value), eval_text, str(e)
            )
            return (False, log_msg)

        return (True, log_msg)

    def process_one_operational_state(self,
                                      response: List[Tuple[Any, str]],
                                      field: OptFields,
                                      key=False,
                                      sequence=None):
        """Check if a response contains an expected result.

        Args:
          response (list): List of tuples containing
                           NETCONF - lxml.Element, xpath.
                           GNMI - value, xpath
          field (dict): Expected field in result includes
                        datatype, nodetype, and value.
        Returns:
          bool: True if successful.
        """
        if field.default_xpath:
            xpath = field.default_xpath
        else:
            xpath = field.xpath

        log_msg = 'ERROR: "{0} value: {1}" Not found.'.format(
            xpath, str(field.value))
        datatype = ''
        result = False

        for resp in response:
            datatype = field.datatype
            if datatype == 'ascii':
                if field.op != "==":
                    log.error(
                        f"ASCII datatype can be used only with '==' operator not with {field['op']}")
                    break
                return resp.get("value") == field.value
            else:
                for reply, reply_xpath in resp:
                    if self.et.iselement(reply):
                        # NETCONF response
                        value_state = self._process_values(reply, '')
                        value = value_state.get('reply_val', 'empty')
                        name = self.et.QName(reply).localname
                    else:
                        # GNMI response
                        if reply is False:
                            value = reply
                        else:
                            if reply == '':
                                value = 'empty'
                            else:
                                value = reply
                        name = reply_xpath[reply_xpath.rfind('/') + 1:]
                    if field.xpath == reply_xpath and \
                            name == field.name:

                        if datatype == 'empty':
                            field.value = 'empty'

                        result, log_msg = self.check_opfield(value, field)

                        # new_response contains all responses from the first match,
                        # hence, not necessarily, first value will be the target value
                        # any value in the new_response can be the target value
                        # <List1> ---->  Response is trimmed from here
                        #    <Key>K1</Key>
                        #    <Prop>v1<Prop>
                        #    <Key>K2</Key>
                        #    <Prop>v2<Prop>
                        #    <Key>K3</Key>
                        #    <Prop>v3<Prop>
                        # </List1>
                        if sequence and not result:
                            log.error(log_msg)
                            return result
                        if result:
                            if not datatype:
                                log.warning(
                                    "{0} has no datatype; default to string".format(
                                        xpath
                                    )
                                )
                            log.info(log_msg)
                            return True

        if key:
            log.info('Parent list key "{0} == {1}" not required.'.format(
                field.name, field.value
            ))
            return True

        if not datatype:
            log.warning(
                "{0} has no datatype; default to string".format(
                    xpath
                )
            )
        # Dont log non matched returns for on_change
        log.error(log_msg)
        return result

    def pre_process_keys(self,
                         returns: List[OptFields],
                         response: List[Tuple[Any, str]]) -> List[Tuple[Any, str]]:
        """Check for lists with multiple keys in returns xpaths.
            and store the order of keys.

        Args:
            returns (list): List of fields in returns containing
                            list keys in xpath
            response (list): List of tuples containing
                            NETCONF - lxml.Element, xpath.
                            GNMI - value, xpath
        Implementation:
            Eg: We have a returns field['xpath']:
            field['xpath'] = /Sys/Cont1/List1[key1=val1]/Cont2/List2[key2=val2][key3=val3]
            Since List2 has multiple keys under it we store the order
            that key2 comes first and key3 comes second,
            so that we can compare it and correct the order in response.

            Store in key_orders = [
                                    [
                                      (val2,/Sys/Cont1/List1/Cont2/List2/key2),
                                      (val3,/Sys/Cont1/List1/Cont2/List2/key3)
                                    ]
                                  ]
        """
        key_orders = []
        for field in returns:
            xpath = field.xpath
            key_order = []
            prev_start_index = -1
            prev_end_index = -1
            for match in re.finditer(self.RE_FIND_KEYS, xpath):
                key = match.group()
                start_index = match.start()
                end_index = match.end()
                # Extract the key name
                # Eg: '[Key1=Val1]'
                # key_name = Key1
                key_name = key.split('=')[0].strip('[')
                # Extract the key value
                # Eg: '[Key1=Val1]'
                # key_val = Val1
                key_val = key.split('=')[1].strip(']')
                key_val = re.sub('"', '', key_val)
                # Extract the key path from xpath
                # Eg: /Sys/Cont/Lis[Key1=Val1]
                # key_path = /Sys/Cont/Lis/Key1
                key_path = xpath.split(key)[0] + '/' + key_name
                key_path = re.sub(self.RE_FIND_KEYS, '', key_path)

                # We have the start and end index of keys found
                # to detect if we have multiple keys or not
                # Eg. Sys/List[k1=v1][k2=v2]
                # End index of '[k1=v1]' == Start index of '[k2=v2]'
                # If yes then we have detected a multiple list
                # Store them as (key_value, key_path)
                if start_index == prev_end_index:
                    if (prev_key_val, prev_key_path) not in key_order:
                        key_order.append((prev_key_val, prev_key_path))
                    key_order.append((key_val, key_path))
                else:
                    # If multiple keys are found then only store it
                    if len(key_order) > 1:
                        key_orders.append(key_order)
                    key_order = []

                # Keep track of previous indexes, key_val, key_path.
                # to match them with current
                prev_start_index = start_index
                prev_end_index = end_index
                prev_key_path = key_path
                prev_key_val = key_val

            # If multiple keys are found then only store it
            if len(key_order) > 1:
                key_orders.append(key_order)

        # After storing all the key_orders, we send these key orders
        # to find_groups_in_response() function which will find all
        # these key orders in response even when they are not in correct order
        if key_orders:
            self.find_groups_in_response(key_orders, response)
        return response

    def pre_process_returns(self, returns: List[OptFields]) -> List[OptFields]:
        """Check for keys embedded in xpaths and extract them into separate fields.
        Args:
            returns (list): List of fields in returns containing
                            list keys in xpath as well.
            Eg:
            returns:
                [
                    {
                        'nodetype': 'leaf',
                        'value': 'test03',
                        'op': '==',
                        'selected': 'True',
                        'name': 'rtMap',
                        'xpath': '/System/igmp-items/inst-items/dom-items/Dom-list[name="default"]/rtMap
                    }
                ]

        Returns:
            new_returns (list): List of dict with possible new fields containing xpath/key pairs.
            Eg:
            new_returns:
                [
                    {
                        'sequence' : 1,
                        'nodetype': 'leaf',
                        'value': 'default',
                        'op': '==',
                        'key': True,
                        'selected': 'True',
                        'name': 'name',
                        'xpath': '/System/igmp-items/inst-items/dom-items/Dom-list/name
                    },
                    {
                        'sequence' : 1,
                        'nodetype': 'leaf',
                        'value': 'test03',
                        'op': '==',
                        'selected': 'True',
                        'name': 'rtMap',
                        'xpath': '/System/igmp-items/inst-items/dom-items/Dom-list/rtMap
                    }
                ]
        """
        new_returns = []
        sequence_no = 1
        for field in returns:
            xpath = field.xpath
            for key in self.RE_FIND_KEYS.findall(xpath):
                # Extract the key name
                # Eg: '[Key1=Val1]'
                # key_name = Key1
                key_name = key.split('=')[0].strip('[')
                # Extract the key value
                # Eg: '[Key1=Val1]'
                # key_val = Val1
                key_val = key.split('=')[1].strip(']')
                key_val = re.sub('"', '', key_val)
                # Extract the key path from xpath
                # Eg: /Sys/Cont/Lis[Key1=Val1]
                # key_path = /Sys/Cont/Lis/Key1
                key_path = xpath.split(key)[0] + '/' + key_name
                key_path = re.sub(self.RE_FIND_KEYS, '', key_path)

                # Create returns field for the key found
                new_returns.append(OptFields(name=key_name,
                                             xpath=key_path,
                                             value=key_val,
                                             op='==',
                                             selected=True,
                                             key=True,
                                             sequence=sequence_no,
                                             nodetype='leaf'))
            field.sequence = sequence_no
            field.default_xpath = field.xpath
            field.xpath = re.sub(self.RE_FIND_KEYS, '', field.xpath)
            new_returns.append(field)
            sequence_no += 1
        return new_returns

    def find_groups_in_response(self, key_orders, response):
        """Find the all the key_orders groups in response/opfields
        Args:
            key_orders (list): List of list of tuples containing (key_value, key_path)
            Paths:
                1. /cont/lis[k=v]/cont/lis[key1=val1][key2=val2]
                2. /cont/lis[k=v]/cont/lis[key3=val3][key4=val4]
            Eg key_orders:
                [
                    [(val1, /cont/lis/cont/lis/key1), (val2, /cont/lis/cont/lis/key2)], # For path 1
                    [(val3, /cont/lis/cont/lis/key3), (val4, /cont/lis/cont/lis/key4)]  # For path 2
                ]

        Implementation:
            Eg response:
            [
                (some_val,some_path),(some_val,some_path),
                # Below section of response is Group 1 of key_orders.
                # Order of keys may be different as shown in this example. (key1 comes second and key2 comes first)
                (val2, /cont/lis/cont/lis/key2), (val1, /cont/lis/cont/lis/key1)
                # Below section of response is Group 1 of key_orders.
                # Order of keys may be different as shown in this example. (key3 comes second and key4 comes first)
                (val4, /cont/lis/cont/lis/key4), (val3, /cont/lis/cont/lis/key3)
            ]

        # This function finds all the groups of key_orders in response even when they are not in correct order.
        # Group is each key order of N multiple keys.
        # Eg group1 = [(val1, key1_path),(val2, key2_path)], group2 = [(val3, key3_path),(val4 key4_path)]
        # Eg: For group 1 in response key1 comes second and key2 comes first
        # We found key1 and key2 at Index [2,1] in response
        # This index will be sent to reorder_keys_in_opfield() function to correct it as [1,2]
        """
        response = response[0]
        # Iterate over all the groups in key_orders
        for key_order in key_orders:
            values = []
            # Store the key_values of each key_path.
            for field in key_order:
                values.append(field[0])
            # We store the first key path
            # Eg: key1 path = /cont/lis/cont/lis/key1
            #     key2 path = /cont/lis/cont/lis/key2
            # Notice that we have a common list path between both
            # Store first_key_path = /cont/lis/cont/lis/key1
            first_key_path = key_order[0][1]
            # Extract the list of first_key_path
            # list_in_key = /cont/lis/cont/lis
            # Now '/cont/lis/cont/lis' this list path will be
            # common for all keys in the group
            # This will help us identify all the list keys in response
            # to check whether they are together or not.
            list_in_key = first_key_path[:first_key_path.rfind('/')]
            key_len = len(key_order)
            count = 0
            key_indexes = []
            for index, resp in enumerate(response):
                # For every response, we trim the path upto last '/'
                # To match it with out key list.
                # Eg: resp = (value, Sys/cont/list/key)
                # trim path to 'Sys/cont/list' and match it with
                # our target list '/cont/lis/cont/lis'
                list_in_response = resp[1][:resp[1].rfind('/')]
                # If list is matched, check whether the response value is in
                # our values[] list (has all the key_values of the group)
                # This makes sure that the key found in response is in our current group.
                # For every key found increase the count and check with key_len
                # key_len is total number of keys for each group.
                if (list_in_key == list_in_response and resp[0] in values):
                    count += 1
                    key_indexes.append(index)
                else:
                    count = 0
                    key_indexes = []

                # all keys are found and we have store the indexes
                if (count == key_len):
                    # Send those indexes for reordering
                    self.reorder_keys_in_opfield(
                        response, key_indexes, key_order)
                    key_indexes = []
                    count = 0

    def reorder_keys_in_opfield(self, response, key_indexes, key_order):
        """Correct the key order in the response
        Args:
            key_indexes (list): [2,1] (Key Indexes found in response)
            key_order: [(val1, cont/lis/cont/lis/key1), (val2, cont/lis/cont/lis/key2)]

        Implementation:
            Eg response:
            [
                (some_val,some_path),(some_val,some_path),
                # Below section of response is Group 1 of key_orders.
                # But order of keys are different (key1 comes second and key2 comes first)
                (val2, cont/lis/cont/lis/key2), (val1, cont/lis/cont/lis/key1),
                (some_val,some_path),(some_val,some_path)
            ]

                Group 1 in response = (val2, cont/lis/cont/lis/key2), (val1, cont/lis/cont/lis/key1)
                key_indexes = [2,1]

                Reorder it:
                    We have key_order: [(val1, cont/lis/cont/lis/key1), (val2, cont/lis/cont/lis/key2)]
                    and key_indexes = [2,1]

                    Store response[2] = key_order[0]
                    Store response[1] = key_order[1]

        Return: Response with correct key_order
                response =
                    [
                        (some_val,some_path),(some_val,some_path),
                        (val1, cont/lis/cont/lis/key1), (val2, cont/lis/cont/lis/key2),
                        (some_val,some_path),(some_val,some_path)
                    ]

        """
        index = key_indexes[0]
        for field in key_order:
            # Substituting fields(key_val,key_path) from key_order to response
            # will ultimately fix the order in response
            # as key_order fields has the correct order already
            response[index] = field
            index += 1

    def trim_response(self,
                      response: List[Tuple[Any, str]],
                      parent_key_indexes: dict,
                      field: OptFields):
        """Trims the response for specific list entry

        Args:
            response (list): List of tuples containing
                           NETCONF - lxml.Element, xpath.
                           GNMI - value, xpath
            Eg:
                response:
                    [
                        (myContainer/myList1/key, k1),
                        (myContainer/myList1/Val, v1),
                        (myContainer/myList2/key, k2), --> Parent Index
                        (myContainer/myList2/Val, v2), --> Property to validate
                        (myContainer/myList2/key, k3),
                        (myContainer/myList2/Val, v3)
                    ]

        Returns:
            new_response: trimmed response for specific list entry.
            Eg:
                response:
                    [
                        (myContainer/myList1/key, k2),
                        (myContainer/myList1/Val, v2),
                        (myContainer/myList2/key, k3),
                        (myContainer/myList2/Val, v3)
                    ]
        """
        parent_dict = self.get_parent_dict(parent_key_indexes, field.xpath)
        parent_key_index = list(parent_dict.values())[0][0]

        # Trim the response for specific list entry
        new_response = [
            response[0][
                parent_key_index:
                ]
            ]

        return new_response, parent_key_index

    def process_sequencial_operational_state(self,
                                             response: List[Tuple[Any, str]],
                                             returns: List[OptFields],
                                             key=False):
        """Given multiple list entries, pick the specific entry required and validate.

        response:
                [
                    (myContainer/myList1/key, Key1),
                    (myContainer/myList1/Val, Val1),
                    (myContainer/myList2/key, Key2),
                    (myContainer/myList2/Val, Val2)
                ]

        returns:
            1. container/list/key=key1 (key: True)
            2. container/list/value (key: False) -> validate value for key 1
            3. container/list/key=key2 (key: True)
            4. container/list/value (key: False) -> validate value for key 2

        Implementation:
            For key fields: Find the parent key index and cut the response from that point.
                            Store the index of current key field.
            For leaf fields: Find parent key index and cut the response from that point.
            Start the validation.

        Args:
            response (list): List of tuples containing
                            NETCONF - lxml.Element, xpath.
                            GNMI - value, xpath
            opfields (list): List of dict representing opfields.

        Returns:
            bool: True if successful.
        """
        sequence = False
        results = []
        index = 0
        parent_key_indexes = {}
        sequence_broke_no = -1
        sequence_no = 0
        prev_seq_no = 0
        for field in returns:
            isKey = False
            key_found = False
            index = 0
            sequence_no = field.sequence
            if field.default_xpath:
                xpath = field.default_xpath
            else:
                xpath = field.xpath
            # Determine if current field is a key or not
            if field.key:
                isKey = True
            # Refresh the parent_key_indexes when new sequence starts
            if not sequence_no == prev_seq_no:
                parent_key_indexes = {}
            # Check if sequence is running or broken
            # If broken then skip all the values in that sequence
            # by logging Not Found.
            if sequence_no == sequence_broke_no:
                log_msg = 'ERROR: "{0} value: {1}" Not found.'.format(
                    xpath, str(field.value))
                log.error(log_msg)
                results.append(False)
                continue
            else:
                sequence_broke_no = 0
            # Get the new response by trimming the actual response
            # to just the list we are looking for
            new_response, parent_key_index = self.trim_response(
                response, parent_key_indexes, field)
            # Start loop from the new_response
            for resp in new_response:
                for reply, reply_xpath in resp:
                    # If it's a leaf value, then
                    # the response is already trimmed
                    # based on previous key field, so
                    # directly jump to validation
                    if not isKey:
                        break
                    index += 1
                    if self.et.iselement(reply):
                        # NETCONF response
                        value_state = self._process_values(reply, '')
                        value = value_state.get('reply_val', 'empty')
                        name = self.et.QName(reply).localname
                    else:
                        # GNMI response
                        if reply is False:
                            value = reply
                        else:
                            if reply == '':
                                value = 'empty'
                            else:
                                value = reply
                        name = reply_xpath[reply_xpath.rfind('/') + 1:]

                    if field.xpath == reply_xpath and \
                            name == field.name:
                        if isKey:
                            result, log_msg = self.check_opfield(value, field)
                            if result:
                                # Trim the new response from the index where
                                # current key is found
                                key_found = True
                                next_index = self.find_next_index(
                                    resp, index, field.xpath, field.value)
                                new_response = [
                                    resp[
                                        index-1:next_index
                                    ]
                                ]
                                # Store current key index
                                parent_key_indexes[field.xpath] = [
                                    parent_key_index + index, field.value]
                                break

                # If a key-value is not found in the entire response
                # then the sequence is broken
                if isKey and not key_found:
                    log_msg = 'ERROR: "{0} value: {1}" Not found.'.format(
                        xpath, str(field.value))
                    results.append(False)
                    log.error(log_msg)
                    sequence_broke_no = sequence_no
                else:
                    if not isKey:
                        # Validation of leaf with the trimmed response
                        sel = field.selected
                        if sel is False or str(sel).lower() == 'false':
                            continue
                        if not self.process_one_operational_state(new_response, field, key, sequence):
                            result = False
                            results.append(result)
            prev_seq_no = sequence_no

        if False in results:
            return False
        else:
            return True

    def process_operational_state(self,
                                  response: List[Tuple[Any, str]],
                                  returns: List[OptFields],
                                  key: bool = False,
                                  sequence: Any = None) -> bool:
        """Test NETCONF or GNMI operational state response.

        Args:
          response (list): List of tuples containing
                           NETCONF - lxml.Element, xpath.
                           GNMI - value, xpath
          opfields (list): List of dict representing opfields.
        Returns:
          bool: True if successful.
        """
        result = True

        if not returns:
            log.error(
                banner("OPERATIONAL STATE FAILED: No opfields to compare")
            )
            return False
        if isinstance(returns[0], dict):
            returns = [OptFields(**opfield) for opfield in returns]
        if not response:
            log.error(
                banner("OPERATIONAL STATE FAILED: Expected data")
            )
            return False

        if isinstance(response[0], tuple):
            # yang.connector only returned one list of fields
            response = [response]

        list_found = self.check_list_in_returns(returns)
        new_returns = []
        if list_found:
            # Check for multiple keys and correct the order in response
            new_response = self.pre_process_keys(returns, response)
            # Update returns for list keys
            new_returns = self.pre_process_returns(returns)
            sequence = True

        # To process the operational state in a sequence
        if sequence:
            result = self.process_sequencial_operational_state(
                new_response, new_returns, key)
        else:
            returns = self.process_returns(returns)
            for r_field in returns:
                sel = r_field.selected
                if sel is False or str(sel).lower() == 'false':
                    continue
                if not self.process_one_operational_state(response, r_field, key):
                    result = False
        return result

    def process_returns(self, returns: List[OptFields]):
        """Process returns with list values"""
        returns_processed = []
        for ret in returns:
            if isinstance(ret.value, list):
                for val in ret.value:
                    ret_new = deepcopy(ret)
                    ret_new.value = val
                    returns_processed.append(ret_new)
            else:
                returns_processed.append(ret)
        return returns_processed

    def find_next_index(self, response, index, xpath, value):
        """Get next index of the list key in the response

        Args:
          response (list): List of tuples containing
                           NETCONF - lxml.Element, xpath.
                           GNMI - value, xpath
          index (Integer): First index of current list
          xpath (String): List key xpath
        Returns:
          Integer: The index till the response needs to be trimmed.

        Eg:
            <List1> ---->  This is parent_key_index
                <Key>K1</Key>
                <Prop>v1<Prop> ---> Property to validate
            </List1>
            <List2> -----> Return next_index
                <Key>K2</Key>
                <Prop>v2<Prop>
            </List2>
        """
        for ix, resp in enumerate(response[index:]):
            if resp[1] == xpath and not str(resp[0]) == value:
                return ix+index

        return len(response)

    def check_list_in_returns(self, returns: List[OptFields]) -> bool:
        """Check if there are lists in returns

        Args:
          returns (list): List of dictionaries containing
                        returns fields.
        Returns:
          bool: True if List found, else False.
        """
        for field in returns:
            if "[" in field.xpath:
                return True

        return False

    def get_parent_dict(self, parent_key_indexes, current_xpath):
        """Return last parent key index of a key/leaf value

        Args:
            parent_key_indexes: Dictionary {key path: index in response}
            current_xpath: xpath of the current field in returns.

        Returns:
            parent key index of the current xpath.

        Implementation:
            current_xpath = container/list/value
            parent_key_indexes = {"container/list/key": 3}

            Trim the names
                current_xpath = container/list/value
                    -> current_xp = container/list
                parent_key_indexes[0] = container/list/key
                    -> xp = container/list

                if "container/list" in "container/list/key", then it is a parent_key.
                Return the parent_key_index.
        """
        parent_key_index = 0
        parent_key_xpath = "/"
        parent_key_value = ""
        parent_dict = {}
        for xpath, values in parent_key_indexes.items():
            # Trim name from the xpaths
            index = values[0]
            value = values[1]
            xp = xpath[:xpath.rfind('/')]
            current_xp = current_xpath[:current_xpath.rfind('/')]
            # if xp is in current_xp, that means
            # xp is parent key of current_xp
            if not xpath == current_xpath and xp in current_xp:
                parent_key_index = index
                parent_key_xpath = xpath
                parent_key_value = value

        parent_dict[parent_key_xpath] = [parent_key_index, parent_key_value]
        return parent_dict

    def verify_reply(self, response, expected, opfields: List[OptFields]):
        """Verify values and namespaces are what is expected.

        Expected tags and response tags have been checked for names
        and order so make sure namespace and values are correct.

        Args:
          response (list): List of reply lxml.etree.Elements.
          expected (list): List of expected lxml.etree.Elements.
          opfields (list): List of dict containing expected values.
        Returns:
          bool: True if successful.
        """
        result = True
        missing_ns_msg = ''
        wrong_values = ''
        missing_tags = ''
        ns_set = set()
        value_sequence_number = 0

        for expect, xpath in expected:
            for reply, reply_xpath in response:
                if reply.tag == expect.tag and xpath == reply_xpath:
                    break
            else:
                # Missing an expected tag
                missing_tags += expect.tag + '\n'
                result = False
                continue
            # add namespace to the set as we parse through the response/expect
            for ns in expect.nsmap.values():
                ns_set.add(ns)

            for ns in reply.nsmap.values():
                if ns != self.NETCONF_NAMESPACE and ns not in ns_set:
                    missing_ns_msg += 'Tag:{0} Namespace:{1}\n'.format(
                        self.et.QName(expect.tag).localname, ns
                    )
                    result = False

            value_state = self._process_values(reply, expect)

            if 'no_values' in value_state:
                response.remove((reply, reply_xpath))
                continue

            if opfields and 'reply_val' in value_state:
                # We have a value and we have opfields. The opfields may not be
                # in sequence, so loop through and see if this is a field we
                # are interested in.
                for field in opfields:
                    if field.selected is False:
                        opfields.remove(field)
                        continue
                    if 'xpath' in field and reply_xpath == field.xpath and \
                            self.et.QName(reply).localname == field.name:
                        if not self.check_opfield(value_state['reply_val'],
                                                  field):
                            result = False
                        opfields.remove(field)
                        break
                    elif value_sequence_number == int(field.id):
                        # Backward compatible - not as reliable
                        # because fields may be out of order
                        if not self.check_opfield(value_state['reply_val'],
                                                  field):
                            result = False
                        opfields.remove(field)
                        break

                value_sequence_number += 1

            elif 'match' not in value_state:
                wrong_values += 'Tag:{0} Value:{1} Expected:{2}\n'.format(
                    self.et.QName(expect.tag).localname,
                    value_state.get('reply_val', 'None'),
                    value_state.get('expect_val', 'None')
                )
                result = False
            response.remove((reply, reply_xpath))

        if not result:
            if missing_tags:
                log.error("{0} Following tags are missing:\n{1}".format(
                    'OPERATIONAL-VERIFY FAILED',
                    missing_tags
                )
                )
            if missing_ns_msg:
                log.error("{0} Missing namespaces:\n{1}".format(
                    'OPERATIONAL-VERIFY FAILED',
                    missing_ns_msg
                )
                )
            if wrong_values:
                log.error("{0} Wrong values:\n{1}".format(
                    'OPERATIONAL-VERIFY FAILED',
                    wrong_values
                )
                )
        if len(response) and 'explicit' in self.with_defaults:
            result = False
            extra_tags = [el.tag for el, xpath in response]
            log.error(
                "{0} Following tags are not expected in response:\n{1}".format(
                    'OPERATIONAL-VERIFY FAILED',
                    '\n'.join(extra_tags)
                )
            )

        return result

    def verify_rpc_data_reply(self, decoded_response: List[tuple], rpc_data: dict) -> bool:
        # TODO Move to verifiers.py when netconf is implemented
        """Construct a GET based off an edit message and verify results.

        Args:
          response (List[tuple]): List of Value, Xpath tuple value is associated with.
          rpc_data (dict): Xpaths and values associated to edit message.
        Returns
          bool: True = passed, False = failed.
        """
        result = True
        nodes: List[OperationalFieldsNode] = []
        list_keys: List[OptFields] = []
        par_xp = ''
        del_parent = False
        if 'explicit' in self.with_defaults:
            # RFC 6243 - Only tags set by client sould be in reply
            log.info('WITH DEFAULTS - EXPLICIT MODE')
        elif 'report-all' in self.with_defaults:
            # RFC 6243 - if value is default it should match
            log.info('WITH DEFAULTS - REPORT-ALL MODE')
        else:
            # RFC 6243 not supported
            log.info('WITH DEFAULTS - NOT REPORTED')

        for node in rpc_data.get('nodes', []):
            # original xpath with key/value required to validate
            # key values with multilist entries in response
            xpath_original = re.sub(self.RE_FIND_PREFIXES, '/', node.get('xpath', ''))

            # Find missing prefixes and log warning
            matches = re.findall(self.RE_FIND_KEY_PREFIX, xpath_original)
            if matches:
                for m in matches:
                    prefix = m[0]
                    name = m[1]
                    if not prefix:
                        log.warning(f'RPC reply key "{name}" is missing prefix in {xpath_original}')

            # remove prefixes from key names (if they exist)
            # e.g.
            # /native/route-map[name="set-community-list"]/route-map-seq[ios-route-map:ordering-seq="10"]
            # becomes (note `name` does not have a prefix, but `ordering-seq` has):
            # /native/route-map[name="set-community-list"]/route-map-seq[ordering-seq="10"]
            xpath_original = re.sub(self.RE_FIND_KEY_PREFIX, r'[\g<name>', xpath_original)

            # Remove leading and trailing whitespace in the key content
            # e.g.
            # /native/router/bgp[id="6"]/neighbor[id=" 100.5.6.6 "]/remote-ass
            # becomes
            # /native/router/bgp[id="6"]/neighbor[id="100.5.6.6"]/remote-as
            xpath_original = re.sub(self.RE_FIND_QUOTED_VALUE, r'"\g<value>"', xpath_original)

            # xpath with keys and namespace prefix stripped.
            xpath = re.sub(self.RE_FIND_KEYS, '', node.get('xpath', ''))
            xpath = re.sub(self.RE_FIND_PREFIXES, '/', xpath)

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
                self.add_key_nodes(parent_path, list_keys)

            if node.get('nodetype', '') == 'container':
                if edit_op in ['delete', 'remove']:
                    # presence container
                    par_xp = xpath
                    del_parent = True
                    continue
                self.add_key_nodes(node.get('xpath', ''), list_keys)
                continue

            if 'explicit' not in self.with_defaults and \
                    'report-all' in self.with_defaults:
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
            log.info('NO DATA RETURNED')
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
                            log.error(
                                "Config not removed. {0} operation failed".format(edit_op))
                            return False
        for node in nodes:
            if not self.process_operational_state(decoded_response, [node.opfields]):
                if node.edit_op in ['delete', 'remove'] and not node.default_value:
                    continue
                result = False
        for node in list_keys:
            if not self.process_operational_state(decoded_response, [node], key=True):
                result = False
        return result

    def add_key_nodes(self, xpath: str, nodes: List[OptFields]):
        """Add the List key nodes to the opfields"""
        # Remove the prefixes from the xpath.
        # Ex: convert /ios:foo/ios:foo1[ios:name='val']/ios:foo2 to
        # /foo/foo1[ios:name='val']/foo2
        xpath = re.sub(self.RE_FIND_PREFIXES, '/', xpath)
        # Loop through all the key/value in the xpath
        for key in self.RE_FIND_KEYS.findall(xpath):
            # Ex: for [foo="val"] the keyname will be 'foo'
            # Ex: for [prefix:foo="val"] the keyname will be 'foo'
            m = re.search(self.RE_FIND_KEY_PREFIX, key)
            if m:
                keyname = m.groupdict().get('name')
            else:
                raise ValueError(f'Unable to find key name in xpath {xpath} for key {key}')
            # Ex: [foo="val"] will return "val"
            # Ex: [foo=" val "] will return "val"
            m = re.search(self.RE_FIND_QUOTED_VALUE, key)
            if m:
                keyval = m.groupdict().get('value')
            else:
                raise ValueError(f'Unable to find value in xpath {xpath} for key {key}')
            # contruct xpath /xpath/list/foo by appending the key name.
            key_path = xpath.split(key)[0] + '/' + keyname
            # If there are multiple key/values in xpath, substitute other
            # key value pairs with empty string.
            key_path = re.sub(self.RE_FIND_KEYS, '', key_path)
            for entry in nodes:
                if entry.xpath == key_path:
                    break
            else:
                nodes.append(OptFields(name=keyname, value=keyval,
                             xpath=key_path, selected=True, op='=='))

    def process_rpc_reply(self, resp):
        """Transform XML into elements with associated xpath.

        Args:
          resp (list) or (str): list returned from netconf_send or
                                well formed rpc-reply XML.
        Returns:
          list: List of tuples (lxml.Element, xpath (str))
        """
        resp_xml = self._get_resp_xml(resp)

        if not resp_xml:
            log.error(
                banner("OPERATIONAL-VERIFY FAILED: No response to verify.")
            )
            return False

        try:
            resp = self.et.fromstring(resp_xml.encode('utf-8'))
            log.info(self.et.tostring(resp, pretty_print=True).decode('utf-8'))
        except self.et.XMLSyntaxError as e:
            log.error(
                banner('OPERATIONAL-VERIFY FAILED: Response XML:\n{0}'
                       .format(str(e)))
            )
            return False

        # Associate xpaths with response tags
        response = []
        xpath = []
        for el in resp.iter():
            if self.et.QName(el).localname == 'rpc-reply':
                # Don't evaluate rpc-reply tag
                continue
            if not response and self.et.QName(el).localname == 'data':
                # Don't evaluate rpc-reply/data tag
                continue
            parent = el.getparent()
            xpath.append('/' + self.et.QName(el).localname)
            while True:
                if parent is not None:
                    xpath.append('/' + self.et.QName(parent).localname)
                    parent = parent.getparent()
                else:
                    break

            response.append(
                (el, ''.join(reversed(xpath)).replace('/rpc-reply/data', ''))
            )
            xpath = []

        return response
