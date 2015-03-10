 #!/bin/bash

function sfu()
{
    # setup ROOT, Python etc.
    #export ROOT_VERSION=5.34.09.hsg7 #5.34.07
    # export ROOT_VERSION=5.34.10 # skims
    #export ROOT_VERSION=5.34.head
    #export ROOT_VERSION=5.34.14
    export ROOT_VERSION=5.34.18 # new TMVA
    source /atlas/software/bleedingedge/setup.sh
    export PATH=${HOME}/.local/bin${PATH:+:$PATH}

    # setup Python user base area
    export PYTHONUSERBASE=/cluster/data10/endw/local/sl5
    #export PYTHONUSERBASE=${homenodepath}/local/${OS_VERSION}
    export PATH=${PYTHONUSERBASE}/bin${PATH:+:$PATH}
}

sfu


# This script will work in either bash or zsh.

# deterine path to this script
# http://stackoverflow.com/questions/59895/can-a-bash-script-tell-what-directory-its-stored-in
SOURCE_HTAUTAUGENERATION_SETUP="${BASH_SOURCE[0]:-$0}"

DIR_HTAUTAUGENERATION_SETUP="$( dirname "$SOURCE_HTAUTAUGENERATION_SETUP" )"
while [ -h "$SOURCE_HTAUTAUGENERATION_SETUP" ]
do
  SOURCE_HTAUTAUGENERATION_SETUP="$(readlink "$SOURCE_HTAUTAUGENERATION_SETUP")"
  [[ $SOURCE_HTAUTAUGENERATION_SETUP != /* ]] && SOURCE_HTAUTAUGENERATION_SETUP="$DIR_HTAUTAUGENERATION_SETUP/$SOURCE_HTAUTAUGENERATION_SETUP"
  DIR_HTAUTAUGENERATION_SETUP="$( cd -P "$( dirname "$SOURCE_HTAUTAUGENERATION_SETUP"  )" && pwd )"
done
DIR_HTAUTAUGENERATION_SETUP="$( cd -P "$( dirname "$SOURCE_HTAUTAUGENERATION_SETUP" )" && pwd )"

#echo "sourcing ${SOURCE_HTAUTAUGENERATION_SETUP}..."