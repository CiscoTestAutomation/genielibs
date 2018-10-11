# -- EIGRP
# nxos: interface <intf> / ip authentication key-chain eigrp someword someword2
# nxos: interface <intf> / ip authentication mode eigrp someword md5
# nxos: interface <intf> / ip bandwidth eigrp someword 1
# nxos: interface <intf> / ip bandwidth-percent eigrp someword 1
# nxos: interface <intf> / ip delay eigrp someword 1
# nxos: interface <intf> / ip delay eigrp someword 1 picoseconds
# nxos: interface <intf> / ip distribute-list eigrp someword prefix-list someword2 in
# nxos: interface <intf> / ip distribute-list eigrp someword prefix-list someword2 out
# nxos: interface <intf> / ip distribute-list eigrp someword route-map rpl1 in
# nxos: interface <intf> / ip distribute-list eigrp someword route-map rpl1 out
# nxos: interface <intf> / ip eigrp someword bfd
# nxos: interface <intf> / ip eigrp someword bfd disable
# nxos: interface <intf> / ip eigrp someword shutdown
# nxos: interface <intf> / ip hello-interval eigrp someword 1
# nxos: interface <intf> / ip hold-time eigrp someword 1
# nxos: interface <intf> / ip mtu eigrp someword 210
# nxos: interface <intf> / ip next-hop-self eigrp someword
# nxos: interface <intf> / ip offset-list eigrp someword prefix-list someword2 in <0-2147483647>
# nxos: interface <intf> / ip offset-list eigrp someword prefix-list someword2 out <0-2147483647>
# nxos: interface <intf> / ip offset-list eigrp someword route-map rpl1 in <0-2147483647>
# nxos: interface <intf> / ip offset-list eigrp someword route-map rpl1 out <0-2147483647>
# nxos: interface <intf> / ip passive-interface eigrp someword
# nxos: interface <intf> / ip router eigrp someword
# nxos: interface <intf> / ip split-horizon eigrp someword
# nxos: interface <intf> / ip summary-address eigrp someword 1.2.3.4 255.255.255.0
# nxos: interface <intf> / ip summary-address eigrp someword 1.2.3.4 255.255.255.0 1
# nxos: interface <intf> / ip summary-address eigrp someword 1.2.3.4 255.255.255.0 1 leak-map someword2
# nxos: interface <intf> / ip summary-address eigrp someword 1.2.3.4 255.255.255.0 leak-map someword2
# nxos: interface <intf> / ip summary-address eigrp someword 1.2.3.0/24
# nxos: interface <intf> / ip summary-address eigrp someword 1.2.3.0/24 1
# nxos: interface <intf> / ip summary-address eigrp someword 1.2.3.0/24 1 leak-map someword2
# nxos: interface <intf> / ip summary-address eigrp someword 1.2.3.0/24 leak-map someword2
# nxos: interface <intf> / ipv6 authentication key-chain eigrp someword someword2
# nxos: interface <intf> / ipv6 authentication mode eigrp someword md5
# nxos: interface <intf> / ipv6 bandwidth eigrp someword 1
# nxos: interface <intf> / ipv6 bandwidth-percent eigrp someword 1
# nxos: interface <intf> / ipv6 delay eigrp someword 1
# nxos: interface <intf> / ipv6 delay eigrp someword 1 picoseconds
# nxos: interface <intf> / ipv6 distribute-list eigrp someword prefix-list someword2 in
# nxos: interface <intf> / ipv6 distribute-list eigrp someword prefix-list someword2 out
# nxos: interface <intf> / ipv6 distribute-list eigrp someword route-map rpl1 in
# nxos: interface <intf> / ipv6 distribute-list eigrp someword route-map rpl1 out
# nxos: interface <intf> / ipv6 eigrp someword shutdown
# nxos: interface <intf> / ipv6 hello-interval eigrp someword 1
# nxos: interface <intf> / ipv6 hold-time eigrp someword 1
# nxos: interface <intf> / ipv6 mtu eigrp someword 210
# nxos: interface <intf> / ipv6 next-hop-self eigrp someword
# nxos: interface <intf> / ipv6 offset-list eigrp someword prefix-list someword2 in <0-2147483647>
# nxos: interface <intf> / ipv6 offset-list eigrp someword prefix-list someword2 out <0-2147483647>
# nxos: interface <intf> / ipv6 offset-list eigrp someword route-map rpl1 in <0-2147483647>
# nxos: interface <intf> / ipv6 offset-list eigrp someword route-map rpl1 out <0-2147483647>
# nxos: interface <intf> / ipv6 passive-interface eigrp someword
# nxos: interface <intf> / ipv6 router eigrp someword
# nxos: interface <intf> / ipv6 split-horizon eigrp someword
# nxos: interface <intf> / ipv6 summary-address eigrp someword 1:2::3/128
# nxos: interface <intf> / ipv6 summary-address eigrp someword 1:2::3/128 1
# nxos: interface <intf> / ipv6 summary-address eigrp someword 1:2::3/128 1 leak-map someword2
# nxos: interface <intf> / ipv6 summary-address eigrp someword 1:2::3/128 leak-map someword2

