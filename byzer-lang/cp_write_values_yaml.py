#!/usr/bin/env python

import ruamel.yaml
from kubernetes import client, config

config.load_kube_config()
v1 = client.CoreV1Api()
apiServer = v1.api_client.configuration.host

yaml = ruamel.yaml.YAML()
yaml.preserve_quotes = True
with open('values.example.yaml') as fp:
    data = yaml.load(fp)
for elem in data:
    data['clusterUrl'] = apiServer
    break  # no need to iterate further
with open('values.yaml', 'w') as outfile:
    yaml.dump(data, outfile)
