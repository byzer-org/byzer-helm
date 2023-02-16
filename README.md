# Byzer-helm

Byzer helm project is desighed to help the users deploy Byzer-lang  and Byzer Notebook in Kubernetes.

## tested helm

1. helm >= 3.9 

## Repo

```
helm repo add byzer http://store.mlsql.tech/charts
helm repo update
```

## Byzer-lang

Command with `--set`:

```shell
helm install -n byzer --create-namespace bz byzer/Byzer-lang \
--set clusterUrl=https://192.168.3.42:16443 \
--set fs.defaultFS=oss://xxxx \
--set fs.impl=org.apache.hadoop.fs.aliyun.oss.AliyunOSSFileSystem \
--set fs."oss\.endpoint"=oss-cn-hangzhou.aliyuncs.com \
--set fs."oss\.accessKeyId"=xxxx \
--set fs."oss\.accessKeySecret"=xxxxx
```

Command with `--values values.[instance name].yaml`


```shell
helm install -n byzer --create-namespace bz byzer/Byzer-lang --values values.bz.yaml
```

The content of `values.overwrite.yaml`:

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
```

The more configuration examples of object store e.g. S3, Blob,Cos please check the [values.example.yaml](https://github.com/byzer-org/byzer-helm/blob/master/byzer-lang/values.example.yaml)

If you want to deploy multi byzer-lang Engine, you should run it with different name and serviceAccount. For example: 


```shell
helm install -n byzer --create-namespace bmz byzer/Byzer-lang \
--set clusterUrl=https://192.168.3.42:16443 \
--set fs.defaultFS=oss://xxxx \
--set fs.impl=org.apache.hadoop.fs.aliyun.oss.AliyunOSSFileSystem \
--set fs."oss\.endpoint"=oss-cn-hangzhou.aliyuncs.com \
--set fs."oss\.accessKeyId"=xxxx \
--set fs."oss\.accessKeySecret"=xxxxx \
--set serviceAccount.name=byzer-bmz
```

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



## Byzer-notebook

```shell
helm install -n byzer --create-namespace nb byzer/Byzer-notebook \
--set name=nb-byzer-notebook \
--set engine=bz-byzer-lang-service \
--set domain=cluster.local \
--set notebook."database\.ip"=192.168.3.14 \
--set notebook."database\.username"=xxx \
--set notebook."database\.password"=xxxx
```

Notice that the name is the Byzer Notebook service name, and the engine is the byzer engine service name which the byzer notebook try to connect.
