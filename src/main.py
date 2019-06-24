import time

from github import Github, GithubException
import re

import logging

# from logging.handlers import RotatingFileHandler

git_logger = logging.getLogger()
git_logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
git_logger.addHandler(stream_handler)

github = Github("[VA GENERER UN TOKEN DANS TES SETTINGS GITHUB]", per_page=100)

mail_pattern = '([\\w-]+@student.42.fr)'

emails = {}
search_results = github.search_code(query='"@student.42.fr"')
nb_pages = search_results.totalCount

i = 0
final_page = 10
while i < final_page:
    for content_file in search_results.get_page(i):
        git_logger.info('Parsing results from {}'.format(content_file.repository.html_url))
        str_content = content_file.decoded_content.decode('utf-8')
        matches = re.findall(mail_pattern, str_content)
        if matches:
            for match in matches:
                email = re.search(mail_pattern, match)
                email = email.group(1)
                if email not in emails:
                    emails[email] = []
                if content_file.repository.html_url not in emails[email]:
                    emails[email].append(content_file.repository.html_url)
    i = i + 1

for email, repos in emails.items():
    print(email)
    for repo in repos:
        print("\t{}".format(repo))