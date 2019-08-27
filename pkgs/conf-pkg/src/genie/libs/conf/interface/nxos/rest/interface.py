from genie.conf.base.config import RestConfig
from ..interface import Interface as InterfaceCli


class Interface(InterfaceCli):
    def build_config(self, apply=True, unconfig=False,
                     **kwargs):

        # Get the cli output from Cli Interface
        output = InterfaceCli.build_config(self=self,
                                           apply=False,
                                           unconfig=unconfig,
                                           **kwargs)

        # Get the straight cli from the Config object
        output = '\n'.join(output.cli_config)

        # Add the necessary lines in front and at the end
        output = '{pri}\n{output}\n{show}'.format(\
                  output=output,
                  pri='configure private sandbox',
                  show='show configuration session nx-api rest')

        if apply:
            out = RestConfig(device=self.device, unconfig=unconfig,
                             cli_payload=output, dn='api/mo/sys.json',
                             partition='nx-api rest')
            out.apply()
        else:
            return RestConfig(device=self.device, unconfig=unconfig,
                              cli_payload=output, dn='api/mo/sys.json',
                              partition='nx-api rest')