import scapy.all as scapy
from scapy_http import http
import optparse
import os

def parseArgs():
    parser = optparse.OptionParser()
    parser.add_option("-i","--iface", help="the interface to sniff on", dest="iface")
    (options, arguments) = parser.parse_args()
    if not options.iface:
        parser.error("You should specify an interface.")
    return options
def checkRoot():
    if os.getuid() != 0:
        print("You are not permitted to run this script! You must be root.")
        exit(1)
def sniff(interface):
    scapy.sniff(iface=interface,store=False,prn=processPackets)

def processPackets(packet):
    if packet.haslayer(scapy.IP) and (packet.haslayer(scapy.TCP) or packet.haslayer(scapy.UDP)):
        sourceIP = packet["IP"].src
        destinationIP = packet["IP"].dst
        sourcePort = packet["UDP"].sport if packet.haslayer(scapy.UDP) else packet["TCP"].sport
        destinationPort = packet["UDP"].dport if packet.haslayer(scapy.UDP) else packet["TCP"].dport
        protocol = "UDP" if packet.haslayer(scapy.UDP) else "TCP"
        print(f"[{protocol}] {sourceIP}:{sourcePort} > {destinationIP}:{destinationPort}")
checkRoot()
options = parseArgs()
sniff(options.iface)