Python3 required for execution:
`sudo apt-get install python3.6`

System have to know path to komodod. e.g.:
`export PATH=$PATH:~/komodo/src`

Before execution be sure than daemon for needed AC up.

At the moment token creation process is covered.

test_modules.py - test modules code

run_test.py     - running auto-testing (`python3 -m unittest -v run_test.py`)

trading.py      - some interactive CLI for manual interaction with Tokens CC,
                  now possible only create token and list all avaliable in CC tokens
                  soon I'll add possibility to list / place / fill trades

oracle.py       - interactive CLI for oracle CC. Now possible to prepare oracle
                  for data publishing (create, register, subscribe) in easy way
