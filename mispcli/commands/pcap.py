#! /usr/bin/env python
import os
import sys
from mispcli.commands.base import Command
from mispy import MispServer
from scapy.all import rdpcap
from scapy.packet import NoPayload
from IPy import IP

class CommandPcap(Command):
    name = "pcap"
    description = "Check for indicators in a pcap file"

    def add_arguments(self, parser):
        parser.add_argument('--server', '-s',  help='Server used for the request')
        parser.add_argument('FILE',  help='Pcap file')
        parser.add_argument('--verbose', '-v', action='store_true', help='Pcap file')

    def parse_http_header(self, headers):
        # TODO: extract user-agent
        data = headers.strip().split('\r\n')
        host = None
        for d in data[1:]:
            if d.startswith('Host:'):
                host = d.split()[1]
        return {'host': host, 'path': data[0].split()[1]}

    def run(self, conf, args):
        if args.server:
            if args.server not in conf:
                print('Invalid server name')
                sys.exit(1)
            else:
                server = MispServer(
                    url=conf[args.server]['url'],
                    apikey=conf[args.server]['key'],
                )
        else:
            server = MispServer(
                url=conf['default']['url'],
                apikey=conf['default']['key'],
                ssl_chain=False
            )
        packets = rdpcap(args.FILE)
        indicators = set()
        for p in packets:
            if 'IP' in p:
                if IP(p['IP'].src).iptype() != 'PRIVATE':
                    indicators.add(p['IP'].src)
                if IP(p['IP'].dst).iptype() != 'PRIVATE':
                    indicators.add(p['IP'].dst)
                # DNS layer
                if 'DNS' in p:
                    indicators.add(p['DNS'].qd.qname.decode('utf-8')[:-1])
                    if p['DNS'].an:
                        for i in range(p['DNS'].ancount):
                            indicators.add(p['DNS'].an[i].rrname.decode('utf-8')[:-1])
                            # Sometimes a bytes sometimes a str, weird
                            if isinstance(p['DNS'].an[i].rdata, str):
                                rdata = p['DNS'].an[i].rdata
                            else:
                                rdata = p['DNS'].an[i].rdata.decode('utf-8')
                            try:
                                if IP(rdata).iptype() != 'PRIVATE':
                                    indicators.add(rdata)
                            except ValueError:
                                # Not a valid IP
                                pass
                # HTTP layer
                if 'TCP' in p:
                    # Sadly we have to limit to port 80
                    if p['TCP'].dport == 80:
                        if not isinstance(p['TCP'].payload, NoPayload):
                            # There is a payload
                            if b'HTTP/1' in p['TCP'].payload.load:
                                if b'Host:' in p['TCP'].payload.load:
                                    # Parse HTTP headers here
                                    infos = self.parse_http_header(p['TCP'].payload.load.decode('utf-8'))
                                    if infos['host']:
                                        indicators.add(infos['host'])
                                    else:
                                        infos['host'] = p['IP'].dst
                                    indicators.add('http://%s%s' % (infos['host'], infos['path']))

                    # TODO: HTTPs
        # Check in MISP now
        found = False
        for ioc in indicators:
            if args.verbose:
                print('Checking %s' % ioc)
            res = server.attributes.search(value=ioc)
            if len(res) > 0:
                found = True
                print("Search %s, result founds:" % ioc)
                for event in res:
                    print("[+] %i - %s" % (event.id, event.info))
        if not found and not args.verbose:
            print('Nothing found')
