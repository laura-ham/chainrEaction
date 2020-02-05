# chainrEaction

This is a repository containing the code written for the hackathon ChainrEaction 3-5 Feb 2020.
**WARNING:** this code is created for a _hackathon_, meaning that the code is very messy.

## Getting Started

- Start Ganache: `ganache-cli`
- Deploy the token in the folder `my-token` with: `truffle deploy`
- Copy the returned `contract address` to `address` in `connect.py`
- Run `./geth attach http://127.0.0.1:8545` in the folder where `geth` is stored. Then run `eth.accounts` to retrieve accounts which where initialized. 
- Copy this array of accounts into `user_ids` in `connect.py`
- Create some initial users (optional) and at least one recycling center (required) in `application.py` in the global `users` variable.
