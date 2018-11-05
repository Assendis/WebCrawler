# MSN Web Crawler

It discovers news in msn.com and It saves to my database with news' source.
Also, It runs in every 5 minutes with crontab and writes to *asude.log* file.

Requirements:
Sqlite3
BeautifulSoup
Requests

Installation:
pip install -r requirements.txt
crontab -e

Add the line:
*/5 * * * * /usr/bin/python /home/to/path/crawler.py

To run:
python crawler.py

To follow the changes:
tail -f asude.log
