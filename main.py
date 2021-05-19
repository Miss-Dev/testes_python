from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re

from pathlib import Path
import requests


# pages = set()
# para o caso de gerar números aleatórios
# random.seed(datetime.datetime.now())


# obter links internos do site
def getLinks(bs, url):
    url = '{}://{}'.format(urlparse(url).scheme, urlparse(url).netloc)
    linksInternos = []

    for link in bs.find_all('a', href=re.compile('^(/|.*' + url + ')')):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in linksInternos:
                if link.attrs['href'].startswith('/'):
                    linksInternos.append(url + link.attrs['href'])
                else:
                    linksInternos.append(link.attrs['href'])
    return linksInternos


def getPDF(bs, url):
    url = '{}://{}'.format(urlparse(url).scheme, urlparse(url).netloc)
    pdf = ''
    for link in bs.find_all('a', href=re.compile('^(/|.*' + url + ')')):
        if link.attrs['href'] is not None:
            if link.attrs['href'].startswith('/') and link.attrs['href'].endswith('.pdf'):
                pdf = url + link.attrs['href']
                break
    return pdf


# obter link em que o arquivo componente organizacional mais recente se encontra
def getLinkprincipal(lista, final):
    link_princ = ["Link principal"]
    for i in lista:
        if i.endswith(final):
            link_princ.append(i)
            break
    return link_princ


if __name__ == '__main__':
    link = "http://www.ans.gov.br/prestadores/tiss-troca-de-informacao-de-saude-suplementar"
    html = urlopen(link)
    bs = BeautifulSoup(html, 'html.parser')
    try:
        coletor = getLinks(bs, link)
        link_princ = getLinkprincipal(coletor, '2021')
        html = urlopen(link_princ[1])
        bs = BeautifulSoup(html, 'html.parser')
        pdf_link = getPDF(bs, link_princ[1])

        filename = Path('arquivo_componente_organizacional.pdf')

        response = requests.get(pdf_link)
        filename.write_bytes(response.content)

    except:
        print("Ocorreu um erro!")

    print(link_princ)
    print(pdf_link)
