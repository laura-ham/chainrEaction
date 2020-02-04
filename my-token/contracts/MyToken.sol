pragma solidity ^0.5.1;

contract MyToken{

    mapping(address => bool) public isRecyclingPlant;
    mapping(address => mapping(uint256 => int256)) public balanceOfRGoods;
    mapping(address => mapping(uint256 => int256)) public boughtBalanceOfRGoods;
    mapping(address => mapping(uint256 => int256)) public balanceOfNRGoods;
    mapping(address => mapping(uint256 => int256)) public boughtBalanceOfNRGoods;
    mapping(address => mapping(uint256 => int256)) public recycledBalanceOfGoods;


    struct recycleSubmission{
        address owner;
        uint256 product;
        int256 weight;
    }

    mapping(address => recycleSubmission[]) public plantQueue;

    function createUser(bool _isRecyclingPlant) public {
        isRecyclingPlant[msg.sender]=_isRecyclingPlant;
    }

    function pickUpLitter(uint256 _product,int256 _weight) public {
        balanceOfRGoods[msg.sender][_product]+=_weight;
    }

    function verifyWaste(bool _isValid) public {
        require(isRecyclingPlant[msg.sender]);
        require(plantQueue[msg.sender].length >0);
        if(_isValid){
            uint len =plantQueue[msg.sender].length;
            recycleSubmission memory x =plantQueue[msg.sender][len-1];
            recycledBalanceOfGoods[x.owner][x.product]+=x.weight;
            balanceOfRGoods[msg.sender][x.product]+=x.weight;
            plantQueue[msg.sender].pop();

        } else {
            plantQueue[msg.sender].pop();
        }
    }

    function recycleWaste(address _destination, uint256 _product) public {
        require(isRecyclingPlant[_destination]);
        plantQueue[_destination].push(recycleSubmission(msg.sender,_product,balanceOfRGoods[msg.sender][_product]+balanceOfNRGoods[msg.sender][_product]));
        balanceOfRGoods[msg.sender][_product]=0;
        balanceOfNRGoods[msg.sender][_product]=0;
    }

    function buyGoods(address _seller,uint256 _product,int256 _rweight,int256 _nrweight) public {
        require(balanceOfRGoods[_seller][_product]>=_rweight);
        require(balanceOfNRGoods[_seller][_product]>=_nrweight);
        balanceOfRGoods[_seller][_product]-=_rweight;
        balanceOfNRGoods[msg.sender][_product]+=_nrweight;
        balanceOfRGoods[_seller][_product]-=_rweight;
        balanceOfNRGoods[msg.sender][_product]+=_nrweight;
        boughtBalanceOfRGoods[msg.sender][_product]+=_rweight;
        boughtBalanceOfNRGoods[msg.sender][_product]+=_nrweight;
    }

}