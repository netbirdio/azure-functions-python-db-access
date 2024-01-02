#!/bin/sh

echo "Starting netbird"
/bin/netbird up &

echo "Starting Azure Functions handler"
/azure-functions-host/Microsoft.Azure.WebJobs.Script.WebHost