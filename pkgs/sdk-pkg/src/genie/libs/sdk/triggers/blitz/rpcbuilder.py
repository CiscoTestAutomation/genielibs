"""Build NETCONF RPC XML from user-provided inputs."""

import re
import logging
from collections import OrderedDict
from html import unescape
from pyats.log.utils import banner
log = logging.getLogger(__name__)

try:
    import lxml.etree as et
    from lxml.etree import QName
    from lxml.builder import ElementMaker
except Exception:
    pass

NETCONF_NS_1_0 = "urn:ietf:params:xml:ns:netconf:base:1.0"
YANG_NS_1 = "urn:ietf:params:xml:ns:yang:1"
WITH_DEFAULTS_NS = "urn:ietf:params:xml:ns:yang:ietf-netconf-with-defaults"
NMDA_NS = "urn:ietf:params:xml:ns:yang:ietf-netconf-nmda"
NMDA_DATASTORE_NS = "urn:ietf:params:xml:ns:yang:ietf-datastores"
NMDA_ORIGIN = "urn:ietf:params:xml:ns:yang:ietf-origin"

class RpcInputError(ValueError):
    """Raised by :meth:`YSNetconfRPCBuilder.get_payload` on invalid input."""

    def __init__(self, parameter, value, reason):
        self.parameter = parameter
        self.value = value
        self.reason = reason
        super(RpcInputError, self).__init__(str(self))

    def __str__(self):
        return "ERROR: Invalid {0}:\n{1}\n  {2}".format(
            self.parameter, self.value, self.reason)


class XPathError(RpcInputError):
    """Exception raised when the XPath is malformed."""

    def __init__(self, value, reason):
        super(XPathError, self).__init__('xpath', value, reason)


class XMLValueError(RpcInputError):
    """Exception raised when the xml_value is malformed."""

    def __init__(self, value, reason):
        super(XMLValueError, self).__init__('xml_value', value, reason)


