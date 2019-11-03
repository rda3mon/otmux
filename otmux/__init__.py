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
            return "ssh -oStrictHostKeyChecking=no {};bash".format(host)
        else:
            run_command = run_command.replace('"', '\\"')
            return "ssh -oStrictHostKeyChecking=no {} '{}' | sed \"s/^/{}#/\" > {}/{}.log;bash".format(host, run_command, host, out_directory, host)

    def run(self, hosts, session_name, create_session, pane_size, session_count, filters, run_command, out_directory, stay, dry):
        hosts = self.filter_hosts(hosts, filters)

        first = hosts[0]
        session_command = ""
        if create_session is True:
            command = '''tmux new -s {} -d "{}"'''.format(session_name, self.construct_command(first, run_command, out_directory))
            session_command = "-t {}".format(session_name)
        else:
            command = '''tmux new-window "{}"'''.format(self.construct_command(first, run_command, out_directory))



        flag = True # first host is already loaded
        windows = 1
        count = 0
        for host in hosts:
            for i in range(0, session_count):
                if flag:
                    flag = False
                    continue
                count += 1
                if count%pane_size == 0:
                    windows += 1;
                    command += ''' \; new-window {} "{}"'''.format(session_command, self.construct_command(host, run_command, out_directory))
                else:
                    command += ''' \; split-window {} -h "{}"'''.format(session_command, self.construct_command(host, run_command, out_directory))
                command += " \; select-layout {} tiled".format(session_command)

        for window in range(windows, 0, -1):
            if len(hosts) > 1:
                command += " \; set-window-option {} synchronize-panes on".format(session_command)
            if window != 1:
                command += " \; select-window {} -t-1".format(session_command)
            elif create_session:
                command += " \; select-pane {}".format(session_command + ":1")
            else:
                command += " \; select-pane {}".format("-t 1")

        if not stay and create_session is True:
            command += " \; switch-client -t {}:1".format(session_name)

        if dry:
            print("Dry Command: {}".format(command));
        else:
            exit_status = call(command, shell=True)
