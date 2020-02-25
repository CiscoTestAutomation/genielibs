''' 
NTP Genie Ops Object for IOS - CLI.
'''
import copy

# super class
from genie.libs.ops.ntp.ntp import Ntp as SuperNtp

# Parser
from genie.libs.parser.ios.show_ntp import ShowNtpAssociations, \
										   ShowNtpStatus, \
										   ShowNtpConfig


class Ntp(SuperNtp):
	'''NTP Genie Ops Object'''

	def set_defaults(self, peer, vrf):
		'''Set defaults'''

		for local_mode in self.info['associations']['address'][peer]\
			['local_mode'].keys():
			if 'local_mode' not in self.info['vrf'][vrf]['associations']\
				['address'][peer]:
				mode_dict = self.info['vrf'][vrf]['associations']['address']\
					[peer].setdefault('local_mode', {}).setdefault(local_mode, {})
			else:
				mode_dict = self.info['vrf'][vrf]['associations']['address']\
					[peer]['local_mode'][local_mode]

			if 'isconfigured' not in self.info['vrf'][vrf]['associations']['address'][peer]:
				# Case of default configuration
				isconfigured_value = False
				address = peer
			else:
				for val in self.info['vrf'][vrf]['associations']['address'][peer]\
					['isconfigured']:
					if 'isconfigured' in self.info['vrf'][vrf]['associations']\
						['address'][peer]['isconfigured'][val]:
						isconfigured_value = self.info['vrf'][vrf]['associations']\
							['address'][peer]['isconfigured'][val]['isconfigured']
						address = self.info['vrf'][vrf]['associations']['address']\
							[peer]['isconfigured'][val]['address']
					else:
						# Case of default configuration
						isconfigured_value = False
						address = peer

			# Build a dictionary with the local_mode keys
			local_keys = {}
			for key in self.info['associations']['address'][peer]['local_mode']\
				[local_mode]:
				local_keys[key] = self.info['associations']['address'][peer]\
					['local_mode'][local_mode][key]		

			local_dict = self.info['vrf'][vrf]['associations']['address'][peer]\
				['local_mode'][local_mode].setdefault('isconfigured', {}).\
				setdefault(isconfigured_value, {})
			local_dict['address'] = address
			local_dict['vrf'] = vrf
			local_dict['isconfigured'] = isconfigured_value
			local_dict.update(local_keys)

			new_dict = copy.deepcopy(self.info['vrf'][vrf]['associations']\
				['address'][peer]['local_mode'][local_mode])

			# Reset dictionary and replace with the intended structure
			self.info['vrf'][vrf]['associations']['address'][peer]\
				['local_mode'][local_mode] = {}
			self.info['vrf'][vrf]['associations']['address'][peer]\
				['local_mode'][local_mode]['isconfigured'] = \
				new_dict['isconfigured']

		try:
			del(self.info['vrf'][vrf]['associations']['address'][peer]['isconfigured'])
		except Exception:
			pass

	def learn(self):
		'''Learn NTP Ops'''
		
		########################################################################
		#                               info
		########################################################################

		# clock_state
		# 'associations_address', 'associations_local_mode',
		# 'clock_state', clock_stratum', 'root_delay', 'clock_offset',
		# 'clock_refid'
		self.add_leaf(cmd=ShowNtpAssociations,
					  src='[clock_state]',
					  dest='info[clock_state]')

		# 'associations_address', 'associations_local_mode',
		# 'clock_state', clock_stratum', 'root_delay'
		for src_key, dest_key in {'frequency': 'actual_freq',
								  'precision': 'clock_precision',
								  'reftime': 'reference_time',
								  'rootdispersion': 'root_dispersion'}.items():            
			self.add_leaf(cmd=ShowNtpStatus,
						  src='[clock_state][system_status][%s]' % src_key,
						  dest='info[clock_state][system_status][%s]' % dest_key)

		# unicast_configuration
		self.add_leaf(cmd=ShowNtpConfig,
					  src='[vrf][(?P<vrf>.*)][address][(?P<address>.*)][type][(?P<type>.*)]',
					  dest='info[vrf][(?P<vrf>.*)][unicast_configuration][address]'
						   '[(?P<address>.*)][type][(?P<type>.*)]')

		# associations
		self.add_leaf(cmd=ShowNtpConfig,
					  src='[vrf][(?P<vrf>.*)][address][(?P<address>.*)][isconfigured][(?P<isconfigured>.*)]',
					  dest='info[vrf][(?P<vrf>.*)][associations][address][(?P<address>.*)]'
						   '[isconfigured][(?P<isconfigured>.*)]')

		# associations
		asso_keys = ['address', 'local_mode', 'stratum', 'refid', 'reach', 'poll',
					 'offset', 'delay', 'receive_time']
		for key in asso_keys:
			self.add_leaf(cmd=ShowNtpAssociations,
						  src='[peer][(?P<address>.*)][local_mode][(?P<local_mode>.*)][%s]' % key,
						  dest='info[associations][address][(?P<address>.*)]'
							   '[local_mode][(?P<local_mode>.*)][%s]' % key)


		# make to write in cache
		self.make(final_call=True)

		# needs combine structures from ShowConfigurationSystemNtpSet and ShowNtpAssociations
		if hasattr(self, 'info') and 'associations' in self.info :

			peers = list(self.info['associations']['address'].keys()).copy()

			for peer in peers:
				found = False
				if 'vrf' in self.info:
					for i, vrf in enumerate(self.info['vrf']):
						if not self.info['vrf'][vrf]['associations']['address'].get(peer):
							if i == (len(self.info['vrf'])-1) and not found:
								# Last iteration annd peer is not found
								if 'default' in self.info['vrf']:
									self.info['vrf']['default']['associations']\
										['address'][peer] = \
										self.info['associations']['address'][peer]
								else:
									self.info['vrf'].setdefault('default', {}).\
										setdefault('associations', {}).\
										setdefault('address', {})[peer] = \
										self.info['associations']['address'][peer]
								self.set_defaults(peer, 'default')
							else:
								# Not the last iteration and the peer address is not yet found
								continue
						else:
							# peer was found under one of the vrfs
							found = True
							self.set_defaults(peer, vrf)
				else:
					self.info.setdefault('vrf', {}).setdefault('default', {}).\
						setdefault('associations', {}).\
						setdefault('address', {})[peer] = \
						self.info['associations']['address'][peer]
					self.info['vrf']['default']['associations']['address'][peer].\
						setdefault('isconfigured', {}).setdefault('False', {})
					self.set_defaults(peer, 'default')

			# remove the non-combined key
			try:
				del(self.info['associations'])
			except Exception:
				pass