import smtplib
import pandas as pd
import pyodbc
import os
import time 
from email.message import EmailMessage

#Database Credentials
server = r'DESKTOP-RK8PG4R\SQLSERVER'
database = os.getenv('database')
username = os.getenv('username')
password = os.getenv('password')

#Sender Email Credentials
login_mail = os.getenv('usermail')
password_mail = os.getenv('passmail')
email_sender = "sender@outlook.com"
#-----------------------------------------------------------------------------------------------------------------------------------------------
#Conecting to database
connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = connection.cursor()

#Querying
dados = cursor.execute("""SELECT * FROM VENDAS""")

#Fetching records
dataframe = pd.DataFrame.from_records(dados.fetchall())

#Ranem Columns
dataframe.columns = ['Vendedor','Produto','Valor', 'Quantidade']


#Target mails
vendedor_email = {'Oselio':email_1,'Felipe':email_2}

#Complete excel file
dataframe.to_excel(r"C:\Users\Oselio\OneDrive\Área de Trabalho\Outputs\output.xlsx",sheet_name='Dados',index= None)

for items in vendedor_email.items():
    

    new_df = dataframe.loc[(dataframe.Vendedor == str(items[0]))]

    new_df.to_excel(r"C:\Users\Oselio\OneDrive\Área de Trabalho\Outputs\excel_output ("+str(items[0])+").xlsx",sheet_name='Dados',index= None)
    time.sleep(2)

    server  = smtplib.SMTP("smtp-mail.outlook.com",587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(login_mail,password_mail)

    msg = EmailMessage()
    msg['Subject'] = "Situação de Vendas"
    msg['From'] = email_sender
    msg['To'] = items[1]
    msg.set_content("""Bom dia! 
Segue anexo planilha com o analítico de vendas.
    """)

    with open(r"C:\Users\Oselio\OneDrive\Área de Trabalho\Outputs\excel_output ("+str(items[0])+").xlsx", 'rb') as f:
        file_data = f.read()
    msg.add_attachment(file_data, maintype="application", subtype="xlsx", filename="Vendas ("+str(items[0])+").xlsx")

    server.send_message(msg)