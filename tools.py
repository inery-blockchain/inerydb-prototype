from paramiko  import SSHClient, AutoAddPolicy
import os, json

#HOST INFO
config = open('config.json', 'r') 
config = json.load(config)

host = config["NODE_IP"]
user = config["NODE_USER"]
pw = config["NODE_PASSWORD"]

def log(message):
	print("====================================================================================")
	print(message.center(50, ' '))
	print("====================================================================================")

def connect() :
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    ssh.connect(host, username=user, password=pw)
    return ssh
def create_account(name) :
    res = '--stake-net \"1 INR\" --stake-cpu \"1 INR\" --buy-mem-bytes 1048576'
    ssh = connect()
    if is_account(name) :
        log("User with that account already exist, please try different name")
        exit()
    #create your key pair
    stdin,stdout,stderr= ssh.exec_command('cline create key --to-console')
    keypair= stdout.readlines()
    privatekey = keypair[0]
    privatekey = privatekey.split()[2]
    publickey = keypair[1]
    publickey = publickey.split()[2]
    #import keys in wallet 
    ssh.exec_command('cd; ./unlockWallet.py')
    ssh.exec_command('cline wallet import  --private-key {}'.format(privatekey))

    stdin,stdout,stderr=ssh.exec_command('cline system newaccount --transfer createacc {} {} {}'.format(name,publickey, res))
    output = stdout.readlines()
    if (output) :
        log("Successfully created account!")
        log("Public key :  " + publickey)
        log("Private key : " + privatekey)
        log("Your Inery account name : " + name)
    else :
        log("Account creation failed")

def create_database(name) :
    smt = os.path.exists(os.path.join(os.getcwd(), 'contracts'))
    if smt :
        pass
    else :
        os.system('mkdir contracts')
    else :
        os.system('mkdir tables')
    if is_account(name) :
        pass
    else :
        log("Account with that name doesn't exist. Do you wanna create one?")
        x = input("Type [y/n]\n")
        if x.lower() == 'y' :
            create_account(name)
        else :
            exit()
    contract = generate_contract(name)
    transfer_emmbed(name, contract)

def is_account(acc) :
    log("Verifying {} account..".format(acc))
    ssh = connect()
    stdin,stdout,stderr=ssh.exec_command( "cline get account " + acc)
    err = stderr.readlines()
    if  err :
        return False
    else :
        return True

def transfer_emmbed(name, contract) :
    dir = os.getcwd()
    os.system('cd contracts/{}; ineio-cpp {}.cpp -o {}.wasm'.format(name, contract, contract))
    src1 = dir + '/contracts/{}/{}.wasm'.format(name, contract)
    src2 = dir + '/contracts/{}/{}.abi'.format(name, contract)
    dest1 = '/root/IneryDB/contracts/{}/{}.wasm'.format(name, contract)
    dest2 = '/root/IneryDB/contracts/{}/{}.abi'.format(name, contract)
    ssh = connect()
    ssh.exec_command('mkdir /root/IneryDB/contracts/{}'.format(name))
    ssh.exec_command('cd; ./unlockWallet.py')
    sftp = ssh.open_sftp()
    sftp.put(src1, dest1)
    sftp.put(src2, dest2)
    ssh.exec_command('cline set contract {} /root/IneryDB/contracts/{} {}.wasm {}.abi'.format(name, name, contract, contract))
    log("Successfully created Database")

