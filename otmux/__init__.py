#!/usr/bin/env python3

import argparse
import sys
import re
from subprocess import call
import random

class Otmux():
    def __init__(self):
        pass

    def filter_hosts(self, hosts, filters):
        if filters == "first":
            return [hosts[0]]
        elif filters == "last":
            return [hosts[-1]]
        elif filters == "any":
            return [random.choice(hosts)]
        else:
            return hosts

    def construct_command(self, host, run_command, out_directory):
        if run_command is None:
            return "ssh {}".format(host)
        else:
            run_command = run_command.replace('"', '\\"')
            return "ssh {} '{}' | sed \"s/^/{}#/\" > {}/{}.log".format(host, run_command, host, out_directory, host)

    def run(self, hosts, session_name, pane_size, session_count, filters, run_command, out_directory, dry):
        hosts = self.filter_hosts(hosts, filters)


        first = hosts[0]
        command = '''tmux new -s {} -d "{}"'''.format(session_name, self.construct_command(first, run_command, out_directory))

        flag = True # first host is already loaded
        windows = 1
        count = 0
        for host in hosts:
            for i in range(0, session_count):
                if flag:
                    flag = False
                    continue
                count += 1
                if count%psize == 0:
                    windows += 1;
                    command += ''' \; new-window -t {} "{}"'''.format(session_name, self.construct_command(host, run_command, out_directory))
                else:
                    command += ''' \; split-window -t {} -h "{}"'''.format(session_name, self.construct_command(host, run_command, out_directory))
                command += " \; select-layout -t {} tiled".format(session_name)


        for window in range(windows, 0, -1):
            command += " \; select-window -t {}:{}".format(session_name, window)
            command += " \; set-window-option -t {}:{} synchronize-panes on".format(session_name, window)
        command += " \; select-pane -t {}:1".format(session_name)

        if dry:
            print("Dry Command: {}".format(command));
        else:
            exit_status = call(command, shell=True)
