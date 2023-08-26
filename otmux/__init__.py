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

    def construct_command_ssh(self, host, run_command, out_directory):
        if run_command is None:
            return "ssh -oStrictHostKeyChecking=no {};bash".format(host)
        else:
            run_command = run_command.replace('"', '\\"')
            return "ssh -oStrictHostKeyChecking=no {} '{}' | sed \"s/^/{}#/\" > {}/{}.log;bash".format(host, run_command, host, out_directory, host)

    def construct_command_k8s(self, host, run_command, out_directory, namespace, container, k8s_type, emphemeral_image, shell, tail_number):
            if k8s_type == "shell":
                return "kubectl exec -it {} -n {} -c {} -- {}".format(host, namespace, container, shell)
            elif k8s_type == "debug":
                return "kubectl debug -it {} -n {} --target={} --image={} -- bash".format(host, namespace, container, emphemeral_image)
            else:
                if tail_number is None:
                    return "kubectl logs {} -n {} -c {} -f | less".format(host, namespace, container)
                else:
                    return "kubectl logs {} -n {} -c {} -f --tail={}".format(host, namespace, container, tail_number)

    def construct_command(self, cmd_type, host, run_command, out_directory, namespace, container, k8s_type, emphemeral_image, shell, tail_number):
        cmd = None;
        if cmd_type == "ssh":
            cmd = self.construct_command_ssh(host, run_command, out_directory)
        elif cmd_type == "k8s":
            cmd = self.construct_command_k8s(host, run_command, out_directory, namespace, container, k8s_type, emphemeral_image, shell, tail_number)

        return cmd

    def run(self, cmd_type, hosts, session_name, create_session, pane_size, session_count, filters, run_command, out_directory, stay, namespace, container, k8s_type, emphemeral_image, shell, tail_number, dry):
        hosts = self.filter_hosts(hosts, filters)

        first = hosts[0]
        session_command = ""
        if create_session is True:
            command = '''tmux new -s {} -d "{}"'''.format(session_name, self.construct_command(cmd_type, first, run_command, out_directory, namespace, container, k8s_type, emphemeral_image, shell, tail_number))
            session_command = "-t {}".format(session_name)
        else:
            command = '''tmux new-window "{}"'''.format(self.construct_command(cmd_type, first, run_command, out_directory, namespace, container, k8s_type, emphemeral_image, shell, tail_number))

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
                    command += ''' \; new-window {} "{}"'''.format(session_command, self.construct_command(cmd_type, host, run_command, out_directory, namespace, container, k8s_type, emphemeral_image, shell, tail_number))
                else:
                    command += ''' \; split-window {} -h "{}"'''.format(session_command, self.construct_command(cmd_type, host, run_command, out_directory, namespace, container, k8s_type, emphemeral_image, shell, tail_number))
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
