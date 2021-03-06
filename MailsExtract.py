from googlesearch import search
import re
import urllib.request
import ssl
from email_validator import validate_email, EmailNotValidError
from pyisemail import is_email
import requests


class Extractor:

    def __init__(self, target):
        self.target = target

    def googlesearch(self):
        query = "intext:@" + self.target
        urls = []
        for j in search(query, tld="co.in", num=20, stop=20, pause=2):
            urls.append(j)
        print(urls)
        return urls

    @staticmethod
    def request(url):
        ssl._create_default_https_context = ssl._create_unverified_context
        req = urllib.request.urlopen(url)
        html = req.read()
        return html

    @staticmethod
    def replace(data):
        data = data.replace(" [at] ", "@")
        data = data.replace(" &agrave ", "@")
        data = data.replace("at", "@")
        data = data.replace(" at ", "@")

        return data

    @staticmethod
    def process(data):

        emails = []
        regex = re.compile(('[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'))
        for email in re.findall(regex, data):
            emails.append(email)
        return emails

    @staticmethod
    def checkmails(emails):
        valid = []
        for email in emails:
            try:
                v = validate_email(email)  # validate and get info
                email = v["email"]  # replace with normalized form
                valid.append(email)
            except EmailNotValidError as exc:
                pass
        return valid

    def crawl(self):
        emails = []
        urls = self.googlesearch()
        for url in urls:
            EMAIL_REGEX = r'[a-zA-Z0-9.\-_+#~!$&\',;=:]+' + '@' + r'[a-zA-Z0-9.-]*'
            data = self.request(url)
            data = data.decode("ISO-8859-1")
            data = self.replace(data)

            for re_match in re.finditer(EMAIL_REGEX, data):
                try:
                    address = re_match.group()
                    bool_result_with_dns = is_email(address, check_dns=True)
                    detailed_result_with_dns = is_email(address, check_dns=True, diagnose=True)

                    if bool_result_with_dns:
                        emails.append(address)
                except requests.exceptions.ConnectionError:
                    print("connection refused")
                except:
                    pass
        return emails


if __name__ == '__main__':
    e = Extractor("mi.parisdescartes.fr")
    print(e.crawl())
