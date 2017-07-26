#!/usr/bin/env bash
puppet resource service @{servicename} ensure=running enable=@{enable}
