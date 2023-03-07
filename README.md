# Byzer-helm

Byzer helm project is desighed to help the users deploy Byzer-lang  and Byzer Notebook in Kubernetes.

## tested helm

1. helm >= 3.9 

## Repo

```
helm repo add byzer http://store.mlsql.tech/charts
helm repo update
```

Alternatively, you can use latest charts by:
```shell
helm repo add byzer http://byzer-org.github.io/byzer-helm
helm repo update
```

## Byzer-lang

### Command with `--set`:

```shell
helm install -n byzer --create-namespace bz byzer/Byzer-lang \
--set clusterUrl=https://192.168.3.42:16443 \
--set fs.defaultFS=oss://xxxx \
--set fs.impl=org.apache.hadoop.fs.aliyun.oss.AliyunOSSFileSystem \
--set fs."oss\.endpoint"=oss-cn-hangzhou.aliyuncs.com \
--set fs."oss\.accessKeyId"=xxxx \
--set fs."oss\.accessKeySecret"=xxxxx \
--set image.repository="registry.cn-shanghai.aliyuncs.com/kyligence-byzer/byzer-lang-k8s-full" \
--set image.tag="3.3.0-2.4.0-SNAPSHOT-2023-02-16"
```

### Command with `--values values.[instance name].yaml`


```shell
helm install -n byzer --create-namespace bz byzer/Byzer-lang --values values.bz.yaml
```

The content of `values.bz.yaml`:

```yaml
clusterUrl: https://192.168.3.42:16443
fs:
  cloud:
    storage:
      enabled: true
  oss.impl: org.apache.hadoop.fs.aliyun.oss.AliyunOSSFileSystem
  defaultFS: oss://xxxxxx
  oss.endpoint: oss-cn-hangzhou.aliyuncs.com
  oss.accessKeyId: xxxxx
  oss.accessKeySecret: xxxxxx 
  
image:
  repository: registry.cn-shanghai.aliyuncs.com/kyligence-byzer/byzer-lang-k8s-full
  pullPolicy: IfNotPresent
  # Overrides the image tag whose default is the chart appVersion.
  tag: "3.3.0-2.4.0-SNAPSHOT-2023-02-16"    
```

The more configuration examples of object store e.g. S3, Blob,Cos please check the [values.example.yaml](https://github.com/byzer-org/byzer-helm/blob/master/byzer-lang/values.example.yaml)

If you want to deploy multi byzer-lang Engine instance, run it with different name and serviceAccount. For example. For example: 


```shell
helm install -n byzer --create-namespace bmz byzer/Byzer-lang \
--set serviceAccount.name=byzer-bmz
...
```

Here we set name as `bmz` and set serviceAccount.name as byzer-bmz.

### Resource

Here is the default configuration:

```yaml
spark:
  driver.memory: 4g
  driver.cores: 2
  driver.maxResultSize: 1g  
  driver.memoryOverheadFactor: 0.4
  executor.memory: 1g
  executor.cores: 1
  executor.instances: 1   
  executor.memoryOverheadFactor: 0.4
```

The requests/limits of memory resource in Kubenertes are caculated with following fomular:

```
driver: ceil (4g * 0.4(memoryOverheadFactor) + 4g) = 6Gi
executor:  (1g * 0.4(memoryOverheadFactor) + 1g) = 1400Mi
```

## Remote Shuffle Service

Example snippet like following: 

```yaml
spark:
  shuffle.manager: org.apache.spark.shuffle.rss.RssShuffleManager  
  rss.master.address: xxxxx:9097
  serializer: org.apache.spark.serializer.KryoSerializer
  rss.shuffle.writer.mode: hash
  rss.push.data.replicate: true
  shuffle.service.enabled: false
  sql.adaptive.localShuffleReader.enabled: false
  sql.adaptive.enabled: true
  sql.adaptive.skewJoin.enabled: true
```

### Prometheus
Example snippet like following: 

```yaml
spark:
  ui.prometheus.enabled: true  
  metrics.appStatusSource.enabled: true
  kubernetes.driver.annotation.executors.prometheus.io/scrape: true
  kubernetes.driver.annotation.executors.prometheus.io/path: /metrics/executors/prometheus
  kubernetes.driver.annotation.executors.prometheus.io/port: 4040
  kubernetes.driver.annotation.jmx.prometheus.io/scrape: true
  kubernetes.driver.annotation.jmx.prometheus.io/path: /metrics
  kubernetes.driver.annotation.jmx.prometheus.io/port: 8080
  kubernetes.executor.annotation.jmx.prometheus.io/scrape: true
  kubernetes.executor.annotation.jmx.prometheus.io/path: /metrics
  kubernetes.executor.annotation.jmx.prometheus.io/port: 8080
  metrics.conf.*.sink.jmx.class: org.apache.spark.metrics.sink.JmxSink
```

### Add new jar to image

Suppose the user want to add a new jar to Byzer-lang Image, the first step is to create 
an new dockerfile. The content like following:

```dockerfile
# The base image includes
# 1. OpenJDK8
# 2. Spark 3.3.0-bin-hadoop3
# Byzer-lang
# Byzer-lang plugins
# azure-hadoop shade jar
# Directory structure
# |- /work
# |--- spark
# |--- jdk
# |- /home
# |--- deploy
# |------ byzer-lang
# |-------- plugin
# |-------- libs
# |-------- main
# |-------- bin
# |-------- logs

ARG TAG
FROM byzer/byzer-lang-k8s-base:$TAG

ADD https://download.byzer.org/byzer/misc/cloud/oss/byzer-objectstore-oss-3.3_2.12-0.1.0-SNAPSHOT.jar /home/deploy/byzer-lang/libs/
ADD https://download.byzer.org/byzer/misc/rss-shuffle-manager-1.0.0-shaded.jar $SPARK_HOME/jars
```

Then build：

```shell
export BYZER_LANG_VERSION=${BYZER_LANG_VERSION:-2.4.0-SNAPSHOT}
export SPARK_VERSION=${SPARK_VERSION:-3.3.0}

docker build -t byzer/byzer-lang-k8s-full:"${SPARK_VERSION}-${BYZER_LANG_VERSION}" \
--build-arg TAG="${SPARK_VERSION}-${BYZER_LANG_VERSION}" \
-f "/byzer/full/Dockerfile" \
"/byzer/full"
```

## Byzer-notebook

```shell
helm install -n byzer --create-namespace nb byzer/Byzer-notebook \
--set name=nb-byzer-notebook \
--set engine=bz-byzer-lang-service \
--set domain=cluster.local \
--set notebook."database\.ip"=192.168.3.14 \
--set notebook."database\.username"=xxx \
--set notebook."database\.password"=xxxx \
--set image.repository="registry.cn-shanghai.aliyuncs.com/kyligence-byzer/byzer-notebook" \
--set image.tag="1.2.3-2023-02-16"
```

Notice that the name is the Byzer Notebook service name, and the engine is the byzer engine service name which the byzer notebook try to connect.

