# Cryptoex

Python wrapper to access the API of multiple cryptocurrency exchanges.

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
from cryptoex.bittrex import Bittrex

trex = Bittrex()
trex.get_currencies()
```

For private calls either pass `key` and `secret` to `Bittrex` directly,
or use one of `Bittrex.add_key(key, secret)` or `Bittrex.load_key(file)`.
In this example I load the key from a file `bittrex.key` that contains
the key on the first line and the secret on the second.