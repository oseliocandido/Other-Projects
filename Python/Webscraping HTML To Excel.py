import requests
import bs4
import pandas as pd
import re
import xlsxwriter
import time

response = requests.get(url = "https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops")
soup = bs4.BeautifulSoup(response.text,"lxml")

preco_lista = []
descricao_lista = []
review_lista = []

pattern_preco = re.compile(r"\d.\.\d{2}")
pattern_reviews = re.compile(r"\d.")

for objeto in soup.find_all("div",{"class": "col-sm-4 col-lg-4 col-md-4"}):
    div_maior = objeto.find("div",{"class": "thumbnail"})
    
    raw_preco = div_maior.find("div",{"class": "caption"}).h4.text
    raw_descricao = div_maior.find("div",{"class": "caption"}).p.text
    raw_reviews = div_maior.find("div",{"class": "ratings"}).p.text

    extracted_preco = pattern_preco.search(raw_preco).group(0)
    extracted_reviews = pattern_reviews.search(raw_reviews).group(0)

    preco_lista.append(extracted_preco)
    descricao_lista.append(raw_descricao)
    review_lista.append(extracted_reviews)

dataframe = pd.DataFrame({"Descricao":descricao_lista,"Precos":preco_lista,"Reviews":review_lista})
path = r"C:\Users\Oselio\OneDrive\Área de Trabalho\Web_Scraper\Scraped.xlsx"

writer = pd.ExcelWriter(path,engine = 'xlsxwriter')
dataframe.to_excel(writer, startrow = 0, sheet_name='Sheet1', index=False)

workbook = writer.book
worksheet = writer.sheets['Sheet1']
worksheet.set_column(0, 0, 140)
worksheet.add_table('A1:C118',{'header_row': False,'autofilter': True,'style': 'Table Style Light 16','name': 'Products'})

writer.save()