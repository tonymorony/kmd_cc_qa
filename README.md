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

Oracle mass testing tools: 

1) oracle_mass_creation.py - creating as much oracles as you need with needed type, creating as much UTXOs as you need.  Creating 3 files:
 a) oracles_list (list of oracles txids) 
 b) register_list (list of registration txids)
 c) subscriptions_list (list of subscription txids)

2) oracle_mass_datapublish.py - using oracles_list and data_sample as inputs. Put data string by sting from data_sample to each oracle from oracles_list. As output creating data_batonids with latest batontxid for each oracle

3) oracle_mass_dataread.py - using oracles_list, data_batonids and data_sample (just to get depth). Reading data from each oracle baton by baton and put it to files like data_%oracletxid%)

