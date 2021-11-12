from scripts.handy_funcs import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy import deploy_fund_me
import pytest
from brownie import network, accounts, exceptions


def test_can_fund_and_withdraw():
    # Arrange
    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee() + 1000
    # Act 1
    tx_fund = fund_me.fund({"from": account, "value": entrance_fee})
    tx_fund.wait(1)
    # Assert
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee
    # Act 2
    tx_withdraw = fund_me.withdraw({"from": account})
    tx_withdraw.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for local testing")
    fund_me = deploy_fund_me()
    bad_actor = accounts.add()
    # Act & assert
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})
