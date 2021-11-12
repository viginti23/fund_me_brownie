from brownie import network, accounts, config, MockV3Aggregator
from web3 import Web3

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ['development', 'ganache-local']
FORKED_BLOCKCHAIN_ENVIRONMENTS = ['mainnet-fork', 'mainnet-fork-dev']

DECIMALS = 8
STARTING_PRICE = 20_000_000_000


def get_account():
    if (network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
            or network.show_active() in FORKED_BLOCKCHAIN_ENVIRONMENTS):
        return accounts[0]  # pull from our development accounts
    else:
        return accounts.add(config['wallets']['from_key'])


def deploy_mocks():
    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks...")
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": get_account()})
    print('Mocks deployed!')
