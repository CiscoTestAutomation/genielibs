''' 
ARP Genie Ops Object for IOSXR - CLI.
'''
import copy

# super class
from genie.libs.ops.arp.arp import Arp as SuperArp

# Parser
from genie.libs.parser.iosxr.show_arp import ShowArpDetail, \
											 ShowArpTrafficDetail

from genie.libs.parser.iosxr.show_interface import ShowIpv4VrfAllInterface


class Arp(SuperArp):
	'''ARP Genie Ops Object'''

	def learn(self):
		'''Learn ARP Ops'''

		########################################################################
		#                               info
		########################################################################

		src_global = '[interfaces][(?P<interfaces>.*)][ipv4][neighbors]'\
			'[(?P<neighbors>.*)]'
		dest_global = 'info[interfaces][(?P<interfaces>.*)][ipv4][neighbors]'\
			'[(?P<neighbors>.*)]'

		# Missing keys: 'remaining_expire_time'
		# 'ip'
		self.add_leaf(cmd=ShowArpDetail,
					  src=src_global + '[ip]',
					  dest=dest_global + '[ip]')

		# 'link_layer_address'
		self.add_leaf(cmd=ShowArpDetail,
					  src=src_global + '[link_layer_address]',
					  dest=dest_global + '[link_layer_address]')

		# 'origin'
		self.add_leaf(cmd=ShowArpDetail,
					  src=src_global + '[origin]',
					  dest=dest_global + '[origin]')

		src_interface = '[(?P<intf>.*)][ipv4]'
		dest_interface = 'info[interfaces][(?P<intf>.*)][arp_dynamic_learning]'

		# Missing keys: 'local_proxy_enable'
		# 'proxy_enable'
		self.add_leaf(cmd=ShowIpv4VrfAllInterface,
					  src=src_interface + '[proxy_arp]',
					  dest=dest_interface + '[proxy_enable]')

		src_stat = '[(?P<module>(0/0/CPU0))][statistics]'
		dest_stat = 'info[statistics]'

		# Missing keys: 'in_total', 'in_gratuitous_pkts', 'all_dynamic_pkts',
		# 'all_static_pkts', 'in_drops', 'out_drops', 'out_total'
		req_key = ['in_replies_pkts', 'in_requests_pkts',\
				   'out_requests_pkts', 'out_replies_pkts',\
				   'out_gratuitous_pkts', ]

		for key in req_key:
			self.add_leaf(cmd=ShowArpTrafficDetail,
						  src=src_stat + '[{}]'.format(key),
						  dest=dest_stat + '[{}]'.format(key))

		self.make(final_call=True)

		# Parser return a string and 'proxy_arp' attribute is a boolean
		if hasattr(self, 'info') and 'interfaces' in self.info:
			for intf in self.info['interfaces']:
				if 'arp_dynamic_learning' in self.info['interfaces'][intf] and \
					'proxy_enable' in self.info['interfaces'][intf]\
					['arp_dynamic_learning']:
					if self.info['interfaces'][intf]['arp_dynamic_learning']\
						['proxy_enable'] == 'disabled':
						self.info['interfaces'][intf]['arp_dynamic_learning']\
							['proxy_enable'] = False
					else:
						self.info['interfaces'][intf]['arp_dynamic_learning']\
							['proxy_enable'] = True