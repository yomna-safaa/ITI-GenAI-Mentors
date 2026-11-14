steps:

```sh
python -m venv .itienv

Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.itienv\Scripts\activate
```

requirements + run demo:

```sh
pip install requests python-dotenv
python .\api_demo.py

python -m pip freeze > requirements.txt
# deacivate
```