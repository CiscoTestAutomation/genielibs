# python
import re

# super class
from genie.libs.ops.platform.nxos.rev1.platform import Platform as NxosPlatform

class Platform(NxosPlatform):
    '''Platform Ops Object'''
    show_module = 'show module'
    show_module_revision = '1'
    show_inventory = 'show inventory'
    show_inventory_option = ''