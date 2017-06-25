# -*- coding: utf-8 -*-
import json
import time
from collections import OrderedDict

import etcd
from etcd import EtcdKeyNotFound

ETCD_CLIENT = None

BASE_DIR = '/cowry'
CONFIG_DIR = '/'.join((BASE_DIR, 'config')) + '/'
WORKER_DIR = '/'.join((BASE_DIR, 'worker')) + '/'

def etcd_client():
    global ETCD_CLIENT
    if not ETCD_CLIENT:
        ETCD_CLIENT = etcd.Client(host='etcd', port=2397)
    return ETCD_CLIENT


def etcd_ls(key, recursive=False, load_json=True):
    try:
        leaf = etcd_client().read(key, recursive=recursive)
        res = OrderedDict()
        if len(leaf._children) == 0:
            return res
        for r in leaf.leaves:
            l = len(key)
            if not key.endswith('/'):
                l += 1
            k = r.key[l:]
            res[k] = r.value
            if r.value is not None and len(r.value) > 0 and load_json:
                res[k] = json.loads(r.value)
        return res
    except EtcdKeyNotFound:
        return []


def etcd_mkdir(key):
    try:
        return etcd_client().get(key)
    except EtcdKeyNotFound:
        return etcd_client().write(key, value=None, dir=True,
                                   prevExist=False)


def etcd_get(key, load_json=True):
    try:
        r = etcd_client().get(key)
        res = r.value
        if r.value is not None and len(r.value) > 0 and load_json:
            res = json.loads(r.value)
        return res
    except EtcdKeyNotFound:
        return None


def etcd_watch(key, timeout=None, recursive=None):
    while True:
        try:
            r = etcd_client().watch(key, timeout=timeout, recursive=recursive)
        except etcd.EtcdWatchTimedOut:
            LOG.warning('etcd_watch timeout, rewatch now...')
        except Exception as e:
            LOG.error('etcd_watch error: %s' % e)
            time.sleep(1)
        else:
            if r:
                yield r


def etcd_exists(key):
    try:
        etcd_client().get(key)
        return True
    except EtcdKeyNotFound:
        return False


def etcd_version():
    ec = etcd_client()
    data = ec.api_execute('/version', ec._MGET).data.decode('utf-8')
    try:
        return json.loads(data)
    except (TypeError, ValueError):
        raise etcd.EtcdException("Cannot parse json data in the response")


def etcd_wait_ready():
    start = time.time()
    ec = etcd_client()
    while True:
        if time.time() - start > 30:
            return
        try:
            r = ec.api_execute('/version', ec._MGET)
            if r.status == 200:
                return
        except Exception:
            LOG.warning("Fetch etcd version failed, maybe etcd not ready, sleep 1 second to next check.")
        time.sleep(1)
