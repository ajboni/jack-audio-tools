#!/usr/bin/env python3
#
#  client.py
#
"""Query JACK status from a client perspective."""

import argparse
import string
import sys
import json
import jack


def main(args=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        '-c', '--client-name',
        metavar='NAME',
        default='jack_client',
        help="JACK client name (default: %(default)s)")
    ap.add_argument(
        'command',
        nargs='?',
        default='query',
        choices=['query'],
        help="Transport command")

    args = ap.parse_args(args)

    try:
        client = jack.Client(args.client_name)
    except jack.JackError as exc:
        return "Could not create JACK client: {}".format(exc)

    result = 0
    if args.command == 'check':
        # If we get this far we are connected to jack.
        print("running")
        result = 0
    if args.command == 'query':
        res = {
            "status": "running",
            "cpu_load": client.cpu_load(),
            "block_size": client.blocksize,
            "realtime": client.realtime,
            "sample_rate": client.samplerate,
        }

        json.dump(res, sys.stdout, indent=2)
        result = 0

    client.close()
    return result


if __name__ == '__main__':
    sys.exit(main() or 0)
