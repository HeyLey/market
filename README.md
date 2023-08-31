A simple application that lets the user buy, sell products etc. which should be stored in some kind of data storage.

The basic use cases of a customer:
- buying / selling a product
- products going back into stock

Start db (Mac OS M1):

arch -arm64 brew install postgresql@14
brew services start postgresql

Then run init.sql

Db Connection and secrets:
Please edit config.py

App main:
app.py

