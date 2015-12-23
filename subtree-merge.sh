#!/bin/zsh
repo="$1"
short=${${repo/#git*com:8leggedunicorn\/}/%.git/}
git remote add -f $short $repo
# Merge the ${short} repository into master repository:
git merge -s ours --no-commit ${short}/master
# Create a new dir ${short}, copy the Git history to it:
git read-tree --prefix=${short}/ -u ${short}/master
# Merge in changes:
git commit -m "merged in ${short}"
