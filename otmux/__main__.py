#!/usr/bin/env python3

import sys
import os.path
import argparse
import re

path = os.path.realpath(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(path)))

import otmux

def parseHosts(hostsString):
    hosts = None
    try:
        hosts = re.split(r"[, \t]+", hostsString.strip())
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

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Multi remote actions using Tmux and ssh')

    hostsGroup = parser.add_mutually_exclusive_group(required=True)
    hostsGroup.add_argument("-m", "--hosts", help="hosts with (space, comma, tab) seperated", type=parseHosts)
    hostsGroup.add_argument("-H", "--hostsfile", help="host file, line seperated", type=parseHostsFile)

    parser.add_argument("-p", "--psize", help="number of sessions per window. Default=9", type=int, default=9)
    parser.add_argument("-s", "--sessions", help="number of sessions per instance. Default=1", type=int, default=1)
    parser.add_argument("-n", "--session-name", help="session name", required=True)
    parser.add_argument("-i", "--instances", help="instance to login", default="all", choices=["all", "first", "last", "any"])
    parser.add_argument("-c", "--command", help="command to run remotely")
    parser.add_argument("-o", "--out-directory", help="output the logs to directory")
    parser.add_argument("-d", "--dry", help="Dry run", action="store_true", default=False)

    args = parser.parse_args()

    hosts = None
    if args.hosts is not None:
        hosts = args.hosts
    elif args.hostsfile is not None:
        hosts = args.hostsfile

    otmux.Otmux().run(hosts, args.session_name, args.psize, args.sessions, args.instances, args.command, args.out_directory, args.dry)

