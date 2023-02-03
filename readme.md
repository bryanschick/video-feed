python -m venv env

PowerShell -ExecutionPolicy Bypass
.\env\Scripts\activate

pip install feedparser
pip freeze > requirements.txt
pip install -r requirements.txt

python script.py

https://feedparser.readthedocs.io/en/latest/common-rss-elements.html