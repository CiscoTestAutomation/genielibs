import re
import logging
import ast
from genie.utils.dq import Dq
log = logging.getLogger()


def load_saved_variable(self, val, key=None):
    # Replace %VARIABLES{variables} with saved variables
    p = re.compile(r'%VARIABLES+\{(?P<var_name>[\w\s+-_.]+)\}')
    group = {}
    m = re.finditer(p, val)
    match_counter = 0
    for item in m:
        group.update({val[item.start():item.end()]:
        item.groupdict()['var_name']})
        match_counter +=1

    for blitz_key, blitz_val in group.items():
        if match_counter > 1 or blitz_key != val:
            val = val.replace(blitz_key, \
                str(self.parameters['save_variable_name'][blitz_val]))
        else: 
            val = self.parameters['save_variable_name'][blitz_val]

    return key, val
    
def find_saved_variable(**arguments):
    # Rotating throught the key:value pairs, either returning the dictionary
    # OR sending it to load_saved_variable to replace vairables.
    self = arguments.pop('self')
    ret_dict = {}
    for key, val in arguments.items():

        if isinstance(val, int) or isinstance(val, float) or val == None:
            ret_dict.update({key:val})
        elif isinstance(val, str):
            key, val = load_saved_variable(self, val, key)
            ret_dict.update({key:val})
        elif isinstance(val, list):
            rotate_list = []
            for item in val:
                kwargs = {'self': self}
                if isinstance(item, dict):
                    kwargs.update(item)
                    rotate_list.append((find_saved_variable(**kwargs)))
                else:
                    kwargs.update({key:item})
                    rotate_list.append((list(find_saved_variable(**kwargs).values())[0]))

            ret_dict.update({key:rotate_list}) 
        elif isinstance(val, dict):
            kwargs = {'self':self}
            kwargs.update(val)
            ret_dict.update({key:find_saved_variable(**kwargs)})

    return ret_dict

def filter_variable(self, output, save=None):
    #filtering the action output
    if not save or 'filter' not in save:
        return output

    if not isinstance(output, dict):
        return output

    p = re.compile(r'(?P<function>[\S\s]+)\((?P<arguments>[\S\s]+)\)')
    try :
        dq_output = Dq(output)
    except Exception as e:
        log.errored('Issue creating filtering object, as the output is not as expected, {}'.format(str(e)))
    
    filters = save.get('filter')
    filters_list= filters.split('.')
    for filter in filters_list:
        # Will never go in the first time, as dq_output is created above
        # If subsequent aren't a Dq object, than fail
        if not isinstance(dq_output, Dq):
            raise Exception('The output of the previous function does not'
                            ' provide the appropriate input for the next function ==> {}'.format(previous_filter))
    
        m = p.match(filter)
        if m:
            function = m.groupdict()['function']
            # Finding the *args and **kwargs with the help of ast.parse
            tree = ast.parse("f({})".format(m.groupdict()['arguments']))
            funccall = tree.body[0].value
            args = [ast.literal_eval(arg) for arg in funccall.args]
            kwargs = {arg.arg: ast.literal_eval(arg.value) for arg in funccall.keywords}

            # Calling the function
            dq_output = getattr(dq_output, function)(*args, **kwargs) 

        previous_filter = filter
    return dq_output.reconstruct() if isinstance(dq_output, Dq) \
        else dq_output

def get_variable(**kwargs):
    # Get the variable that will be replaced/unload
    self = kwargs.get('self')
    device = kwargs.pop('device', None)
    _kwargs = find_saved_variable(**kwargs)
    if device:
        _kwargs.update({'self': self, 'device': device})
    else:
        _kwargs.update({'self': self})
    return _kwargs

def save_variable(self, output, save_variable_name=None):
    # Save output variable
    if save_variable_name:
        self.parameters.setdefault('save_variable_name',{}) 
        self.parameters['save_variable_name'].update({save_variable_name:output})
        return output, save_variable_name
    
    return None


