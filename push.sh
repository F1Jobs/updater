#!/bin/bash

# Bash script which runs the updater script, checks for any unstaged
# changes in the local 'client' directory, and if found, stages,
# commits and pushes them to the client's remote git repository
# (https://github.com/F1Jobs/client), from where the website is
# served. The only directory in the client repo where changes are
# intended is 'data/'. This script is run every 'x' minutes(usually
# x=30) with cron.

# There are certain things to be ensured before anyone even attempts
# to run this. These things are assumed to be present and no part of
# this script is configured to handle errors that arise from absence
# or misconfiguration of these requirements.
# - Python 3.5 or greater is installed
# - PhantomJS executable (2.1.x) is present and added to the PATH
# - Python libraries required by 'getjobs.py' are installed
# - git is installed and configured to push to the remote repos
# - You are on the 'master' branch, and the remote or local repos
#   are not corrupted in any form

# Get to the updater directory inside updater repo
cd updater

# Run the updater script
python3 getjobs.py

# Get to the client directory
cd /home/ayush/Projects/client

# Check if there is something to be committed, if yes, stage the changes,
# otherwise terminate indicating success
if [[ $(git status --porcelain | head -c1 | wc -c) -ne 0 ]]; then
    git add --all
else
    exit 0
fi

# Commit the changes
git commit -m "Site updated"

# A fancy 1-liner that can replace the above two sections if you don't care
# about untracked files
# git diff --exit-code --no-patch && exit 0 || git commit -a -m "Site updated"

# Push to remote
git push origin master