var Web3 = require('web3');
var web3;
window.addEventListener('load', function() {
// Checking if Web3 has been injected by the browser (Mist/MetaMask)
if (typeof web3 !== 'undefined') {
  // Use Mist/MetaMask's provider
  web3js = new Web3(web3.currentProvider);
} else {
  console.log('No web3? You should consider trying MetaMask!')
  // fallback - use your fallback strategy (local node / hosted node + in-dapp id mgmt / fail)
  web3js = new Web3(new Web3.providers.HttpProvider("https://ropsten.infura.io/TUBXa5ntAP9rtqdhFQNE"));
}

});

// Loads our contracts abi and then uses it to get access to our deployed contract.
var contactAddress = '0xd1549e0e7b4d6fb320a5377c618d4f3d20385f27';

var contractAbi = [ { "constant": true, "inputs": [], "name": "name", "outputs": [ { "name": "",
  "type": "string" } ], "payable": false, "stateMutability": "view", "type":
  "function" }, { "constant": false, "inputs": [ { "name": "_spender", "type":
  "address" }, { "name": "_value", "type": "uint256" } ], "name": "approve",
  "outputs": [ { "name": "success", "type": "bool" } ], "payable": false,
  "stateMutability": "nonpayable", "type": "function" }, { "constant": true,
  "inputs": [], "name": "totalSupply", "outputs": [ { "name": "", "type":
  "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, {
  "constant": false, "inputs": [ { "name": "_from", "type": "address" }, { "name":
  "_to", "type": "address" }, { "name": "_value", "type": "uint256" } ], "name":
  "transferFrom", "outputs": [ { "name": "success", "type": "bool" } ], "payable":
  false, "stateMutability": "nonpayable", "type": "function" }, { "constant":
  true, "inputs": [], "name": "decimals", "outputs": [ { "name": "", "type":
  "uint8" } ], "payable": false, "stateMutability": "view", "type": "function" }, {
  "constant": false, "inputs": [ { "name": "_value", "type": "uint256" } ],
  "name": "burn", "outputs": [ { "name": "success", "type": "bool" } ], "payable":
  false, "stateMutability": "nonpayable", "type": "function" }, { "constant":
  true, "inputs": [ { "name": "_uniqueURL", "type": "string" } ], "name":
  "getBounty", "outputs": [ { "name": "shareCoinInBounty", "type": "uint32" }, {
  "name": "eachPayout", "type": "uint32" }, { "name": "bountyCreater", "type":
  "address" } ], "payable": false, "stateMutability": "view", "type": "function" }, {
  "constant": false, "inputs": [ { "name": "_uniqueURL", "type": "string" } ],
  "name": "payoutTwitterBounty", "outputs": [ { "name": "", "type": "bool" } ],
  "payable": false, "stateMutability": "nonpayable", "type": "function" }, {
  "constant": true, "inputs": [ { "name": "_owner", "type": "address" } ], "name":
  "balanceOf", "outputs": [ { "name": "balance", "type": "uint256" } ], "payable":
  false, "stateMutability": "view", "type": "function" }, { "constant": true,
  "inputs": [], "name": "symbol", "outputs": [ { "name": "", "type": "string" } ],
  "payable": false, "stateMutability": "view", "type": "function" }, { "constant":
  false, "inputs": [ { "name": "_to", "type": "address" }, { "name": "_value",
  "type": "uint256" } ], "name": "transfer", "outputs": [ { "name": "success",
  "type": "bool" } ], "payable": false, "stateMutability": "nonpayable", "type":
  "function" }, { "constant": false, "inputs": [ { "name": "_totalBountyValue",
  "type": "uint32" }, { "name": "_eachPayout", "type": "uint32" }, { "name":
  "_uniqueURL", "type": "string" } ], "name": "createTwitterBounty", "outputs": [ {
  "name": "success", "type": "bool" } ], "payable": false, "stateMutability":
  "nonpayable", "type": "function" }, { "constant": true, "inputs": [ { "name":
  "_owner", "type": "address" }, { "name": "_spender", "type": "address" } ],
  "name": "allowance", "outputs": [ { "name": "remaining", "type": "uint256" } ],
  "payable": false, "stateMutability": "view", "type": "function" }, { "inputs": [],
  "payable": false, "stateMutability": "nonpayable", "type": "constructor" }, {
  "payable": false, "stateMutability": "nonpayable", "type": "fallback" }, {
  "anonymous": false, "inputs": [ { "indexed": true, "name": "from", "type":
  "address" }, { "indexed": false, "name": "value", "type": "uint256" } ], "name":
  "TokensBurned", "type": "event" }, { "anonymous": false, "inputs": [ {
  "indexed": false, "name": "creatorAddress", "type": "address" }, { "indexed":
  false, "name": "value", "type": "uint256" } ], "name": "TwitterBountyCreated",
  "type": "event" }, { "anonymous": false, "inputs": [ { "indexed": false, "name":
  "paidOutTo", "type": "address" }, { "indexed": false, "name": "amountPaidOut",
  "type": "uint256" } ], "name": "TwitterBountyPaidOut", "type": "event" }, {
  "anonymous": false, "inputs": [ { "indexed": true, "name": "_from", "type":
  "address" }, { "indexed": true, "name": "_to", "type": "address" }, { "indexed":
  false, "name": "_value", "type": "uint256" } ], "name": "Transfer", "type":
  "event" }, { "anonymous": false, "inputs": [ { "indexed": true, "name":
  "_owner", "type": "address" }, { "indexed": true, "name": "_spender", "type":
  "address" }, { "indexed": false, "name": "_value", "type": "uint256" } ],
  "name": "Approval", "type": "event" } ]

var shareCoinContract = web3.eth.contract(contractAbi);
var shareCoinInstance = shareCoinContract.at(contactAddress);
var userBalance; //Will be set when user loads up the page
