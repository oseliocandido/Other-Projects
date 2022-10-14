import tkinter as tk
import psycopg2
from PIL import Image
import datetime
import dateutil
from dateutil.relativedelta import relativedelta
import time
import os

#INTERFACE GRÁFICA
def submit():
    global descritivo
    global categoria
    global pessoas
    global estabelecimento
    global valor_total
    global data_compra
    global parcelas
    global pagamento
    global vencimento

    descritivo = entry_descritivo.get()
    categoria = entry_categoria.get()
    pessoas = entry_pessoas.get()
    estabelecimento = entry_estabelecimento.get()
    valor_total = float(entry_valor_total.get())
    data_compra = entry_data_compra.get()
    parcelas = int(entry_parcelas.get())
    pagamento = entry_pagamento.get()
    vencimento = entry_data_vencimento.get()
    forms.destroy()

def clear_entry():
    entry_descritivo.delete(0,"end")
    entry_categoria.delete(0,"end")
    entry_pessoas.delete(0,"end")
    entry_estabelecimento.delete(0,"end")
    entry_valor_total.delete(0,"end")
    entry_parcelas.delete(0,"end")
    entry_pagamento.delete(0,"end")
    entry_data_compra.delete(0,"end")
    entry_data_vencimento.delete(0,"end")



#Inicio
forms = tk.Tk()
forms.title("Formulário")
forms.resizable(False,False)
forms.iconbitmap(r"C:\Users\Oselio\OneDrive\Dados\Frequente\Controle\Financeiro\ETL\Imagens\eita.ico")

#Resolução do monitor
x_resolution = forms.winfo_screenwidth()
y_resolution = forms.winfo_screenheight()

#Tamanho do formulário
width = 620
height = 400

#Inicio das coordenadas do formulário na tela
forms_x_pos = int(x_resolution / 2 - width / 2)
forms_y_pos = int(y_resolution / 2 - height / 2)

#Instanciação do formulária na tela
forms.geometry(f"{width}x{height}+{forms_x_pos}+{forms_y_pos}")



#Background
background = tk.Canvas(forms,height=400,width=620)
background.pack()


img = tk.PhotoImage(file=r"C:\Users\Oselio\OneDrive\Dados\Frequente\Controle\Financeiro\ETL\Imagens\background.png")
big_label = background.create_image((0,0),image=img,anchor="nw")

entry_color = "#ffffff"
fill_color = "#42e0ff"


#Parte esquerda do Canvas
background.create_text((12,95),text="Descritivo",font = "Arial 15",fill=fill_color,anchor="w")
background.create_text((12,185),text="Categoria",font = "Arial 15",fill=fill_color,anchor="w")
background.create_text((12,250),text="Pessoas",font = "Arial 15",fill=fill_color,anchor="w")
background.create_text((12,315),text="Estabelecimento",font = "Arial 15",fill=fill_color,anchor="w")

entry_descritivo = tk.Entry(forms,bg=entry_color)
entry_descritivo.place(relx=0.02,rely=0.27,relwidth=0.40,relheight=0.05)

entry_categoria = tk.Entry(forms,bg=entry_color)
entry_categoria.place(relx=0.02,rely=0.5,relwidth=0.22,relheight=0.05)

entry_pessoas = tk.Entry(forms,bg=entry_color)
entry_pessoas.place(relx=0.02,rely=0.65,relwidth=0.22,relheight=0.05)

entry_estabelecimento = tk.Entry(forms,bg=entry_color)
entry_estabelecimento.place(relx=0.02,rely=0.82,relwidth=0.22,relheight=0.05)


#Parte direita do Canvas
background.create_text((310,185),text="Valor Total",font = "Arial 15",fill=fill_color,anchor="w")
background.create_text((474,185),text="Parcelas",font = "Arial 15",fill=fill_color,anchor="w")
background.create_text((310,250),text="Pagamento",font = "Arial 15",fill=fill_color,anchor="w")
background.create_text((474,250),text="Data Compra",font = "Arial 15",fill=fill_color,anchor="w")
background.create_text((310,95),text="Data de Vencimento",font = "Arial 15",fill=fill_color,anchor="w")


entry_data_vencimento = tk.Entry(forms,bg=entry_color)
entry_data_vencimento.place(relx=0.5,rely=0.27,relwidth=0.30,relheight=0.05)

entry_valor_total = tk.Entry(forms,bg=entry_color)
entry_valor_total.place(relx=0.5,rely=0.5,relwidth=0.22,relheight=0.05)

entry_parcelas = tk.Entry(forms,bg=entry_color)
entry_parcelas.place(relx=0.76,rely=0.5,relwidth=0.22,relheight=0.05)

