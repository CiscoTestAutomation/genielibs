import re
import logging
import os
from genie.utils.dq import Dq
from pyats.datastructures import AttrDict
from pyats.easypy import runtime

log = logging.getLogger(__name__)


def apply_dictionary_filter(self, output, filters=None):
    #filtering the action output
    if not filters or \
       not isinstance(output, dict) or \
       not Dq.query_validator(filters):
        return output

    return Dq.str_to_dq_query(output, filters)


def apply_regex_filter(self, output, filters=None):
    # Applying regex filter to execute output
    if not filters:
        return output

    if not isinstance(output, str):
        raise Exception("regex filter can be applied only to string output.")

    pattern = re.compile(filters)
    match = re.search(pattern, output)

    if match:
        return match.groupdict()

    return {k: '' for k in pattern.groupindex.keys()}


def apply_regex_findall(self, output, pattern=None):
    # Applying regex pattern to execute output
    if not pattern:
        return output

    if not isinstance(output, str):
        raise Exception("regex findall can only be applied to string output.")

    pattern = re.compile(pattern)
    return re.findall(pattern, output)


def apply_list_filter(self, output, list_index=None, filters=None):

    if not list_index and not filters:
        return output

    # If the index of the value that wants to be saved is known
    if isinstance(list_index, int):
        try:
            output = output[list_index]
        except IndexError as e:
            raise IndexError(e)
        else:
            return output

    # For slicing : "[1:9]"
    elif isinstance(list_index, str):
        slice_indices = list_index.strip('][').split(':')

        # in case of "[2]" raise exception
        if len(slice_indices) != 2:
            raise Exception(
                "Please check input {input}".format(input=list_index))

        # in case input is like [:8]
        if not slice_indices[0]:
            slice_indices[0] = 0

        # in case input is like [2:]
        if not slice_indices[1]:
            slice_indices[1] = len(output)

        try:
            sliced_output = output[int(slice_indices[0]):int(slice_indices[1])]
        except ValueError as e:
            raise ValueError(e)
        else:
            if not sliced_output:
                log.warning("The sliced outputs are empty.")

            return sliced_output

    # if checking if a value or a regex to a value exist
    # match those items, and return a list of items
    list_of_matches = []
    for item in output:
        pattern = re.compile(str(filters))
        match = re.fullmatch(pattern, str(item))
        if match:
            list_of_matches.append(item)

    # if only one item in the list of matches, just get that output,
    # else get the entire list
    return list_of_matches


def get_variable(**kwargs):

    self = kwargs.get('self')
    section = kwargs.get('section')
    _kwargs = _find_saved_variable(**kwargs)
    _kwargs.update({'self': self, 'section': section})
    log.debug('return of get_variable: {}'.format(_kwargs))
    return _kwargs


def _find_saved_variable(**kwargs):
    # Rotating through the key:value pairs, either returning the dictionary
    # OR sending it to load_saved_variable to replace vairables.
    log.debug('_find_saved_variable kwargs: {}'.format(kwargs))
    self = kwargs.pop('self')
    if hasattr(kwargs['section'], 'uid'):
        section = kwargs.pop('section')
    else:
        # a case which API has argument 'section', but not section object
        section = kwargs['section']
    # The dictionary as output with markups replaced/loaded
    ret_dict = {}
    for key, val in kwargs.items():

        # if string than we will check if we could load any of the saved data in it
        if isinstance(val, str):
            key, val = _load_saved_variable(self, section, val, key)
            ret_dict.update({key: val})

        # if dictionary, then necessary to go to through every level recursively to check if any replacement is necessary
        elif isinstance(val, dict):
            kwargs = {'self': self, 'section': section}
            kwargs.update(val)
            ret_dict.update({key: _find_saved_variable(**kwargs)})

        # for the list, just going through every item in it and call back this function with those values
        elif isinstance(val, list):
            rotate_list = []
            for item in val:
                kwargs = {'self': self, 'section': section}
                if isinstance(item, dict):
                    kwargs.update(item)
                    rotate_list.append((_find_saved_variable(**kwargs)))
                else:
                    kwargs.update({key: item})
                    rotate_list.append(
                        (list(_find_saved_variable(**kwargs).values())[0]))
            ret_dict.update({key: rotate_list})

        # if the dict as input is digit or its not, it goes directly back to the return dictionary
        else:
            ret_dict.update({key: val})

    log.debug('return of _find_saved_variable: {}'.format(ret_dict))
    return ret_dict


def _load_saved_variable(self, section, val, key=None):
    orig_val = val
    # Replace %VARIABLES{variables} with saved variables
    p = re.compile(r'%VARIABLES+\{(?P<var_name>[^{}]+)\}')
    group = {}
    m = re.finditer(p, val)

    for item in m:
        markup_string = val[item.start():item.end()]
        var_name = item.groupdict()['var_name']
        group.update({markup_string: var_name})

    # for pyATS Health Check
    # use section.parent for self.parent
    if not hasattr(self.parent, 'parameters'):
        self.parent = section.parent

    for blitz_key, blitz_val in group.items():

        # if input with testscript. then var is saved in self.parent.parameters
        if 'testscript.' in blitz_val and \
            blitz_val != 'testscript.name':
            saved_vars_dict = self.parent.parameters.setdefault(
                'save_variable_name', {})

        # else it is self.parameters
        else:
            saved_vars_dict = self.parameters.setdefault(
                'save_variable_name', {})

        #  Access object properties, list index, or dictionary value using key
        # '%VARIABLES{interface[0].name}'
        # '%VARIABLES{interface.name}'
        # '%VARIABLES{interface['name']}'
        if ('.' in blitz_val or '[' in blitz_val) and\
           blitz_val not in self.parameters['save_variable_name']:

            # handling for `health_settings.devices`. TODO; AttrDict support
            if blitz_val != 'testscript.health_settings.devices':
                var_value = _load_chained_saved_vars(saved_vars_dict,
                                                     blitz_val)
            else:
                var_value = saved_vars_dict['testscript'].setdefault(
                    'health_settings.devices', {})
        else:
            try:
                var_value = saved_vars_dict[blitz_val]
            except KeyError:
                var_value = None

        if blitz_key == val:
            val = var_value
        else:
            var_value = str(var_value).strip()
            if var_value:
                val = val.replace(blitz_key, var_value)
            else:
                val = val.replace(blitz_key, '')

    log.debug("{} resolved to '{}'".format(orig_val, val))
    return key, val


