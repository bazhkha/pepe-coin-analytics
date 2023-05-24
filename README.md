# Phân tích PEPE Token 🐸

## Mô tả
[PEPE](https://www.pepe.vip/) là một token ERC20, được tạo ra bởi một (hoặc một nhóm) người ẩn danh trên mạng lưới Blockchain Ethereum vào ngày [14-04-2023](https://etherscan.io/tx/0x2afae7763487e60b893cb57803694810e6d3d136186a6de6719921afd7ca304a). Giá trị của 1 $PEPE đạt đỉnh vào ngày 05-05-2023, tăng khoảng **380,000 lần** so với ngày đầu phát hành. Với hơn **800,000 giao dịch** (tính đến ngày 21-05-2023).

Vậy có gì trong những giao dịch này? Điều gì khiến một chú ếch xanh có bước nhảy hàng trăm nghìn lần như thế, những ai đã tác động đến thị trường của PEPE? Và một người bình thường có thể đạt được lợi nhuận thông qua việc giao dịch PEPE không?

Thông qua quá trình phân tích dữ liệu onchain của PEPE, sẽ một phần nào đó trả lời được những câu hỏi trên và tìm ra một số pattern của các cá voi khi trading meme token.

![PEPE meme](https://assets.teenvogue.com/photos/57ebd71b82c30dac286b6150/16:9/w_1280,c_limit/pepe-fb.jpg)

## Cài đặt và lấy dữ liệu

**1. Cài đặt môi trường và thư viện (Cho việc phân tích dữ liệu)**

- Môi trường: Python
- Cài đặt thư viện:
```bash
pip install pandas numpy matplotlib networkx requests jinja2
```

**2. Lấy dữ liệu bằng Dune Analytics**

Dữ liệu trên Blockchain có thể được lấy bằng nhiều cách khác nhau, trong đó sử dụng **[Dune Analytics](https://dune.com/browse/dashboards)** là một cách nhanh chóng và tiện lợi để lấy dữ liệu onchain đã được decode.

Các bạn có thể tự tạo query để lấy dữ liệu giao dịch của PEPE hoặc sử dụng các câu query dưới đây:

> Do Dune giới hạn dung lượng download file csv là 1GB và 2 bảng `erc20_ethereum.evt_Transfer` và `dex.trades` trên Dune có khối lượng dữ liệu lớn nên việc join 2 bảng tốn khá nhiều thời gian. Do đó mình tách làm 2 câu query và thực hiện việc join bằng pandas.

[1. Get swap transacions](https://dune.com/queries/2451707)
### 
```sql
-- Default values
-- {{blockchain}} = ethereum
-- {{token_address}} = 0x6982508145454Ce325dDbE47a25d4ec3d2311933
-- {{start_time}} = 2023-04-14
-- {{end_time}} = 2023-04-15

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
WHERE blockchain = '{{blockchain}}'
    AND (
        token_bought_address = {{token_address}}
        OR token_sold_address = {{token_address}}
    )
    AND block_time BETWEEN TIMESTAMP '{{start_time}}' AND TIMESTAMP '{{end_time}}'
ORDER BY block_time
```

[Get transfer transactions](https://dune.com/queries/2494730)
###
```sql
-- Default values
-- {{blockchain}} = ethereum
-- {{token_address}} = 0x6982508145454Ce325dDbE47a25d4ec3d2311933
-- {{start_time}} = 2023-04-14
-- {{end_time}} = 2023-04-15

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
FROM erc20_{{blockchain}}.evt_Transfer AS evt_transfer
LEFT JOIN {{blockchain}}.transactions AS tx
    ON tx.hash = evt_transfer.evt_tx_hash
    AND tx.block_time BETWEEN TIMESTAMP '{{start_time}}' AND TIMESTAMP '{{end_time}}'
WHERE evt_transfer.contract_address = {{token_address}}
    AND evt_transfer.evt_block_time BETWEEN TIMESTAMP '{{start_time}}' AND TIMESTAMP '{{end_time}}'
ORDER BY 2 DESC
```

## Phân tích

### Tổng quan
Trong gần 40 ngày giao dịch đã có:
    
- **822,804 giao dịch** được thực hiện
- **183,322 users**
- Tổng Khối lượng giao dịch đạt hơn **5 tỷ đô**
- Tổng số ETH trả cho phí giao dịch: **12,064 ETH**

Trong ngày đầu tiên khi thanh khoản được cung cấp, đã có **61 "early bird"** (address) được tạo ra chỉ để mua PEPE. Những address này không phải ngẫu nhiên mà đều có sự liên kết với cách thức giao dịch giống nhau. Mình tìm được 3 nhóm address như hình bên dưới, các address khác cũng có phương thức tương tự nhưng chuyển vào các ví mới nên mình chưa tìm được sự liên kết.


### Giao dịch 

Ngoài `swap` và `transfer` thì gần như token PEPE không được sử dụng trong bất kỳ trường hợp nào khác.

![methods](./img/methods.png)

Các giao dịch `swap` chiếm **75.4%** trong tổng số các giao dịch đã thực thi. Chiếm phần lớn trong số 24.6% các giao dịch còn lại là các giao dịch `transfer`.

![swap-type-ratio](./img/swap-type-ratio.png)

Điều này diễn tả đúng với disclaimer của PEPE team khi tạo ra token này, chỉ để giải trí và không có giá trị nội tại 🐸.

![disclaimer](./img/pepe-disclaimer.png)

Các **giao dịch mua** chiếm tỷ trọng lớn kể từ khi PEPE được giao dịch.

![daily-tx](./img/daily-tx.png)

![buy-sell-pressure.png](./img/buy-sell-pressure.png)

### Volume and Price

Nhìn chung với một meme thì volume của PEPE từ những ngày đầu đã khá lớn so với những token khác trong tình hình thị trường downtrend.

![daily-volume](./img/daily-volume.png)

Có một điều gì đã xảy ra vào ngày 05-05 đã khiến độ fomo của PEPE đạt đỉnh khiến khối lượng giao dịch và giá token PEPE bắt đầu tăng đột biến. Sau đó chỉ 1 ngày, PEPE đạt ATH với **ROI ~380 nghìn lần**.
> j4f: Nếu đầu tư $1 vào PEPE vào ngày 14-04 và bán vào ngày 06-05 thì bạn sẽ có $380,000 🤑

![hourly-price](./img/hourly-price.png)

Vì là một token trên Ethereum nên thanh khoản tập trung hầu hết trên Uniswap.

![market-share](./img/market-share.png)
