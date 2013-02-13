import collectd
import logging
import datetime
import time

server_uri = None
interval = 15
values = dict()

def maasi_config(c):
  global child, server_uri, interval
  for child in c.children:
    if child.key == 'server_uri':
      server_uri = child.values[0]
    if child.key == 'interval':
      interval = child.values[0]

def maasi_init():
  d = {
    'server_uri': server_uri,
    'interval': interval
    }
  logging.info('initiating maasi daemon')
  collectd.register_write(maasi_collect, data=d)
  collectd.register_read(maasi_send)

def maasi_send(data=None):
  time.sleep(1)
  global server_uri, values
  fp = open('/var/log/maasi.log', 'a')
  fp.write("%s\n" %str(values.keys()))
  fp.close()
  # clear the values
  values = dict()

def maasi_collect(v, data=None):
  global server_uri, values
  for i in v.values:
    if v.plugin not in values:
      values[v.plugin] = dict()
    if v.type_instance:
      metric = v.type + "__" + v.type_instance
    else:
      metric = v.type

    values[v.plugin][metric] = i

collectd.register_config(maasi_config)
collectd.register_init(maasi_init)
