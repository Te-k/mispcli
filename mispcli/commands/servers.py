#! /usr/bin/env python
import os
import sys
from mispcli.commands.base import Command
from mispy import MispServer

class CommandServers(Command):
    name = "servers"
    description = "List configured servers"

    def add_arguments(self, parser):
        pass

    def run(self, conf, args):
        for c in conf:
            print('%s: %s' % (
                    c,
                    conf[c]['url']
                )
            )
