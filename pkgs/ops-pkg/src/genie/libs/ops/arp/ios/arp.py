''' 
ARP Genie Ops Object for IOS - CLI.
'''
import copy

# super class
from genie.libs.ops.arp.arp import Arp as SuperArp

# Parser
from genie.libs.parser.ios.show_arp import ShowIpArp, \
										   ShowIpArpSummary, \
										   ShowIpTraffic

from genie.libs.parser.ios.show_interface import ShowIpInterface
from genie.libs.parser.ios.show_vrf import ShowVrf


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
		self.add_leaf(cmd=ShowIpArp,
					  src=src_global + '[ip]',
					  dest=dest_global + '[ip]')

		# 'link_layer_address'
		self.add_leaf(cmd=ShowIpArp,
					  src=src_global + '[link_layer_address]',
					  dest=dest_global + '[link_layer_address]')

		# 'origin'
		self.add_leaf(cmd=ShowIpArp,
					  src=src_global + '[origin]',
					  dest=dest_global + '[origin]')

		self.add_leaf(cmd=ShowVrf,
					  src='vrf[(?P<vrf>.*)][interfaces]',
					  dest='info[vrf][(?P<vrf>.*)][interfaces]')
		# save to cache
		self.make()
		if hasattr(self, 'info') and 'vrf' in self.info:
			for vrf in self.info['vrf']:
				self.add_leaf(cmd=ShowIpArp,
							  src=src_global + '[ip]',
							  dest=dest_global + '[ip]',
							  vrf=vrf)

				# 'link_layer_address'
				self.add_leaf(cmd=ShowIpArp,
							  src=src_global + '[link_layer_address]',
							  dest=dest_global + '[link_layer_address]',
							  vrf=vrf)

				# 'origin'
				self.add_leaf(cmd=ShowIpArp,
							  src=src_global + '[origin]',
							  dest=dest_global + '[origin]',
							  vrf=vrf)
			del (self.info['vrf'])
		src_interface = '[(?P<intf>.*)]'
		dest_interface = 'info[interfaces][(?P<intf>.*)][arp_dynamic_learning]'

		# 'local_proxy_enable'
		self.add_leaf(cmd=ShowIpInterface,
					  src=src_interface + '[local_proxy_arp]',
					  dest=dest_interface + '[local_proxy_enable]')

		# 'proxy_enable'
		self.add_leaf(cmd=ShowIpInterface,
					  src=src_interface + '[proxy_arp]',
					  dest=dest_interface + '[proxy_enable]')

		dest_summary = 'info[statistics]'

		# incomplete_total
		self.add_leaf(cmd=ShowIpArpSummary,
					  src='[incomp_entries]',
					  dest=dest_summary + '[incomplete_total]')

		# entries_total
		self.add_leaf(cmd=ShowIpArpSummary,
					  src='[total_entries]',
					  dest=dest_summary + '[entries_total]')

		src_stat = '[arp_statistics]'
		dest_stat = 'info[statistics]'

		# Missing keys: 'out_gratuitous_pkts', 'out_drops', 
		# 'in_gratuitous_pkts', 'all_dynamic_pkts', 'all_static_pkts'

		# 'in_requests_pkts'
		self.add_leaf(cmd=ShowIpTraffic,
					  src=src_stat + '[arp_in_requests]',
					  dest=dest_stat + '[in_requests_pkts]')

		# 'in_replies_pkts'
		self.add_leaf(cmd=ShowIpTraffic,
					  src=src_stat + '[arp_in_replies]',
					  dest=dest_stat + '[in_replies_pkts]')

		# 'out_requests_pkts'
		self.add_leaf(cmd=ShowIpTraffic,
					  src=src_stat + '[arp_out_requests]',
					  dest=dest_stat + '[out_requests_pkts]')

		# 'out_replies_pkts'
		self.add_leaf(cmd=ShowIpTraffic,
					  src=src_stat + '[arp_out_replies]',
					  dest=dest_stat + '[out_replies_pkts]')

		# 'in_drops'
		self.add_leaf(cmd=ShowIpTraffic,
					  src=src_stat + '[arp_drops_input_full]',
					  dest=dest_stat + '[in_drops]')

		self.make(final_call=True)