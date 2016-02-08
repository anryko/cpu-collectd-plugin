#!/usr/bin/env python
# -*- coding: utf-8; -*-

import collectd
import time


# Global variables

NAME = 'cpu_info'
VERBOSE = True


# Helper functions

def get_stats():
    """ Reads /proc/stat and returns array of cpu stats.
    """
    with open('/proc/stat', 'r') as f:
        arr = f.readline().split()
    arr.pop(0)
    return ([float(a) for a in arr ] + [0] * 10)[:10]


def log(t, message):
    """ Log messages to collectd logger
    """
    if t == 'err':
        collectd.error('{0}: {1}'.format(NAME, message))
    elif t == 'warn':
        collectd.warning('{0}: {1}'.format(NAME, message))
    elif t == 'verb':
        if VERBOSE:
            collectd.info('{0}: {1}'.format(NAME, message))
    else:
        collectd.info('{0}: {1}'.format(NAME, message))


def configure_callback(conf):
    """ Config data from collectd
    """
    log('verb', 'configure_callback Running')
    global NAME, VERBOSE
    for node in conf.children:
        if node.key == 'Name':
            NAME = node.values[0]
        elif node.key == 'Verbose':
            if node.values[0] == 'False':
                VERBOSE = False
        else:
            log('warn', 'Unknown config key: {0}'.format(node.key))


def read_callback():
    """ Prepare data for collectd
    """
    log('verb', 'read_callback Running')

    stats = get_cpustats()

    if not stats:
        log('verb', 'No statistics received')
        return

    for metric, percent in stats:
        log('verb', 'Sending value: {0} {1}'.format(metric, percent))
        value = collectd.Values(plugin=NAME)
        value.type = 'percent'
        value.type_instance = metric
        value.values = [ str(percent) ]
        value.dispatch()


def get_cpustats():
    """ Get CPU stats in percentages
    """
    cpu = get_stats()
    time.sleep(5)
    cpun = get_stats()

    deltas = [ n[0] - n[1] for n in zip(cpun, cpu) ]
    dj = sum(deltas)
    percent = [ ((d / dj) * 100) for d in deltas ]

    columns = [
        'user',
        'nice',
        'system',
        'idle',
        'wait',
        'interrupt',
        'softirq',
        'steal',
        'guest',
        'guestn'
    ]

    return zip(columns, percent)


# Register to collectd
collectd.register_config(configure_callback)
collectd.warning('Initialising {0}'.format(NAME))
collectd.register_read(read_callback)
