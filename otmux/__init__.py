#!/usr/bin/env python

import argparse
import sys
import re
from subprocess import call
import random

def remote(hosts, session, psize, session_count, instances):
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
    exit_status = call(command, shell=True)

def login(hosts):
    pass


def parseHosts(hostsString):
    hosts = None
    try:
        hosts = re.split(r"[ \t]+", hostsString.strip())
    except:
        raise argparse.ArgumentTypeError("Invalid hostsfile. Failed with "
                                         + str(sys.exc_info()[0]) + ", error: " + str(sys.exc_info()[1]))
    if len(hosts) < 1:
        raise argparse.ArgumentTypeError("Invalid number of hosts passed")

    return hosts


def parseHostsFile(hostsFile):
    hosts = None
    try:
        with open(hostsFile, "r") as f:
            hosts = re.split(r"[ \n\t]", (f.read()).strip())
    except:
        raise argparse.ArgumentTypeError("Invalid hostsfile. Failed with "
                                         + str(sys.exc_info()[0]) + ", error: " + str(sys.exc_info()[1]))
    if len(hosts) < 1:
        raise argparse.ArgumentTypeError("Invalid number of hosts passed")

    return hosts


def main():
    parser = argparse.ArgumentParser(description='Multi remote actions using Tmux and ssh')

    hostsGroup = parser.add_mutually_exclusive_group(required=True)
    hostsGroup.add_argument("-m", "--hosts", help="hosts, space seperated", type=parseHosts)
    hostsGroup.add_argument("-H", "--hostsfile", help="host file, line seperated", type=parseHostsFile)

    actionGroup = parser.add_mutually_exclusive_group(required=True)
    actionGroup.add_argument("-r", "--remote", help="should you perform operations remotely", action="store_true")
    actionGroup.add_argument("-l", "--login", help="should you login into each of the hosts", action="store_true", default=False)

    parser.add_argument("-p", "--psize", help="number of sessions per window. Default=9", type=int, default=9)
    parser.add_argument("-c", "--count", help="number of sessions per instance. Default=1", type=int, default=1)
    parser.add_argument("-s", "--session", help="session name", required=True)
    parser.add_argument("-i", "--instances", help="instance to login", default="all", choices=["all", "first", "last", "any"])
    parser.add_argument("-d", "--dry", help="Dry run", action="store_true", default=False)

    args = parser.parse_args()

    hosts = None
    if args.hosts is not None:
        hosts = args.hosts
    elif args.hostsfile is not None:
        hosts = args.hostsfile

    if args.remote is True:
        remote(hosts, args.session, args.psize, args.count, args.instances)
    elif args.login is True:
        login(hosts, args.session, args.psize, args.count, args.instances)

__all__ = ['main']
