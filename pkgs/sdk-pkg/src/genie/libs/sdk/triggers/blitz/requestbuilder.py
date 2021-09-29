"""Build RESTCONF request from user-provided inputs."""
from collections import OrderedDict
import os
import logging
import re
import json
log = logging.getLogger(__name__)


# Translate edit-op property in a node to an HTTP method
HTTP_METHODS = {
    'merge': 'PATCH',
    'create': 'POST',
    'replace': 'PUT',
    'delete': 'DELETE',
    'get': 'GET',
}

NO_BODY_METHODS = ['GET', 'DELETE']
WITH_BODY_METHODS = ['PATCH', 'PUT', 'POST']

XPATH_CONCAT_TOKEN_RE = re.compile(
    r"(?:"               # one of
    r'"([^"]*)"'         # double-quoted string
    r"|"                 # or
    r"'([^']*)'"         # single-quoted string
    r")"
)

XPATH_KEY_RE = re.compile(
    r"\[([^=\[\]]+)="    # [key=
    r"(?:"               # one of
    r'"([^"]*)"'         # "double-quoted value"
    r"|"                 # or
    r"'([^']*)'"         # 'single-quoted value'
    r"|"                 # or
    r"concat\((.*)\)"    # concat()
    r")\]"
)

XPATH_BRACKETS_CONTENT_RE = re.compile(r"\[(.*?)\]")

DEVICE_RESTCONF_ENDPOINT = '/restconf/data'


class RequestInputError(ValueError):
    """Raised on invalid input."""

    def __init__(self, parameter, value, reason):
        self.parameter = parameter
        self.value = value
        self.reason = reason
        super(RequestInputError, self).__init__(str(self))

    def __str__(self):
        return "ERROR: Invalid {0}:\n{1}\n  {2}".format(
            self.parameter, self.value, self.reason)


class XPathError(RequestInputError):
    """Exception raised when the XPath is malformed."""

    def __init__(self, value, reason):
        super(XPathError, self).__init__('xpath', value, reason)


