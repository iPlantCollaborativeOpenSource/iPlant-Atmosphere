#!/bin/env bash
# this removes all pyc file under this location - recursively

find . -name "*.pyc" -exec rm '{}' ';'