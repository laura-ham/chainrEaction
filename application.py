from flask import render_template, jsonify, request, redirect, url_for, Flask
from subprocess import check_output
from os import path, chdir, getcwd
from random import randint
import connect

app = Flask(__name__)
w3, contract = connect.initiate()

def getRandomIdx():
    l = [str(randint(0,10)) for i in range(3)]
    return ''.join(l)

def render_with_user(filename):
    user = request.args.get("user", "0")
    success_str = request.args.get("success_str", "")
    return render_template(
        filename,
        user = user, 
        success_str = success_str)

# index page
@app.route("/")
@app.route('/index')
def hello():
    #return "Hello, World!"
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
    return render_template('leaderboard.html')

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
    user = request.args.get("user", "C0") # C0 is our default
    return render_with_user('consumer.html')

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
    output = run_node_cmd('addInput', rst)

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
        "--footprint", footprint,
        "--weight", weight,
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