class RestconfRequestBuilder(object):
    """Class used to build URL, and body for a ResTCONF request from provided data."""
    #
    # Public API
    #
    def __init__(self, request_data, returns):
        """Create list of requests from request data"""
        # Nodes and XPaths from request data
        self.nodes = request_data.get('nodes', [])
        self.xpaths = [node.get('xpath') for node in self.nodes if node.get('xpath', None)]
        # Map XPath to its node data
        self.xpath_to_nodedata = {node['xpath']: node for node in self.nodes}
        # String present in all XPaths
        self.common_prefix = self.gen_common_prefix(self.xpaths)
        # Components for REST request
        self.http_method = self.get_http_method_from_nodes(self.nodes)
        self.url = self.gen_url(self.common_prefix, request_data, returns, self.http_method)
        self.body = self.gen_body(self.xpaths, self.common_prefix, request_data, self.http_method)
        self.json_body = json.dumps(self.body, indent=2)
        self.content_type = 'application/yang-data+json'

    def get_http_method_from_nodes(self, nodes):
        if not nodes or not len(nodes):
            raise RequestInputError('nodes', None, 'No nodes are present in data')

        ref_edit_op = nodes[0]['edit-op'].lower() or 'merge'
        if not all([node['edit-op'].lower() == ref_edit_op for node in nodes]):
            # Check if all edit-ops are the same, if not raise error
            raise RequestInputError(
                'edit-op',
                'Edit-op not the same across all nodes',
                'Edit-op must the same in all nodes for this test'
            )

        try:
            http_method = HTTP_METHODS[ref_edit_op]
        except KeyError:
            raise RequestInputError(
                'edit-op',
                ref_edit_op,
                f'Invalid edit-op, must be one of the following: {", ".join(HTTP_METHODS.keys())}'
            )
        return http_method

    def gen_common_prefix(self, xpaths):
        """Get string/xpath that is present in all xpaths"""
        common_prefix = os.path.commonprefix(xpaths)
        tokens = common_prefix.split('/')
        last_element_colon_tokens = tokens[-1].split(':')
        if tokens[-1].find(':') and not len(last_element_colon_tokens[-1]):
            # If the last token only have namespace and not module name, omit from common prefix
            return '/'.join(tokens[:-1])

        return common_prefix

    def replace_keys_with_params(self, xpath):
        """Replace all keys in URL/XPath with RESTCONF-compatible parameters"""
        if '[' not in xpath or ']' not in xpath:
            # Keys are not present
            return xpath

        xpath_tokens = xpath.split('/')
        formatted_tokens = []

        for token in xpath_tokens:
            # Get all keys in XPath token
            keys = XPATH_KEY_RE.findall(token)
            # Find the beginning open brace
            if keys:
                # If there are keys in this token, replace with params
                open_brace_index = token.find('[')
                # Retrieve token without keys inside brackets
                token = token[:open_brace_index]
                # Add in RESTCONF-friendly params
                for i in range(len(keys)):
                    if i == 0:
                        token = '{0}={1}'.format(token, keys[i][1])
                    elif i > 0:
                        token = '{0},{1}={2}'.format(token, keys[i][0], keys[i][1])
            formatted_tokens.append(token)
        # Join all tokens together after splitting by slash
        formatted_xpath = '/'.join(formatted_tokens)

        return formatted_xpath

    def remove_keys(self, xpath, duplicates_only=False):
        """Remove all or only duplicate keys in xpath/URL"""
        if '[' not in xpath or ']' not in xpath or not xpath:
            # Keys are not present or url is empty
            return xpath

        formatted_xpath = xpath

        if duplicates_only:
            # Remove duplicates from tokens and add to processed_tokens when done
            tokens = xpath.split('/')
            processed_tokens = []

            for token in tokens:
                # Find and extract string from between square brackets
                brackets_content = XPATH_BRACKETS_CONTENT_RE.findall(token)

                if len(token) and len(brackets_content):
                    # Map key names to raw key string in token
                    token_keys = {}
                    for content in brackets_content:
                        key = content.split('=')
                        if key[0] not in token_keys.keys() or (key[0] in token_keys.keys() and key[0] != key[1]):
                            token_keys[key[0]] = key[1]
                        # Remove key from token
                        token = token.replace('[{0}={1}]'.format(key[0], key[1]), '')
                    # Re-add valid non-duplicate keys back to token
                    for key in token_keys:
                        token += '[{0}={1}]'.format(key, token_keys[key])
                processed_tokens.append(token)

            formatted_xpath = '/'.join(processed_tokens)

        elif not duplicates_only:
            # Remove all keys from url/xpath
            while '[' in formatted_xpath and ']' in formatted_xpath:
                open_brace_index = formatted_xpath.find('[')
                close_brace_index = formatted_xpath.find(']')

                formatted_xpath = '{0}{1}'.format(
                    formatted_xpath[0:open_brace_index],
                    formatted_xpath[close_brace_index + 1:]
                )

        return formatted_xpath

    @staticmethod
    def replace_or_delete_namespaces(xpath, request_data, mode='replace'):
        """Replace/delete all namespace(s) in URL with module name(s) or """
        valid_modes = ['replace', 'delete']
        namespaces = request_data.get('namespace', None)
        formatted_xpath = xpath

        if namespaces and mode in valid_modes:
            for namespace in namespaces:
                if namespace in xpath:
                    if mode == 'delete':
                        formatted_xpath = formatted_xpath.replace('{0}:'.format(namespace), '')
                    elif mode == 'replace':
                        modulename = namespaces[namespace].split('/')[-1]
                        formatted_xpath = formatted_xpath.replace(namespace, modulename)
        return formatted_xpath

    def gen_url(self, xpath, request_data, returns, http_method):
        """Generate a valid RESTCONF/REST URL"""
        # Base URL will be the start of the URL, appended by remainder URL
        base_url = DEVICE_RESTCONF_ENDPOINT
        # URL that will be appended to base URL
        remainder_url = xpath
        # Result of appending base_url and remainder_url together
        url = ''

        if http_method == 'POST':
            xpath_has_key = True if XPATH_KEY_RE.search(xpath) else False
            substring = self.get_xpath_last_key_substring(remainder_url)
            if xpath_has_key:
                # Remove last key substring from URL
                remainder_url = remainder_url.replace(substring, '')
            else:
                # Keep URL except cut off last slash token
                remainder_url = '/'.join(remainder_url.split('/')[:-1])
        elif http_method == 'GET' and returns:
            tokens = remainder_url.split('/')
            remainder_url = f"/{tokens[0] if tokens[0] else tokens[1]}"

        # Remove duplicate keys
        remainder_url = self.remove_keys(remainder_url, duplicates_only=True)
        # Replace keys in xpath with RESTCONF-compatible parameters
        remainder_url = self.replace_keys_with_params(remainder_url)
        # Transform namespace into module name
        remainder_url = self.replace_or_delete_namespaces(remainder_url, request_data, mode='replace')
        # URL must start at device's RESTCONF endpoint followed by the xpath/remainder of URL
        url = '{0}{1}'.format(base_url, remainder_url)

        return url

    def get_xpath_last_key_substring(self, xpath):
        """ Returns substring of XPath starting from the last occurence of key in it """
        if not XPATH_KEY_RE.search(xpath):
            # No keys in XPath
            return xpath

        return xpath[
            xpath.index(
                next((
                    token for token in reversed(xpath.split('/')) if XPATH_KEY_RE.search(token)
                ))
            ) - 1:
        ]

    def gen_post_method_body(self, xpaths, common_prefix, request_data):
        """Generate a valid RESTCONF/REST body for one xpath compliant with POST method"""
        # Body of all generated xpath bodies merged together
        merged_body = OrderedDict()

        for xpath in xpaths:
            # Get targeted node data
            node_data = self.xpath_to_nodedata[xpath]
            # Body for this xpath to be merged into main body later
            body = OrderedDict()
            xpath_has_key = True if XPATH_KEY_RE.search(xpath) else False
            if xpath_has_key:
                # Get XPath beginning from the last slash token that includes a key
                formatted_xpath = self.get_xpath_last_key_substring(xpath)
                formatted_xpath = self.replace_or_delete_namespaces(formatted_xpath, request_data, mode='delete')

                formatted_xpath_tokens = [token for token in formatted_xpath.split('/') if len(token)]
                reversed_xpath_tokens = list(reversed(formatted_xpath_tokens))

                # Walk through xpath elements from end to beginning and generate nested body dict
                for i in range(len(reversed_xpath_tokens)):
                    token_with_key = reversed_xpath_tokens[i]
                    token = self.remove_keys(token_with_key)
                    # If token has a key, insert key and value into body
                    keys = XPATH_KEY_RE.findall(token_with_key)
                    if i == 0:
                        # Leaf node, set value
                        body[token] = node_data.get('value', '')
                    elif i > 0:
                        if keys:
                            body[token] = [{
                                reversed_xpath_tokens[i - 1]: body[reversed_xpath_tokens[i - 1]]
                            }]
                        else:
                            # Not leaf node, generate nested dicts
                            body[token] = {
                                reversed_xpath_tokens[i - 1]: body[reversed_xpath_tokens[i - 1]]
                            }
                        del body[reversed_xpath_tokens[i - 1]]
                    if keys:
                        # Insert key and values into body
                        for key in keys:
                            body[token][0][key[0]] = key[1]
            elif not xpath_has_key:
                # Last slash token of XPath with namespace removed
                key = self.replace_or_delete_namespaces(xpath.split('/')[-1], request_data, mode='delete')
                # Value set by user
                value = node_data.get('value', '')
                body = OrderedDict({
                    key: value
                })
            merged_body = self.merge_dictionaries(merged_body, body)

        return merged_body

    def gen_body(self, xpaths, common_prefix, request_data, http_method):
        body = OrderedDict()
        if http_method in WITH_BODY_METHODS:
            if http_method == 'POST':
                body = self.gen_post_method_body(xpaths, common_prefix, request_data)
            else:
                body = self.gen_nonpost_method_body(xpaths, common_prefix, request_data)
        return body

    def gen_nonpost_method_body(self, xpaths, common_prefix, request_data):
        """Generate a valid RESTCONF/REST body for one xpath for methods that are not POST, DELETE, or GET"""
        # Body of all generated xpath bodies merged together
        merged_body = OrderedDict()

        for xpath in xpaths:
            # Get targeted node data
            node_data = self.xpath_to_nodedata[xpath]
            body = OrderedDict()

            # Format XPath to remove common prefix (except last slash token), namespaces, and keys
            formatted_xpath = xpath
            # Remove common prefix from xpath, while keeping last element of prefix
            last_elem_omitted_prefix = '/'.join(self.common_prefix.split('/')[:-1])
            formatted_xpath = xpath.replace(last_elem_omitted_prefix, '')
            # Remove namespaces from XPath
            formatted_xpath = self.replace_or_delete_namespaces(formatted_xpath, request_data, mode='delete')
            # Remove duplicate keys from XPath
            formatted_xpath = self.remove_keys(formatted_xpath, duplicates_only=True)

            # Split by slash and reverse xpath elements to build body from leaf to top parent node
            xpath_tokens = [token for token in formatted_xpath.split('/') if len(token)]
            reversed_xpath_tokens = list(reversed(xpath_tokens))
            # Remove keys from XPath and create tokens to set nested dict property names
            keyless_xpath = self.remove_keys(formatted_xpath)
            nodename_tokens = [token for token in keyless_xpath.split('/') if len(token)]
            reversed_nodename_tokens = list(reversed(nodename_tokens))

            for i in range(len(reversed_xpath_tokens)):
                # Walk through XPath token from end to beginning and generate nested body dict
                token = reversed_xpath_tokens[i]
                # Detect and find presence of keys in token
                token_keys = XPATH_KEY_RE.findall(token)
                if i == 0:
                    # Leaf node, set value, use nodename with no keys to set property name
                    body[reversed_nodename_tokens[i]] = node_data.get('value', '')
                elif i > 0:
                    # Not leaf node, generate nested dicts, only use nodename to set dict property
                    body[reversed_nodename_tokens[i]] = {
                        reversed_nodename_tokens[i - 1]: body[reversed_nodename_tokens[i - 1]]
                    }
                    # Add key and value to nested dict body, and remove from XPath token
                    if token_keys:
                        for key in token_keys:
                            # Append key and value to existing nested dict
                            body[reversed_nodename_tokens[i]] = {
                                **body[reversed_nodename_tokens[i]],
                                key[0]: key[1],
                            }
                    # Delete child node, we have appended it to the parent node above
                    del body[reversed_nodename_tokens[i - 1]]
            # Merge generated body to merged bodies to return
            merged_body = self.merge_dictionaries(merged_body, body)

        return merged_body

    def merge_dictionaries(self, a, b, path=None):
        "Merge dictionary b into dictionary a"
        if path is None:
            path = []
        for key in b:
            if key in a:
                if isinstance(a[key], dict) and isinstance(b[key], dict):
                    # If a and b are dicts, continue merging
                    self.merge_dictionaries(a[key], b[key], path + [str(key)])
                elif a[key] == b[key]:
                    # Do not merge dicts with same values
                    pass
                else:
                    raise Exception('Conflict at %s' % '.'.join(
                        path + [str(key)]
                    ))
            else:
                a[key] = b[key]
        return a


if __name__ == "__main__":  # pragma: no cover
    import doctest
    doctest.testmod()
