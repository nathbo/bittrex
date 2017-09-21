# Crypto-Exchanges

Python wrapper to access the API of multiple cryptocurrency exchanges.
I am not affiliated with any of the exchanges.
I love python and use those exchanges regularly, so I wanted to create a good environment to access al of those exchanges. Over the time I will add more exchanges, and later also some data-formatting functions.

I know there are already packages out there, but I wanted to create my own package to learn more about documentation, packaging, and tests.

Implemented so far:
* Bittrex
* Poloniex

## Installation
```
pip install crypto-exchanges
```

## Example usage
Using the Public API without authentification
```python
from cryptoex import Bittrex

trex = Bittrex()
trex.get_currencies()
```

For private calls either pass `key` and `secret` to `Bittrex` directly,
or use one of `Bittrex.add_key(key, secret)` or `Bittrex.load_key(file)`.
In this example I load the key from a file `bittrex.key` that contains
the key on the first line and the secret on the second.
```python
from cryptoex import Bittrex

trex = Bittrex('bittrex.key')
trex.get_balance('BTC')
```
