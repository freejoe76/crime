#!/bin/bash
# Aliases of commonly used commands. A shortcut list.
# Usage:
# $ source source.sh
alias gpa='git pull -a'

alias fixmongo='sudo rm /var/lib/mongodb/mongod.lock; sudo -u mongodb mongod -f /etc/mongodb.conf --repair'
alias setlocal='export DENVERCRIME_SETTINGS=/home/joe/crime/site/public/settings.cfg; echo "Python Environment: $DENVERCRIME_SETTINGS"'
alias setprod='export DENVERCRIME_SETTINGS=/path/to/settings.cfg; echo "Python Environment: $DENVERCRIME_SETTINGS"'
alias dbs="sudo mongod --config /etc/mongodb.conf"
alias venv='. ~/crime/crime/bin/activate'
alias sss="source source.bash"
