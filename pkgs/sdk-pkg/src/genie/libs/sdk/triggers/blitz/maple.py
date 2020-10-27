import re
import os
import sys
import json
import inspect
import logging
import importlib

from os.path import expanduser
from collections import OrderedDict
from pyats.datastructures import AttrDict

from genie.utils import Dq

from .markup import save_variable
from .actions_helper import _output_query_template

log = logging.getLogger()


def maple(self, steps, device, maple_plugin_input, maple_action=None, output=None, include=None, exclude=None, continue_=True, **kwargs):

    '''
        3 types of maple plugins exist: 
            1) confirm
            2) matcher
            3) command
        
        Example of converting maple plugins into equivalent blitz action
        apply:
            devices:
                N93_3:
                    type: dmerest
                    commands: |
                        #@# command:{       <-- plugin_type  (command|matcher|confirm)
                            "method":"processdme",
                            "options":[
                                {"method":"GET"},
                                {"url":"http://ott-ads-019:8025/api/mo/sys/fm/mplssgmntrtg.json"}
                            ]} 
                        #@#
        ==================================================================================
        Blitz equivalent of the abovementioned command maple plugin
        - maple:
            # maple_plugin_input keyword below is section dict containing all the maple_action information and is input to blitz code  
            
            maple_plugin_input: '{"type": "dmerest", "commands":   < -- string representation of the dictionary representation of the maple_plugin with maple_action_type and rule_id for use in blitz
                        "command:{\n
                            \"method\":\"processdme\",\n
                            \"options\":[\n
                                        {\"method\":\"GET\"},\n
                                        {\"url\":\"http://ott-ads-019:8025/api/mo/sys/fm/mplssgmntrtg.json\"}\n
                                        ]}"}'
            
            device: N93_3
            maple_action: apply <-- necessary for blitz
            save:
            - variable_name: my_variable
              append: true
            continue: false
    '''

    '''
    Example of maple_plugin_input:
    maple_plugin_input: '{"type": "dmerest", "commands":   < -- string representation of the dictionary representation of the maple_plugin with maple_action_type and rule_id for use in blitz
            "command:{\n
                \"package\":\"CommandPlugins\",\n
                \"method\":\"processdme\",\n
                \"options\":[\n
                            {\"method\":\"GET\"},\n
                            {\"url\":\"http://ott-ads-019:8025/api/mo/sys/fm/mplssgmntrtg.json\"}\n
                            ]}"}'
    '''
    # cast the maple_plugin_input input into json_data
    # maple_plugin_input keyword of the yaml file is dictionary casted as string
    maple_plugin_input = json.loads(maple_plugin_input, object_pairs_hook=OrderedDict)
    plugin_extract = re.compile(r'(?P<plugin_type>\w+):{(?P<plugin_data>[\S\s]+)}')

    # extracting 'commands' keyword in maple_plugin_input and match it with above regex
    # Plugin_type == command|matcher|confirm
    # plugin_data == info that'd be used int maple code
    m = plugin_extract.match(Dq(maple_plugin_input).get_values('commands', index=0))
    matched_group = m.groupdict()
    json_data_str = "{{{}}}".format(matched_group['plugin_data'])
    plugin_data = json.loads(json_data_str)



    # package extracted form plugin_data, containing the package that contains maple plugin
    package = plugin_data.pop('package', None)
    # maple plugin function name
    method = plugin_data.pop('method', None)
    # if there the class that contains maple plugin method
    _class = plugin_data.pop('class', None)

    # if no method to call raise the exception
    if not method:
        raise Exception('No method was provided to call')

    # objects == kwargs to the maple plugin method which mostly coming from maple_plugin_input 
    # plugin_source contains the package that plugin is in (e.g CommandPlugins, MatcherPlugins etc)
    # It is possible that the plugin_source is a class as well
    objects, plugin_source = _maple_plugins_input(self, steps, device, plugin_data, maple_action,
                                                  matched_group, maple_plugin_input, package, method, _class=_class, output=output)
    
    # if plugin_source is class create an object of that class 
    # store its name in plugin_source_print_str
    if inspect.isclass(plugin_source):
        plugin_source_print_str = plugin_source.__name__
        plugin_source = plugin_source()

    # if plugin_source only a module
    # Only store its name in plugin_source_print_str
    # replace package name in module name and strip all the "." the name of the module would be stored
    else:
        plugin_source_print_str = plugin_source.__name__.replace(plugin_source.__package__, '').strip('.')

    # Calling the maple method
    with steps.start("Calling method '{m}' from maple plugin '{p}' on '{d}'".\
                      format(m=method, p=plugin_source_print_str, d=device.name), continue_=continue_) as step:

        # calling the function in the plugin
        # receveing the output of the plugin method
        ret_value = getattr(plugin_source, method)(objects)

        # matchObjs in maple == save_variable_name in blitz
        # ixiaObjs in maple is saving ixia values in maple
        # still storing as same as save_variable_name
        # They need to be extracte from ret_value and store 
        # in self.parameters['save_variable_name']
        if 'matchObjs' in ret_value:
            for key, val in ret_value['matchObjs'].items():
                save_variable(self, key, val)
        if 'ixiaObjs' in ret_value:
            for key, val in ret_value['ixiaObjs'].items():
                if val != {}:
                    save_variable(self, key, val)

        # checking if there is a results that needs to be used 
        # to pass or fail the action
        if 'result' in ret_value:
            if matched_group['plugin_type'] == 'confirm':
                result = ret_value['result']
            if matched_group['plugin_type'] == 'command':
                result = ret_value['result'][0]
            if result == True:
                step.passed()
            else:
                step.failed()

    return ret_value.get('output')

