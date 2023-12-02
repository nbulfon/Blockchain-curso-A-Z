// bulfonCoins_ICO

// version del compilador
pragma solidity ^0.8.23;


contract bulfonCoin_ICO {

    // nro max de bulfonCoins disponibles para la venta ->
    uint public max_bulfonCoins = 1000000;

    // tipo de cambio de bulfonCoin/USD ->
    uint public usd_to_bulfonCoins = 1000;

    // nro total de bulfonCoins comprados por inversores ->
    uint public total_bulfonCoins_bought = 0;


    // mapping, que dada la dirección del inversor, devuelve su equivalencia, tanto en bulfonCoins como en USD ->
    mapping(address => uint) equity_bulfonCoins;
     mapping(address => uint) equity_usd;

    // comprobar si un inversor puede comprar bulfonCoins ->
    modifier can_buy_bulfonCoins(uint usd_invested) {
        require (usd_invested * usd_to_bulfonCoins + total_bulfonCoins_bought <= max_bulfonCoins);
        _;
    }

    // obtener el balance de bulfonCoins de un inversor ->
    function equity_in_bulfonCoins(address investor) external view returns(uint) {
        return equity_bulfonCoins[investor];
    }

    // obtener el balance de USD de un inversor ->
        function equity_in_usd(address investor) external view returns(uint) {
        return equity_usd[investor];
    }

    // Comprar bulfonCoins
    function buy_bulfonCoins(address investor, uint usd_invested) external 
    can_buy_bulfonCoins(usd_invested) {
        uint bulfonCoins_bought = usd_invested * usd_to_bulfonCoins;
        equity_bulfonCoins[investor] += bulfonCoins_bought;
        equity_usd[investor] = equity_bulfonCoins[investor] / usd_to_bulfonCoins;
        total_bulfonCoins_bought += bulfonCoins_bought;
    }
    
    // Vender bulfonCoins
    function sell_bulfonCoins(address investor, uint bulfonCoins_sold) external {
        equity_bulfonCoins[investor] -= bulfonCoins_sold;
        equity_usd[investor] = equity_bulfonCoins[investor] / usd_to_bulfonCoins;
        total_bulfonCoins_bought -= bulfonCoins_sold;
    }

}