from web3 import Web3
import json

def initiate():
    #connection to RPC server

    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

    address = "0x15B0ba8dB834ade5a83F66F282DF5b79b80cC0D3"

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
    id = w3.geth.personal.newAccount(user)
    if type == "R":
        is_recycling_center = True
        w3.geth.personal.unlockAccount(id, user, 0)
        myContract.functions.createUser(is_recycling_center).transact({"from":id})
    return user, id

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

# #resultRecycleWaste = myContract.functions.recycleWaste(user,0).call({"from":user})
# #print(resultRecycleWaste)

if __name__ == "__main__":
    w3, myContract = initiate()
    print(w3.geth.personal.newAccount('the-passphrase'))