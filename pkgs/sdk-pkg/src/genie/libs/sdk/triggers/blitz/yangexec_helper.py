from collections import OrderedDict, abc
import re

START_RANGES = '|'.join(
    f'[{r}]'
    for r in [
        '\xC0-\xD6',
        '\xD8-\xF6',
        '\xF8-\u02FF',
        '\u0370-\u037D',
        '\u037F-\u1FFF',
        '\u200C-\u200D',
        '\u2070-\u218F',
        '\u2C00-\u2FEF',
        '\u3001-\uD7FF',
        '\uF900-\uFDCF',
        '\uFDF0-\uFFFD',
    ]
)

NAME_START_CHAR_RE = re.compile(r"(:|[A-Z]|_|[a-z]|{0})".format(START_RANGES))
NAME_CHAR_RE = re.compile(r"(\-|\.|[0-9]|\xB7|[\u0300-\u036F]|[\u203F-\u2040])")

def dict_to_ordereddict(element):
    """ Converts nested dictionary to OrderedDict"""
    if isinstance(element, (tuple, list)):
        return [dict_to_ordereddict(item) for item in element]

    if isinstance(element, dict):
        element = OrderedDict(element)

    if isinstance(element, OrderedDict):
        for key, value in element.items():
            element[key] = dict_to_ordereddict(value)

    return element

class Node(object):
    """Node in XML document tree, the XML tag encapsulates a value, or multiple values/children"""
    # Map for ecape characters and their replacements
    entities = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;'
    }

    def __init__(self, wrap='', tag='', data=None, repeat_iterables_parent=True):
        # Tag is the value between "<" and ">"
        self.tag = self.sanitize_element(tag)
        # Wrap is the starting and ending tags for any Node element and its children (if children exist)
        self.wrap = self.sanitize_element(wrap)
        # Data in dictionary format
        self.data = data
        # Type of node, can be: "flat", "mapping", or "iterable"
        self.type = self.get_type(data)
        # Items in the YANG list will have its wrap repeated for each item in list by default
        self.repeat_iterables_parent = repeat_iterables_parent

        if self.type == 'flat' and isinstance(self.data, str):
            # Make sure we deal with entities
            for entity, replacement in self.entities.items():
                self.data = self.data.replace(entity, replacement)

    def serialize(self, join_strings):
        """Convert Node to XML string"""
        # Determine the start and end of this node
        wrap = self.wrap
        end, start = '', ''

        if self.wrap:
            start = f'<{wrap}>'
            end = f'</{wrap}>'

        # Convert data in node to value and children
        value, children = self.convert()

        # Content of each node
        content = ''
        if children:
            if self.type != "iterable":
                # If node is not iterable, wrap in same tag
                content = join_strings((c.serialize(join_strings) for c in children), wrap)
            else:
                if self.repeat_iterables_parent:
                    # Iterables repeat the wrap for each child
                    result = []
                    for child in children:
                        content = child.serialize(join_strings)
                        if child.type == 'flat':
                            result.append(content)
                        else:
                            content = join_strings([content], True)
                            result.append(''.join((start, content, end)))
                    # Join list of strings together
                    return join_strings(result, False)
                else:
                    result = []
                    for c in children:
                        result.append(c.serialize(join_strings))
                    return "".join([start, join_strings(result, True), end])

        return ''.join((start, value, content, end))

    def get_type(self, data):
        """Return the type of the data on this node"""
        if isinstance(data, str):
            return 'flat'
        elif isinstance(data, abc.Mapping) or isinstance(data, OrderedDict):
            return 'mapping'
        elif isinstance(data, abc.Iterable):
            return 'iterable'

        return 'flat'

    def convert(self):
        """Convert self to tuple of (value, children)"""
        node_value = ''
        data_type = self.type
        data = self.data
        children = []

        if data_type == 'mapping':
            for key in data:
                item = data[key]
                children.append(
                    Node(key, '', item, repeat_iterables_parent=self.repeat_iterables_parent)
                )
        elif data_type == 'iterable':
            for item in data:
                children.append(
                    Node('', self.wrap, item, repeat_iterables_parent=self.repeat_iterables_parent)
                )
        else:
            node_value = str(data)
            if self.tag:
                node_value = f'<{self.tag}>{node_value}</{self.tag}>'

        return node_value, children

    @staticmethod
    def sanitize_element(element):
        """Convert element to valid XML tag"""
        if element and isinstance(element, str):
            if element.lower().startswith('xml'):
                element = f'_{element}'
            if ':' in element:
                # Remove YANG namespaces
                element = element[element.index(':') + 1:]
            return ''.join(
                ['_' if not NAME_START_CHAR_RE.match(element) else '']
                + ['_' if not (NAME_START_CHAR_RE.match(c) or NAME_CHAR_RE.match(c)) else c for c in element]
            )

        return element


class DictionaryToXML(object):
    """Converts a dictionary into XML string"""
    def __init__(self, data):
        # Change dictionary data to OrderedDict to preserve order of keys
        ordereddict_data = dict_to_ordereddict(data)
        # Format XML for RpcVerify to process
        self.xml_str = f'''
            <?xml version="1.0" encoding="UTF-8"?>
            <rpc-reply>
                <data>{self.convert(ordereddict_data)}</data>
            </rpc-reply>
        '''

    def _join_strings(self):
        """Returns a function that given a list of strings, will return that list as a single, indented, string"""
        return lambda nodes, wrap: ''.join(nodes)

    def convert(self, data, repeat_iterables_parent=True):
        """Create a Node tree from the data and return it as a serialized XML string"""
        join_strings = self._join_strings()
        # Convert dictionary to string recursively, starting with top-nested dictionary key-value
        return Node(
            wrap='', data=data, repeat_iterables_parent=repeat_iterables_parent
        ).serialize(join_strings)