def _maple_plugins_input(self, steps, device, plugin_data, maple_action,
                         matched_group, maple_plugin_input, package, method, _class=None, output=None):

    # kwargs to the maple plugin method
    objects= {}
    testbed = self.parameters['testbed'] 
    saved_vars = self.parameters.get('save_variable_name', {})

    # populating the objects dictionary to be send as inputs to plugins
    objects.update(plugin_data)
    objects.update({'testbed': testbed, 'uut': device, 'matchObjs': saved_vars})

    if maple_action:
        objects.update({'type': maple_action})

    # populating rest of the data that needs to be in objects
    # they have to extractd from plugin_data
    if 'options' in plugin_data:
        for option in plugin_data['options']:
            objects.update(option)

    # determining the plugin to be called as inputted
    # Or sending to default commands class that contains various plugins
    if package:

        try:
            # if package exist and no class
            plugin_source = importlib.import_module(package.replace('maple.', ''))

            # if _class then plugin_source equal that class
            if _class:
                plugin_source = getattr(plugin_source, _class)
        except Exception:
            raise ("package provided {} is not a valid package".format(package))

    # if no package provided
    # default package is plugins.system.Commands
    else:
        plugin_source = importlib.import_module('plugins.system.Commands')

    if not hasattr (plugin_source, method):
        raise Exception('The method')

    # Each plugin might have an input tailord to itself
    # adjusting the plugin specific inputs.
    if matched_group['plugin_type'] == 'command':
        objects.update({'section': maple_plugin_input})
        # command plugins want the string value of maple_plugin_input as an input

    elif matched_group['plugin_type'] == 'matcher':

        # matcher plugins should execute a command
        # before calling the plugin and plugins should receive that 
        # show command output as an input
        if 'command' in plugin_data:
            try:
                output = device.execute(plugin_data['command'])
                objects.update({'output': output})
            except Exception:
                steps.failed('No output was generated of the command provided')
        else:
            steps.failed('No command provided, action failed')


    elif matched_group['plugin_type'] == 'confirm':
        if output:
            objects.update({'output': output})
    
    # further adjustments are necessary for ixianative
    if device.type == 'ixia':
        objects = _ixia_add_on(self, objects, device)

    return objects, plugin_source

def _ixia_add_on(self, objects, device):

    # saving the ixia saved variables (that is different than normal saved variables)
    # into the objects that would be the input to the plugin
    objects.setdefault('ixiaObjs', {})
    objects['ixiaObjs'].setdefault('ixiaNet', {})
    objects['ixiaObjs'].setdefault('ixiaNetSelf', {})
    objects['ixiaObjs'].setdefault('ixiaNetStop', {})

    # if an ixiaNet object was provided from previous ixia plugin calls it is stored
    # they should be passed into the plugin as input
    if 'save_variable_name' in self.parameters and 'ixiaNet' in self.parameters['save_variable_name']:
        objects['ixiaObjs']['ixiaNet'].update(self.parameters['save_variable_name']['ixiaNet'])

    if 'save_variable_name' in self.parameters and 'ixiaNetSelf' in self.parameters['save_variable_name']:
        objects['ixiaObjs']['ixiaNetSelf'].update(self.parameters['save_variable_name']['ixiaNetSelf'])

    if 'save_variable_name' in self.parameters and 'ixiaNetStop' in self.parameters['save_variable_name']:
        objects['ixiaObjs']['ixiaNetStop'].update(self.parameters['save_variable_name']['ixiaNetStop'])

    return objects

def maple_search(self, steps, search_string, device, continue_=True, include=None, exclude=None, **kwargs):

    log.info(search_string)
    return _output_query_template(self, search_string, steps, device, command=None,
                                  include=include, exclude=exclude, max_time=None, 
                                  check_interval=None, continue_=continue_, action='maple_search')