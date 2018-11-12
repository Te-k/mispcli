#! /usr/bin/env python
import os
import sys
from mispcli.commands.base import Command
from mispy import MispServer, MispEvent, MispAttribute
import csv


class CommandImport(Command):
    name = "import"
    description = "Gather information on an ASN"

    def add_arguments(self, parser):
        parser.add_argument('--server', '-s',
                default='default',
                help='Server used for the request')
        parser.add_argument('FILE', help='File to be imported')
        parser.add_argument('EVENTID', type=int,
                help='File to be imported')

    def run(self, conf, args):
        server = MispServer(
            url=conf[args.server]['url'],
            apikey=conf[args.server]['key']
        )
        # For now only misp csv
        with open(args.FILE) as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')

            line = reader.__next__()
            if line == ['uuid', 'event_id', 'category', 'type', 'value', 'comment', 'to_ids', 'date']:

                event = server.events.get(args.EVENTID)
                count = 0
                for row in reader:
                    new_attr = MispAttribute()
                    new_attr.uuid = row[0]
                    new_attr.category = row[2]
                    new_attr.type = row[3]
                    new_attr.value = row[4]
                    new_attr.comment = row[5]
                    new_attr.to_ids = (row[6] == '1')
                    new_attr.distribution = 5
                    event.attributes.add(new_attr)
                    count += 1
                server.events.update(event)
                print('%i attributes added to the event' % count)
            elif line == ['uuid', 'event_id', 'category', 'type', 'value', 'comment', 'to_ids', 'date', 'object_relation', 'attribute_tag', 'object_uuid', 'object_name', 'object_meta_category']:
                # TODO : handle objects correctly
                event = server.events.get(args.EVENTID)
                count = 0
                for row in reader:
                    new_attr = MispAttribute()
                    new_attr.uuid = row[0]
                    new_attr.category = row[2]
                    new_attr.type = row[3]
                    new_attr.value = row[4]
                    new_attr.comment = row[5]
                    new_attr.to_ids = (row[6] == '1')
                    new_attr.distribution = 5
                    event.attributes.add(new_attr)
                    count += 1
                server.events.update(event)
                print('%i attributes added to the event' % count)
            else:
                print('Invalid csv file')
                sys.exit(1)
