#!/bin/bash

# Simple Shell script to install the commit message hook.
#
# @author lgndluke
# ================================================================================================================

if cp commit-msg .git/hooks; then
  echo "Successfully installed commit-msg hook!"
else
  echo "Failed to install commit-msg hook!"
fi

echo "Script finished."
