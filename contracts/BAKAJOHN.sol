// SPDX-License-Identifier: MIT
pragma solidity ^0.8.16;

import "./ERC721.sol";
import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/utils/Strings.sol";

/* TEST
QmUqWSwWM15DKQyLdiksBFsRuAxSPWNJNh8Ur53MZKRhKq/BAKAJOHN#, 
QmbyKoLbEeJUtD4YFrcAZr8tpNghozuvUQ8VY793KzMybW/BAKAJOHN#, 
QmTx5oSguesGsDQnvZqPMwfLq78Yq2RDAUSqdPd9TCcR91/BAKAJOHN#
*/

contract Bakajohn is ERC721, ERC721Enumerable, ERC721URIStorage, Pausable, Ownable {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIdCounter;

    uint256 constant MAX_SUPPLY = 500;
    string constant PREFIX_URI = "https://ipfs.io/ipfs/";
    string[3] private _stage;
    string[3] private _stageJson;

    struct token {
        uint256 tokenId;
        uint32 stage;
        uint32 txTime;
    }
    mapping (uint256 => token) BKJ;

    // 空投地址
    address[] giveAwayList; 

    constructor(string memory stage_1, string memory stage_2, string memory stage_3) ERC721("Bakajohn", "BKJ") {
        _stage = [
            stage_1,
            stage_2,
            stage_3
        ];

        _stageJson = [
            "A.json",
            "B.json",
            "C.json"
        ];
    }

    function _engenderURI(uint256 _tokenId) public view returns (string memory) {
        string memory tokenIdStr;
        if (_tokenId >= 100) {
            tokenIdStr = Strings.toString(_tokenId + 1);
        }
        else{
            tokenIdStr = (_tokenId < 10) ? 
            string(abi.encodePacked("00", Strings.toString(_tokenId))) 
            : 
            string(abi.encodePacked("0",Strings.toString(_tokenId))) ;
        }
        uint32 currentStage = BKJ[_tokenId].stage;
        string memory URI = string(abi.encodePacked(PREFIX_URI, _stage[currentStage], "/", tokenIdStr, _stageJson[currentStage])); 
        return URI;
    }

    function _evolveStage(uint256 _tokenId) private {
        if ( BKJ[_tokenId].stage >= 2 ) { return; }
        else { BKJ[_tokenId].stage++; }
        string memory newUri = _engenderURI(_tokenId);
        _setTokenURI(_tokenId, newUri);
    }

    event tokenURIListener(string);
    function publicSafeMint(address to, uint amount) public {
        require (_tokenIdCounter.current() + amount < MAX_SUPPLY, "Cannot mint given amount.");
        require (amount > 0, "Must give a mint amount.");
        require(amount <= 5, "Amount should be smaller than 5");        
        for (uint256 i = 0; i < amount; i++){
            uint256 tokenId = _tokenIdCounter.current();
            BKJ[tokenId].stage = 0;
            BKJ[tokenId].txTime = 0;
            _tokenIdCounter.increment();
            _safeMint(to, tokenId);
            _setTokenURI(tokenId, _engenderURI(tokenId));
        }
    }

    function putAddressInGiveAwayList(
        address inputNextAddress_1,
        address inputNextAddress_2,
        address inputNextAddress_3,
        address inputNextAddress_4,
        address inputNextAddress_5,
        address inputNextAddress_6,
        address inputNextAddress_7,
        address inputNextAddress_8,
        address inputNextAddress_9,
        address inputNextAddress_10
    ) public onlyOwner {
        require(giveAwayList.length < 100);
        giveAwayList.push(inputNextAddress_1);
        giveAwayList.push(inputNextAddress_2);
        giveAwayList.push(inputNextAddress_3);
        giveAwayList.push(inputNextAddress_4);
        giveAwayList.push(inputNextAddress_5);
        giveAwayList.push(inputNextAddress_6);
        giveAwayList.push(inputNextAddress_7);
        giveAwayList.push(inputNextAddress_8);
        giveAwayList.push(inputNextAddress_9);
        giveAwayList.push(inputNextAddress_10);
    }

    uint currentGiveAwayMintAmount = 0;
    function giveAwayMint(uint amount) public onlyOwner{
        require (currentGiveAwayMintAmount < 100, "Cannot mint given amount.");
        require (amount > 0, "Must give a mint amount.");
        for (uint i = currentGiveAwayMintAmount; i < currentGiveAwayMintAmount + amount; i++){
            address to = giveAwayList[i]; 
            uint256 tokenId = _tokenIdCounter.current();
            BKJ[tokenId].stage = 0;
            BKJ[tokenId].txTime = 0;
            _tokenIdCounter.increment();
            _safeMint(to, tokenId);
            _setTokenURI(tokenId, _engenderURI(tokenId));
            emit tokenURIListener(tokenURI(tokenId));
        }
        currentGiveAwayMintAmount += amount;
    }
    
    function pause() public onlyOwner {
        _pause();
    }

    function unpause() public onlyOwner {
        _unpause();
    }

    function _beforeTokenTransfer(address from, address to, uint256 tokenId)
        internal
        whenNotPaused
        override(ERC721, ERC721Enumerable)
    {
        super._beforeTokenTransfer(from, to, tokenId);
    }

    // The following functions are overrides required by Solidity.

    function _burn(uint256 tokenId) internal override(ERC721, ERC721URIStorage) {
        super._burn(tokenId);
    }

    function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        return super.tokenURI(tokenId);
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721, ERC721Enumerable)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }

        // The URI of BKJ changes when NFTs are transfering
    function _transfer(
        address from,
        address to,
        uint256 tokenId
    ) internal virtual override ( ERC721 ) {
        require(ERC721.ownerOf(tokenId) == from, "ERC721: transfer from incorrect owner");
        require(to != address(0), "ERC721: transfer to the zero address");

        _beforeTokenTransfer(from, to, tokenId);

        // Clear approvals from the previous owner
        _approve(address(0), tokenId);

        _balances[from] -= 1;
        _balances[to] += 1;
        _owners[tokenId] = to;

        emit Transfer(from, to, tokenId);

        _afterTokenTransfer(from, to, tokenId);

        if (BKJ[tokenId].txTime < 3) {
            _evolveStage(tokenId);
            BKJ[tokenId].txTime++;
        }
    }
}