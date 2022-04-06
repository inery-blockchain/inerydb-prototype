#!/usr/bin/python3
import argparse
from tools import *


parser = argparse.ArgumentParser()

parser.add_argument("--set", help="insert data in your table", action='store_true')
parser.add_argument("--embedd", help="name of contract and name of account to merge", nargs='+')


args = parser.parse_args()

if args.set :
    account = input("Account name : \n")
    table = input("Table name : \n" )
    action = 'set' + table
    accAbi = get_abi(account)
    accJson = json.loads(accAbi)

    argumentList = []
    for obj in accJson['structs'] :
        if obj["name"] == action :
            argumentList = obj["fields"] 
    numArg = len(argumentList)
    proData = "'["
    partStringData = ",\"{}\""
    partIntData = ",{}"
    endData = "]'"
    partData = ''
    for e in argumentList :
        if e['type'] == 'string' :
            partData += partStringData.format(input('Set "{}" field <string> type \n'.format(e['name'])))
        if e['type'] == 'int32' :
            partData += partIntData.format(input('Set "{}" field <int> type \n'.format(e['name'])))
    partData = partData[1:]

    data = proData + partData + endData
  
    push_action(account, action, data)

if args.embedd :
    transfer_emmbed(args.embedd[0],args.embedd[1] )