entry_pagamento = tk.Entry(forms,bg=entry_color)
entry_pagamento.place(relx=0.5,rely=0.65,relwidth=0.22,relheight=0.05)

entry_data_compra = tk.Entry(forms,bg=entry_color)
entry_data_compra.place(relx=0.76,rely=0.65,relwidth=0.22,relheight=0.05)

titulo = tk.Label(forms,
                    text="Formulário de Gastos",
                    bg = "black",
                    font = "Arial 20 bold",
                    fg = "white",
                    bd=5,relief = "solid")
titulo.place(x=0,y=0,relwidth=1,relheight=0.15)

button_submit = tk.Button(forms,command=submit,text = "Submit!",bg="#ffffff")
button_submit.place(relx=0.8,rely=0.8,relwidth=0.17,relheight=0.14)

button_clear = tk.Button(forms,command=clear_entry,text = "Clear",bg="#ffffff")
button_clear.place(relx=0.64,rely=0.8,relwidth=0.14,relheight=0.14)

forms.mainloop()
#-------------------------------------------------------------------------------------------------------------------
#ETL

#Data do Segundo Vencimento
if pagamento == "Crédito":
    vencimento_datetime_object =  datetime.datetime.strptime(vencimento, "%Y/%m/%d")
    delta_parcelas = relativedelta(months=+(parcelas-1))
    segundo_vencimento= vencimento_datetime_object + delta_parcelas


valor_parcela = float(valor_total / parcelas)




server = r'DESKTOP-RK8PG4R\SQLSERVER'
database = os.getenv('database')
username = os.getenv('username')
password = os.getenv('password')


#Conexão com dados e input de dados
con  = psycopg2.connect(dbname = database,user=username,password = password,host =database)
cursor = con.cursor()


#Inputar valores do app no banco de dados
cursor.execute("""INSERT INTO dim_desc_pagamento (
Descrição_Geral, 
Categoria,
Pessoas,
Estabelecimento ,
Valor_Total	,
Quantidade_de_Parcelas,
Valor_da_Parcela) VALUES 
    (%s, %s, %s, %s, %s, %s, %s)""",(descritivo,categoria,pessoas,estabelecimento,valor_total,parcelas,valor_parcela,))
cursor.execute("""INSERT INTO dim_data_compra (Data_da_compra) VALUES (%s)""", (data_compra,))
cursor.execute("""INSERT INTO dim_forma_pagamento (Pagamento) VALUES  (%s)""", (pagamento,))


#Pegar id_transacao
cursor.execute("""SELECT MAX(Id_Pagamento) FROM dim_associativa""")
max_id_pagamento = cursor.fetchone()[0]
first_pagamento  = int(max_id_pagamento) +1

#Pegar id_pagamento
cursor.execute("""SELECT MAX(Id_Transação) FROM dim_desc_pagamento""")
max_id_transacao = cursor.fetchone()[0]
first_transacao  = int(max_id_transacao)

#Pagamentos A Crédito
if pagamento == "Crédito":
    cursor.execute("""INSERT INTO dim_vencimentos (Id_Transação,Data_Primeira_Parcela,Data_Ultima_Parcela)  VALUES  (%s ,%s , %s)""", 
                        (str(first_transacao),str(vencimento),str(segundo_vencimento),))    
    for contador in range(0,parcelas):
        id_pagamento_add = contador + first_pagamento

        data_vencimento =  datetime.datetime.strptime(vencimento, "%Y/%m/%d")
        delta_parcela = relativedelta(months=+(contador))
        proximo_vencimento = str(data_vencimento + delta_parcela)


        cursor.execute("""INSERT INTO dim_associativa (Id_Pagamento,Id_Transação,Data_do_Pagamento) VALUES (%s, %s, %s)""", (id_pagamento_add,first_transacao,proximo_vencimento,))
        cursor.execute("""INSERT INTO fato_pagamentos (Id_pagamento,Valor_do_Pagamento) VALUES  (%s, %s)""", (id_pagamento_add,valor_parcela,))

#Débito
else:
        cursor.execute("""INSERT INTO dim_associativa (Id_Pagamento,Id_Transação,Data_do_Pagamento) VALUES (%s,%s,%s)""", 
                        (str(first_pagamento-1),first_transacao,data_compra))

        cursor.execute("""INSERT INTO fato_pagamentos (Id_pagamento,Valor_do_Pagamento) VALUES  (%s,%s)""",
                        (str(first_pagamento-1),valor_parcela))   

con.commit()

cursor.close()
con.close()