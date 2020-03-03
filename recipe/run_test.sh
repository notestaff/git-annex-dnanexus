#!/bin/bash

set -e -o pipefail -x

echo "PREPARE" | git-annex-remote-dnanexus | grep PREPARE-SUCCESS
echo "PREPARE" | git-annex-remote-dnanexus | grep PREPARE-SUCCESS


