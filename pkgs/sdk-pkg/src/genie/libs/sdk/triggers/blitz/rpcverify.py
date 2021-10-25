#! /usr/bin/env python
import re
import logging
from six import string_types
from pyats.log.utils import banner


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


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

    def __init__(self, value, field):
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
    def field(self, field):
        self._field = field
        datatype = field.get('datatype', '')
        self.datatype = datatype
        if datatype.startswith('int') or datatype.startswith('uint'):
            self.fval = int(field.get('value'))
            if datatype not in self.integer_limits:
                raise TypeError('Invalid datatype')
            self.min, self.max = self.integer_limits[datatype]
            if self.value < self.min or self.value > self.max:
                self.min_max_failed = True
        elif datatype in ['decimal64', 'float']:
            self.fval = float(field.get('value'))
            self.min, self.max = self.integer_limits['int64']
            if self.value < self.min or self.value > self.max:
                self.min_max_failed = True
        elif datatype == 'boolean':
            if field.get('op') not in ['==', '!=']:
                self.bool_failed = True
            if self.value in [1, '1', 'true']:
                self.value = 'true'
            elif self.value in [0, '0', 'false']:
                self.value = 'false'
            else:
                self.bool_failed = True
            if str(field.get('value')).lower() in ['1', 'true']:
                self.fval = 'true'
            elif str(field.get('value')).lower() in ['0', 'false']:
                self.fval = 'false'
            else:
                self.bool_failed = True
        elif datatype == 'identityref':
            # TODO: basetype is string so might not get identityref.
            # strip prefix from values
            val = field.get('value')
            self.fval = val[val.find(':') + 1:]
            val = self.value
            self.value = val[val.find(':') + 1:]
        else:
            self.fval = field.get('value')
        self.op = field.get('op')
        self.fname = field.get('name', 'unknown field')

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
        if self.op == '==':
            return self.value == self.fval
        elif self.op == '!=':
            return self.value != self.fval
        elif self.op == '<':
            return self.value < self.fval
        elif self.op == '>':
            return self.value > self.fval
        elif self.op == '<=':
            return self.value <= self.fval
        elif self.op == '>=':
            return self.value >= self.fval


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
            raise(e)
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
    def check_opfield(self, value, field):
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

        try:
            # set this to operation in case we get an exception
            eval_text = field['op']

            datatype = field.get('datatype', None)

            if field['op'] == 'range':
                r1 = r2 = None
                try:
                    if not datatype:
                        value = float(value)
                except ValueError:
                    log_msg = 'OPERATION VALUE {0}: {1} invalid for range {2}{3}'.format(
                            field['xpath'],
                            str(value),
                            str(field['value']),
                            ' FAILED'
                        )
                    return (False, log_msg)

                if len(field['value'].split(',')) == 2:
                    rng = field['value'].split(',')
                    r1 = rng[0]
                    r2 = rng[1]
                elif len(field['value'].split()) == 2:
                    rng = field['value'].split()
                    r1 = rng[0]
                    r2 = rng[1]
                elif field['value'].count('-') == 1:
                    rng = field['value'].split('-')
                    r1 = rng[0]
                    r2 = rng[1]

                try:
                    if datatype:
                        if datatype.startswith('int') or \
                                datatype.startswith('uint'):
                            r1 = int(r1)
                            r2 = int(r2)
                            # change value to int type for subsequent compare operation
                            value = int(value)
                        else:
                            r1 = float(r1)
                            r2 = float(r2)
                            # change value to float type for subsequent compare operation
                            value = float(value)
                    else:
                        r1 = float(r1)
                        r2 = float(r2)
                        # change value to float type for subsequent compare operation
                        value = float(value)
                except TypeError:
                    log_msg = 'OPERATION VALUE {0}: range datatype "{1}" {2}{3}'.format(
                        field['xpath'],
                        datatype,
                        str(field['value']),
                        ' FAILED'
                    )
                    return (False, log_msg)
                if value >= r1 and value <= r2:
                    log_msg = 'OPERATION VALUE {0}: {1} in range {2} SUCCESS'.format(
                            field['xpath'], str(value), str(field['value'])
                        )
                else:
                    log_msg = 'OPERATION VALUE {0}: {1} out of range {2}{3}'.format(
                            field['xpath'],
                            str(value),
                            str(field['value']),
                            ' FAILED'
                        )
                    return (False, log_msg)
            else:
                if not datatype:
                    value = str(value)
                    fval = str(field.get('value'))
                    if (value.isnumeric() and not fval.isnumeric()) or \
                            (fval.isnumeric() and not value.isnumeric()):
                        # the eval_text will show the issue
                        eval_text = '"' + value + '" ' + field['op']
                        eval_text += ' "' + fval + '"'
                        log_msg = 'OPERATION VALUE {0}: {1} FAILED'.format(
                                field['xpath'], eval_text
                            )
                        return (False, log_msg)
                    if value.isnumeric():
                        eval_text = value + ' ' + field['op'] + ' '
                        eval_text += fval
                    else:
                        try:
                            # See if we are dealing with floats
                            v1 = float(value)
                            v2 = float(fval)
                            eval_text = str(v1) + ' ' + field['op'] + ' '
                            eval_text += str(v2)
                        except (TypeError, ValueError):
                            if value.startswith('"') and value.endswith('"'):
                                eval_text = value + ' ' + field['op']
                            else:
                                eval_text = '"' + value + '" ' + field['op']
                            if fval.startswith('"') and fval.endswith('"'):
                                eval_text += ' ' + fval
                            else:
                                eval_text += ' "' + fval + '"'
                    if eval(eval_text):
                        log_msg = 'OPERATION VALUE {0}: {1} SUCCESS'.format(
                                field['xpath'], eval_text
                            )
                    else:
                        log_msg = 'OPERATION VALUE {0}: {1} FAILED'.format(
                                field['xpath'], eval_text
                            )
                        return (False, log_msg)
                else:
                    log_tmp = 'OPERATION VALUE {0}: {1} {2} {3} {4}'
                    failed_type = 'FAILED'
                    evaldt = EvalDatatype(value, field)
                    if evaldt.evaluate():
                        log_msg = log_tmp.format(
                                field['xpath'], str(value),
                                field['op'], str(field['value']),
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
                                field['xpath'], str(value),
                                field['op'], str(field['value']),
                                failed_type
                            )
                        return (False, log_msg)

        except Exception as e:
            log_msg = 'OPERATION VALUE {0}: {1} {2} FAILED\n{3}'.format(
                    field['xpath'], str(value), eval_text, str(e)
                )
            return (False, log_msg)

        return (True, log_msg)

    def process_one_operational_state(self, response, field, key=False):
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
        log_msg = 'ERROR: "{0}" Not found.'.format(field['xpath'])
        for resp in response:
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
                        value = reply or 'empty'
                    name = reply_xpath[reply_xpath.rfind('/') + 1:]
                if 'xpath' in field and field['xpath'] == reply_xpath and \
                        name == field['name']:
                    datatype = field.get('datatype')
                    if not datatype:
                        log.warning(
                            "{0} has no datatype; default to string".format(
                                field['xpath']
                            )
                        )
                    elif datatype == 'empty':
                        field['value'] = 'empty'
                    result, log_msg = self.check_opfield(value, field)
                    if result:
                        log.info(log_msg)
                        return True
        if key:
            log.info('Parent list key "{0} == {1}" not required.'.format(
                field['name'], field['value']
            ))
            return True
        log.error(log_msg)
        return False

    def process_operational_state(self, response, returns, key=False):
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
        opfields = returns

        if not opfields:
            log.error(
                banner("OPERATIONAL STATE FAILED: No opfields to compare")
            )
            return False
        if not response:
            log.error(
                banner("OPERATIONAL STATE FAILED: Expected data")
            )
            return False

        if isinstance(response[0], tuple):
            # yang.connector only returned one list of fields
            response = [response]

        for field in returns:
            sel = field.get('selected', False)
            if sel is False or str(sel).lower() == 'false':
                continue
            if not self.process_one_operational_state(response, field, key):
                result = False

        return result

    def verify_reply(self, response, expected, opfields):
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
                    if field.get('selected', True) is False:
                        opfields.remove(field)
                        continue
                    if 'xpath' in field and reply_xpath == field['xpath'] and \
                            self.et.QName(reply).localname == field['name']:
                        if not self.check_opfield(value_state['reply_val'],
                                                  field):
                            result = False
                        opfields.remove(field)
                        break
                    elif value_sequence_number == int(field['id']):
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

    # Pattern to detect keys in an xpath
    RE_FIND_KEYS = re.compile(r'\[.*?\]')
    RE_FIND_PREFIXES = re.compile(r'/.*?:')
    # Pattern to detect prefix in the key name
    RE_FIND_KEY_PREFIX = re.compile(r'\[.*?:')

    def verify_rpc_data_reply(self, response, rpc_data):
        """Construct a GET based off an edit message and verify results.

        Args:
          response (tuple): Value, Xpath value is associated with.
          rpc_data (dict): Xpaths and values associated to edit message.
        Returns
          bool: True = passed, False = failed.
        """
        result = True
        nodes = []
        list_keys = []
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
                    nodes.append(
                        {'name': xpath.split('/')[-1],
                         'value': default,
                         'xpath': xpath,
                         'selected': True,
                         'op': '=='}
                    )
                    continue

            if edit_op not in ['delete', 'remove']:
                nodes.append(
                    {'name': xpath.split('/')[-1],
                     'value': value,
                     'xpath': xpath,
                     'selected': True,
                     'op': '=='}
                )

        if not response and not nodes and \
                edit_op in ['delete', 'remove']:
            log.info('NO DATA RETURNED')
            return True
        for node in nodes:
            if not self.process_operational_state(response, [node]):
                result = False
        for node in list_keys:
            if not self.process_operational_state(response, [node], key=True):
                result = False
        return result

    def add_key_nodes(self, xpath, nodes):
        """Add the List key nodes to the opfields"""
        # Remove the prefixes from the xpath.
        # Ex: convert /ios:foo/ios:foo1[ios:name='val']/ios:foo2 to
        # /foo/foo1[ios:name='val']/foo2
        xpath = re.sub(self.RE_FIND_PREFIXES, '/', xpath)
        # Loop through all the key/value in the xpath
        for key in self.RE_FIND_KEYS.findall(xpath):
             # Remove the prefix from list key name,
             # Ex: changes [ios:foo="val"] to foo="val"]
             key_no_pfx = re.sub(self.RE_FIND_KEY_PREFIX, '', key)
             # Split the key/value on "=", get the first entry,
             # and strip the '[' if present.
             # Ex: for [foo="val"] the keyname will be 'foo'
             keyname = key_no_pfx.split('=')[0].strip('[')
             # Get the value field from [foo="val"]
             # second entry after spliting on "=" will get the value
             # strip the ending ']'.
             # Ex: [foo="val"] will return '"val"' after stripping the ']'
             keyval = key_no_pfx.split('=')[1].strip(']')
             # To remove double quotes from the value
             # Ex: Change '"val"' to 'val'
             keyval = re.sub('"', '', keyval)
             # contruct xpath /xpath/list/foo by appending the key name.
             key_path = xpath.split(key)[0] + '/' + keyname
             # If there are multiple key/values in xpath, substitute other
             # key value pairs with empty string.
             key_path = re.sub(self.RE_FIND_KEYS, '', key_path)
             for entry in nodes:
                 if entry['xpath'] == key_path:
                     break
             else:
                 nodes.append(
                     {'name': keyname,
                      'value': keyval,
                      'xpath': key_path,
                      'selected': True,
                      'op': '=='}
                 )

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

    def parse_rpc_expected(self, resp_xml, expect_xml, opfields=[]):
        """Check if values are correct according expected XML.

        As an XML message is parsed, some XML tags have values assigned
        to them and some are just containers for other tags.  It is possible
        that the user is expecting one or more XML tags to be missing.  In
        expected XML, those cases are communicated by a "-" (minus) inserted
        in front of the XML tag that should be missing.  As the expected XML
        is parsed, those tags are identified, stored, and checked in response.

        Tags with values are assigned a sequence number according to the order
        within the expected XML.  The returned XML value should always be in
        the same order.  If opfields are passed in, they will match the
        sequence number.

        It is possible that the user is not interested in one or more values.
        In those cases, the sequence number will not be found in the opfields
        list and they will be skipped.

        When opfeilds are found, the assigned operation will be performed on
        the value, and if the operation returns True, the field test passed.

        Args:
          resp_xml (str): Actual rpc-reply XML.
          expected_xml (str): Expected rpc-reply XML.
          opfields (list): Expected values and operations to perform.
        Return:
          bool: Pass is True.
        """
        result = True

        if not opfields:
            log.info('EXPECTED XML:\n{0}'.format(expect_xml))

        if not opfields and not expect_xml:
            log.error(
                banner("OPERATIONAL-VERIFY FAILED: No XML for verification.")
            )
            return False

        if not resp_xml:
            log.error(
                banner("OPERATIONAL-VERIFY FAILED: No response to verify.")
            )
            return False

        # Preprocess expected XML text for unexpected tags
        lines = expect_xml.strip().splitlines()
        oper_expected = ""
        for line in lines:
            # lines with "-" (minus) should not show up in reply
            line = re.sub(r'^- *<([-0-9a-z:A-Z_]+)',
                          r'<\1 expected="false" ', line)
            oper_expected += line + "\n"

        try:
            expect = self.et.fromstring(oper_expected)
        except self.et.XMLSyntaxError as e:
            log.error(
                banner('OPERATIONAL-VERIFY FAILED: Expected XML:\n{0}'
                    .format(str(e)))
            )
            return False

        response = self.process_rpc_reply(resp_xml)
        if response is False:
            # Returning an empty list is ok
            return False

        expected = []
        xpath = []
        # Associate xpaths with expected tags
        for el in expect.iter():
            if self.et.QName(el).localname == 'rpc-reply':
                # Don't evaluate rpc-reply tag
                continue
            if not expected and self.et.QName(el).localname == 'data':
                # Don't evaluate rpc-reply/data tag
                continue
            xpath.append('/' + self.et.QName(el).localname)
            parent = el.getparent()
            while True:
                if parent is not None:
                    xpath.append('/' + self.et.QName(parent).localname)
                    parent = parent.getparent()
                else:
                    break
            expected.append(
                (
                    el,
                    re.sub(
                        r'^/rpc-reply/data|^/data',
                        '',
                        ''.join(reversed(xpath)),
                    )
                )
            )
            xpath = []

        # Expected XML should have at least one top level tag with one child
        if 'explicit' in self.with_defaults and len(expected) < 2:
            expected = []

        # Is any data expected to be returned?
        if expected and 'explicit' in self.with_defaults:
            # First element will always be top container so check it's child
            top_child, child_xpath = expected[1]
            # Attribute expected=false was added to unexpected elements
            if 'expected' in top_child.attrib:
                # Top level child is expected to be gone so we expect no data
                expected = []

        if expected or opfields:
            if not response:
                log.error(
                    banner("OPERATIONAL-VERIFY FAILED: rpc-reply has no data.")
                )
                return False

        if not expected and not opfields and not response:
            log.error(
                banner(
                    "OPERATIONAL-VERIFY SUCCESSFUL: {0}.".format(
                        'Expected no data in rpc-reply'
                    )
                )
            )
            return True

        if not expected and not opfields and response:
            log.error(
                banner(
                    "OPERATIONAL-VERIFY FAILED: Expected no data in rpc-reply."
                )
            )
            return False

        result, expected, response = self.process_expect_reply(response,
                                                               expected)
        if result and expected and response:
            result = self.verify_reply(response, expected, opfields)

        if result:
            log.info('OPERATIONAL-VERIFY SUCCESSFUL')
        return result


