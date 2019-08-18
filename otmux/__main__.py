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
        otmux.Otmux().remote(hosts, args.session, args.psize, args.count, args.instances, args.dry)
    elif args.login is True:
        otmux.Otmux().login(hosts, args.session, args.psize, args.count, args.instances, args.dry)

