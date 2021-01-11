__doc__ = """
Crawl tất cả các bài viết có label
Python(http://www.familug.org/search/label/Python), Command, sysadmin và 10 bài
viết mới nhất ở homepage của http://www.familug.org/

Tạo file `index.html`, chứa 4 cột tương ứng cho:

```
Python | Command | Sysadmin | Latest
```

Mỗi cột chứa các link bài viết, khi bấm vào sẽ mở ra bài gốc tại FAMILUG.org

Tham khảo giao diện tại:
- https://themes.getbootstrap.com/
- http://getskeleton.com/#examples

Push code lên GitLab repo, tạo 1 GitLab Page để view kết quả.
https://pages.gitlab.io/

Nâng cao: push code lên GitHub và tạo 1 GitHub Page: https://pages.github.com/
"""

import requests
import bs4
import sqlite3


conn = sqlite3.connect("familug.db")
c = conn.cursor()
c.execute('CREATE TABLE fami_lastest (name CHAR, link CHAR)')
c.execute('CREATE TABLE fami_python (name CHAR, link CHAR)')
c.execute('CREATE TABLE fami_command (name CHAR, link CHAR)')
c.execute('CREATE TABLE fami_sysadmin (name CHAR, link CHAR)')


def get_lastest(url):
	r = requests.get(url)
	tree = bs4.BeautifulSoup(markup=r.text, features='lxml')
	node = tree.find_all(name='h3', attrs={'class': 'post-title entry-title'})
	list_lastest = []
	for i in node:
		title = i.text
		link = str(i.contents[1]).split('"')[1]
		list_lastest.append((title, link))
	return list_lastest


def get_python():
	r = requests.get('https://www.familug.org/search/label/Python?max-results=100')
	tree = bs4.BeautifulSoup(markup=r.text, features='lxml')
	node = tree.find_all(name='h3', attrs={'class': 'post-title entry-title'})
	list_python = []
	for i in node:
		title = i.text
		link = str(i.contents[1]).split('"')[1]
		list_python.append((title, link))
	for title, link in list_python:
		c.execute('INSERT INTO fami_python VALUES (?, ?)', (title, link))


def get_command():
	r = requests.get('https://www.familug.org/search/label/Command?max-results=100')
	tree = bs4.BeautifulSoup(markup=r.text, features='lxml')
	node = tree.find_all(name='h3', attrs={'class': 'post-title entry-title'})
	list_command = []
	for i in node:
		title = i.text
		link = str(i.contents[1]).split('"')[1]
		list_command.append((title, link))
	for title, link in list_command:
		c.execute('INSERT INTO fami_command VALUES (?, ?)', (title, link))


def get_sysadmin():
	r = requests.get('https://www.familug.org/search/label/sysadmin?max-results=100')
	tree = bs4.BeautifulSoup(markup=r.text, features='lxml')
	node = tree.find_all(name='h3', attrs={'class': 'post-title entry-title'})
	list_sysadmin = []
	for i in node:
		title = i.text
		link = str(i.contents[1]).split('"')[1]
		list_sysadmin.append((title, link))
	for title, link in list_sysadmin:
		c.execute('INSERT INTO fami_sysadmin VALUES (?, ?)', (title, link))


def main():
	for title, link in get_lastest('https://www.familug.org/') + get_lastest('https://www.familug.org/search?updated-max=2020-04-14T22:15:00%2B07:00&max-results=4'):
		c.execute('INSERT INTO fami_lastest VALUES (?, ?)', (title, link))

	get_python()
	get_command()
	get_sysadmin()
	conn.commit()
	conn.close()


if __name__ == "__main__":
    main()
