#!/usr/bin/env python3

import argparse
import subprocess
import sys


def output(command):
    return subprocess.check_output(command, text=True).strip()


def main():
    parser = argparse.ArgumentParser(description='Deploy tls.wbond.net')
    parser.add_argument('--host', default='wbond.net')
    parser.add_argument('--user', default='root')
    parser.add_argument('--revision')
    args = parser.parse_args()

    revision = args.revision or output(['git', 'rev-parse', 'HEAD'])
    result = subprocess.run([
        'ssh', '%s@%s' % (args.user, args.host),
        '/usr/local/sbin/deploy-site', 'tls.wbond.net', revision,
    ])
    return result.returncode


if __name__ == '__main__':
    sys.exit(main())
