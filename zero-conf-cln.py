#!/usr/bin/env python3
"""Use the openchannel hook to selectively opt-into zeroconf
"""

import json
import sys

from pyln.client import Plugin

plugin = Plugin()


@plugin.hook('openchannel')
def on_openchannel(openchannel, plugin, **kwargs):
    plugin.log(repr(openchannel))
    mindepth = plugin.zeroconf_mindepth

    if openchannel['id'] == plugin.zeroconf_allow_peer:
        plugin.log(f"This peer is in the zeroconf allowlist, setting mindepth={mindepth}")
        return {'result': 'continue', 'mindepth': mindepth}
    else:
        return {'result': 'continue'}


@plugin.hook('custommsg')
def on_custommsg(peer_id, payload, plugin, **kwargs):
    if peer_id != plugin.zeroconf_allow_peer:
        return {'result': 'continue'}

    # Decode payload
    payload_bytes = bytes.fromhex(payload)

    # Check msg type
    msg_type = int.from_bytes(payload_bytes[:2], byteorder='big', signed=False)
    if msg_type != 55443:
        return {'result': 'continue'}

    msg_contents = json.loads(payload_bytes[2:])

    # Check msg method
    msg_method = msg_contents.get('method')
    if msg_method is None or msg_method != "getzeroconfinfo":
        return {'result': 'continue'}

    # Check msg id
    msg_id = msg_contents.get('id')
    if msg_id is None:
        return {'result': 'continue'}

    # Construct reply
    reply_contents = {
        'id': msg_id,
        'result': {
            "allows_your_zeroconf": True,
        }
    }
    plugin.log(f"custommsg: Replying affirmatively to {msg_id}")

    # Encode reply
    reply_bytes = (55445).to_bytes(2, 'big') + json.dumps(reply_contents).encode('utf-8')

    plugin.rpc.sendcustommsg(peer_id, reply_bytes.hex())

    return {'result': 'continue'}


plugin.add_option(
    'zeroconf-allow',
    None,
    'A node_id to allow zeroconf channels from',
)

plugin.add_option(
    'zeroconf-mindepth',
    0,
    'Number of confirmations to require from allowlisted peers',
)


@plugin.init()
def init(options, configuration, plugin):
    plugin.log(f"initializing with configuration: {configuration}")
    plugin.log(f"initializing with options: {options}")

    plugin.zeroconf_mindepth = int(plugin.get_option('zeroconf-mindepth'))

    plugin.zeroconf_allow_peer = plugin.get_option('zeroconf-allow')
    if plugin.zeroconf_allow_peer is None:
        error_msg = "init: option zeroconf-allow is not set"
        plugin.log(error_msg, level="error")
        sys.exit(error_msg)


plugin.run()
