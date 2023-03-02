#!/usr/bin/env python3
"""Use the openchannel hook to selectively opt-into zeroconf
"""

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
