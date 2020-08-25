import json
import random
import string
from genie.libs.sdk.triggers.blitz.maple_converter.legacy_maple_converter import Internal_Converter

class Legacy_DME_Converter(Internal_Converter):
    
    def __init__(self, command, maple_action):

        self.command = command
        self.maple_action = maple_action
    
    def legacy_dme_to_maple_plugin_converter(self):

        ''' layout of the legacy dme input

            confirm/apply/unapply:    <-- maple_action
                 devices:
                    N93_3:
                        rule-1: (Optional)
                            type: dmerest
                            commands: |
                                post,,http://ott-ads-019:8025/api/mo/sys/fm/mplssgmntrtg.json,,fmMplsSgmntRtg,,adminSt||enabled     <-- post legacy dme call with no payload file
                                <method: "POST">,,<url>,,<root name of the json paylod>,, <payload dictionary info>
                                
                                post,,http://ott-ads-019:8025/api/mo/sys/fm/mplssgmntrtg.json,,payload.json            <-- post/put/get legacy dme call with a payload/schema file
                                <method: "POST"|PUT|GET>,,<url>,,<json payload_file OR json schema_file>
                                
                                get,,http://ott-ads-019:8025/api/mo/sys/fm/mplssgmntrtg.json                        <-- delete/get legacy dme call
                                <method: "DELETE"|get>,,<url>

            ================================================================================
            Example of dme maple plugins:

            confirm:    <-- maple_action
                devices:
                    N93_3:
                        rule-1:
                            type: dmerest
                            commands: |
                                #@# command:{
                                    "method":"processdme",
                                    "options":[
                                        {"method":"POST"|"GET"|"PUT"|"DELETE"}, 
                                        {"url":<url>}
                                        {"payload"|"schema": <payload or schema file>}          <-- Optional
                                    ]} 
                                #@#
            _____________________________
            Function description: This function recieves a legacy dme input of maple and generates
                                  dme maple plugin

            note: 
                1) post/put dme calls are always inside apply action
                2) delete dme calls are always inside unapply action
                3) get dme calls are always inside confirm actions

            args:
                command: a string represneting the legacy dme input post,,http://ott-ads-019:8025/api/mo/sys/fm/mplssgmntrtg.json,,fmMplsSgmntRtg,,adminSt||enabled 
                        datatype: str

                maple_action: the maple action whether apply, unapply, confirm
                        datatype: str

            returned value: 
            type(list): a list containing equivalents of dme maple plugins inputs. such as:
                ['{"method":"POST"}', '{"url": "http://ott-ads-019:8025/api/mo/sys/fm/mplssgmntrtg.json"}, '{"payload": <payload_name>.json}']
        '''

        list_of_methods = ['get', 'delete', 'put', 'post']

        # splitting the legacy command into a list 
        command_list = self.command.split(',,')

        # The first item of the list is always and it should be method 
        method = command_list[0]
        if method.lower() not in list_of_methods:
            raise Exception('The method {} is not valid rest method'.format(method))

        # method and url as arguments are common between all the methods
        command_list[0] = '{{"method":"{}"}},\n'.format(command_list[0].upper())
        command_list[1] = '{{"url":"{}"}},\n'.format(command_list[1])

        if self.maple_action == 'apply' or self.maple_action == 'unapply':

            # If the size of splitted list is 4 
            # Then the payload is manually inputed and needs 
            # to be converted into Json and saved into a file
            if len(command_list) == 4:

                # Dictionary name
                object_name = command_list[2]

                # TODO - complete commenting

                # Translating list items 2 and 3 into an actual payload.json
                values = command_list[3]
                values = values.replace('||','=')
                values=values.split('~~')
                _dict = {k:v for k,v in (x.split('=') for x in values)}
                payload = {object_name: {
                        "attributes": _dict
                    }
                }
                # Give the Json file a random name
                letters = string.ascii_lowercase
                payload_name = ''.join(random.choice(letters) for i in range(6)) + '.json'

                # TODO use context manager
                # writing the json into the actual file
                payload_file = open(payload_name, 'a') 
                payload_file.write(json.dumps(payload))
                payload_file.close()
            
                # resizing the initial command list adding the payload file as the last item of the list 
                command_list = command_list[0:2]
                command_list.append(payload_name)

            # methods put/post should have a payload file 
            if method == 'put' or method == 'post':
                
                try:
                    command_list[2] = '{{"payload":"{}"}},\n'.format(command_list[2])
                except Exception as e:
                    raise (str(e))

            if len(command_list) == 3 and method == 'delete':
                command_list[2] = '{{"ignore_error":"{}"}},\n'.format(command_list[2])
        else:
            if len(command_list) == 3:
                command_list[2] = '{{"schema":"{}"}},\n'.format(command_list[2])

        return self.legacy_cmds_to_maple_plugin_converter('processdme', command_list)

