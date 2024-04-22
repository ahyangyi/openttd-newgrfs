#!/bin/bash
export GOPATH=$PWD/gopath
go install github.com/ahyangyi/gorender/cmd@daeb83b4
mv gopath/bin/cmd gopath/bin/gorender
go install github.com/ahyangyi/cargopositor/cmd@152f976
mv gopath/bin/cmd gopath/bin/positor
go install github.com/ahyangyi/gandalf/cmd@f44011df
mv gopath/bin/cmd gopath/bin/layer-filter
