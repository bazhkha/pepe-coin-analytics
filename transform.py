import pandas as pd

df_evt_transfers_1 = pd.read_csv('./data/raw/evt_transfer/evt_transfer_transactions_1.csv')
df_evt_transfers_2 = pd.read_csv('./data/raw/evt_transfer/evt_transfer_transactions_2.csv')
df_evt_transfers = pd.concat([df_evt_transfers_1, df_evt_transfers_2])

df_swaps = pd.read_csv('./data/raw/swap_transactions.csv')

df = pd.merge(
  df_evt_transfers,
  df_swaps,
  left_on='hash',
  right_on='tx_hash',
  how='left'
).sort_values(by='block_time_x')

df = df.assign(tx_fee = lambda x: (x.gas_price * x.gas_used) / 1e18)

df = df[[
  'block_time_x',
  'block_number',
  'hash',
  'tx_fee',
  'nonce',
  'from',
  'to',
  'method_id',
  'project',
  'token_bought_symbol',
  'token_sold_symbol',
  'token_bought_amount',
  'token_sold_amount',
  'amount_usd',
  'tx_from',
  'tx_to'
]]

df.rename(columns={'block_time_x': 'block_time'}, inplace=True)

df.to_csv('./data/transactions.csv', index=False)
print('Done ✨')
