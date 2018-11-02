import os
import sys
import argparse
import configparser
from mispcli.commands.base import Command


def parse_config():
    """Parse configuration file, returns a list of servers"""
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.expanduser("~"), ".misp"))
    servers = {}
    for s in config.sections():
        try:
            info = {
                    'url': config.get(s, 'url'),
                    'key': config.get(s, 'key')
            }
            servers[s.lower()] = info
            if config.get(s, 'default').lower() == 'true':
                servers['default'] = info
        except configparser.NoOptionError:
            pass

    return servers


def init_plugins():
    plugin_dir = os.path.dirname(os.path.realpath(__file__)) + '/commands'
    plugin_files = [x[:-3] for x in os.listdir(plugin_dir) if x.endswith(".py")]
    sys.path.insert(0, plugin_dir)
    for plugin in plugin_files:
        mod = __import__(plugin)

    PLUGINS = {}
    for plugin in Command.__subclasses__():
        PLUGINS[plugin.name] = plugin()
    return PLUGINS


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='Commands')

    # Init plugins
    plugins = init_plugins()
    for p in sorted(plugins.keys()):
        sp = subparsers.add_parser(
            plugins[p].name,
            help=plugins[p].description
        )
        plugins[p].add_arguments(sp)
        sp.set_defaults(command=p)

    args = parser.parse_args()
    config = parse_config()
    # TODO : deal with servers here
    if len(config) == 0:
        print('No servers configured')
        sys.exit(1)
    if hasattr(args, 'command'):
        plugins[args.command].run(config, args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
