Python3 required for execution:
`sudo apt-get install python3.6`

System have to know path to komodod. e.g.:
`export PATH=$PATH:~/komodo/src`

Before execution be sure than daemon for needed AC up.

test_modules.py - test modules code

run_test.py     - running auto-testing (`python3 -m unittest -v run_test.py`)

trading.py      - interactive CLI for manual interaction with Tokens CC.
                  Now possible create token and list all avaliable in CC tokens
                  soon I'll add possibility to list / place / fill trades

oracle.py       - interactive CLI for oracle CC. Now possible to prepare oracle
                  for data publishing (create, register, subscribe) in easy way.
                  Next step is to add functionallity to transfer various data types
                  from/to files to/from blockchain
