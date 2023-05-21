# pepe-coin-analytics

## Query data from Dune analytics

## Install
pip install pandas numpy matplotlib networkx requests jinja2

// https://dune.com/queries/2451707
### Query swap transactions 
```sql
SELECT
    -- blockchain,
    CONCAT(project, '-', version) AS project,
    -- block_date,
    block_time,
    token_bought_symbol,
    token_sold_symbol,
    -- token_pair,
    token_bought_amount,
    token_sold_amount,
    -- token_bought_amount_raw,
    -- token_sold_amount_raw,
    amount_usd,
    -- token_bought_address,
    -- token_sold_address,
    -- taker,
    -- maker,
    -- project_contract_address,
    -- trace_address,
    -- evt_index,
    tx_hash,
    tx_from,
    tx_to
FROM dex.trades
WHERE blockchain = 'ethereum'
    AND (
        token_bought_address = 0x6982508145454ce325ddbe47a25d4ec3d2311933
        OR token_sold_address = 0x6982508145454ce325ddbe47a25d4ec3d2311933
    )
    AND block_time BETWEEN TIMESTAMP '{{start_time}}' AND TIMESTAMP '{{end_time}}'
ORDER BY block_time
```

// https://dune.com/queries/2494730
### Query event transfer
```sql
SELECT
    tx.block_time
    , tx.block_number
    , tx.hash
    -- , tx.value
    -- , tx.gas_limit
    , tx.gas_price
    , tx.gas_used
    -- , (tx.gas_used * tx.gas_price) / 1e18 AS tx_fee
    -- , tx.max_fee_per_gas
    -- , tx.max_priority_fee_per_gas
    -- , tx.priority_fee_per_gas
    , tx.nonce
    -- , tx.index
    , tx."from"
    , tx."to"
    , SUBSTRING(CAST(tx.data AS VARCHAR), 1, 2 + 8) AS method_id
    -- , tx.data
    -- , tx."type"
    -- , tx.access_list
    -- , evt_transfer."from" AS sender
    -- , evt_transfer."to" AS receiver
FROM erc20_ethereum.evt_Transfer AS evt_transfer
LEFT JOIN ethereum.transactions AS tx
    ON tx.hash = evt_transfer.evt_tx_hash
    AND tx.block_time BETWEEN TIMESTAMP '{{start_time}}' AND TIMESTAMP '{{end_time}}'
WHERE evt_transfer.contract_address = 0x6982508145454Ce325dDbE47a25d4ec3d2311933
    AND evt_transfer.evt_block_time BETWEEN TIMESTAMP '{{start_time}}' AND TIMESTAMP '{{end_time}}'
ORDER BY 2 DESC

```

