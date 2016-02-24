#!/usr/bin/env python

import os
import sys
import yaml
from time import sleep
from threading import Thread
from cement.core.foundation import CementApp
from cement.ext.ext_argparse import ArgparseController, expose
from cement.utils import shell
# from blessings import Terminal

# term = Terminal()
from colorama import init, Fore, Back
init(autoreset=True)
FORES = [ 
    Fore.WHITE,
    Fore.CYAN, 
    Fore.MAGENTA, 
    Fore.BLUE, 
    Fore.YELLOW, 
    Fore.GREEN, 
    Fore.RED, 
]
BACKS = [
    Back.RED,
    Back.GREEN,
    Back.YELLOW, 
    Back.BLUE, 
    Back.MAGENTA, 
    Back.CYAN,    
]
COLORS = []
for color in FORES:
    COLORS.append(color)
    for back_color in BACKS:
        COLORS.append(color + back_color)
for color in BACKS:
    COLORS.append(color)

# need more options when doing crazy shit loads of threads...
COLORS = COLORS + COLORS + COLORS + COLORS + COLORS + COLORS + COLORS + COLORS


def runner(command, verbose=False):
    if verbose:
        runit = getattr(shell, 'exec_cmd2')
    else:
        runit = getattr(shell, 'exec_cmd')

    p = runit(
            command, 
            shell=True, 
            stdout=shell.PIPE, 
            stderr=shell.PIPE,
            )
    return p

class BaseController(ArgparseController):
    class Meta:
        label = 'base'
        arguments = [
            (
                ['-v', '--verbose'],
                dict(
                    help='verbose level output',
                    dest='verbose',
                    action='store_true',
                    ),
            ),
            (
                ['--no-color'],
                dict(
                    help='do not use terminal colors',
                    dest='no_color',
                    action='store_true',
                    ),
            ),
        ]

    @expose(hide=True)
    def default(self):
        print('A sub-command is required.  See `--help`')
        self.app.exit_code = 1
        

    @expose(
        arguments=[
            (
                ['run_config'], 
                dict(
                    help='path to run configuration file', 
                    action='store',
                    metavar='PATH',
                    )
            ),
            (
                ['-m'], 
                dict(
                    help='run mode [thread, process]', 
                    action='store',
                    choices=['thread', 'process'],
                    metavar='MODE',
                    default='thread',
                    dest='mode',
                    )
            ),
            (
                ['--with-prep'], 
                dict(
                    help='do prep commands', 
                    action='store_true',
                    dest='with_prep',
                    )
            ),
        ],
    )
    def run(self):
        assert os.path.exists(self.app.pargs.run_config), \
            "Run configuration file %s does not exist" % \
            self.app.pargs.run_config
        config = yaml.load(open(self.app.pargs.run_config, 'r').read())

        assert config, "Run configuration is un-readable (Invalid Yaml?)"
        assert 'commands' in config.keys(), \
            "Run configuration has no commands defined"
            
        if 'sleep' not in config.keys():
            config['sleep'] = 1
        if 'prep' not in config.keys():
            config['prep'] = []

        if self.app.pargs.with_prep and 'prep' in config.keys():
            for prep in config['prep']:
                shell.exec_cmd(prep, shell=True)

        items = []

        index = 0
        for command in config['commands']:
            item = {
                'command' : command, 
                'id' : index,
                'color' : COLORS[index],
            }
            item[self.app.pargs.mode] = None
            items.append(item)
            index += 1

        while True:
            for i in items:
                mode = self.app.pargs.mode
                spawn = getattr(shell, 'spawn_%s' % mode)
                verbose = self.app.pargs.verbose

                if i[mode] is None or not i[mode].is_alive():
                    if self.app.pargs.no_color:
                        msg = '{mode} #{id}: {command}'.format(
                            mode=mode.capitalize(),
                            id=i['id'],
                            command=i['command'],
                            )
                    else:
                        msg = '{color}{mode} #{id}: {command}'.format(
                                mode=mode.capitalize(),
                                color=i['color'],
                                id=i['id'],
                                command=i['command'],
                                )
                    print(msg)
                    i[mode] = spawn(runner, args=(i['command'], verbose))
                else:
                    pass

            sleep(int(config['sleep']))


class NaughtyBoy(CementApp):
    class Meta: 
        label = 'naughtyboy'
        base_controller = BaseController
        exit_on_close = True

def main():
    with NaughtyBoy() as app:
        try:
            app.run()
        except AssertionError as e:
            print("Caught AssertionError: %s" % e.args[0])
            app.exit_code = 1

if __name__ == '__main__':
    main()
