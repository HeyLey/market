A simple application that lets the user buy, sell products etc. which should be stored in some kind of data storage.

The basic use cases of a customer:
- buying / selling a product
- products going back into stock

Start db (Mac OS M1):
```
arch -arm64 brew install postgresql@14
brew services start postgresql
```
Then run db/init.sql

Db Connection and secrets:
Please edit config.py

Install requirements:
```
pip install -r requirements.txt
```

App main file:
app.py

Run app:
```
python -m flask run 
```
or
```
python app.py
```

Set port and host (example):
```
python -m flask run  --host 127.0.0.1 --port 8000
```
