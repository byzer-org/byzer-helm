import ruamel.yaml
from kubernetes import client, config
import socket
from urllib.parse import urlparse


def get_cluster_url() -> str:
    config.load_kube_config()
    v1 = client.CoreV1Api()
    api_server = v1.api_client.configuration.host
    parse_result = urlparse(api_server)
    if parse_result.hostname == "127.0.0.1":
        host = socket.gethostbyname(socket.gethostname())
        api_server = parse_result.scheme + "://" + host + ":" + str(parse_result.port)
        print(api_server)
    return api_server


def rewrite_conf(conf: dict) -> dict:

    conf['clusterUrl'] = get_cluster_url()

    spark_conf = conf['spark']
    spark_conf['driver.memory'] = "1024m"
    spark_conf['driver.cores'] = "1"
    spark_conf['executor.memory'] = "512m"
    spark_conf['kubernetes.driver.limit.cores'] = "400m"
    spark_conf['kubernetes.driver.request.cores'] = "400m"
    spark_conf['kubernetes.executor.limit.cores'] = "200m"
    spark_conf['kubernetes.executor.request.cores'] = "200m"

    byzer_conf = conf['byzer']
    byzer_conf['mainJar'] = "byzer-lang-3.3.0-2.12-2.3.5.jar"

    image_conf = conf['image']
    image_conf["repository"] = "byzer/byzer-lang-k8s-full"
    image_conf["tag"] = "3.3.0-2.3.5-2023-03-09"

    conf['fs']['cloud']['storage']['enabled'] = False
    conf['readinessProbe']['initialDelaySeconds'] = 120
    conf['minReadySeconds'] = 120
    conf['livenessProbe']['initialDelaySeconds'] = 120

    return conf


yaml = ruamel.yaml.YAML()
yaml.preserve_quotes = True
with open('values.example.yaml') as fp:
    data = yaml.load(fp)
rewrite_conf(data)

with open('values.yaml', 'w') as outfile:
    yaml.dump(data, outfile)
