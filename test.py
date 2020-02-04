from web3 import Web3
import json

#connection to RPC server

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

print(w3.isConnected)

address = "0x15B0ba8dB834ade5a83F66F282DF5b79b80cC0D3"

#loading JSON file to read ABI description of contract
truffleFile = json.load(open("/home/vmuser/my-token/build/contracts/MyToken.json"))
abi = truffleFile['abi']

#Smart contract definition

myContract = w3.eth.contract(address=address, abi=abi)

#dummy value for user
user = w3.toChecksumAddress("0x755349b9f94f10625a4d5b71ecac86407cf279dd")
shop = w3.toChecksumAddress("0x47f9af9218218549489bd3335ea64d623f9d4787")

#create User function

resultCreateUser = myContract.functions.createUser(True).transact({"from":user})

print(resultCreateUser)

#isRecyclingPlant

resultIsRecyclingPlant = myContract.functions.isRecyclingPlant(user).call()
print(resultIsRecyclingPlant)

#dummy values to pickUpTrash
product = 0
weight = 10

resultLitter = myContract.functions.pickUpLitter(product,weight).call()
print(resultLitter)

#test to see if the dummy values appended

resultLitterTest = myContract.functions.balanceOfGoods(user,0).call()
print(resultLitterTest)

#dummy values for recycleWaste

#resultRecycleWaste = myContract.functions.recycleWaste(user,0).call({"from":user})
#print(resultRecycleWaste)



