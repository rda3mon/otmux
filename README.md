# otmux
perform multiple remote activities using tmux

## Usage
```
usage: otmux [-h] (-m HOSTS | -H HOSTSFILE) (-r | -l) -s SESSION [-d]

Multi remote actions using Tmux and ssh

optional arguments:
  -h, --help            show this help message and exit
  -m HOSTS, --hosts HOSTS
                        hosts, space seperated
  -H HOSTSFILE, --hostsfile HOSTSFILE
                        host file, line seperated
  -r, --remote          should you perform operations remotely
  -l, --login           should you login into each of the hosts
  -s SESSION, --session SESSION
                        session name
  -d, --dry             Dry run

```
