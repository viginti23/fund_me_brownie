from brownie import FundMe, MockV3Aggregator, network, config
from scripts.handy_funcs import get_account, deploy_mocks, LOCAL_BLOCKCHAIN_ENVIRONMENTS


def deploy_fund_me():
    account = get_account()
    # We can pass any parameter to contract's constructor through .deploy()
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        # if we are deploying it to a live network (mainnet, kovan) or fork network
        price_feed_address = config['networks'][network.show_active()]['eth_usd_price_feed']
    else:  # local, development
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address
    fund_me = FundMe.deploy(price_feed_address, {"from": account},
                            publish_source=config['networks'][network.show_active()].get('verify'))
    print(f'Contract deployed to {fund_me.address}.')
    return fund_me


def main():
    deploy_fund_me()
