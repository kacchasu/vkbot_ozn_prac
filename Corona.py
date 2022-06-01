import requests
import bs4 as bs
import re
from datetime import datetime
import matplotlib.pyplot as plt


class Corona:
    def __init__(self, region):
        self.region = region

        self.date = ""
        self.cases = ""
        self.active = ""
        self.cured = ""
        self.died = ""

        self.new_cases = ""
        self.new_active = ""
        self.new_cured = ""
        self.new_died = ""

        self.date_list = []
        self.active_list = []
        self.cured_list = []
        self.died_list = []
        self.cases_list = []

        self.logging("CRE", "corona class object: created")

    # for logging
    @staticmethod
    def logging(key, comm):
        f1 = open("log.txt", "a")
        t1 = datetime.now()
        f1.write(key + " --- ")
        f1.write(t1.strftime("%d/%m/%Y %H:%M") + " --- ")
        f1.write("corona class: " + comm + '\n')

    # get covid for russia
    def get_russia_covid(self):
        corona_request = requests.get("https://coronavirusstat.ru/")
        corona_soup = bs.BeautifulSoup(corona_request.text, "html.parser")

        self.date = corona_soup.find('strong').get_text()
        self.logging("GET", "corona class object: got date")

        self.cases = corona_soup.find_all('div', 'h2')[0].next_element.get_text()
        self.active = corona_soup.find_all('div', 'h2')[1].next_element.get_text()
        self.cured = corona_soup.find_all('div', 'h2')[2].next_element.get_text()
        self.died = corona_soup.find_all('div', 'h2')[3].next_element.get_text()

        self.new_cases = corona_soup.find('span', 'font-weight-bold text-text-dark').get_text()
        self.new_active = corona_soup.find('span', 'font-weight-bold text-primary').get_text()
        self.new_cured = corona_soup.find('span', 'font-weight-bold text-success').get_text()
        self.new_died = corona_soup.find('span', 'font-weight-bold text-danger').get_text()

    # get covid stat
    def get_covid_stat(self):
        corona_request = requests.get("https://coronavirusstat.ru/country/russia/")
        corona_soup = bs.BeautifulSoup(corona_request.text, "html.parser")

        for i in range(10):
            corona_row = corona_soup.find('tbody').find_all('tr')[i]
            self.date_list.append(corona_row.find('th').get_text())
            self.active_list.append(int(corona_row.find_all('td')[0].contents[0].strip()))
            self.cured_list.append(int(corona_row.find_all('td')[1].contents[0].strip()))
            self.died_list.append(int(corona_row.find_all('td')[2].contents[0].strip()) + int(
                corona_row.find_all('td')[1].contents[0].strip()))
            self.cases_list.append(int(corona_row.find_all('td')[3].contents[0].strip()))

        self.date_list = self.date_list[::-1]
        self.cured_list = self.cured_list[::-1]
        self.active_list = self.active_list[::-1]
        self.died_list = self.died_list[::-1]

        plt.figure(figsize=(9, 7))
        plt.bar(self.date_list, self.died_list, width=1, label='Умерло', color='seagreen')
        plt.bar(self.date_list, self.cured_list, width=1, label='Вылечено', color='darkorange')
        plt.bar(self.date_list, self.active_list, width=1, label='Активных', color='royalblue')
        plt.legend(loc='upper left')
        plt.xticks(rotation=30)
        plt.suptitle('Россия - детальная статистика - коронавирус')
        plt.ylim(0, 20000000)
        plt.savefig('corona.jpg')

        self.logging("GET", "corona class object: got corona stat")

    def get_corona_region(self):
        corona_request = requests.get("https://coronavirusstat.ru/")
        corona_soup = bs.BeautifulSoup(corona_request.text, "html.parser")

        self.date = corona_soup.find('strong').get_text()
        self.logging("GET", "corona class object: got date")

        if corona_soup.find('a', href=re.compile('^/country/'), text=re.compile(self.region)) != None:
            self.region = corona_soup.find('a', href=re.compile('^/country/'), text=re.compile(self.region)).get_text()
        else:
            return -1
        self.logging("GET", "corona class object: got region")

        self.cases = \
            corona_soup.find_all('a', href=re.compile('^/country/'), text=re.compile(self.region))[
                -1].parent.parent.parent.parent.find_all('div', 'h6 m-0')[0].contents[0].strip()
        self.active = \
            corona_soup.find_all('a', href=re.compile('^/country/'), text=re.compile(self.region))[
                -1].parent.parent.parent.parent.find_all('div', 'h6 m-0')[1].contents[1].get_text()
        self.cured = \
            corona_soup.find_all('a', href=re.compile('^/country/'), text=re.compile(self.region))[
                -1].parent.parent.parent.parent.find_all('div', 'h6 m-0')[2].contents[1].get_text()
        self.died = \
            corona_soup.find_all('a', href=re.compile('^/country/'), text=re.compile(self.region))[
                -1].parent.parent.parent.parent.find_all('div', 'h6 m-0')[3].contents[1].get_text()

        self.new_cases = corona_soup.find_all('a', href=re.compile('^/country/'), text=re.compile(self.region))[
            -1].parent.parent.parent.parent.find_all('div', 'h6 m-0')[0].contents[1].get_text()
        self.new_active = \
            corona_soup.find_all('a', href=re.compile('^/country/'), text=re.compile(self.region))[
                -1].parent.parent.parent.parent.find_all('div', 'h6 m-0')[1].contents[3].get_text()
        self.new_cured = corona_soup.find_all('a', href=re.compile('^/country/'), text=re.compile(self.region))[
            -1].parent.parent.parent.parent.find_all('div', 'h6 m-0')[2].contents[3].get_text()
        self.new_died = corona_soup.find_all('a', href=re.compile('^/country/'), text=re.compile(self.region))[
            -1].parent.parent.parent.parent.find_all('div', 'h6 m-0')[3].contents[3].get_text()

        if self.new_cases == "":
            self.new_cases = "+0"
        if self.new_active == "":
            self.new_active = "+0"
        if self.new_cured == "":
            self.new_cured = "+0"
        if self.new_died == "":
            self.new_died = "+0"

        self.logging("GET", "corona class object: got corona region stat")
