#!/bin/bash
export GOPATH=$PWD/gopath
go install github.com/ahyangyi/gorender/cmd@latest
mv gopath/bin/cmd gopath/bin/gorender
go install github.com/mattkimber/cargopositor/cmd@latest
mv gopath/bin/cmd gopath/bin/positor
