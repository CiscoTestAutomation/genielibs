''' 
LISP Genie Ops Object for IOSXE - CLI.
'''

# Genie
from genie.libs.ops.lisp.lisp import Lisp as SuperLisp
from genie.ops.base import Context


class Lisp(SuperLisp):
    '''Lisp Ops Object'''

    def learn(self):
        '''Learn Lisp object'''

        ########################################################################
        #                               info
        ########################################################################

        # lisp_router_instances
        #   lisp_router_instance_id
        info_src = '[lisp_router_instances][(?P<lisp_router_instance>.*)]'
        info_dest = 'info[lisp_router_instances][(?P<lisp_router_instance>.*)]'

        # lisp_router_instance_id
        self.add_leaf(cmd='show lisp all service {service}'.format(service='ipv4'),
                      src=info_src+'[lisp_router_instance_id]',
                      dest=info_dest+'[lisp_router_instance_id]',
                      service='ipv4')

        # locator_sets
        #   locator_set_name
        #       local_interface - N/A
        #           ls_interface - N/A
        #               interface - N/A
        #               interface_type - N/A
        #               priority - N/A
        #               weight - N/A
        #               multicast_priority - N/A
        #               multicast_weight -N/A

        # lisp_role - N/A
        #   lisp_role_type - N/A
        #       lisp_role_type -N/A

        # lisp_router_id
        #   site_id
        #   xtr_id
        self.add_leaf(cmd='show lisp all service {service}'.format(service='ipv4'),
                      src=info_src+'[lisp_router_id]',
                      dest=info_dest+'[lisp_router_id]',
                      service='ipv4')

        ####################################################################
        #                           service
        ####################################################################

        # Loop over all services
        for service in ['ipv4', 'ipv6', 'ethernet']:

            service_src = info_src + '[service][{service}]'.format(service=service)
            service_dest = info_dest + '[service][{service}]'.format(service=service)

            # Get all instance_id's in Lisp configuration
            self.add_leaf(cmd='show lisp all service {service} summary'.format(service=service),
                          src=service_src+'[virtual_network_ids]',
                          dest='info[{service}][instance_ids]'.format(service=service),
                          service=service)
            self.make() ; self.make()

            # service
            self.add_leaf(cmd='show lisp all service {service}'.format(service=service),
                          src=service_src+'[service]',
                          dest=service_dest+'[service]',
                          service=service)

            # lisp_role - N/A
            #   lisp_role_type - N/A
            #       lisp_role_type -N/A

            # virtual_network_ids
            #   instance_id
            #       lisp_role
            #           lisp_role_type
            #               lisp_role_type
            self.add_leaf(cmd='show lisp all service {service} summary'.format(service=service),
                          src=service_src+'[virtual_network_ids][(?P<vni>.*)][lisp_role]',
                          dest=service_dest+'[virtual_network_ids][(?P<vni>.*)][lisp_role]',
                          service=service)

            # Get instance_ids for this service
            if hasattr(self, 'info') and service in self.info and \
                'instance_ids' in self.info[service]:
                
                # Loop over all instance_ids
                for instance_id in sorted(self.info[service]['instance_ids']):

                    # locator_sets
                    #   locator_set_name
                    #       locator_set_name
                    self.add_leaf(cmd='show lisp all instance-id {instance_id} {service} database'.format(service=service, instance_id=instance_id),
                                  src=info_src+'[locator_sets][(?P<ls>.*)][locator_set_name]',
                                  dest=info_dest+'[locator_sets][(?P<ls>.*)][locator_set_name]',
                                  service=service, instance_id=instance_id)

                    # ==========
                    # map_server
                    # ==========
                    ms_src = service_src + '[map_server]'
                    ms_dest = service_dest + '[map_server]'

                    # map_server
                    #   enabled
                    self.add_leaf(cmd='show lisp all instance-id {instance_id} {service}'.format(instance_id=instance_id, service=service),
                                  src=ms_src+'[enabled]',
                                  dest=ms_dest+'[enabled]',
                                  service=service, instance_id=instance_id)

                    # map_server
                    #   sites
                    #       ms_site_id
                    #           site_id
                    #           auth_key - N/A
                    #               auth_key_value - N/A
                    #               auth_key_type - N/A
                    self.add_leaf(cmd='show lisp all instance-id {instance_id} {service} server detail internal'.format(service=service, instance_id=instance_id),
                                  src=ms_src+'[sites][(?P<site>.*)][site_id]',
                                  dest=ms_dest+'[sites][(?P<site>.*)][site_id]',
                                  service=service, instance_id=instance_id)

                    # =====================
                    # map_server
                    #   virtual_network_ids
                    # =====================
                    vni_src = ms_src+'[virtual_network_ids][(?P<iid>.*)]'
                    vni_dest = ms_dest+'[virtual_network_ids][(?P<iid>.*)]'

                    # map_server
                    #   virtual_network_ids
                    #       instance_id
                    #           vni
                    #           extranets
                    #               ms_extranet
                    #                   extranet
                    #                   provider
                    #                       ms_extranet_provider_eid
                    #                           eid_record
                    #                           bidirectional
                    #                   subscriber
                    #                       ms_extranet_provider_eid
                    #                           eid_record
                    #                           bidirectional
                    for key in ['vni', 'extranets']:
                        self.add_leaf(cmd='show lisp all extranet {extranet} instance-id {instance_id}'.format(instance_id=instance_id, extranet='ext1'),
                                      src=vni_src+'[{key}]'.format(key=key),
                                      dest=vni_dest+'[{key}]'.format(key=key),
                                      instance_id=instance_id, extranet='ext1')

                    # map_server
                    #   virtual_network_ids
                    #       counters
                    #           map_registers_in
                    #           map_notify_records_out
                    #           proxy_reply_records_out
                    #           map_requests_forwarded_out
                    #           map_registers_in_auth_failed
                    for key in ['map_register_records_in',
                                'map_notify_records_out',
                                'map_server_proxy_reply_records_out',
                                'map_server_map_requests_forwarded',
                                'map_registers_in_auth_failed',
                                ]:
                        # reset key names
                        if key == 'map_server_proxy_reply_records_out':
                            key2 = 'proxy_reply_records_out'
                        elif key == 'map_server_map_requests_forwarded':
                            key2 = 'map_requests_forwarded_out'
                        elif key == 'map_register_records_in':
                          key2 = 'map_registers_in'
                        else:
                            key2 = key
                        # add the leaf
                        self.add_leaf(cmd='show lisp all instance-id {instance_id} {service} statistics'.format(service=service, instance_id=instance_id),
                                      src=service_src+'[statistics][EID][control][{key}]'.format(key=key),
                                      dest=ms_dest+'[virtual_network_ids][{iid}][counters][{key2}]'.format(iid=instance_id, key2=key2),
                                      service=service, instance_id=instance_id)

                    # =====================
                    # map_server
                    #   virtual_network_ids
                    #       mappings
                    # =====================
                    mapping_src = vni_src+'[mappings][(?P<ms_eid>.*)]'
                    mapping_dest = vni_dest+'[mappings][(?P<ms_eid>.*)]'

                    # mappings
                    #   ms_eid_id
                    #       eid_id
                    #       site_id
                    #       more_specifics_accepted
                    #       mapping_expiration_timeout - N/A
                    for key in ['eid_id', 'site_id', 'more_specifics_accepted']:
                        self.add_leaf(cmd='show lisp all instance-id {instance_id} {service} server detail internal'.format(service=service, instance_id=instance_id),
                                      src=mapping_src+'[{key}]'.format(key=key),
                                      dest=mapping_dest+'[{key}]'.format(key=key),
                                      service=service, instance_id=instance_id)

                    # mappings
                    #   ms_eid_id
                    #       eid_address
                    #           address_type
                    #           virtual_network_id
                    #           ipv4
                    #               ipv4
                    #           ipv4_prefix
                    #               ipv4_prefix
                    #           ipv6
                    #               ipv6
                    #           ipv6_prefix
                    #               ipv6_prefix
                    for key in ['address_type', 'virtual_network_id', 'ipv4',
                                'ipv4_prefix', 'ipv6', 'ipv6_prefix']:
                        self.add_leaf(cmd='show lisp all instance-id {instance_id} {service} server detail internal'.format(service=service, instance_id=instance_id),
                                      src=mapping_src+'[eid_address][{key}]'.format(key=key),
                                      dest=mapping_dest+'[eid_address][{key}]'.format(key=key),
                                      service=service, instance_id=instance_id)

                    # mappings
                    #   ms_eid_id
                    #       mapping_records
                    #           xtr_id
                    #           site_id
                    #           time_to_live
                    #           creation_time
                    #           authoritative - N/A
                    #           static - N/A
                    for key in ['xtr_id', 'site_id', 'time_to_live', 'creation_time']:
                        self.add_leaf(cmd='show lisp all instance-id {instance_id} {service} server detail internal'.format(service=service, instance_id=instance_id),
                                      src=mapping_src+'[mapping_records][(?P<xtr>.*)][{key}]'.format(key=key),
                                      dest=mapping_dest+'[mapping_records][(?P<xtr>.*)][{key}]'.format(key=key),
                                      service=service, instance_id=instance_id)

                    # mappings
                    #   ms_eid_id
                    #       mapping_records
                    #           eid
                    #               address_type
                    #               virtual_network_id
                    #               ipv4
                    #                   ipv4
                    #               ipv4_prefix
                    #                   ipv4_prefix
                    #               ipv6
                    #                   ipv6
                    #               ipv6_prefix
                    #                   ipv6_prefix
                    for key in ['address_type', 'virtual_network_id', 'ipv4',
                                'ipv4_prefix', 'ipv6', 'ipv6_prefix']:
                        self.add_leaf(cmd='show lisp all instance-id {instance_id} {service} server detail internal'.format(service=service, instance_id=instance_id),
                                      src=mapping_src+'[mapping_records][(?P<xtr>.*)][eid][{key}]'.format(key=key),
                                      dest=mapping_dest+'[mapping_records][(?P<xtr>.*)][eid][{key}]'.format(key=key),
                                      service=service, instance_id=instance_id)

                    # mappings
                    #   ms_eid_id
                    #       mapping_records
                    #           xtr_id
                    #               negative_mapping - N/A
                    #                   map_reply_action - N/A
                    #               positive_mapping - N/A
                    #                   rlocs - N/A
                    #                       id - N/A
                    #                           id - N/A
                    #                           locator_address - N/A
                    #                               address_type - N/A
                    #                               virtual_network_id - N/A
                    #                               ipv4 - N/A
                    #                               ipv4_prefix - N/A
                    #                               ipv6 - N/A
                    #                               ipv6_prefix - N/A
                    #                           priority - N/A
                    #                           weight - N/A
                    #                           multicast_priority - N/A
                    #                           multicast_weight - N/A

                    # map_server
                    #   mapping_system_type - N/A

                    # map_server
                    #   summary
                    #       number_configured_sites
                    #       number_registered_sites
                    #       af_datum
                    #           address_type
                    #               address_type
                    #               number_configured_eids
                    #               number_registered_eids
                    for key in ['number_configured_sites', 
                                'number_registered_sites', 'af_datum']:
                        self.add_leaf(cmd='show lisp all instance-id {instance_id} {service} server summary'.format(service=service, instance_id=instance_id),
                                      src=service_src+'[instance_id][(?P<iid>.*)][map_server][summary][{key}]'.format(key=key),
                                      dest=ms_dest+'[summary][{key}]'.format(key=key),
                                      service=service, instance_id=instance_id)

                    # map_server
                    #   counters
                    #       map_registers_in - N/A
                    #       map_registers_in_auth_failed - N/A
                    #       map_notify_records_out - N/A
                    #       proxy_reply_records_out - N/A
                    #       map_requests_forwarded_out - N/A

                    # ============
                    # map_resolver
                    # ============
                    mr_src = service_src + '[map_resolver]'
                    mr_dest = service_dest + '[map_resolver]'

                    # map_resolver
                    #   enabled
                    self.add_leaf(cmd='show lisp all instance-id {instance_id} {service}'.format(service=service, instance_id=instance_id),
                                  src=mr_src+'[enabled]',
                                  dest=mr_src+'[enabled]',
                                  service=service, instance_id=instance_id)

                    # map_resolver
                    #   mapping_system_type - N/A
                    #   ms_address - N/A

                    # ===
                    # itr
                    # ===
                    itr_src = service_src + '[itr]'
                    itr_dest = service_dest + '[itr]'

                    # itr
                    #   enabled
                    #   rloc_probing - N/A
                    #       interval - N/A
                    #       retries - N/A
                    #       retries_interval - N/A
                    #   itr_rlocs - N/A
                    #   map_resolvers
                    #       itr_map_resolver
                    #           map_resolver
                    #   proxy_itrs
                    #       proxy_itr
                    #           proxy_etr_address
                    for key in ['enabled', 'map_resolvers', 'proxy_itrs']:
                        self.add_leaf(cmd='show lisp all instance-id {instance_id} {service}'.format(service=service, instance_id=instance_id),
                                      src=itr_src+'[{key}]'.format(key=key),
                                      dest=itr_dest+'[{key}]'.format(key=key),
                                      service=service, instance_id=instance_id)

                    # ===========
                    # itr
                    #   map_cache
                    # ===========
                    map_cache_src = itr_src + '[map_cache][(?P<iid>.*)]' 
                    map_cache_dest = itr_dest + '[map_cache][(?P<iid>.*)]'

                    # itr
                    #   map_cache
                    #       instance_id
                    #           vni
                    self.add_leaf(cmd='show lisp all instance-id {instance_id} {service} map-cache'.format(service=service, instance_id=instance_id),
                                  src=map_cache_src+'[vni]',
                                  dest=map_cache_dest+'[vni]',
                                  service=service, instance_id=instance_id)

                    # ========================
                    # itr
                    #   map_cache
                    #       instance_id
                    #           mappings
                    #               itr_map_id
                    # ========================
                    mappings_src = map_cache_src+'[mappings][(?P<map_id>.*)]'
                    mappings_dest = map_cache_dest+'[mappings][(?P<map_id>.*)]'

                    # itr
                    #   map_cache
                    #       instance_id
                    #           mappings
                    #               itr_map_id
                    #                   id
                    #                   time_to_live
                    #                   creation_time
                    #                   authoritative - N/A
                    #                   static - N/A
                    for key in ['id', 'time_to_live', 'creation_time']:
                        self.add_leaf(cmd='show lisp all instance-id {instance_id} {service} map-cache'.format(service=service, instance_id=instance_id),
                                      src=mappings_src+'[{key}]'.format(key=key),
                                      dest=mappings_dest+'[{key}]'.format(key=key),
                                      service=service, instance_id=instance_id)

                    # itr
                    #   map_cache
                    #       instance_id
                    #           mappings
                    #               itr_map_id
                    #                   eid
                    #                       address_type
                    #                       vrf
                    #                       ipv4
                    #                           ipv4
                    #                       ipv4_prefix
                    #                           ipv4_prefix
                    #                       ipv6
                    #                           ipv6
                    #                       ipv6_prefix
                    #                           ipv6_prefix
                    for key in ['address_type', 'vrf', 'ipv4', 'ipv4_prefix'
                                'ipv6', 'ipv6_prefix']:
                        self.add_leaf(cmd='show lisp all instance-id {instance_id} {service} map-cache'.format(service=service, instance_id=instance_id),
                                      src=mappings_src+'[eid][{key}]'.format(key=key),
                                      dest=mappings_dest+'[eid][{key}]'.format(key=key),
                                      service=service, instance_id=instance_id)

                    # itr
                    #   map_cache
                    #       instance_id
                    #           mappings
                    #               itr_map_id
                    #                   negative_mapping
                    #                       map_reply_action
                    self.add_leaf(cmd='show lisp all instance-id {instance_id} {service} map-cache'.format(service=service, instance_id=instance_id),
                                  src=mappings_src+'[negative_mapping][map_reply_action]',
                                  dest=mappings_dest+'[negative_mapping][map_reply_action]',
                                  service=service, instance_id=instance_id)

                    # itr
                    #   map_cache
                    #       instance_id
                    #           mappings
                    #               itr_map_id
                    #                   positive_mapping
                    #                       rlocs
                    #                           id
                    #                               id
                    #                               priority
                    #                               weight
                    #                               multicast_priority
                    #                               multicast_weight
                    for key in ['id', 'priority', 'weight', 'multicast_priority',
                                'multicast_weight']:
                        self.add_leaf(cmd='show lisp all instance-id {instance_id} {service} map-cache'.format(service=service, instance_id=instance_id),
                                  src=mappings_src+'[positive_mapping][rlocs][(?P<id>.*)][{key}]'.format(key=key),
                                  dest=mappings_dest+'[positive_mapping][rlocs][(?P<id>.*)][{key}]'.format(key=key),
                                  service=service, instance_id=instance_id)

                    # itr
                    #   map_cache
                    #       instance_id
                    #           mappings
                    #               itr_map_id
                    #                   positive_mapping
                    #                       rlocs
                    #                           id
                    #                               locator_address
                    #                                   address_type
                    #                                   virtual_network_id
                    #                                   ipv4
                    #                                       ipv4
                    #                                   ipv4_prefix
                    #                                       ipv4_prefix
                    #                                   ipv6
                    #                                       ipv6
                    #                                   ipv6_prefix
                    #                                       ipv6_prefix
                    for key in ['address_type', 'virtual_network_id', 'ipv4',
                                'ipv4_prefix', 'ipv6', 'ipv6_prefix']:
                        self.add_leaf(cmd='show lisp all instance-id {instance_id} {service} map-cache'.format(service=service, instance_id=instance_id),
                                  src=mappings_src+'[positive_mapping][rlocs][(?P<id>.*)][locator_address][{key}]'.format(key=key),
                                  dest=mappings_dest+'[positive_mapping][rlocs][(?P<id>.*)][locator_address][{key}]'.format(key=key),
                                  service=service, instance_id=instance_id)

                    # ===
                    # etr
                    # ===
                    etr_src = service_src + '[etr]'
                    etr_dest = service_dest + '[etr]'

                    # etr
                    #   enabled
                    #   encapsulation
                    for key in ['enabled', 'encapsulation']:
                        self.add_leaf(cmd='show lisp all instance-id {instance_id} {service}'.format(service=service, instance_id=instance_id),
                                      src=etr_src+'[{key}]'.format(key=key),
                                      dest=etr_dest+'[{key}]'.format(key=key),
                                      service=service, instance_id=instance_id)

                    # etr
                    #   mapping_servers
                    #       etr_map_server
                    #           ms_address
                    #           auth_key - N/A
                    #           auth_key_type - N/A
                    self.add_leaf(cmd='show lisp all instance-id {instance_id} {service}'.format(service=service, instance_id=instance_id),
                                  src=etr_src+'[mapping_servers][(?P<ms>.*)][ms_address]',
                                  dest=etr_dest+'[mapping_servers][(?P<ms>.*)][ms_address]',
                                  service=service, instance_id=instance_id)

                    # etr
                    #   local_eids
                    #       instance_id
                    #           vni
                    self.add_leaf(cmd='show lisp all instance-id {instance_id} {service} database'.format(service=service, instance_id=instance_id),
                                  src=etr_src+'[local_eids][(?P<iid>.*)][vni]',
                                  dest=etr_dest+'[local_eids][(?P<iid>.*)][vni]',
                                  service=service, instance_id=instance_id)

                    # etr
                    #   local_eids
                    #       instance_id
                    #           use_petrs
                    #               etr_use_ptr
                    #                   use_petr
                    #                   priority - N/A
                    #                   weight - N/A
                    self.add_leaf(cmd='show lisp all instance-id {instance_id} {service}'.format(service=service, instance_id=instance_id),
                                  src=etr_src+'[use_petrs]',
                                  dest=etr_dest+'[local_eids][{iid}][use_petrs]'.format(iid=instance_id),
                                  service=service, instance_id=instance_id)

                    # etr
                    #   local_eids
                    #       instance_id
                    #           dynamic_eids
                    #               etr_dyn_eid_id
                    #                   id
                    #                   rlocs
                    #                   loopback_address
                    #                   priority
                    #                   weight
                    #                   record_ttl - N/A
                    #                   want_map_notify - N/A
                    #                   proxy_reply - N/A
                    #                   registration_interval - N/A
                    #           eids
                    #               etr_eid_id
                    #                   id
                    #                   rlocs
                    #                   loopback_address
                    #                   priority
                    #                   weight
                    #                   record_ttl - N/A
                    #                   want_map_notify - N/A
                    #                   proxy_reply - N/A
                    #                   registration_interval - N/A
                    for etr_type in ['dynamic_eids', 'eids']:
                        for key in ['id', 'rlocs', 'loopback_address', 'priority',
                                    'weight']:
                            self.add_leaf(cmd='show lisp all instance-id {instance_id} {service} database'.format(service=service, instance_id=instance_id),
                                      src=etr_src+'[local_eids][(?P<iid>.*)][{etr_type}][(?P<dyn_id>.*)][{key}]'.format(etr_type=etr_type, key=key),
                                      dest=etr_dest+'[local_eids][(?P<iid>.*)][{etr_type}][(?P<dyn_id>.*)][{key}]'.format(etr_type=etr_type, key=key),
                                      service=service, instance_id=instance_id)

                    # etr
                    #   local_eids
                    #       instance_id
                    #           dynamic_eids
                    #               etr_dyn_eid_id
                    #                   eid_address
                    #                       address_type
                    #                       vrf
                    #                       ipv4
                    #                           ipv4
                    #                       ipv4_prefix
                    #                           ipv4_prefix
                    #                       ipv6
                    #                           ipv6
                    #                       ipv6_prefix
                    #                           ipv6_prefix
                    #           eids
                    #               etr_dyn_eid_id
                    #                   eid_address
                    #                       address_type
                    #                       vrf
                    #                       ipv4
                    #                           ipv4
                    #                       ipv4_prefix
                    #                           ipv4_prefix
                    #                       ipv6
                    #                           ipv6
                    #                       ipv6_prefix
                    #                           ipv6_prefix
                    for etr_type in ['dynamic_eids', 'eids']:
                        for key in ['address_type', 'vrf', 'ipv4', 'ipv6',
                                    'ipv4_prefix', 'ipv6_prefix']:
                            self.add_leaf(cmd='show lisp all instance-id {instance_id} {service} database'.format(service=service, instance_id=instance_id),
                                      src=etr_src+'[local_eids][(?P<iid>.*)][{etr_type}][(?P<dyn_id>.*)][eid_address][{key}]'.format(etr_type=etr_type, key=key),
                                      dest=etr_dest+'[local_eids][(?P<iid>.*)][{etr_type}][(?P<dyn_id>.*)][eid_address][{key}]'.format(etr_type=etr_type, key=key),
                                      service=service, instance_id=instance_id)


            # Delete instance_ids for this service
            try:
                del self.info[service]
            except:
                pass

        ########################################################################
        #                           Final Structure
        ########################################################################

        # Make final Ops structure
        self.make(final_call=True)
