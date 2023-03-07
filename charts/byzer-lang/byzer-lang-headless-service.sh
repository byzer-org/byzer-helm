#!/usr/bin/env bash

driver_pod=$(kubectl get pod| grep "byzer-lang-deployment" | cut -d" " -f1)
[[ -z ${driver_pod} ]] && echo "Unable to get Byzer-lang driver pod" && exit 1

cat <<EOF
Byzer-lang driver pod ${driver_pod}
Creating Byzer-lang driver headless service
EOF

kubectl expose pod "${driver_pod}" --type=ClusterIP --cluster-ip=None