def _load_chained_saved_vars(last_attr, reuse_var_name):
    """getting the value of chained saved variables
       input:
            last_attr: dict to search. Either [self.parameters or self.parent.parameters]
            reuse_var_name: variable name that will be reused
       output:
            returns the value of the chained saved variable accordingly

       example:
            %VARIABLES{function.attribute}
            resue_var_name: function_var_name
            last_attr self.parameters

            %VARIABLES{testscript.name}
            resue_var_name: testscript.name
            last_attr self.parent.parameters
    """
    # split variable name on "." and "["
    # to be able to parse list or dict, or objects with attributes
    chained_var_list = re.split(r'[\.\[]', reuse_var_name)
    for attr in chained_var_list:

        if ']' in attr:
            attr = attr.replace(']', '')
            attr = int(attr) if attr.isdigit() else attr

        try:
            last_attr = last_attr[attr]
        except TypeError:
            if hasattr(last_attr, attr):
                last_attr = getattr(last_attr, attr)
            else:
                log.debug(
                    "The value {} is not supporting such attribute {}".format(
                        last_attr, attr))
                last_attr = ''
                break
        except KeyError:
            if attr in ['_keys', '_values']:
                temp_value_holder = getattr(last_attr, attr.replace('_', ''))()
                last_attr = next(iter(temp_value_holder))
            else:
                log.debug("The key '{}' doesn't exist in {}".format(
                    attr, last_attr))
                last_attr = ''
                break

    return last_attr


def save_output_to_file(file_name, file_content, append_to_file=False):
    """
    Saves the output of an action to a file.

    Args:
        file_name: (str) The name of the file
        file_content: (str|dict|list) The output of an action
        append_to_file: (str|bool) If the output should be saved to a file in append or write mode
    """

    if append_to_file in (True, 'True'):
        mode = 'a'
    elif append_to_file in (False, 'False'):
        mode = 'w'
    else:
        raise Exception(
            'Given append value unsupported! Supported values: True, False')

    try:
        # save to current working directory
        file_path = os.path.join(runtime.directory, file_name)
        with open(file_path, mode) as f:
            # add a linebreak to separate from other outputs
            f.write(str(file_content) + '\n')
        log.info('Action output saved to: {}'.format(file_path))
    except Exception as e:
        log.error('Failed to write file {}'.format(file_name))
        log.error(e)
        return


def save_variable(self,
                  section,
                  save_variable_name,
                  output=None,
                  append=None,
                  append_in_list=None,
                  append_in_dict=None):

    # for pyATS Health Check
    # use section.parent for self.parent
    if not hasattr(self.parent, 'parameters'):
        self.parent = section.parent

    # Save output variable
    self.parameters.setdefault('save_variable_name', {})
    self.parent.parameters.setdefault('save_variable_name',
                                      AttrDict({'testscript': AttrDict({})}))

    save_variable_name_str = save_variable_name

    # if testscript. lets save in a global level
    if 'testscript.' in save_variable_name and \
        save_variable_name != 'testscript.name':

        # using AttrDict to save in parent and to retrieve
        save_variable_name = save_variable_name.replace('testscript.', '')
        saved_vars = self.parent.parameters['save_variable_name'].setdefault(
            'testscript', {})
    else:
        saved_vars = self.parameters['save_variable_name']

    if save_variable_name in saved_vars:

        saved_val = saved_vars[save_variable_name]
        if append:
            if output:
                saved_vars.update(
                    {save_variable_name: saved_val + '\n' + output})
                log.debug(
                    'Appended the following into the variable {},  {}'.format(
                        save_variable_name_str, str(output)))

        elif append_in_list:
            if isinstance(saved_val, list):
                saved_val.append(output)
                saved_vars.update({save_variable_name: saved_val})
                log.debug('Appended {} to list variable {}'.format(
                    str(output), save_variable_name_str))

        elif append_in_dict:
            if isinstance(saved_val, dict):
                saved_val.update(output)
                saved_vars.update({save_variable_name: saved_val})
                log.debug('Appended {} to dict variable {}'.format(
                    str(output), save_variable_name_str))
        else:
            saved_vars.update(
                {save_variable_name: output if output is not None else ''})
            log.debug('Saved {} in variable {}'.format(str(output),
                                                       save_variable_name_str))
    elif append_in_list:
        saved_vars.update({save_variable_name: [output]})
        log.debug('Saved {} in list variable {}'.format(
            str(output), save_variable_name_str))
    else:
        saved_vars.update(
            {save_variable_name: output if output is not None else ''})
        log.debug('Saved {} in variable {}'.format(str(output),
                                                   save_variable_name_str))