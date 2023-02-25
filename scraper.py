import requests
import lxml.html as html
from openpyxl import workbook


HOME_URL = 'https://www.aodfinder.org/parishes?__hstc=227631426.717ac726bfb3dd1685dc12d93c3d2368.1676306872078.1677012115480.1677166806890.3&__hssc=227631426.2.1677166806890&__hsfp=3547924738'

XPATH_LINK_TO_ARTICLE = '//div[@class="finder-results"]//@id'
#XPATH_TITLE = Titulo
XPATH_DIR = '//p[@class="place-meta"]//text()'

XPATH_MAIL ='//a[@class="place-meta"]//@href'
XPATH_NAME ='//div[@class="clergy"]//text()'
XPATH_IG = '//h2[@class="place-meta-title"]//text()'

def get_title(link):
    #separamos por "/" y nos quedamos con el ultimo que elemento 
    url = link.split('/')[-1]
    #separamos por "-" y eliminamos el ultimo elemento
    title_list=url.split('-')[:-1]
    #Unimos lo anterior
    title = " ".join(title_list)

    return(title)


def parse_notice(link,f):
    try:
        response = requests.get("https://www.aodfinder.org/parishes/" + link)
        if response.status_code == 200:
            
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)

            try:
                url = "https://www.aodfinder.org/parishes/"+link                 
                ig = parsed.xpath(XPATH_IG)
                dir = parsed.xpath(XPATH_DIR)
                
                mail = parsed.xpath(XPATH_MAIL)
                name = parsed.xpath(XPATH_NAME) 

                f.write(url)
                f.write('\n\n')
                f.write(str(ig))
                f.write('\n\n')
                f.write(str(dir))
                f.write('\n\n')
                f.write(str(mail))
                f.write('\n\n')
                f.write(str(name))
                f.write('\n\n')


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
            #transforma el doc principar html para leer despues en archivos
            parsed = html.fromstring(home)
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            
            #print(links_to_notices)

            #today = datetime.date.today().strftime('%d-%m-%Y')


            """if not os.path.isdir(today):
                os.mkdir(today)
            """
            with open('copy.txt', 'w', encoding='utf-8') as f:
                for link in links_to_notices:
                    parse_notice(link,f)
               

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def run():
    parse_home()
    

if __name__ == "__main__":
    run()