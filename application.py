from flask import render_template, jsonify, request, redirect, url_for, Flask
from subprocess import check_output
from os import path, chdir, getcwd
from random import randint
import connect
import json

app = Flask(__name__)
w3, contract = connect.initiate()

# with open('keys.json', mode='w', encoding='utf-8') as f:
#     json.dump([], f)

global users
users = {"C1": "0x401943d512de0120888b3271e8380c688e9da1ed", "R1": "0x02f26e196d9c5ea9623e75a46e96da118e4a4735"}
user_ids = ["0x3a6d23e2cb1cb1852eb2e6e3a4cffd6500a2f538", "0x3b9071e114c56a1ab01620fa4db01d37ae4b4a7f", "0x6ab1d2eba3685badb4ec8e7ee11e11fc27571680", "0x4ce859dbf20f2ef8947632fe3569ceb50c286008", "0xc1ff87f82b8ad5dc504737f953a32e63fa0cbfbf", "0x1f05fa49c4853495f02b9f3bd0e163b781b36259", "0x4866679b42fd0b5da0d2d6b55a1c1c2319af3657", "0x5d916828e373ca913cc34ff19b3fd3858a1195c6", "0x1180e416899c34d33660e45f1b2bada60ce40a67", "0x045df9b38723d8f71e6bb99b80f3e1ab617bea3f"]

result = connect.isRecyclingPlant(w3, contract, users["R1"])
print(result)
connect.createplant(w3, contract, users["R1"])
result = connect.isRecyclingPlant(w3, contract, users["R1"])
print(result)

def getRandomIdx():
    l = [str(randint(0,10)) for i in range(3)]
    return ''.join(l)

def render_with_user(filename, points=0):
    user = request.args.get("user", "0")
    success_str = request.args.get("success_str", "")
    return render_template(
        filename,
        user = user, 
        points = points,
        success_str = success_str)

# index page
@app.route("/")
@app.route('/index')
def hello():
    #return "Hello, World!"
    print(users)
    return render_template('index.html')

# create user landing page
@app.route('/create_user')
def create_user():
    # return 'CREATE USER'
    return render_template('create_user.html')


# create user landing page
@app.route('/leaderboard')
def leaderboard():
    # return 'CREATE USER'
    scores = {}
    for key,value in users.items():
        print(value)
        scores[key] = connect.get_recycled_balance(w3, contract, value)
    #return scores
    scores_new = {k: v for k, v in sorted(scores.items(), key=lambda item: item[1], reverse=True)}
    return render_template('leaderboard.html', scores=scores_new, counter=0)

# create user function
@app.route('/register_new_user', methods = ['POST'])
def register_new_user():
    idx = getRandomIdx()

    name = request.form.get("name")
    user_type = request.form.get("type")

    curUser = user_type + idx

    rst = [
        "--name", name,
        "--type", user_type,
        "--id", curUser
        ]
    
    id = connect.createUser(w3, contract, curUser, user_type)

    global users
    users[curUser] = id[1]

    # with open('keys.json', mode='a+', encoding='utf-8') as feedsjson:
    #     feeds = json.load(feedsjson)
    #     entry = {}
    #     entry['user'] = curUser
    #     entry['id'] = id
    #     json.dump(entry, feeds)


    #output = run_node_cmd('createUser', rst)

    # What page to get back to?
    return_point = "NA"
    if curUser[0] == "C":
        return_point = 'consumer'
    elif curUser[0] == "S":
        return_point = 'shop'
    elif curUser[0] == "R":
        return_point = 'recyclingcenter'
    elif curUser[0] == "D":
        return_point = 'distributor'
    elif curUser[0] == "P":
        return_point = 'producer'
    else:
        # Should not happen
        print("Can't figure out user")
    return redirect(url_for(return_point, user=curUser, success_str=None))

# consumer page
@app.route('/consumer')
def consumer():
    # return 'CONSUMER INDEX PAGE'
    user = request.args.get("user", "C1") # C0 is our default
    user = users[user]
    points = connect.get_recycled_balance(w3, contract, user)
    return render_with_user('consumer.html', points = points)

# consumer page
@app.route('/shop')
def shop():
    # return 'CONSUMER INDEX PAGE'
    user = request.args.get("user", "S0") # C0 is our default
    return render_with_user('shop.html')

