pragma solidity ^0.4.4;

import "./StandardToken.sol";

//name this contract whatever you'd like

contract ShareCoin is StandardToken {

    // This notifies clients about the amount burnt
    event Burn(address indexed from, uint256 value);
    // Notifies the clients when a Twitter Bounty is successfully created
    event TwitterBountyCreated(address creatorAddress, uint256 value);
    //Notifies the clients when a Twitter Bounty is successfully paid out
    event TwitterBountyPaidOut(address paidOutTo, uint256 amountPaidOut);

    struct Bounty {
        uint32 shareCoinInBounty;
        uint32 eachPayout;
        string uniqueURL;
    }

    //Array of K,V with URL of tweet as Key, the bounty as value
    mapping(string => Bounty) public urlToBounty;


    /* Public variables of the token */
    string public name;                   //fancy name: eg Simon Bucks
    uint8 public decimals;                //How many decimals to show. ie. There could 1000 base units with 3 decimals.
    string public symbol;                 //An identifier: eg SBX
    address private owner;

    function ShareCoin() {
        owner = msg.sender;
        balances[owner] = 10000000;               // Give the creator all initial tokens (100000 for example)
        totalSupply = 10000000;                        // Update total supply (100000 for example)
        name = "ShareCoin";                                   // Set the name for display purposes
        decimals = 0;                            // Amount of decimals for display purposes
        symbol = "SHC";                               // Set the symbol for display purposes
    }

    function () {
        //if ether is sent to this address, send it back.
        throw;
    }


    /**
     * Destroy tokens
     *
     * Remove `_value` tokens from the system irreversibly
     *
     * @param _value the amount of money to burn
     */
    function burn(uint256 _value) public returns (bool success) {
        require(balances[msg.sender] >= _value);   // Check if the sender has enough
        balances[msg.sender] -= _value;            // Subtract from the sender
        totalSupply -= _value;                      // Updates totalSupply
        Burn(msg.sender, _value);
        return true;
    }


    // Creates an instance of a Bounty
    // @param _totalBounty How many total SHCs the bounty is worth
    // @param _eachPayout How much one payout of the bounty will be in SHC
    // @param _uniqueURL The URL of the tweet that will be used to identify the bounty
    // @return will always return true unless Creator does not have enough SHC
    function createTwitterBounty (
        uint256 _totalBountyValue,
        uint256 _eachPayout,
        string _uniqueURL)
        public returns (bool success) {
            //checks if creator has enough SHC to create bounty
            require(balances[msg.sender] >= _totalBountyValue);
            //Subtracts bounty amount from creator
            balances[msg.sender] -= _totalBountyValue;
            //creates a new bounty with a unique URL
            Bounty newBounty = Bounty(_totalBountyValue, _eachPayout, _uniqueURL);
            //adds the new bounty as a value to a map of bounties with creator address as key
            urlToBounty[_uniqueURL] = newBounty;
            //Triggers bounty creation event
            TwitterBountyCreated(msg.sender, _totalBountyValue);
            return true;
        }

    // Pays a user SHC for completing bounty
    // Will return false if the bounty does not have the funds to payout
    // @param address _to is the user wallet address that the funds will be sent to
    // @param string _uniqueURL is the URL of the tweet used to identify the bounty
    function payoutTwitterBounty(string _uniqueURL) public returns (bool) {
        //Reference to the bounty to be manipulated
        Bounty memory bountyToBePaid = urlToBounty[_uniqueURL];
        //Returns false if the bounty does not have the balance to pay out
        require(bountyToBePaid.shareCoinInBounty >= bountyToBePaid.eachPayout);
        //Subtracts the payout from the bounty
        bountyToBePaid.shareCoinInBounty -= bountyToBePaid.eachPayout;
        //Sends the amount of SHC for the bounty to the user
        transfer(msg.sender, bountyToBePaid.eachPayout);
        //Triggers bounty payout event
        TwitterBountyPaidOut(msg.sender, bountyToBePaid.eachPayout);
        return true;
    }

}
