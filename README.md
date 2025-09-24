# Crypto trading telegram bot

Usage:

```bash
cp env_secrets_sample.py env_secrets.py
# Get your secrets...
pip install -r requirements.txt
python main.py
```

## Description

Get the current `/price` of a hardcoded crypto via Telegram bot commands, using the ccxt library and the Binance API.

You can also use `/buy` and `/sell` commands, either simulated or real.

Everything is logged into a file like this:

```log
[2025/09/24 11:22:44] Error buying 50$ of ETH/USDC:
binance Account has insufficient balance for requested action.

### INIT BUY ###

[2025/09/24 11:44:14]
  Purchased amount: 0.011957545928933912 ETH/USDC @ 4181.46
  Cost: 50$
  Fee: 0.0375$
  Fee percentage: 0.075%
  Total cost: 50.0375$

### END BUY ###

### INIT SELL ###

[2025/09/24 11:44:19]
  Sold amount: 0.011957545928933912 ETH/USDC @ 4181.46
  Cost: 50.0$
  Fee: 0.0375$
  Fee percentage: 0.075%
  Total recovered: 49.9625$

### END SELL ###

Summary:
  Operation balance without fees: 0.0$
  Operation fees: 0.075$
  Operation balance: -0.07500000000000284$

################################################


```