class YSNetconfRPCBuilder(object):
    """Class used to build a NETCONF RPC XML from provided data."""

    skip_next_hop = ['case', 'choice', 'input', 'output']
    """Nodetypes that must not be included in an RPC, but skipped over instead.

    In other words, nodes that are schema nodes but not data nodes.
    """

    #
    # Public API
    #

    def __init__(self,
                 prefix_namespaces="minimal",
                 netconf_ns=NETCONF_NS_1_0,
                 nsmap=None):
        """Create an RPC builder to help construct RPC XML.

        Args:
          prefix_namespaces (str): "always" to always prefix XML namespaces,
            "minimal" to only prefix when necessary.
          netconf_ns (str): XML namespace to use for building NETCONF elements.
            Defaults to netconf 1.0 namespace, but can be overridden for e.g.
            netconf 1.1 namespace or no namespace at all.
          nsmap (dict): Mapping of prefixes to XML namespaces
        """
        self.netconf_ns = netconf_ns
        if not nsmap:
            nsmap = {}
        else:
            nsmap = nsmap.copy()
        self.nsmap = nsmap
        if prefix_namespaces == "always":
            if netconf_ns:
                self.nsmap['nc'] = netconf_ns
        elif prefix_namespaces == "minimal":
            if netconf_ns:
                self.nsmap[None] = netconf_ns
        else:
            raise ValueError('Unknown prefix_namespaces value "{0}"'
                             .format(prefix_namespaces))

        self.prefix_namespaces = prefix_namespaces

        self.keep_prefixes = set()
        """Namespace prefixes to keep even if 'unused'.

        Primarily used to ensure that namespaced **values** retain
        their prefixes.
        """

        self.netconf_element = ElementMaker(namespace=netconf_ns,
                                            nsmap=self.nsmap)
        """Factory used to create XML elements in the NETCONF namespace."""

        yanglib_pfx = None if prefix_namespaces == 'minimal' else 'yanglib'
        self.yang_element = ElementMaker(namespace=YANG_NS_1,
                                         nsmap={yanglib_pfx: YANG_NS_1})
        """Factory used to create XML elements in the YANG namespace."""

        ncwd_pfx = None if prefix_namespaces == 'minimal' else 'ncwd'
        self.ncwd_element = ElementMaker(namespace=WITH_DEFAULTS_NS,
                                         nsmap={ncwd_pfx: WITH_DEFAULTS_NS})
        """Factory to create XML elements in the with-defaults namespace."""

        self.get_data = ElementMaker(namespace=NMDA_NS,
                                     nsmap={'ds': NMDA_DATASTORE_NS,
                                            'or': NMDA_ORIGIN})
        """Factory to create "get-data" element RFC 8526."""

        self.edit_data = ElementMaker(namespace=NMDA_NS,
                                      nsmap={'ds': NMDA_DATASTORE_NS})
        """Factory to create "edit-data" element RFC 8526."""

    def add_netconf_attr(self, elem, attr, value):
        """Add an appropriately namespaced attribute to the given Element."""
        elem_ns = QName(elem).namespace
        if self.nsmap.get(None) == elem_ns:
            # No need to prefix the attribute
            elem.attrib[attr] = str(value)
        else:
            # LXML does not allow us to create an un-prefixed attrib on a
            # prefixed element, so if elem is prefixed, and we didn't specify
            # a NETCONF namespace prefix, use NETCONF 1.0 ns.
            attr_ns = self.netconf_ns or NETCONF_NS_1_0
            elem.attrib[QName(attr_ns, attr)] = str(value)

    def get_payload(self, cfgs, root_element):
        """Construct XML RPC payload derived from the given list of cfgs.

        Args:
          cfgs (list): List of "cfg" dicts, each with mandatory key "xpath"
            (described below) and optional keys "value" (text value of the
            described leaf node), "xml_value" (value of the described "anyxml"
            or "anydata" node) and/or "edit-op" (a
            `NETCONF edit-config operation`_).
          root_element (lxml.etree.Element): Containing Element to populate
            with a hierarchy of sub-elements corresponding to the given cfgs
            list.

        Returns:
          lxml.etree.Element: root_element, now populated with additional
          sub-element(s) as appropriate.

        Raises:
          RpcInputError: if any parameters in :attr:`cfgs` are malformed
            in such a way to prevent construction of the RPC.

        Example:
          Given an empty ``<ocif:interfaces>`` ``root_element`` and a
          simple single-entry ``cfgs``::

              [{
                  "xpath": \
'/ocif:interfaces/ocif:interface[name="eth0"]/ocif:config/ocif:mtu',
                  "value": "9000",
              }]

          the updated and returned ``root_element`` will be::

              <ocif:interfaces
               xmlns:ocif="http://openconfig.net/yang/interfaces">
                <ocif:interface>
                  <ocif:name>eth0</ocif:name>
                  <ocif:config>
                    <ocif:mtu>9000</ocif:mtu>
                  </ocif:config>
                </ocif:interface>
              </ocif:interfaces>

        For each "cfg" in the "cfgs" list, the "xpath" parameter is more
        precisely an XPath `abbreviated`_ `location path`_, evaluated in the
        `context`_ described in `RFC 6020`_. Currently the only predicates
        supported by this API are "child" expressions describing the values
        of any list keys, similar to the YANG `instance-identifier`_ built-in
        type. In brief, the "xpath" should be a string of form
        ``/root-node/node/list-node[key1="val1"][key2="val2"]/node/leaf-node``.

        .. warning::
           For each "cfg", the "xpath" SHOULD include predicates for any and
           all list keys (e.g., ``[name="eth0"]``). This method doesn't know
           what list keys are expected, so it will not reject XPaths that are
           in fact missing a key(s) according to the underlying YANG model,
           but the resulting RPC will be invalid for the YANG model.

           Similarly, to generate a valid RPC, if a list has more than one
           key, the key predicates in the XPath SHOULD be in the expected
           order as defined in the YANG model. This is again because this
           method does not know the required key ordering and if the keys
           are mis-ordered in the parameters passed to this method, they will
           be mis-ordered in the resulting RPC as well.

        .. note::
           When the list keys are correctly specified as XPath predicates,
           cfg entries specifically describing the list key(s) are optional,
           as list key elements will be automatically created based on the
           XPath predicates. In other words, given the above example, the
           following additional "cfg" is unneeded but would not be harmful::

              {
                  "xpath": \
'/ocif:interfaces/ocif:interface[name="eth0"]/ocif:name',
                  "value": "eth0",
              }

        .. _`NETCONF edit-config operation`: \
https://tools.ietf.org/html/rfc4741#section-7.2
        .. _abbreviated: \
https://www.w3.org/TR/1999/REC-xpath-19991116/#path-abbrev
        .. _`location path`: \
https://www.w3.org/TR/1999/REC-xpath-19991116/#location-paths
        .. _context: https://tools.ietf.org/html/rfc6020#section-6.4
        .. _`RFC 6020`: https://tools.ietf.org/html/rfc6020
        .. _instance-identifier: \
https://tools.ietf.org/html/rfc6020#section-9.13
        """
        for cfg in cfgs:
            if 'xpath' not in cfg:
                log.warning('No xpath in %s', cfg)
                continue

            # Validate all cfgs before making any changes
            # Will raise an RpcInputError if anything is invalid
            self._get_nodes(cfg['xpath'], root_element,
                            value=cfg.get('value'),
                            xml_value=cfg.get('xml_value'),
                            edit_op=cfg.get('edit-op'),
                            validate_only=True)

            # No exception raised - we're good to proceed,
            # and shouldn't see any exception at this point
            try:
                self._get_nodes(cfg['xpath'], root_element,
                                value=cfg.get('value'),
                                xml_value=cfg.get('xml_value'),
                                edit_op=cfg.get('edit-op'))
            except RpcInputError as exc:    # pragma: no cover
                log.error("Error encountered AFTER passing input validation;"
                          " please investigate!\n{0}".format(exc))
                raise

        if self.prefix_namespaces == "always":
            # We initially registered all namespace prefixes known to the
            # containing module, many of which may be unused for this
            # particular RPC. Unused namespaces add clutter so strip them out.
            et.cleanup_namespaces(root_element,
                                  keep_ns_prefixes=sorted(self.keep_prefixes))

        if len(root_element) > 0:
            log.debug('get_payload: constructed XML:\n%s',
                      et.tostring(root_element, encoding='unicode',
                                  pretty_print=True))
        else:
            log.warning("No payload XML constructed")

        return root_element

    #
    # Private APIs below
    #
    _XPATH_PREFIX_IDENTIFIER_RE = re.compile(
        '''([a-zA-Z_][-a-zA-Z0-9_.]*):([a-zA-Z_][-a-zA-Z0-9_.]*)''')
    """Regex matching a prefixed identifier in an XPath.

    Matches strings like ``ocif:interface`` and returns the prefix and
    identifier (here, ``ocif`` and ``interface``) as match subgroups.
    Used by :meth:`_get_nodes`.
    """

    _XPATH_KEY_RE = re.compile(
        r"\[([^=\[\]]+)="    # [key=
        r"(?:"               # one of
        r'"([^"]*)"'         # "double-quoted value"
        r"|"                 # or
        r"'([^']*)'"         # 'single-quoted value'
        r"|"                 # or
        r"([0-9]*)"          # integer value
        r"|"                 # or
        r"concat\((.*)\)"    # concat()
        r")\]"
    )
    """Regex for an XPath predicate representing a list key and value.

    Matches strings like ``[name="foobar"]`` and returns the key and value
    (here, ``name`` and ``foobar``) as match subgroups. Note that the key is
    always subgroup 1, whereas the value will be subgroup 2 (if double-quoted),
    3 (if single-quoted), or 4 (if based on concat()) depending on the input.
    Used by :meth:`_get_nodes`.
    """

    _XPATH_CONCAT_TOKEN_RE = re.compile(
        r"(?:"               # one of
        r'"([^"]*)"'         # double-quoted string
        r"|"                 # or
        r"'([^']*)'"         # single-quoted string
        r")"
    )
    """Regex for a single-quoted or double-quoted string.

    Double-quoted strings are returned as match group 1, single-quoted as
    match group 2.
    Used by :meth:`_get_nodes`.
    """

    def _get_nodes(self, xpath, root_elem,
                   value=None, xml_value=None, edit_op=None,
                   validate_only=False):
        r"""Construct Elements for the given leaf under the given parent.

        Helper method to :meth:`get_payload`.
        Makes use of :const:`_XPATH_KEY_RE` and :const:`_XPATH_CONCAT_TOKEN_RE`
        to handle list key predicates::

          >>> YSNetconfRPCBuilder._XPATH_KEY_RE.findall(
          ...      '''foo[bar="baz"][bat-qux='frobozz']''')
          [('bar', 'baz', '', '', ''), ('bat-qux', '', 'frobozz', '', '')]
          >>> YSNetconfRPCBuilder._XPATH_KEY_RE.findall(
          ... 'ipv6[ip="2001:0dB8:AC10:FE01::"][prefix="/64"]')
          [('ip', '2001:0dB8:AC10:FE01::', '', '', ''), ('prefix', '/64', '', '', '')]
          >>> YSNetconfRPCBuilder._XPATH_KEY_RE.findall(
          ... "ipv4[ip='10.0.10.77'][prefix='/24']")
          [('ip', '', '10.0.10.77', '', ''), ('prefix', '', '/24', '', '')]
          >>> YSNetconfRPCBuilder._XPATH_KEY_RE.findall(
          ... '''foo:bar[description=concat("I said ", \'"\', ''' +
          ... '''"I said, \'hello\'", \'"\', "!")]''')
          [('description', '', '', '', '"I said ", \'"\', "I said, \'hello\'", \'"\', "!"')]
          >>> tokens = YSNetconfRPCBuilder._XPATH_CONCAT_TOKEN_RE.findall(
          ... '"I said ", \'"\', "I said, \'hello\'", \'"\', "!"')
          >>> tokens
          [('I said ', ''), ('', '"'), ("I said, 'hello'", ''), ('', '"'), ('!', '')]
          >>> ''.join(''.join(tok) for tok in tokens)
          'I said "I said, \'hello\'"!'

        Args:
          xpath (str): Absolute data node identifier (/ns:name/ns:name2..)
          root_elem (lxml.etree.Element): Parent Element to add children to.
          value (str): Text value, if any, to set for this leaf. May include
            HTML/XML escape sequences such as ``&gt;``.
          xml_value (str): XML string to set (as un-escaped XML) for this leaf.
          edit_op (str): Text, if any, to set on a "nc:operation" attribute of
            the new leaf element
          validate_only (bool): If True, do not build any XML elements, only
            validate the correctness of the ``xpath``.
        Raises:
          XPathError: if the xpath is not a valid schema node identifier
          XMLValueError: if the xml_value is not a valid XML string
        """  # noqa: E501
        # Find and/or create the intermediate Elements
        # TODO: we could probably find some way to do this more automatically
        #       using lxml.XSLT?

        if not xpath.startswith('/'):
            raise XPathError(xpath, "must start with '/'")
        xpath_base = xpath

        parent = root_elem
        child = None
        prev_keys_values = {}

        # Validate the xpath (& xml_value if any) before creating any elements
        xml_child = None
        if xml_value is not None:
            try:
                xml_child = et.fromstring(xml_value)
            except et.XMLSyntaxError as exc:
                raise XMLValueError(xml_value, str(exc))

        n = 1
        while xpath:
            log.debug("Parsing remnant of xpath: %s", xpath)
            if xpath[0] != "/":
                raise XPathError(xpath_base, "expected /... but found {0}"
                                 .format(xpath))
            xpath = xpath[1:]
            if not xpath:
                raise XPathError(xpath_base, "trailing slash")
            # A valid component could be:
            # pfx:localname
            # pfx:localname[key1="value1"]
            # pfx:localname[key1="value1:value2"][foo:keyA="valueA"]
            # pfx:localname[key1='"foo/bar"'][foo:keyB=concat("hello","world")]
            #
            # TODO: we do not yet support:
            # pfx:localname[key1="value1" and key2="value2"]
            identifier = self._XPATH_PREFIX_IDENTIFIER_RE.match(xpath)
            if not identifier:
                raise XPathError(
                    xpath_base,
                    'expected a prefixed identifier at segment {0}, '
                    'but got "{1}"'
                    .format(n, xpath))
            pfx, localname = identifier.groups()
            xpath = xpath[identifier.end():]
            log.debug("  ...minus pfx/localname: %s", xpath)

            if pfx not in self.nsmap:
                raise XPathError(
                    xpath_base,
                    'Unknown xpath namespace prefix "{0}" on segment {1} -- '
                    'known prefixes are {2}'
                    .format(pfx, n, sorted(str(k) for k in self.nsmap.keys())))

            ns = self.nsmap.get(pfx)
            qname = QName(ns, localname)

            keys_values = OrderedDict()
            while self._XPATH_KEY_RE.match(xpath):
                # _XPATH_KEY_RE may match as:
                # key, value, '', '', ''
                # key, '', value, '', ''
                # key, '', '', value, ''
                # key, '', '', '', value
                pred_key_value = self._XPATH_KEY_RE.match(xpath)
                pred_key = pred_key_value.group(1)
                pred_value = ""
                if pred_key_value.group(2):     # double-quoted string
                    pred_value = pred_key_value.group(2)
                elif pred_key_value.group(3):   # single-quoted string
                    pred_value = pred_key_value.group(3)
                elif pred_key_value.group(4):   # integer value
                    pred_value = pred_key_value.group(4)
                elif pred_key_value.group(5):   # concat(....)
                    concat_tokens = self._XPATH_CONCAT_TOKEN_RE.findall(
                        pred_key_value.group(5))
                    pred_value = ''.join(''.join(tok) for tok in concat_tokens)
                keys_values[pred_key] = pred_value
                xpath = xpath[pred_key_value.end():]
                log.debug("  ...minus keys / values: %s", xpath)

            for k, v in keys_values.items():
                try:
                    self._qname(k, ns)
                except ValueError:
                    raise XPathError(
                        xpath_base,
                        'Invalid key string "{0}" on segment {1} -- '
                        'known prefixes are {2}'.format(
                            k, n, sorted(str(k) for k in self.nsmap.keys())))

            if validate_only:
                n += 1
                continue

            # Build elements

            if xpath:
                # Intermediate node - create it if not already present
                # Filter existing nodes by keys/values if any
                child = None
                for candidate in parent.findall(qname):
                    # Be careful not to clobber the 'value' method arg!
                    for k, v in keys_values.items():
                        key_item = candidate.find(self._qname(k, ns))
                        # If the candidate doesn't have the keys that's ok,
                        # but if they're present, they must match
                        if key_item is None or (key_item.text or "") == v:
                            # So far, so good!
                            continue

                        # Else we have a key_item that appears not to match.
                        # Check one corner case involving namespace prefixes.
                        if self.prefix_namespaces == 'minimal' and ':' in v:
                            try:
                                qv = self._qname(v)
                                if (qv.namespace == ns and
                                        key_item.text == qv.localname):
                                    # The prefixed value "v" matches the ns of
                                    # key_item and its un-prefixed text,
                                    # meaning it's a match after all. Carry on.
                                    continue
                            except ValueError:
                                # Can happen if, for example,
                                # "v" is an IPv6 address like "2001::1",
                                # in which case we tried and failed to use
                                # "2001" as a namespace prefix. Not an error.
                                pass

                        # Definitely not a matching item.
                        break
                    else:
                        # All keys_values (if any) match this candidate
                        child = candidate
                        break

                if child is None:
                    child = self._make_element(parent, qname)

                    # Make sure keys are present and first if any
                    for k, v in keys_values.items():
                        self._make_element(child, self._qname(k, ns), value=v)

                parent = child

                prev_keys_values = dict(
                    (self._qname(k, ns), v) for k, v in keys_values.items())
            else:
                # Terminal node
                # Create it **unless** it was already created as a list key
                # Set value/edit-op if any
                if (qname not in prev_keys_values or
                        parent.find(qname) is None):
                    child = self._make_element(parent, qname,
                                               value=value,
                                               xml_child=xml_child,
                                               edit_op=edit_op)
                else:
                    child = parent.find(qname)
                    # (child.text or "") because in the case of an
                    # empty element, child.text == None, but value == "".
                    if (child.text or "") != value:
                        # Check if value has namespace and if we are set to
                        # minimal, see if it matches without namespace.
                        actual_match = False
                        try:
                            if value is None:
                                log.warning(
                                    'Value not set; Xpath valid?\n{0}'.format(
                                        str(xpath)
                                    )
                                )
                                value = ''
                            if (
                                value and ':' in value and
                                self.prefix_namespaces == 'minimal' and
                                self._qname(value).namespace == ns and
                                child.text == self._qname(value).localname
                            ):
                                actual_match = True
                        except ValueError:
                            # Not actually a namespaced value, just a string
                            # that happens to contain ':'
                            pass
                        if not actual_match:
                            log.error(
                                "List key value mismatch in RPC request! "
                                'Value from XPath: "%s", requested value "%s"'
                                "\nWill use XPath value and ignore request",
                                str(child.text), str(value))
                    # TODO: does nc:operation even apply to key nodes?
                    if edit_op:
                        self.add_netconf_attr(child, 'operation', edit_op)

                for k, v in keys_values.items():
                    self._make_element(child, self._qname(k, ns), value=v)

            n += 1

        return child

    def _qname(self, name, default_ns=None):
        """Make a name into a QName.

        Helper method to :meth:`_get_nodes`.

        Args:
          name (str): Name, either prefixed 'foo:bar' or unprefixed 'bar'.
          default_ns (str): Namespace to use if no prefix given.
        Returns:
          lxml.etree.QName
        """
        if ':' in name:
            pfx, localname = name.split(':', 1)
            ns = self.nsmap.get(pfx)
            if not ns:
                raise ValueError("Unknown namespace prefix '{0}'!".format(pfx))
            return QName(ns, localname)
        else:
            return QName(default_ns, name)

    def _make_element(self, parent, qname,
                      value=None, xml_child=None, edit_op=None):
        """Construct an Element based on the given cfg data.

        Helper method to :meth:`_get_nodes`.

        Args:
          parent (lxml.etree.Element): Parent for the new element
          qname (lxml.etree.QName): Namespace and localname for the new element
          value (str): Text value, if any, to set on the new element
            (with appropriate XML escapes if needed). May be 'pre-escaped' by
            the caller with HTML/XML escape sequences, if desired.
          xml_child (lxml.etree.Element): XML set as child of the new element
          edit_op (str): Text, if any, to set on a "nc:operation" attribute of
            the new element

        Returns:
          lxml.etree.Element: Newly constructed XML element.
        """
        # Define namespace-to-prefix mapping(s) this element needs to know
        if self.prefix_namespaces == "always":
            # All relevant namespaces already declared at root level
            nsmap = self.nsmap
        elif self.prefix_namespaces == "minimal":
            nsmap = {None: qname.namespace}

        # Handle prefixed values, e.g. 'ianaift:ethernetCsmacd'
        if value and ':' in str(value):
            pfx, localname = value.split(':', 1)
            if pfx in self.nsmap:
                # Make sure we don't discard this xmlns!
                self.keep_prefixes.add(pfx)
                # Declare the namespace on the element if needed
                if self.prefix_namespaces == "minimal":
                    # If the value namespace is the same as the element,
                    # then the element will be un-prefixed and the value
                    # needs to be too.
                    if self.nsmap[pfx] == qname.namespace:
                        value = localname
                    else:
                        nsmap[pfx] = self.nsmap[pfx]

        el = et.SubElement(parent, qname, nsmap=nsmap)

        if edit_op:
            self.add_netconf_attr(el, 'operation', edit_op)
        if value:
            # We use html.unescape here so that if the user passed through
            # 'pre-escaped' values like &lt; or &#92; they don't get
            # 're-escaped' into values like &amp;lt; or &amp;#92;.
            el.text = unescape(value)
        elif xml_child is not None:
            el.append(xml_child)

        return el


if __name__ == "__main__":  # pragma: no cover
    import doctest
    doctest.testmod()
