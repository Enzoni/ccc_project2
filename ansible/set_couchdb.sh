#!/bin/bash

# COMP90024 Assignment 2
# Team: 38
# City: Melbourne
# Members:
# Ziran Gu (1038782)
# Jueying Wang (1016724)
# Yifei Zhou(980429)
# Jiakai Ni (988303)
# Ziyue Liu (1036109)

export ANSIBLE_HOST_KEY_CHECKING=True
. ./group38-openrc.sh; ansible-playbook --ask-become-pass deploy_applications.yaml -i inventory/hosts.ini