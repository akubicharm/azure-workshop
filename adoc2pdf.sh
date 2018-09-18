#!/bin/bash

checkDirname() {
  _d=$1
  if [ $_d -a -d $_d ] ; then
    echo $_d
  fi
}

checkFilename() {
  _d=$1
  _f=$2
  if [ $_f -a -f $_d/$_f ] ; then
    echo $_f
  fi
}

_dir=""
_file=""

if [ $# -eq 2 ] ; then
   _dir=`checkDirname $1`
   _file=`checkFilename $_dir $2`
fi
  
while [ -z $_dir ] ; do
  echo -n "asciidoc directory[$_dir]> "
  read _d
  _dir=`checkDirname $_d`
  echo "DIRECTORY [ $_dir ]"
done

while [ -z $_file ] ; do
  echo -n "target file[$_file]> "
  read _f
  _file=`checkFilename $_dir $_f`
  echo "FILE [ $_file ]"
done

echo "docker run -it -v `pwd`/$_dir:/documents/ asciidoctor/docker-asciidoctor asciidoctor-pdf $_file"
docker run -it -v `pwd`/$_dir:/documents/ asciidoctor/docker-asciidoctor asciidoctor-pdf $_file
