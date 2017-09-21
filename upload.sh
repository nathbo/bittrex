# How to upload
rm -r dist crypto_exchanges.*
python setup.py sdist
twine upload dist/*
rm -r dist crypto_exchanges.*
