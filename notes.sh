#!/bin/sh
python3 notes.py > notes.ly
lilypond notes.ly
