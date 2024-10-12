#!/bin/bash
export GOPATH=$PWD/gopath
go install github.com/ahyangyi/gorender/cmd@ad5c9c2
mv gopath/bin/cmd gopath/bin/gorender
go install github.com/ahyangyi/cargopositor/cmd@f9051fa
mv gopath/bin/cmd gopath/bin/positor
go install github.com/ahyangyi/gandalf/cmd@d0c1c3d
mv gopath/bin/cmd gopath/bin/layer-filter
