# NanoID Generator

Nano ID is a library for generating random IDs. Likewise UUID, there is a probability of duplicate IDs. However, this probability is extremely small.
It uses [py-nanoid](https://github.com/puyuan/py-nanoid) library.



## Test Backend

In src_backend folder, run the api in local server

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Use API Tester or run following command to test 
```bash
curl http://127.0.0.1:8000/v1/nanoid/3
curl -X POST http://127.0.0.1:8000/v1/nanoid/3 -H "Content-Type: application/json" -d "{\"alphabets\": \"1234567890abcdef\", \"length\": 20}"
```