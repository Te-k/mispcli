#! /usr/bin/env python
import os
import sys
from mispcli.commands.base import Command
from mispy import MispServer


class CommandSearch(Command):
    name = "search"
    description = "Search an attribute in MISP"

    def add_arguments(self, parser):
        parser.add_argument('--server', '-s',  help='Server used for the request')
        parser.add_argument('ATTR',  help='Search for this attribute')

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
        # Search attributes
        res = server.attributes.search(value=args.ATTR)
        if len(res) == 0:
                print("\tNo results")
        else:
            for event in res:
                print("[+] %i - %s" % (event.id, event.info))
                for attr in event.attributes:
                    if args.ATTR.strip().lower() in str(attr.value).lower() or \
                        args.ATTR.strip().lower() in str(attr.comment).lower():
                        print("\t%s (%s / %s) %s" % (attr.value, attr.category, attr.type, attr.comment))
