''' 
RoutePolicy Genie Ops Object for NXOS - CLI.
'''


from genie.libs.ops.route_policy.route_policy import RoutePolicy as SuperRoutePolicy

# nxos show_route_map
from genie.libs.parser.nxos.show_route_map import ShowRouteMap


class RoutePolicy(SuperRoutePolicy):
    '''RoutePolicy Genie Ops Object'''

    def learn(self):
        '''Learn RoutePolicy Ops'''

        self.add_leaf(cmd=ShowRouteMap,
                      src='[(?P<policy>.*)][description]',
                      dest='info[(?P<policy>.*)][description]')

        #####################################################################
        #                        Statements section
        #####################################################################

        # Place holder to make it more readable
        src = '[(?P<policy>.*)][statements][(?P<statements>.*)]'
        dest = 'info[(?P<policy>.*)][statements][(?P<statements>.*)]'

        #####################################################################
        #                        Section "conditions"
        #####################################################################

        self.add_leaf(cmd=ShowRouteMap,
                      src=src+'[conditions]',
                      dest=dest+'[conditions]')

        #####################################################################
        #                        Section "actions"
        #####################################################################

        self.add_leaf(cmd=ShowRouteMap,
                      src=src+'[actions]',
                      dest=dest+'[actions]')

        self.make(final_call=True)

        if hasattr(self, 'info'):
            # Delete 'clause' under every statement 'actions' key
            for key in self.info:
              for key2 in self.info[key]['statements']:
                del self.info[key]['statements'][key2]['actions']['clause']

            # Delete 'set_route_origin' under every statement 'actions' key
            for key in self.info:
              for key2 in self.info[key]['statements']:
                if 'set_route_origin' in self.info[key]['statements'][key2]['actions']:
                  del self.info[key]['statements'][key2]['actions']['set_route_origin']
