import os,optparse, subprocess, random

def handleOptions():
    parser = optparse.OptionParser()
    parser.add_option("-i","--interface",help="the interface that you want to change your MAC for",dest="interface")
    parser.add_option("-v","--proper-vendor",help="whether to use a proper vendor",dest="properVendor", default=False, action="store_true")
    (options,arguments) = parser.parse_args()
    if not options.interface:
        parser.error("No interfaces given.")
    return options

def changeMAC(interface, newMAC):
    "change MAC"
    subprocess.call(["ifconfig",interface,"down"])
    subprocess.call(["ifconfig",interface,"hw","ether",newMAC])
    subprocess.call(["ifconfig",interface,"up"])

def checkRoot():
    if os.getuid() != 0:
        print("You must be root to run this tool!")
        exit(1)

def randomMAC(properVendor=False):
    "random MAC generator"
    hexList = [0,1,2,3,4,5,6,7,8,9,'A','B','C','D','E','F']
    vendorsList =[
        ["00","00","0C"], # cisco
        ["00","00","F0"], # samsung
        ["00","13","A9"] # sony
    ]
    generatedMAC = []
    if properVendor == True:
       generatedMAC = vendorsList[(random.randint(0, len(vendorsList) - 1))]
    while(len(generatedMAC) < 6):
        randomHex = ""
        for i in range(2):
            randomHex += str(hexList[random.randint(0, len(hexList) -1)])
        generatedMAC.append(randomHex)
    return ":".join(generatedMAC)

checkRoot()
options = handleOptions()
newMAC = randomMAC(options.properVendor)
changeMAC(options.interface, newMAC)