def generate_contract(accName) :
    contractName = input("Database name : ")
    os.system('mkdir contracts/{}'.format(accName))
    new = open('contracts/{}/{}.cpp'.format(accName, contractName), 'w+')
    const_str = open('gen_helpers/constructor_schema.txt', 'r').read().replace('$classname', contractName)
    tbl_str = open('gen_helpers/table_const_schema.txt', 'r').read()
    struct = open('gen_helpers/struct_schema.txt', 'r').readlines()
    name = struct[0]
    id = struct[1]
    element = struct[2]
    idget = struct[3]
    end = struct[4]
    inst = struct[5]
    action = open('gen_helpers/action_schema.txt', 'r').readlines()
    first = action[0]
    second = action[1]
    setId = action[2]
    setElement = action[3]
    close = action[4]
    numOfTables = int(input("How many tables do you want? "))
    dic=dict()
    k = 0
    #Creating dictinary based on user choice of number of strucutres, elements, theyr types and names
    while k < numOfTables :
        currentTable = "$table{}".format(k+1)
        dic[currentTable] = {}
        dic[currentTable]["elements"] = []
        dic[currentTable]["name"] = input("Enter name of table {} : ".format(k+1))
        numElem = int(input("How many elements should table consist?\n"))
        j=0
        while j < numElem :
            x = {"$type{}".format(j+1) : input("What type is {}. element\n".format(j+1)), "$name{}".format(j+1) : input("Name of {}. element\n".format(j+1))}
            dic[currentTable]["elements"].append(x)
            j+=1
        k+=1
    #Adding tables to contract constructor
    tbl_const_str = ''    
    for table in dic :
        currTbl = tbl_str.replace("$tablename", dic[table]["name"])
        tbl_const_str += currTbl
    new_file = const_str + tbl_const_str + ' {}'
    #Adding structures to class
    cnt =0
    for i in dic :
        x = dic[i]["name"]
        currName = name.replace('$tablename', x)
        currInst = inst.replace('$tablename', x)
        zxc = 'table_insta' + str(cnt)
        currInst = currInst.replace('$table_inst', zxc)
        new_file += '\n' +  currName
        new_file += id
        for j in range(len(dic[i]["elements"])) :
            y = dic[i]["elements"][j]['$type{}'.format(j+1)]
            z = dic[i]["elements"][j]['$name{}'.format(j+1)]
            currElem = element.replace('$type', y).replace('$name', z)
            new_file += currElem
        new_file += idget + '\n'
        new_file += end 
        new_file += currInst
        cnt+=1
    #Create parameter for action list
    parametersList = []
    for m in dic :
        parameters = ''
        for j in range(len(dic[m]["elements"])) : 
            y = dic[m]["elements"][j]['$type{}'.format(j+1)]
            z = dic[m]["elements"][j]['$name{}'.format(j+1)]
            if len(dic[m]["elements"]) > j+1 :
                parameters += y + ' ' + z + ', '
            else :
                parameters += y + ' ' + z
        parameters = '({})'.format(parameters)
        parametersList.append(parameters)
    #Create actions
    pom = 0
    new_file+='\n\n'
    for i in dic :
        currFirst = first.replace("$table", dic[i]["name"])
        currFirst = currFirst.replace("$parameters", parametersList[pom])
        currSecond = second.replace("$table", dic[i]["name"])
        currId = setId.replace("$table", dic[i]["name"])
        elementList = []
        for e in range(len(dic[i]["elements"])) : 
            currElement = dic[i]["elements"][e]["$name{}".format(e+1)]
            currElement = setElement.replace('$name', currElement)
            elementList.append(currElement)
        new_file +=currFirst
        new_file +=currSecond
        new_file +=currId
        for n in elementList :
            new_file += n
        new_file +=close
        new_file +='    }\n'
        pom+=1
    new_file += '    \n};'
    new.write(new_file)
    return contractName

def push_action(account, action, data) :
    ssh= connect()
    ssh.exec_command('cd; ./unlockWallet.py')
    command = 'cline push action {} {} {} -p {}'.format(account, action, data, account)
    stdin,stdout,stderr=ssh.exec_command(command)
    output = stdout.readlines()
    if (output) :
        resp = ''.join(output)
        log(resp)
    else :
        print("Something went wrong...")


def get_table(account, scope, table, l=1800) :
    ssh = connect()
    stdin,stdout,stderr=ssh.exec_command('cline get table -l {} {} {} {}'.format(l, account, scope, table))
    tbl = stdout.readlines()
    resp = ''.join(tbl)    
    data = json.loads(resp)
    json_object = json.dumps(data, indent=4,ensure_ascii=False)    
    return json_object 

def get_abi(account) :
    ssh = connect()
    stdin,stdout,stderr=ssh.exec_command('cline get abi {}'.format(account))
    abi = stdout.readlines()
    data = json.loads(''.join(abi))
    abi = json.dumps(data, indent=4,ensure_ascii=False) 
    return abi

def get_account(accName) :
    ssh = connect()
    stdin,stdout,stderr=ssh.exec_command('cline get account {}'.format(accName))
    outlines=stdout.readlines()
    account=''.join(outlines)
    return account

def query(accTable, key, value) :
    accTblJson = json.loads(accTable)
    list = []
    dic = {}
    for element in accTblJson['rows'] :
        if str(element[key]) == value :
            list.append(element)
    if list :
        dic['rows'] = list
        return dic
    else :
        log("No result found")
        exit()


