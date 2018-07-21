# otmux

Perform multiple remote activities using tmux

## Installation

#### To install from release (Built on linux)

```console
sudo su
curl -L https://github.com/rda3mon/otmux/releases/download/v0.1-pre/otmux -o /usr/local/bin/otmux
chmod +x /usr/local/bin/otmux
```

#### To install from source

For latest release

```console
git clone https://github.com/rda3mon/otmux.git /tmp/otmux && cd /tmp/otmux
make && sudo make install
```

For specific release

```console
git clone https://github.com/rda3mon/otmux.git --branch v0.1-pre /tmp/otmux && cd /tmp/otmux
make && sudo make install
```

## Usage

```console
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
