#! /usr/bin/env python
import os
import sys
from mispcli.commands.base import Command
from mispy import MispServer

class CommandEvents(Command):
    name = "events"
    description = "Gather information on an ASN"

    def add_arguments(self, parser):
        parser.add_argument('--server', '-s',  help='Server used for the request')

    def run(self, conf, args):
        server = MispServer(
            url=conf['default']['url'],
            apikey=conf['default']['key'],
            ssl_chain=False
        )
        events = server.events.list(0)
        for event in sorted(events, key=lambda x:x.id):
            print("%i : %s" % (event.id, event.info))



