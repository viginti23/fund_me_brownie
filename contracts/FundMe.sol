// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";


contract FundMe {
    // using SafeMathChainlink for uint256;
    

    address public owner;
    mapping(address => uint256) public addressToAmountFunded;
    address[] public funders;
    AggregatorV3Interface priceFeed;

    constructor(address _priceFeed) public {
        priceFeed = AggregatorV3Interface(_priceFeed);
        owner = msg.sender;
    }

    function getEntranceFee() public view returns (uint256) {
        // minimumUSD
        uint256 minimumUSD = 5 * 10**18;
        uint256 price = getEthToUsdConversionRate();
        uint256 precision = 1 * 10**18;
        return (minimumUSD * precision) / price;
    }

    modifier onlyOwner {
        require(msg.sender == owner);
        _; // underscore holds place for the rest of the function being modified
    }
    
    function fund() public payable {
        // $50 - we have to set a min value
        uint256 minimumUSD = 5 * 10**18; //USD in Wei
        require(getEthToUsdConvertedAmount(msg.value) >= minimumUSD, "You need to send more ETH!");
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }
    
    function getVersion() public view returns (uint256) {
        return priceFeed.version();
    }
    
    function getEthToUsdConversionRate() public view returns (uint256) {
        (, int256 answer,,,)
         = priceFeed.latestRoundData();
         return uint256(answer* 10**10); // now the function returns the conversion rate in Wei, the smallest denomination 
    }
    
    function getEthToUsdConvertedAmount(uint256 ethAmount) public view returns(uint256) {
        uint256 EthToUsdConversionRate = getEthToUsdConversionRate();
        uint256 ethAmountInUsd = (EthToUsdConversionRate * ethAmount)/10**18; // dividing the result by 10**18 so we have the answer back in ETH
        return ethAmountInUsd;
    }
    
    function withdraw() payable public onlyOwner {
        msg.sender.transfer(address(this).balance);
        
        for (uint256 funderIndex=0; funderIndex<funders.length; funderIndex++){
            address funder = funders[funderIndex];
            addressToAmountFunded[funder] = 0;
        }
        
        funders = new address[](0); // (0) being the size of the new array
    }
} 
    