from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 
import requests
import tabula
import os
from zipfile import ZipFile

driver = webdriver.Chrome()

#acessa o site
driver.get("https://www.gov.br/ans/pt-br/assuntos/prestadores/padrao-para-troca-de-informacao-de-saude-suplementar-2013-tiss")

#Busca versão mais recente
link = driver.find_element(By.LINK_TEXT, "Clique aqui para acessar a versão Novembro/2021")
link.click()

try:
    #comando para clicar no botão "Visualizar" que direciona ao PDF
    element = driver.find_element(By.XPATH, '//*[@id="parent-fieldname-text"]/div/table/tbody/tr[1]/td[3]/a')

    driver.execute_script("arguments[0].click();", element)

    #armazena o endereço do pdf em uma var
    file_url = "https://www.gov.br/ans/pt-br/arquivos/assuntos/prestadores/padrao-para-troca-de-informacao-de-saude-suplementar-tiss/padrao-tiss/padrao-tiss_componente-organizacional_202111.pdf"
    
    #Baixa o componente organizacional (pdf)
    r = requests.get(file_url, stream = True)

    with open("padrao_tiss_padrao_tiss_componente-organizacional_202111.pdf","wb") as pdf:
        for chunk in r.iter_content(chunk_size=1024):
 
            if chunk:
                pdf.write(chunk)

    #Variavel recebe o nome do arquivo
    pdf = "padrao_tiss_padrao_tiss_componente-organizacional_202111.pdf"
    
    #declara as páginas que contem as tabelas desejadas
    dfs = tabula.read_pdf(pdf, pages=[114, 115, 116, 117, 118, 119, 120])

    #cria o arquivo zip
    zipObj = ZipFile('Teste_LeonardoSoares.zip', 'w')
    
    #Extrai as tabelas desejadas e manda para o .zip
    for i in range(len(dfs)):
        dfs[i].to_csv(f"arquivo_{i}.csv")
        zipObj.write(f"arquivo_{i}.csv")
        
    

except: 
    driver.quit()