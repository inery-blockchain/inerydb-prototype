#!/usr/bin/python3
import argparse, os
from tools import *


parser = argparse.ArgumentParser()

parser.add_argument("--account", help="Name of account to retireve info")
parser.add_argument("--table", help="Name of table to save", action='store_true')
parser.add_argument("--query", action='store_true', help="Query Table in Database")

args = parser.parse_args()

if args.account :
    account = get_account(args.account)
    print(account)

if args.table :
    account = input("Enter account name : \n")
    scope = account
    table = input("Enter table name : \n")
    json_table = get_table(account, scope, table)  
    path = os.getcwd()
    path = path + '/tables'
    smt = os.path.exists(os.path.join(os.getcwd(), 'tables'))
    if smt :
        pass
    else :
        os.system('mkdir tables')
    t = open('tables/{}.{}.json'.format(account, table), 'w+', encoding='utf-8')
    t.write(json_table)
    t.close()

if args.query :
    account = input("Enter account name : \n")
    table = input("Enter table name : \n")
    accTable = get_table(account, account, table)
    chck = True 
    while chck :
        key = input("Enter key you wanna search table with: \n")
        value = input("Enter value for key to find: \n")
        accTable = query(accTable, key, value)
        accTable = json.dumps(accTable, indent=4,ensure_ascii=False)
        print(accTable)
        x = input('Do you want to subquery this result? \n type [y/n] : \n')
        if x.lower() != 'y' :
            chck = False
        

