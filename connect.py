from web3 import Web3
import json

global user_ids
user_ids = ["0x401943d512de0120888b3271e8380c688e9da1ed", "0x02f26e196d9c5ea9623e75a46e96da118e4a4735", "0xf0b65ce971e86bdd4fd4ebf85e59b6bfb1312a9a", "0x1734a1fe31ea468c055ef1dd81ef82fe457ff074", "0x7c865611cd3bc6673bbc10f40d2162c3c62dcc93", "0xf478663f01d53095d4d59485ca47de9af47aeea9", "0x5835837b15d55c9e4eb87ba3c6e9ff3db8f99ea6", "0xbb96b4acdfe0411d4d69a1c84bbc4183f5ea5064", "0xee9b1c109bcc9a32970f38e6445a1087146c347a", "0xa80d0f967511b6e78b85a22e280fb1a3d0535a76"]

def initiate():
    #connection to RPC server

    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

    address = "0x6243C788141BCcD9823D460D81590488D3C482BA"

    #loading JSON file to read ABI description of contract
    truffleFile = json.load(open("my-token/build/contracts/MyToken.json"))
    abi = truffleFile['abi']

    #Smart contract definition

    myContract = w3.eth.contract(address=address, abi=abi)

    return w3, myContract

def isRecyclingPlant(w3, myContract, user):
    user = w3.toChecksumAddress(user)
    return myContract.functions.isRecyclingPlant(user).call()

def createUser(w3, myContract, user, type):
    #user = w3.toChecksumAddress(user)
    #type = rst["--type"]
    global user_ids
    id =  w3.toChecksumAddress(user_ids[0])
    user_ids.pop(0)

    if type == "R":
        is_recycling_center = True
        # w3.geth.personal.unlockAccount(id, user, 0)
        myContract.functions.createPlant(is_recycling_center).transact({"from":id})
    return user, id

def recycle(w3, contract, buyer, seller, weight, item_type):
    buyer = w3.toChecksumAddress(buyer)
    seller = w3.toChecksumAddress(seller)
    contract.functions.recycleWaste(buyer,int(item_type),int(weight)).transact({"from":seller,"gas":1000000})
    contract.functions.verifyWaste(True).transact({"from":buyer,"gas":1000000})
    contract.functions.buyGoods(buyer, int(item_type), int(weight)).call({"from":seller})
    result = contract.functions.recycledBalanceOfGoods(seller,int(item_type)).call()
    print('recycled', result)
    result = contract.functions.boughtBalanceOfGoods(buyer,int(item_type)).call()
    print('bought', result)

def createplant(w3, myContract, user):
    id =  w3.toChecksumAddress(user)
    myContract.functions.createPlant(True).transact({"from":id})

# #dummy value for user
# user = w3.toChecksumAddress("0x755349b9f94f10625a4d5b71ecac86407cf279dd")
# shop = w3.toChecksumAddress("0x47f9af9218218549489bd3335ea64d623f9d4787")

# #create User function

# resultCreateUser = myContract.functions.createUser(True).transact({"from":user})

# print(resultCreateUser)

# #isRecyclingPlant

# resultIsRecyclingPlant = myContract.functions.isRecyclingPlant(user).call()
# print(resultIsRecyclingPlant)

# #dummy values to pickUpTrash
# product = 0
# weight = 10

# resultLitter = myContract.functions.pickUpLitter(product,weight).call()
# print(resultLitter)

# #test to see if the dummy values appended

# resultLitterTest = myContract.functions.balanceOfGoods(user,0).call()
# print(resultLitterTest)

# #dummy values for recycleWaste

def buy(w3, myContract, user, seller, weight, product):
    user = w3.toChecksumAddress(user)
    seller = w3.toChecksumAddress(seller)
    myContract.functions.buyGoods(seller, int(product), int(weight)).call({"from":user})

# #resultRecycleWaste = myContract.functions.recycleWaste(user,0).call({"from":user})
# #print(resultRecycleWaste)

if __name__ == "__main__":
    w3, myContract = initiate()
    print(w3.geth.personal.newAccount('the-passphrase'))