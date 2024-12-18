#!/bin/bash
export GOPATH=$PWD/gopath
go install github.com/ahyangyi/gorender/cmd@cdca513
mv gopath/bin/cmd gopath/bin/gorender
go install github.com/ahyangyi/cargopositor/cmd@f9051fa
mv gopath/bin/cmd gopath/bin/positor
go install github.com/ahyangyi/gandalf/cmd@c363ea1
mv gopath/bin/cmd gopath/bin/layer-filter
