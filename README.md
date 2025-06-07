# config_parser
Config_parser is a Python script that can be used to examine a Cisco IOS router configuration file and summarize the protocols being enabled on the networking device. It is meant to be a quick analysis of the enabled routing protocols along with the interface-enabled protocols for IOS-style configurations. The focus is on giving information regarding protocols and not traffic policies. The output includes:
- Firmware version
- hostname
- if encrypted password is enabled
- segment routing protocols enabled (OSPF, IP-IP, BGP, SRv6)
- which interfaces are active/enabled
- interfaces with
 - IPv6
 - MPLS
 - VRRP
 - Layer 2 bridge domains (IRBs)
 - VRF

## Overview/Requirements
This was developed with Python 3.12.2 and no additional libraries necessary other than the base libraries. Your mileage may vary if you are using other versions of Python.

## Usage  
The script only has one required parameter, the configuraiton file name. It also has one optional parameter, `--fileout`, which directs the output to a file instead of to stdout. To run from the CLI, use `python config_parser.py <path/config_file_name>`. The file will print to the screen or the specified output file the basic information about the configuration. 

## Future Directions
* This could be expanded to other similar networking configurations such as Juniper JunOS, and Palo Alto Firewall configurations. 
* Making it more generalizable where users can provide the hierarichal information and the script parses out any information relative to that can be parsed out
* Add the ability to compare configurations for similarities
* Adding other protocols and security information
* Analyze configurations for security properties

## References
* <ins>Cisco LAN Switching Configuration Handbook, Second Edition</ins> by Steve McQuerry
* [Cisco IOS Configuration Fundamentals Configuration Guide, Release 12.2SR](https://www.cisco.com/c/en/us/td/docs/ios/fundamentals/configuration/guide/12_2sr/cf_12_2sr_book.html)
* <ins>Cisco Cookbook</ins> by Kevin Dooley, Ian Brown, O'Reilly Media, Inc.
* [L3VPN Configuration Guide for Cisco 8000 Series Routers, IOS XR Release 25.1.x](https://www.cisco.com/c/en/us/td/docs/iosxr/cisco8000/l3vpn/25xx/configuration/guide/b-l3vpn-cg-cisco8000-25xx.html)
* [Routing Configuration Guide for Cisco 8000 Series Routers, IOS XR Release 25.1.x](https://www.cisco.com/c/en/us/td/docs/iosxr/cisco8000/routing/25xx/configuration/guide/b-routing-cg-cisco8000-25xx.html)
* [Cisco Catalyst 8000V Edge Software Installation And Configuration Guide](https://www.cisco.com/c/en/us/td/docs/routers/C8000V/Configuration/c8000v-installation-configuration-guide.html)
* [VRRP Configuration on Cisco](https://ipcisco.com/lesson/vrrp-configuration-on-cisco-2/)
* [Configure VLAN Routing and Bridging on a Router with IRB Troubleshooting TechNotes](https://www.cisco.com/c/en/us/support/docs/lan-switching/integrated-routing-bridging-irb/17054-741-10.html)
* [Configure a Basic MPLS VPN Network](https://www.cisco.com/c/en/us/support/docs/multiprotocol-label-switching-mpls/mpls/13733-mpls-vpn-basic.html)
* [MPLS: LDP Configuration Guide, Cisco IOS Release x.x](https://www.cisco.com/c/en/us/td/docs/ios/mpls/configuration/guide/convert/mp_ldp_book.html)