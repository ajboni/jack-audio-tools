#!/usr/bin/env python3
"""Connects/Disconnects two JACK ports."""

import argparse
import string
import sys
import json
import jack


def connect_ports(src, dst, client_name, disconnect):
    """Connects/Disconnects two JACK ports."""

    try:
        client = jack.Client(args.client_name)
    except jack.JackError as exc:
        return "Could not create JACK client: {}".format(exc)

    try:
        src_port = client.get_port_by_name(src)
        dst_port = client.get_port_by_name(dst)

        # Check for src=output
        if not dst_port.is_input:
            raise ValueError(
                f'Error connecting ports: {dst} is not an INPUT port!')

        # Check for dst=input
        if not src_port.is_output:
            raise ValueError(
                f'Error connecting ports: {src} is not an OUTPUT port!')

        # Check both port to be audio
        if src_port.is_audio and not dst_port.is_audio or dst_port.is_audio and not dst_port.is_audio:
            raise ValueError(
                'Error connecting ports: Both ports are expected to be the same type.')

        # Check both midi ports
        if src_port.is_midi and not dst_port.is_midi or dst_port.is_midi and not dst_port.is_midi:
            raise ValueError(
                'Error connecting ports: Both ports are expected to be the same type.')

    except jack.JackError as exc:
        return "Could not get JACK port: {}".format(exc)

    try:
        if not disconnect:
            client.connect(src_port, dst_port)
        else:
            client.disconnect(src_port, dst_port)
    except jack.JackError as exc:
        return f'Could not make the connection between {src} => {dst} : {exc}'


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        '-c', '--client-name',
        default='jack_client',
        help="JACK client name (default: %(default)s)")
    ap.add_argument(
        'source',
        help="Source port. It must be an output port. It must be same type (audio/midi) as dst)")
    ap.add_argument(
        'destination',
        help="Destination port. It must be an input port. It must be same type (audio/midi) as src")
    ap.add_argument(
        '-rm', '--disconnect', '--remove', '--rm',
        action='store_true',
        default=False,
        help="Disconnect both ports.")

    args = ap.parse_args()

    sys.exit(connect_ports(args.source, args.destination,
                           args.client_name, args.disconnect))