# consumer page
@app.route('/recyclingcenter')
def recyclingcenter():
    user = request.args.get("user", "R0") # C0 is our default
    return render_with_user('evaluator.html')

# consumer page
@app.route('/distributor')
def distributor():
    # return 'CONSUMER INDEX PAGE'
    user = request.args.get("user", "D0") # C0 is our default
    return render_with_user('distributor.html')

# consumer page
@app.route('/producer')
def producer():
    # return 'CONSUMER INDEX PAGE'
    user = request.args.get("user", "P0") # C0 is our default
    return render_with_user('producer.html')



@app.route('/myitems')
def items():
    user = request.args.get("complete_user", "C0") # C0 is our default
    return run_node_cmd('queryItemInfosBySrc', 
        ["--src", user] )



@app.route('/create', methods = ['POST'])
def create():
    idx = getRandomIdx()

    weight = request.form.get("weight")
    item_type = request.form.get("type")
    curUser = request.form.get('user')
    footprint = request.form.get('val')
    item = request.form.get('tag')

    infosrc = curUser
    infodst = request.form.get('infodst')
    
    rst = [
        "--idx", idx,
        "--type", item_type,
        "--footprint", footprint,
        "--weight", weight,
        "--item", item,
        "--src", infosrc,
        "--dst", infodst,
        ]
    output = run_node_cmd('addItemInfo', rst)

    # What page to get back to?
    return_point = "NA"
    if curUser[0] == "C":
        return_point = 'consumer'
    elif curUser[0] == "S":
        return_point = 'shop'
    elif curUser[0] == "R":
        return_point = 'recyclingcenter'
    elif curUser[0] == "D":
        return_point = 'distributor'
    else:
        # Should not happen
        print("Can't figure out user")
    return redirect(url_for(return_point, user=curUser[-1], success_str=output))


@app.route('/input', methods = ['POST'])
def buy():
    idx = getRandomIdx()

    weight = request.form.get("weight")
    item_type = request.form.get("type")
    curUser = request.form.get('user')
    footprint = request.form.get('val')
    item = request.form.get('tag')

    infodst = curUser
    infosrc = request.form.get('infosrc')

    rst = [
        "--idx", idx,
        "--type", item_type,
        "--footprint", footprint,
        "--weight", weight,
        "--item", item,
        "--src", infosrc,
        "--dst", infodst,
        ]
    #output = run_node_cmd('addInput', rst)

    print(rst)
    seller = users[infodst]
    buyer = users[infosrc]

    if item_type == "Plastic":
        item_type = 1

    result = connect.buy(w3, contract, buyer, seller, weight, item_type)
    print(result)

    # What page to get back to?
    return_point = "NA"
    if curUser[0] == "C":
        return_point = 'consumer'
    elif curUser[0] == "S":
        return_point = 'shop'
    elif curUser[0] == "R":
        return_point = 'recyclingcenter'
    elif curUser[0] == "D":
        return_point = 'distributor'
    else:
        # Should not happen
        print("Can't figure out user")
    return redirect(url_for(return_point, user=curUser[-1], success_str=result))


@app.route('/recycle', methods = ['POST'])
def recycle():
    idx = getRandomIdx()

    weight = request.form.get("weight")
    item_type = request.form.get("type")
    curUser = request.form.get('user')

    infosrc = curUser
    infodst = request.form.get('infodst')
    
    rst = [
        "--idx", idx,
        "--type", item_type,
        # "--footprint", footprint,
        "--weight", weight,
        "--src", infosrc,
        "--dst", infodst,
        ]
    #output = run_node_cmd('addItemInfo', rst)
    buyer = users[infodst]
    seller = users[infosrc]

    if item_type == "Plastic":
        item_type = 1

    result = connect.recycle(w3, contract, buyer, seller, weight, item_type)


    # What page to get back to?
    return_point = "NA"
    if curUser[0] == "C":
        return_point = 'consumer'
    elif curUser[0] == "S":
        return_point = 'shop'
    elif curUser[0] == "R":
        return_point = 'recyclingcenter'
    elif curUser[0] == "D":
        return_point = 'distributor'
    else:
        # Should not happen
        print("Can't figure out user")
    return redirect(url_for(return_point, user=curUser[-1], success_str=result))

