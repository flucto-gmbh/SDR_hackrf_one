#!/bin/bash

hackrf_sweep -f $1:$2 -r $3 -N 100 -w 50000