if __name__ == '__main__':
    test_recurse_reply = """
<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="101">
  <data>
    <top xmlns="http://rpcverify.com">
      <child1>
        <child2>child2</child2>
        <sibling1>sibling1</sibling1>
        <sibling-recurse>
          <sibchild>sibchild</sibchild>
          <sibchild2>sibchild2</sibchild2>
        </sibling-recurse>
      </child1>
    </top>
  </data>
</rpc-reply>
"""
    received = """
<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"\
     message-id="urn:uuid:d177b38c-bbc7-440f-be0d-487b2e3c3861">
    <data>
        <System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
            <lldp-items>
                <name>genericstring</name>
            </lldp-items>
        </System>
    </data>
</rpc-reply>
"""
    expected = """
<data>
<System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
-  <lldp-items>
-    <name>genericstring</name>
-  </lldp-items>
</System>
</data>
"""
    xml_deleted = """
<nc:rpc-reply message-id="urn:uuid:2680d19b-3ed2-4af8-9d39-2e3dfbb2b501" \
xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
<nc:data>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <router>
      <bgp xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-bgp">
        <id xmlns:nc='urn:ietf:params:xml:ns:netconf:base:1.0'>1</id>
        <address-family>
          <no-vrf>
            <ipv4>
              <af-name xmlns:nc='urn:ietf:params:xml:ns:netconf:base:1.0'>\
unicast</af-name>
-              <ipv4-unicast>
-                <aggregate-address>
-                  <ipv4-address xmlns:nc='urn:ietf:params:xml:ns:netconf:\
base:1.0'>10.0.0.0</ipv4-address>
-                  <ipv4-mask xmlns:nc='urn:ietf:params:xml:ns:netconf:\
base:1.0'>255.0.0.0</ipv4-mask>
-                  <advertise-map>mergeme</advertise-map>
                </aggregate-address>
              </ipv4-unicast>
            </ipv4>
          </no-vrf>
        </address-family>
      </bgp>
    </router>
  </native>
</nc:data>
</nc:rpc-reply>
"""
    xml_not_missing = """
<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" \
message-id="urn:uuid:2680d19b-3ed2-4af8-9d39-2e3dfbb2b501" \
xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
<data>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <router>
      <bgp xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-bgp">
        <id xmlns:nc='urn:ietf:params:xml:ns:netconf:base:1.0'>1</id>
        <address-family>
          <no-vrf>
            <ipv4>
              <af-name xmlns:nc='urn:ietf:params:xml:ns:netconf:base:1.0'>\
unicast</af-name>
              <ipv4-unicast>
                <aggregate-address>
                  <advertise-map>mergeme</advertise-map>
                </aggregate-address>
              </ipv4-unicast>
            </ipv4>
          </no-vrf>
        </address-family>
      </bgp>
    </router>
  </native>
</data>
</rpc-reply>
"""
    log = logging.getLogger("RPC-verfiy")
    logging.basicConfig(level=logging.DEBUG)
    rpcv = RpcVerify(log=log)
    result = rpcv.parse_rpc_expected(test_recurse_reply, test_recurse_reply)
    if result:
        print('\n**** RECURSE TEST PASSED ****\n')
    else:
        print('\n**** RECURSE TEST FAILED ****\n')
    rpcv.capabilities = ['urn:ietf:params:netconf:capability:with-defaults:1.0?\
basic-mode=report-all']
    result = rpcv.parse_rpc_expected(received, expected)
    rpcv.capabilities = ['urn:ietf:params:netconf:capability:with-defaults:1.0?\
basic-mode=explicit&also-supported=report-all-tagged']
    if not result:
        print('\n**** GENERICSTRING NOT DELETED TEST PASSED ****\n')
    else:
        print('\n**** GENERICSTRING NOT DELETED TEST FAILED ****\n')
    rpcv.parse_rpc_expected(xml_not_missing, xml_deleted)
    if not result:
        print('\n**** MERGEME NOT DELETED TEST PASSED ****\n')
    else:
        print('\n**** MERGEME NOT DELETED TEST PASSED ****\n')

    import doctest
    log = logging.getLogger("RPC-verfiy")
    logging.basicConfig(level=logging.DEBUG)
    doctest.testmod()
