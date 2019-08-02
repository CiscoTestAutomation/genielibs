''' 
ARP Genie Ops Object for NXOS - CLI.
'''
# super class
from genie.libs.ops.arp.arp import Arp as SuperArp

# Parser
from genie.libs.parser.nxos.show_arp import ShowIpArpDetailVrfAll, \
											ShowIpArpSummaryVrfAll, \
											ShowIpArpstatisticsVrfAll

from genie.libs.parser.nxos.show_interface import ShowIpInterfaceVrfAll


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
		self.add_leaf(cmd=ShowIpArpDetailVrfAll,
						src=src_global + '[ip]',
						dest=dest_global + '[ip]')

		# 'link_layer_address'
		self.add_leaf(cmd=ShowIpArpDetailVrfAll,
						src=src_global + '[link_layer_address]',
						dest=dest_global + '[link_layer_address]')

		# 'origin'
		self.add_leaf(cmd=ShowIpArpDetailVrfAll,
						src=src_global + '[origin]',
						dest=dest_global + '[origin]')

		src_interface = '[(?P<intf>.*)]'
		dest_interface = 'info[interfaces][(?P<intf>.*)][arp_dynamic_learning]'

		# 'proxy_enable'
		self.add_leaf(cmd=ShowIpInterfaceVrfAll,
						src=src_interface + '[proxy_arp]',
						dest=dest_interface + '[proxy_enable]')

		# 'local_proxy_enable'
		self.add_leaf(cmd=ShowIpInterfaceVrfAll,
						src=src_interface + '[local_proxy_arp]',
						dest=dest_interface + '[local_proxy_enable]')

		dest_summary = 'info[statistics]'

		# incomplete_total
		self.add_leaf(cmd=ShowIpArpSummaryVrfAll,
						src='[incomplete]',
						dest=dest_summary + '[incomplete_total]')

		# entries_total
		self.add_leaf(cmd=ShowIpArpSummaryVrfAll,
						src='[total]',
						dest=dest_summary + '[entries_total]')

		src_stat_in = '[statistics][received]'
		dest_stat_in = 'info[statistics]'

		# Missing keys: 'in_gratuitous_pkts', 'all_dynamic_pkts',
		# 'all_static_pkts'
		self.add_leaf(cmd=ShowIpArpstatisticsVrfAll,
						src=src_stat_in + '[requests]',
						dest=dest_stat_in + '[in_requests_pkts]')

		self.add_leaf(cmd=ShowIpArpstatisticsVrfAll,
						src=src_stat_in + '[replies]',
						dest=dest_stat_in + '[in_replies_pkts]')

		self.add_leaf(cmd=ShowIpArpstatisticsVrfAll,
						src=src_stat_in + '[total]',
						dest=dest_stat_in + '[in_total]')

		self.add_leaf(cmd=ShowIpArpstatisticsVrfAll,
						src=src_stat_in + '[dropped]',
						dest=dest_stat_in + '[in_drops]')

		src_stat_out = '[statistics][sent]'
		dest_stat_out = 'info[statistics]'

		self.add_leaf(cmd=ShowIpArpstatisticsVrfAll,
						src=src_stat_out + '[gratuitous]',
						dest=dest_stat_out + '[out_gratuitous_pkts]')

		self.add_leaf(cmd=ShowIpArpstatisticsVrfAll,
						src=src_stat_out + '[requests]',
						dest=dest_stat_out + '[out_requests_pkts]')

		self.add_leaf(cmd=ShowIpArpstatisticsVrfAll,
						src=src_stat_out + '[replies]',
						dest=dest_stat_out + '[out_replies_pkts]')

		self.add_leaf(cmd=ShowIpArpstatisticsVrfAll,
						src=src_stat_out + '[total]',
						dest=dest_stat_out + '[out_total]')

		self.add_leaf(cmd=ShowIpArpstatisticsVrfAll,
						src=src_stat_out + '[dropped]',
						dest=dest_stat_out + '[out_drops]')

		self.make(final_call=True)

		# Parser return a string and 'proxy_arp' & 'local_proxy_arp' attributes
		# are booleans
		if hasattr(self, 'info') and 'interfaces' in self.info:
			for intf in self.info['interfaces']:
				if 'arp_dynamic_learning' in self.info['interfaces'][intf] and \
					'proxy_enable' in self.info['interfaces'][intf]\
					['arp_dynamic_learning']:
					# proxy_enable
					if self.info['interfaces'][intf]['arp_dynamic_learning']\
						['proxy_enable'] == 'disabled':
						self.info['interfaces'][intf]['arp_dynamic_learning']\
							['proxy_enable'] = False
					else:
						self.info['interfaces'][intf]['arp_dynamic_learning']\
							['proxy_enable'] = True
					# local_proxy_enable
					if self.info['interfaces'][intf]['arp_dynamic_learning']\
						['local_proxy_enable'] == 'disabled':
						self.info['interfaces'][intf]['arp_dynamic_learning']\
							['local_proxy_enable'] = False
					else:
						self.info['interfaces'][intf]['arp_dynamic_learning']\
							['local_proxy_enable'] = True