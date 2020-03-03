#!/bin/bash

set -e -o pipefail

BINARY_HOME=$PREFIX/bin
PACKAGE_HOME=$PREFIX/share/$PKG_NAME-$PKG_VERSION-$PKG_BUILDNUM

mkdir -p $BINARY_HOME
mkdir -p $PACKAGE_HOME

cp ${RECIPE_DIR}/git-annex-remote-dnanexus ${PACKAGE_HOME}/
cp ${RECIPE_DIR}/git-annex-remote-dnanexus.py ${PACKAGE_HOME}/
cp ${RECIPE_DIR}/git-annex-remote-dnanexus.txt ${PACKAGE_HOME}/
ln -s $PACKAGE_HOME/git-annex-remote-dnanexus $BINARY_HOME




