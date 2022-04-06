#!/usr/bin/python3
from tools import *
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--account", help="Unique name for account to create", type=str)
parser.add_argument("--database", help="Existing account name for databse", type=str)

args = parser.parse_args()

if args.account :
    create_account(args.account)
if args.database :
    create_database(args.database)

