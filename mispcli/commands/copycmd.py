#! /usr/bin/env python
import os
import sys
from mispcli.commands.base import Command
from mispy import MispServer, MispEvent, MispAttribute, MispTransportError

class CommandCopy(Command):
    name = "copy"
    description = "Copy attributes between two events"

    def add_arguments(self, parser):
        parser.add_argument('SERVER_SOURCE',  help='Server source for the copy')
        parser.add_argument('EVENT_SOURCE', help='Event source', type=int)
        parser.add_argument('SERVER_DEST', help='Server destination')
        parser.add_argument('EVENT_DEST', type=int,  help='Event destination')

    def run(self, config, args):
       	if args.SERVER_SOURCE.lower() not in config.keys():
            print("Unknown source server, quitting...")
            sys.exit(1)
        else:
            source_server = MispServer(
                url=config[args.SERVER_SOURCE.lower()]['url'],
                apikey=config[args.SERVER_SOURCE.lower()]['key']
            )

        if args.SERVER_DEST.lower() not in config.keys():
            print("Unknown destination server, quitting...")
            sys.exit(1)
        else:
            dest_server = MispServer(
                url=config[args.SERVER_DEST.lower()]['url'],
                apikey=config[args.SERVER_DEST.lower()]['key']
            )

        try:
            source_event = source_server.events.get(args.EVENT_SOURCE)
        except MispTransportError:
            print("Impossible to find the event source, quitting")
            sys.exit(1)

        try:
            dest_event = dest_server.events.get(args.EVENT_DEST)
        except MispTransportError:
            print("Impossible to find the event destination, quitting")
            sys.exit(1)

        for attr in source_event.attributes:
            dest_event.attributes.add(attr)
        #dest_event.objects.set(source_event.objects)

        try:
            dest_server.events.update(dest_event)
        except requests.exceptions.ConnectionError:
            print("Failed connection")
        except MispTransportError:
            print("Failed connection")
        print('Event copied')
        # TODO : add objects
