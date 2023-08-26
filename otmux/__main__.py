#!/usr/bin/env python3

import sys
import os.path
import argparse
import re
import random
import string

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
    parser = argparse.ArgumentParser(description='Multi remote actions using Tmux and ssh or kubectl')

    # Hosts Parser
    hosts_parser = argparse.ArgumentParser(add_help=False);
    hosts_group = hosts_parser.add_mutually_exclusive_group(required=True)
    hosts_group.add_argument("-Hs", "--hosts", help="hosts string with (space, comma, tab) seperated", type=parseHosts)
    hosts_group.add_argument("-H", "--hostsfile", help="host file, line seperated", type=parseHostsFile)

    # Common Parser
    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument("-p", "--psize", help="number of sessions per window. Default=9", type=int, default=20)
    common_parser.add_argument("-s", "--sessions", help="number of sessions per instance. Default=1", type=int, default=1)
    common_parser.add_argument("-sn", "--session-name", help="session name")
    common_parser.add_argument("-sy", "--stay", help="Switch to new session", action="store_true", default=False)
    common_parser.add_argument("-i", "--instances", help="instance to login", default="all", choices=["all", "first", "last", "any"])
    common_parser.add_argument("-c", "--command", help="command to run remotely")
    common_parser.add_argument("-cs", "--create-session", help="Create new session or open in same session", action="store_true", default=False)
    common_parser.add_argument("-o", "--out-directory", help="output the logs to directory")
    common_parser.add_argument("-d", "--dry", help="Dry run", action="store_true", default=False)

    # K8s Shell Parser
    k8s_shell_parser = argparse.ArgumentParser(add_help=False);
    k8s_shell_parser.add_argument("-sh", "--shell", help="Shell to login to container", choices=["bash", "sh"], default="bash")

    # K8s Logs Parser
    k8s_logs_parser = argparse.ArgumentParser(add_help=False);
    k8s_logs_parser.add_argument("-tl", "--tail", help="Number of logs to tail", type=int, default=100)

    # K8s Debug Parser
    k8s_debug_parser = argparse.ArgumentParser(add_help=False);
    k8s_debug_parser.add_argument("-img", "--image", help="Image for ephemeral", required=True)

    # K8s Common Parser
    k8s_common_parser = argparse.ArgumentParser(add_help=False);
    k8s_common_parser.add_argument("-ns", "--namespace", help="K8s namespace", required=True)
    k8s_common_parser.add_argument("-con", "--container", help="k8s pod container", required=True)

    # K8s Parser
    k8s_parser = argparse.ArgumentParser(add_help=False);
    k8s_parsers = k8s_parser.add_subparsers(required=True, dest='k8s_type');
    k8s_parsers.add_parser('logs', parents=[hosts_parser, common_parser, k8s_logs_parser, k8s_common_parser], help='print logs of containers')
    k8s_parsers.add_parser('shell', parents=[hosts_parser, common_parser, k8s_shell_parser, k8s_common_parser], help='login into shell of container')
    k8s_parsers.add_parser('debug', parents=[hosts_parser, common_parser, k8s_debug_parser, k8s_common_parser], help='debug into container with ephemeral containers')

    # SSH Parser
    ssh_parser = argparse.ArgumentParser(add_help=False, parents=[hosts_parser, common_parser]);

    # SSH / K8s Sub parsers
    parsers = parser.add_subparsers(required=True, dest='cmd');
    parsers.add_parser('ssh', parents=[ssh_parser], help='ssh commands in parallel')
    parsers.add_parser('k8s', parents=[k8s_parser], help='k8s kubectl commands in parallel')

    args = parser.parse_args()

    hosts = None
    if args.hosts is not None:
        hosts = args.hosts
    elif args.hostsfile is not None:
        hosts = args.hostsfile

    if args.session_name is None:
        args.session_name = "session-{}".format(''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(5)))

    if args.cmd == "ssh":
        otmux.Otmux().run(args.cmd, hosts, args.session_name, args.create_session, args.psize, args.sessions, args.instances, args.command, args.out_directory, args.stay, None, None, None, None, None, None, args.dry)
    elif args.cmd == "k8s":
        if args.k8s_type == "debug":
            otmux.Otmux().run(args.cmd, hosts, args.session_name, args.create_session, args.psize, args.sessions, args.instances, args.command, args.out_directory, args.stay, args.namespace, args.container, args.k8s_type, args.image, None, None, args.dry)
        elif args.k8s_type == "shell":
            otmux.Otmux().run(args.cmd, hosts, args.session_name, args.create_session, args.psize, args.sessions, args.instances, args.command, args.out_directory, args.stay, args.namespace, args.container, args.k8s_type, None, args.shell, None, args.dry)
        elif args.k8s_type == "logs":
            otmux.Otmux().run(args.cmd, hosts, args.session_name, args.create_session, args.psize, args.sessions, args.instances, args.command, args.out_directory, args.stay, args.namespace, args.container, args.k8s_type, None, None, args.tail, args.dry)

    if args.dry is False and args.create_session is True:
        print("Session - {} created".format(args.session_name))
