__doc__ = """
Làm một website tuyển dụng.

Lấy dữ liệu các job từ: https://github.com/awesome-jobs/vietnam/issues

Lưu dữ liệu vào một bảng ``jobs`` trong SQLite. Xem ví dụ: https://docs.python.org/3/library/sqlite3.html

Tạo website hiển thị danh sách các jobs khi vào đường dẫn ``/``.
Khi bấm vào mỗi job (1 link), sẽ mở ra trang chi tiết về jobs (giống như trên
các trang web tìm viêc).
"""
import requests
import sqlite3
import time


conn = sqlite3.connect('familug.db')
c = conn.cursor()
c.execute('CREATE TABLE awe_jobs (name CHAR, link CHAR)')


def get_jobs_data(number):
	url = 'https://api.github.com/repos/awesome-jobs/vietnam/issues?page={}&q=is%3Aissue+is%3Aopen'.format(number)
	r = requests.get(url)
	list_jobs = []
	for job in r.json():
		title = job['title']
		html_url = job['html_url']
		list_jobs.append((title, html_url))
	return list_jobs


def main():
	
	all_jobs = []
	for number in range(1, 4):
		all_jobs += get_jobs_data(number)

	for title, html_url in all_jobs:
		c.execute('INSERT INTO awe_jobs VALUES (?, ?)', (title, html_url))
	
	conn.commit()
	conn.close()


if __name__ == "__main__":
    main()
