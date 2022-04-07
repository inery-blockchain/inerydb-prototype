## IneryDB prototype python CLI Dapp

### Pre-requirements

1. Active Node
    - You will need IP address and password of active server hosting inery blockchain protocol
    - modify CONFIG.JSON file with your node IP and password, also user if needed.


2. Inery contract development toolkit
Steps for instalation could be found in cdt folder
    - Dependencies for cdt
    - Build contract development toolkit (cdt) on local machine


Value contracts represent databases on Inery blockchain.<br>

Contracts written in C++ are compiled into WASM (Web Assembly) and ABI(Application Binary Interface) files. <br>
WASM and ABI are connected with account on Inery Blockchain.<br>
In order to compile your contracts you will need inery cdt <br>

### Tips for using CLI 

 Step by step process on how to execute helper scripts. 

1. Open Terminal
    - navigate to IneryDB folder
    - from GUI, right click on "IneryDB" folder, then click "Open in Terminal" 
2. Giving scripts the necessary permissions to run
    - give executable permission to all IneryDB scripts, this is done by executing following 	
    - commands in terminal :
        - "chmod 777 IneryDB_create.py" 
        - "chmod 777 IneryDB_get.py" 
        - "chmod 777 IneryDB_set.py" 
3. Execute Script
    - IneryDB scripts are called by executing command in terminal, using appropriate arguments <br>
        example : "./IneryDB_create.py [option] [argument]".


### Features 

Features that we are currently offering are creating databases and managing data on Inery block chain.


### Create on Inery blockchain 

By using "IneryDB_create" along wiht --account and --database, our options for creation.<br>
For start you will be needing an account with original name that fulfills inery_name rules

<strong> Rules of inery_name : </strong>
     Minimum lenght of 3 and maximum lenght of 10 characters, they must be all lowercase letters or numbers from 1-5, without spaces allowed.
     Name of databse and tables can't be same, also database and table name cant start with number and elements names cant be some C++ keywords

1. Account
    - Usage: 
    ./IneryDB_create --account [account_name] <br>
    <strong> account_name is of inery_name type, it must be original </strong>
    Example :
```    
    
            ./IneryDB_create.py --account inery.test
        ====================================================================================
                Verifying inery.test account..          
        ====================================================================================
        ====================================================================================
                Successfully created account!           
        ====================================================================================
        ====================================================================================
        Public key :  INE6hzfzZbT18sJfofzx5nPV15vcbtk3KoXPpdafaXe5hofaaAiRx
        ====================================================================================
        ====================================================================================
        Private key : 5JIneryDBJkJ8B4AUBxMu8C9LwbxxUtuYJaQBMYWYG1y2mVVEKt4vFcoS
        ====================================================================================
        ====================================================================================
            Your Inery account name : inery.test       
        ====================================================================================
```
    
2. Database 
    - Usage: 
    ./IneryDB_create --database [account_name]

    account_name is of inery_name type, it must be representing an existing account, you want to connect with the database.<br>
    <strong> NOTICE! table names must be inery_name type and as of now two types of fields are optimised for use "string" and "int". </strong>
   
    Example : 
```
        ./IneryDB_create.py --database inery.test
    ====================================================================================
            Verifying inery.test account..          
    ====================================================================================
    Database name : mydb
    How many tables do you want? 2
    Enter name of table 1 : table1
    How many elements should table consist?
    3
    What type is 1. element
    string
    Name of 1. element
    name
    What type is 2. element
    int
    Name of 2. element
    age
    What type is 3. element
    string
    Name of 3. element
    Address
    Enter name of table 2 : table2
    How many elements should table consist?
    2
    What type is 1. element
    string
    Name of 1. element
    description
    What type is 2. element
    int
    Name of 2. element
    number
    Warning, empty ricardian clause file
    Warning, empty ricardian clause file
    Warning, action <settable1> does not have a ricardian contract
    Warning, action <settable2> does not have a ricardian contract
    =================================================================
            Successfully created Database           
    =================================================================
```

### Manage your Data

1. Inserting
    - Usage:  ./IneryDB_set.py --set 
    - You will be asked for Account and Table in which you want to insert data
    - After, if informations are correct you will need to insert the data you want according to type of field
