# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# A script that takes a Cisco IOS router configuration and  
# parses important summary features of the configuration. These features
# include:
#  - Firmware version
#  - hostname
#  - encrypted password
#  - segment routing protocols enabled (ospf, ip-ip, bgp, SRv6)
#  - Active/enables interfaces
#  - interfaces with IPv6 enabled
#  - interfaces with MPLS
#  - interfaces with VRRP
#  - interfaces with Layer 2 bridge domains (IRBs)
#  - interfaces with VRFs enabled

# Author: @nhagan2468

import argparse
import re
import sys

# global to write out the information about the configuration
# to the screen or any output files based on the CLI parameters
fout = sys.stdout

# read the file whose name is passed in and return the contents of the file
def readFile(fname):
    try:
        with open(fname) as fin:
            data = fin.read()
            return data
    except FileNotFoundError as ferr:
        print(f"Configuration file {fname} doesn't exist")


# method to search for the match_str in the data and
# then print out the rest of the line for the value
# with full_name as the header for the printout
def parseLine(data, match_str, full_name):
    global fout
    ver_regex = match_str + r"\s+(.*)\n"
    match = re.search(ver_regex, data)
    if match:
        ver_str = match[1]
        print(f"{full_name}: {ver_str}", file=fout)
    else:
        print(f"{full_name}: unknown", file=fout)
   
   
# method to search for the match_str in the data and
# make sure ther isn't a negator of "no" prior to
# the match_str to make it untrue
def isPresent(data, match_str):
    match = re.search(match_str, data)
    no_match = re.search("no " + match_str, data)
    return (match != None) and (no_match == None)


# print out the name of the protocol and the interfaces
# with the protocol enabled on them
def printInterfaces(protName, interfaces):
    global fout
    if len(interfaces) > 0:
        print(protName + ", ".join(interfaces), file=fout)
    else:
        print(protName + "None", file=fout)


# method to get all of the defined interfaces in the config
# and see which protocols are enabled
def collectInterfaceProtocols(data):
    # setup lists of interfaces for each protocol
    iactive = []
    ipv6 = []
    vrrp = []
    irb = []
    mpls = []
    vrf = []
    
    matches = re.finditer(r"\ninterface\s+(.*)\n", data)
    
    for match in matches:
        interface = match[1]
        start_idx = match.start(0)+1
        interface_down = False	# if not explicitly called out, it is up
        vrf_down = True			# if not explicitly called out, it isn't there 
        
        # loop through the interface configuration by looking for
        # the next line that isn't indented as all configuration
        # items associated with this interface will be indented
        nextline_idx = match.end(0)
        line_beg = nextline_idx
        eol = data.find("\n", line_beg)
        indent_match = re.match(r"\s+", data[line_beg:])
        
        while nextline_idx >= 0 and nextline_idx < len(data)-1 and indent_match:
            # dealing with an indented, therefore associated line
            if -1 < data.find("no shutdown", line_beg) < eol:
                # if calling out no shutdown, then active
                interface_down = False
            elif -1 < data.find("shutdown", line_beg) < eol:
                # if calling out shutdown, then deactivated
                interface_down = True
            elif -1 < data.find("ipv6 enable", line_beg) < eol:
                # ipv6 is then enabled on this interface
                ipv6.append(interface)
            elif -1 < data.find("vrrp", line_beg) < eol:
                # VRRP is then configured on the interface
                # mutiple VRRP options, so only pick once for the interface
                if len(vrrp) == 0 or vrrp[len(vrrp)-1] != interface:
                    vrrp.append(interface)
            elif -1 < data.find("bridge-group", line_beg) < eol:
                # IRB is then configured on the interface
                # mutiple irb options, so only pick once for the interface
                if len(irb) == 0 or irb[len(irb)-1] != interface:
                    irb.append(interface)
            elif -1 < data.find("mpls", line_beg) < eol:
                # MPLS is then configured on the interface
                # mutiple mpls options, so only pick once for the interface
                if len(mpls) == 0 or mpls[len(mpls)-1] != interface:
                    mpls.append(interface)
            elif -1 == data.find("no vrf", line_beg) < eol:
                # skip if a negative
                vrf_down = True
            elif -1 < data.find("vrf", line_beg) < eol:
                # a VRF is then configured on the interface
                vrf_down = False
                    
            # grab the next line
            nextline_idx = eol
            line_beg = nextline_idx + 1
            eol = data.find("\n", line_beg)
            indent_match = re.match(r"\s+", data[line_beg:])
                    
        # only once through all the lines decide if the interface is up
        # for the case of assumed active
        if interface_down == False:
            iactive.append(interface)
        if vrf_down == False:
            vrf.append(interface)
            
    # finally print out all of the interfaces for each protocol
    printInterfaces("Active interfaces: ", iactive)
    printInterfaces("IPv6: ", ipv6)
    printInterfaces("VRRP: ", vrrp)
    printInterfaces("IRB: ", irb)
    printInterfaces("MPLS: ", mpls)
    printInterfaces("VRF: ", vrf)
            

# main function that performs the work
if __name__ == "__main__":

    # set-up the argument parser to get the configuration file to parse
    parser = argparse.ArgumentParser()
    parser.add_argument("cfile")
    parser.add_argument("--fileout", "-o", help="optional output file path and name")
    args = parser.parse_args()
    
    # read in the configuration data
    cdata = readFile(args.cfile)

    if args.fileout != None:
        try:
            fout = open(args.fileout, 'w')
        except FileNotFoundError as ferr:
            print(f"output file {args.fileout} cannot be opened")
            print("printing to stdout instead")
            fout = sys.stdout

    # Print the firmware version from the config
    parseLine(cdata, "version", "Firmware Version")

    # Print the hostname from the config
    parseLine(cdata, "hostname", "Hostname")
    
    # Print if encrypted passwords are enabled
    pres = "are" if isPresent(cdata, "service password-encryption") else "are NOT"
    print(f"Encrypted Passwords {pres} enabled", file=fout)
    
    # Print segment routing protocols configured
    print("Routing protocols:", file=fout)
    
    # (ospf, is-is, bgp, SRv6)
    if isPresent(cdata, "router ospf"):
        print("- OSPF", file=fout)
    if isPresent(cdata, "router isis"):
        print("- IS-IS", file=fout)
    if isPresent(cdata, "router bgp"):
        print("- BGP", file=fout)
    if isPresent(cdata, "segment-routing") and isPresent(cdata, "srv6"):
        print("- SRv6", file=fout)
        
    # Print the protocols and the interfaces they are enabled on
    collectInterfaceProtocols(cdata)
    
    if args.fileout != None:
        fout.close()
    
    