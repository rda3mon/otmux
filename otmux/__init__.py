#!/usr/bin/env python3

import argparse
import sys
import re
from subprocess import call
import random

class Otmux():
    def __init__(self):
        pass

    def login(self, hosts, session, psize, session_count, instances, dry):
        if instances == "first":
            hosts = [hosts[0]]
        elif instances == "last":
            hosts = [hosts[-1]]
        elif instances == "any":
            hosts = [random.choice(hosts)]

        first = hosts[0]
        command = "tmux new -s {} -d 'ssh {}'".format(session, first)

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
                    command += " \; new-window -t {} 'ssh {}'".format(session, host)
                else:
                    command += " \; split-window -t {} -h 'ssh {}'".format(session, host)
                command += " \; select-layout -t {} tiled".format(session)

        for window in range(windows, 0, -1):
            command += " \; select-window -t {}:{}".format(session, window)
            command += " \; set-window-option -t {}:{} synchronize-panes on".format(session, window)
        command += " \; select-pane -t {}:1".format(session)

        if dry:
            print("Dry Command: {}".format(command));
        else:
            exit_status = call(command, shell=True)

    def remote(self, hosts, session, psize, session_count, instances, dry):
        print("In Development")