```
    Example : 
    ./IneryDB_set.py --set
        Account name : 
        inery.test
        Table name : 
        table1
        Set "name" field <string> type 
        Steve Williams
        Set "age" field <int> type 
        34
        Set "Address" field <string> type 
        Silicon Valley, California
        ====================================================================================
        #   inery.test <= inery.test::settable1        {"name":"Steve Williams","age":34,
            "Address":"Silicon Valley, California"}
        ====================================================================================
```
2. Retrieveing
    - Usage : 
    ./IneryDB_get.py --table
    - You will be asked to provide Account and Table name info. 
    <strong> Whole table will be saved in table folder with ACCOUNT.TABLE.JSON name </strong>
    

3. Simple query
    - Usage : ./IneryDB_get.py --query
    - You need to provide account and table info. 
    - After you enter KEY to search with like name of element in structure 
    -  and VALUE which corresponds to key that you search for
    -  You can make redundant query calls

    Example :
```

    ./IneryDB_get.py --query 
    Enter account name : 
    persons
    Enter table name : 
    person
    Enter key you wanna search table with: 
    state
    Enter value for key to find: 
    Germany
    {
        "rows": [
            {
                "id": 394,
                "name": "Ananko",
                "surname": "Savand",
                "age": 58,
                "gender": "male",
                "state": "Germany",
                "city": "unknown",
                "street": "unknown",
                "status": "unkown"
            },
            {
                "id": 874,
                "name": "Desislava",
                "surname": "Nakarad",
                "age": 58,
                "gender": "female",
                "state": "Germany",
                "city": "unknown",
                "street": "unknown",
                "status": "unkown"
            },
            {
                "id": 1052,
                "name": "Mojan",
                "surname": "Leštari",
                "age": 26,
                "gender": "male",
                "state": "Germany",
                "city": "unknown",
                "street": "unknown",
                "status": "unkown"
            },
            {
                "id": 1103,
                "name": "Prvoslava",
                "surname": "Biberč",
                "age": 56,
                "gender": "female",
                "state": "Germany",
                "city": "unknown",
                "street": "unknown",
                "status": "unkown"
            },
            {
                "id": 1136,
                "name": "Vukodrag",
                "surname": "Kompal",
                "age": 40,
                "gender": "male",
                "state": "Germany",
                "city": "unknown",
                "street": "unknown",
                "status": "unkown"
            },
            {
                "id": 1209,
                "name": "Staniša",
                "surname": "Baleti",
                "age": 38,
                "gender": "female",
                "state": "Germany",
                "city": "unknown",
                "street": "unknown",
                "status": "unkown"
            },
            {
                "id": 1376,
                "name": "Vukomil",
                "surname": "Zdrav",
                "age": 34,
                "gender": "male",
                "state": "Germany",
                "city": "unknown",
                "street": "unknown",
                "status": "unkown"
            },
            {
                "id": 1749,
                "name": "Živadin",
                "surname": "Ćilerdž",
                "age": 47,
                "gender": "male",
                "state": "Germany",
                "city": "unknown",
                "street": "unknown",
                "status": "unkown"
            }
        ]
    }
    Do you want to subquery this result? 
    type [y/n] : 
    y
    Enter key you wanna search table with: 
    gender
    Enter value for key to find: 
    female
    {
        "rows": [
            {
                "id": 874,
                "name": "Desislava",
                "surname": "Nakarad",
                "age": 58,
                "gender": "female",
                "state": "Germany",
                "city": "unknown",
                "street": "unknown",
                "status": "unkown"
            },
            {
                "id": 1103,
                "name": "Prvoslava",
                "surname": "Biberč",
                "age": 56,
                "gender": "female",
                "state": "Germany",
                "city": "unknown",
                "street": "unknown",
                "status": "unkown"
            },
            {
                "id": 1209,
                "name": "Staniša",
                "surname": "Baleti",
                "age": 38,
                "gender": "female",
                "state": "Germany",
                "city": "unknown",
                "street": "unknown",
                "status": "unkown"
            }
        ]
    }
    Do you want to subquery this result? 
    type [y/n] : 

```


