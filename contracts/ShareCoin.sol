pragma solidity ^0.4.4;

import "./StandardToken.sol";

//name this contract whatever you'd like
contract ShareCoin is StandardToken {

  // This notifies clients about the amount burnt
    event Burn(address indexed from, uint256 value);
    event TwitterBounty(address userAddress, uint256 value);

    function () {
        //if ether is sent to this address, send it back.
        throw;
    }

    /* Public variables of the token */
    //string public name;                   //fancy name: eg Simon Bucks
    uint8 public decimals;                //How many decimals to show. ie. There could 1000 base units with 3 decimals. Meaning 0.980 SBX = 980 base units. It's like comparing 1 wei to 1 ether.
    //string public symbol;                 //An identifier: eg SBX
    address owner;

    function ShareCoin() {
        owner = msg.sender;
        balances[msg.sender] = 10000000;               // Give the creator all initial tokens (100000 for example)
        totalSupply = 10000000;                        // Update total supply (100000 for example)
        //name = tokenName;                                   // Set the name for display purposes
        decimals = 0;                            // Amount of decimals for display purposes
        //symbol = tokenSymbol;                               // Set the symbol for display purposes
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


    // Triggered when a Twitter bouunty to like or retweet a post has been
    // completed by a user
    function twitterBountyPayout(uint256 _value, address _creatorAddress) public returns (bool success) {
        require(balances[_creatorAddress] - _value >= 0);

        balances[msg.sender] += _value;

        TwitterBounty(msg.sender, _value);
        return true;
    }

}
