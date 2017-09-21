# Cryptoex

Python wrapper to access the API of multiple cryptocurrency exchanges.

Implemented so far:
* Bittrex
* Poloniex

## Installation
```
pip install crypto-exchanges
```

## Usage
```python
from cryptoex.bittrex import Bittrex
trex = Bittrex()
trex.get_currencies()
```