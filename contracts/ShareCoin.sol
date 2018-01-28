pragma solidity ^0.4.4;

import "./StandardToken.sol";

//name this contract whatever you'd like

contract ShareCoin is StandardToken {

    // This notifies clients about the amount burnt
    event TokensBurned(address indexed from, uint256 value);
    // Notifies the clients when a Twitter Bounty is successfully created
    event TwitterBountyCreated(address creatorAddress, uint256 value);
    // Notifies the clients when a Twitter Bounty is successfully paid out
    event TwitterBountyPaidOut(address paidOutTo, uint256 amountPaidOut);

    struct Bounty {
        uint32 shareCoinInBounty;
        uint32 eachPayout;
        bytes32 uniqueURL;
        address bountyCreater;
        string tweetID;
    }

    // Array of K,V with URL of tweet as Key, the bounty as value
    mapping(bytes32 => Bounty) internal urlToBounty;

    /* Public variables of the token */
    string public name;                   //fancy name: eg Simon Bucks
    uint8 public decimals;                //How many decimals to show. ie. There could 1000 base units with 3 decimals.
    string public symbol;                 //An identifier: eg SBX
    address private owner;

    function ShareCoin() public {
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
        TokensBurned(msg.sender, _value);
        return true;
    }

    // Creates an instance of a Bounty
    // @param _totalBounty How many total SHCs the bounty is worth
    // @param _eachPayout How much one payout of the bounty will be in SHC
    // @param _uniqueURL The URL of the tweet that will be used to identify the bounty
    // @return will always return true unless Creator does not have enough SHC
    function createTwitterBounty (
        uint32 _totalBountyValue,
        uint32 _eachPayout,
        string _uniqueURL)
        public returns (bool success) {
            //checks if creator has enough SHC to create bounty
            require(balances[msg.sender] >= _totalBountyValue);

            //converts string URL to keccak256 hash
            bytes32 urlAsHash = keccak256(_uniqueURL);

            //Subtracts bounty amount from creator
            balances[msg.sender] -= _totalBountyValue;

            //creates a new bounty with a unique URL
            Bounty memory newBounty = Bounty(_totalBountyValue, _eachPayout, urlAsHash, msg.sender, _uniqueURL);

            //adds the new bounty as a value to a map of bounties with creator address as key
            urlToBounty[urlAsHash] = newBounty;

            //Triggers bounty creation event
            TwitterBountyCreated(msg.sender, _totalBountyValue);
            return true;
        }

    // Pays a user SHC for completing bounty
    // Will return false if the bounty does not have the funds to payout
    // @param address _to is the user wallet address that the funds will be sent to
    // @param string _uniqueURL is the URL of the tweet used to identify the bounty
    function payoutTwitterBounty(string _uniqueURL) public returns (bool) {
        //Converts _uniqueURL to bytes32 hash
        bytes32 urlAsHash = keccak256(_uniqueURL);

        //Reference to the bounty to be manipulated
        Bounty memory bountyToBePaid = urlToBounty[urlAsHash];

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

    // Call function returns a particular bounty's balance and payout amount
    function getBounty(string _uniqueURL) public view
        returns(uint32 shareCoinInBounty, uint32 eachPayout, address bountyCreater) {
            //converts @param _uniqueURL to bytes32 hash
            bytes32 urlAsHash = keccak256(_uniqueURL);

            //Stores a local reference to the bounty to return
            Bounty memory bountyToReturn = urlToBounty[urlAsHash];

            return(bountyToReturn.shareCoinInBounty, bountyToReturn.eachPayout, bountyToReturn.bountyCreater);
        }
}
