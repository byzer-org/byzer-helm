# Byzer-helm

Byzer helm project is desighed to help the users deploy Byzer-lang  and Byzer Notebook in Kubernetes.

## Repo

```
helm repo add byzer http://store.mlsql.tech/charts
```

## Byzer-lang

Create servicecount and role in Kubernetes for Byzer-lang Engine:

```shell
helm install -n byzer --create-namespace bz byzer/Byzer-lang \
--set clusterUrl=https://192.168.3.42:16443 \
--set fs.defaultFS=oss://xxxx \
--set fs.impl=org.apache.hadoop.fs.aliyun.oss.AliyunOSSFileSystem \
--set fs.oss.endpoint=oss-cn-hangzhou.aliyuncs.com \
--set fs.oss.accessKeyId=xxxx \
--set fs.oss.accessKeySecret=xxxxx
```


## Byzer-notebook

```
helm install -n byzer --create-namespace nb byzer/Byzer-notebook \
--set name=nb \
--set engine=bz \
--set notebook.database.ip=192.168.3.14 \
--set notebook.database.username=xxx \
--set notebook.database.password=xxxx
```
