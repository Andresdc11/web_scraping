import requests
import lxml.html as html
import csv

HOME_URL = 'https://catholicmasstime.org/church/state/michigan/'
XPATH_LINK_TO_ARTICLE = '//div[@class="list-group-item"]//@href'
XPATH_DIR = '//*[@id="church-address"]/text()[1]'
XPATH_TEL = '//*[@id="church-address"]/text()[4]'
XPATH_MAIL ='//*[@id="church-address"]/a[1]/@href'
XPATH_WEB ='//*[@id="church-address"]/a[2]/@href'
XPATH_IG = '//h1[@class="church-name card-header"]/text()'
XPARH_POST = '//*[@id="church-address"]/text()[2]'

def get_title(link):
    url = link.split('/')[-1]
    title_list=url.split('-')[:-1]
    title = " ".join(title_list)
    return(title)

def parse_notice(link, writer):
    try:
        response = requests.get("https://catholicmasstime.org" + link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)

            try:
                url = "https://catholicmasstime.org"+link                 
                ig = parsed.xpath(XPATH_IG)
                dir = parsed.xpath(XPATH_DIR)
                post= parsed.xpath(XPARH_POST)
                tel= parsed.xpath(XPATH_TEL)
                mail = parsed.xpath(XPATH_MAIL)
                web = parsed.xpath(XPATH_WEB) 

                row = [url.strip(), ig[0].strip(), dir[0].strip(), post[0].strip(), tel[0].strip(), mail[0].strip(), web[0].strip()]
                writer.writerow(row)

            except IndexError:
                print("as")
                return            

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)

            with open('Michigan_big.csv', 'w', newline='', encoding='utf-8') as f:
                writer= csv.writer(f)
                writer.writerow(['URL', 'Nombre', 'Dirección', 'Código Postal', 'Teléfono', 'Email', 'Sitio Web'])

                for link in links_to_notices:
                    parse_notice(link, writer)

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

def run():
    parse_home()

if __name__ == "__main__":
    run()
