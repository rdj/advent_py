#!/usr/bin/env python3

def readinput():
    with open("input.txt", "r") as infile:
        return infile.read().splitlines()

print(readinput())