'''
corona_request = requests.get("https://coronavirusstat.ru/country/russia/")
corona_soup = bs.BeautifulSoup(corona_request.text, "html.parser")
corona_result = corona_soup.find('strong').get_text()

current_corona_cases = corona_soup.find_all('div', 'h2')[0].next_element.get_text()
current_corona_active = corona_soup.find_all('div', 'h2')[1].next_element.get_text()
current_corona_cured = corona_soup.find_all('div', 'h2')[2].next_element.get_text()
current_corona_died = corona_soup.find_all('div', 'h2')[3].next_element.get_text()

new_corona_cases = corona_soup.find('span', 'font-weight-bold text-text-dark').get_text()
new_corona_active = corona_soup.find('span', 'font-weight-bold text-primary').get_text()
new_corona_cured = corona_soup.find('span', 'font-weight-bold text-success').get_text()
new_corona_died = corona_soup.find('span', 'font-weight-bold text-danger').get_text()

region = 'осковская'
corona_region = corona_soup.find('a', href=re.compile('^/country/'), text=re.compile(region))

current_corona_region_cases = corona_soup.find_all('a', href=re.compile('^/country/'), text=re.compile(region))[
    -1].parent.parent.parent.parent.find_all('div', 'h6 m-0')[0].contents[0].strip()
current_corona_region_active = corona_soup.find_all('a', href=re.compile('^/country/'), text=re.compile(region))[
    -1].parent.parent.parent.parent.find_all('div', 'h6 m-0')[1].contents[1].get_text()
current_corona_region_cured = corona_soup.find_all('a', href=re.compile('^/country/'), text=re.compile(region))[
    -1].parent.parent.parent.parent.find_all('div', 'h6 m-0')[2].contents[1].get_text()
current_corona_region_died = corona_soup.find_all('a', href=re.compile('^/country/'), text=re.compile(region))[
    -1].parent.parent.parent.parent.find_all('div', 'h6 m-0')[3].contents[1].get_text()

new_corona_region_cases = corona_soup.find_all('a', href=re.compile('^/country/'), text=re.compile(region))[
    -1].parent.parent.parent.parent.find_all('div', 'h6 m-0')[0].contents[1].get_text()
new_corona_region_active = corona_soup.find_all('a', href=re.compile('^/country/'), text=re.compile(region))[
    -1].parent.parent.parent.parent.find_all('div', 'h6 m-0')[1].contents[3].get_text()
new_corona_region_cured = corona_soup.find_all('a', href=re.compile('^/country/'), text=re.compile(region))[
    -1].parent.parent.parent.parent.find_all('div', 'h6 m-0')[2].contents[3].get_text()
new_corona_region_died = corona_soup.find_all('a', href=re.compile('^/country/'), text=re.compile(region))[
    -1].parent.parent.parent.parent.find_all('div', 'h6 m-0')[3].contents[3].get_text()
'''
