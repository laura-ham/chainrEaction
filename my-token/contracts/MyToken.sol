pragma solidity ^0.5.1;

contract MyToken{
    
    mapping(address => bool) public isRecyclingPlant;
    mapping(address => mapping(uint256 => uint256)) public recycledBalanceOfGoods;
    
    
    struct recycleSubmission{
        address owner;
        uint256 product;
        uint256 weight;
    }
    
    struct product{
        uint256 weight;
        uint256 quality;
    }
    
    mapping(address => recycleSubmission[]) public plantQueue;
    mapping(address => mapping(uint256 => product)) public balanceOfGoods;
    mapping(address => mapping(uint256 => product)) public boughtBalanceOfGoods;
    
    function createPlant(bool _isRecyclingPlant) public {
        isRecyclingPlant[msg.sender]=_isRecyclingPlant;
    }
    
    function verifyWaste(bool _isValid) public {
        require(isRecyclingPlant[msg.sender]);
        require(plantQueue[msg.sender].length >0);
        if(_isValid){
            uint len =plantQueue[msg.sender].length;
            recycleSubmission memory x =plantQueue[msg.sender][len-1];
            recycledBalanceOfGoods[x.owner][x.product]+=x.weight;
            balanceOfGoods[msg.sender][x.product].weight+=x.weight;
            balanceOfGoods[msg.sender][x.product].quality=100000000;
            plantQueue[msg.sender].pop();
            
        } else {
            plantQueue[msg.sender].pop();
        }
    }
    
    function recycleWaste(address _destination, uint256 _product,uint256 _weight) public {
        require(isRecyclingPlant[_destination]);
        if (_weight >= balanceOfGoods[msg.sender][_product].weight){
            plantQueue[_destination].push(recycleSubmission(msg.sender,_product,_weight));
            balanceOfGoods[msg.sender][_product].weight=0;
        } else {
            plantQueue[_destination].push(recycleSubmission(msg.sender,_product,_weight));
            balanceOfGoods[msg.sender][_product].weight-=_weight;
        }
    }
    
    function buyGoods(address _seller,uint256 _product,uint256 _weight) public {
        require(balanceOfGoods[_seller][_product].weight>=_weight);
        
        boughtBalanceOfGoods[msg.sender][_product].quality=
        ((boughtBalanceOfGoods[msg.sender][_product].quality*boughtBalanceOfGoods[msg.sender][_product].weight)+
        (balanceOfGoods[_seller][_product].quality*_weight))/
        (balanceOfGoods[msg.sender][_product].weight+_weight);
        
        boughtBalanceOfGoods[msg.sender][_product].weight+=_weight;
        
        balanceOfGoods[_seller][_product].weight-=_weight;
        
        balanceOfGoods[msg.sender][_product].quality=((balanceOfGoods[msg.sender][_product].quality*balanceOfGoods[msg.sender][_product].weight)+(balanceOfGoods[_seller][_product].quality*_weight))/(balanceOfGoods[msg.sender][_product].weight+_weight);
        
        balanceOfGoods[msg.sender][_product].weight+=_weight;
    }
    
    function buyNRGoods(uint256 _product,uint256 _weight) public{
        boughtBalanceOfGoods[msg.sender][_product].quality=((boughtBalanceOfGoods[msg.sender][_product].quality*boughtBalanceOfGoods[msg.sender][_product].weight))/(balanceOfGoods[msg.sender][_product].weight+_weight);
        
        boughtBalanceOfGoods[msg.sender][_product].weight+=_weight;
        
        balanceOfGoods[msg.sender][_product].quality=((balanceOfGoods[msg.sender][_product].quality*balanceOfGoods[msg.sender][_product].weight))/(balanceOfGoods[msg.sender][_product].weight+_weight);
        
        balanceOfGoods[msg.sender][_product].weight+=_weight;
    }
}