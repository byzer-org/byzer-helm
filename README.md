# Byzer-helm

Byzer helm project is desighed to help the users deploy Byzer-lang  and Byzer Notebook in Kubernetes.

## Byzer-lang

Create servicecount and role in Kubernetes for Byzer-lang Engine:

```shell
kubectl apply -f byzer-rbac.yaml
```

Then rename `values.example.yaml` to `values.yaml`. Something must be configured according to your requirements:

1. clusterUrl: Kubenertes Cluster URL
2. fs.*: Object Store

## Byzer-notebook

Rename `values.example.yaml` to `values.yaml`. Something must be configured according to your requirements:

1. notebook.url: The url of this deployment.
1. notebook.mlsql.engine-url: The Byzer-lang URL.
2. notebook.database.* : You should create the db before install Byzer Notebook.  Tables will be auto generated.
