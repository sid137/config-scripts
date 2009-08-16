#!/bin/bash
ACML=acml-3-6-0-gnu-32bit.tgz

#AMD ACML Math Librarieis
cat > /etc/profile << "EOF"
LD_LIBRARY_PATH=/opt/acml3.6.0/gnu32/lib
export PATH USER LOGNAME MAIL HOSTNAME HISTSIZE INPUTRC LD_LIBRARY_PATH
EOF

mkdir acml
tar -zxf $ACML -C acml
cd acml
./install-acml-3-6-0-gnu-32bit.sh -accept -installdir=/opt/acml3.6.0
cd .. && rm -rf acml
