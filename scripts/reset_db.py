#!/usr/bin/env python3
"""
FitTrack Demo Database Reset Script
Usage: python scripts/reset_db.py
"""
import os
import sys

# Ensure repository root is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.init_db import init_db

def main():
    print("Resetting FitTrack SQLite database to fresh demo state...")
    init_db(force=True)
    print("FitTrack database successfully reset with sample records!")

if __name__ == '__main__':
    main()
