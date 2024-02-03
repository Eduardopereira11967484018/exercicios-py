import PySimpleGUI as sg
import os
import sqlite3

# Set the current directory to the script's directory
diretorio_corrente = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(diretorio_corrente, 'database.db')

# Establish a connection to the SQLite database
conexao = sqlite3.connect(db_path)
query = '''CREATE TABLE IF NOT EXISTS PRODUCT (LOTE CHAR(10), PRODUTO TEXT, FORNECEDOR TEXT)'''
conexao.execute(query)
conexao.close()

dados = []
Titulos = ['lotes', 'produto', 'fornecedor']

layout = [
    [sg.Text(Titulos[0]), sg.Input(size=5, key=Titulos[0])],
    [sg.Text(Titulos[1]), sg.Input(size=20, key=Titulos[1])],
    [sg.Text(Titulos[2]), sg.Combo(['fornecedor 1', 'fornecedor 2', 'fornecedor 3'], key=Titulos[2])],
    [sg.Button('Adicionar'), sg.Button('Editar'), sg.Button('Salvar', disabled=True), sg.Button('Excluir'), sg.Exit('Sair')],
    [sg.Table(values=dados, headings=Titulos, auto_size_columns=False, justification='right', key='tabela')]
]

Window = sg.Window('Sistema de gerenciamento', layout)

while True:
    event, values = Window.read()

    if event == sg.WIN_CLOSED or event == 'Sair':
        break

    if event == 'Adicionar':
        new_data = [values[Titulos[0]], values[Titulos[1]], values[Titulos[2]]]
        dados.append(new_data)
        Window['tabela'].update(values=dados)

        # Insert new data into the database
        conexao = sqlite3.connect(db_path)
        conexao.execute("INSERT INTO PRODUCT (LOTE, PRODUTO, FORNECEDOR) VALUES (?,?,?)", new_data)
        conexao.commit()
        conexao.close()

    if event == 'Editar':
        selected_row = values['tabela'][0]
        if not selected_row:
            sg.popup('No row selected')
        else:
            sg.popup('Edit selected row')
            for i in range(3):
                Window[Titulos[i]].update(value=dados[selected_row][i])
            Window['Salvar'].update(disabled=False)

    if event == 'Salvar':
        edited_row = values['tabela'][0]
        dados[edited_row] = [values[Titulos[0]], values[Titulos[1]], values[Titulos[2]]]
        Window['tabela'].update(values=dados)
        for i in range(3):
            Window[Titulos[i]].update(value='')
        Window['Salvar'].update(disabled=True)

        # Update data in the database
        conexao = sqlite3.connect(db_path)
        conexao.execute("UPDATE PRODUCT SET PRODUTO = ? WHERE LOTE = ?", (values[Titulos[1]], values[Titulos[0]]))
        conexao.commit()
        conexao.close()

    if event == 'Excluir':
        selected_row = values['tabela'][0]
        if not selected_row:
            sg.popup('No row selected')
        else:
            if sg.popup_ok_cancel('This operation cannot be undone') == 'OK':
                # Delete data from the database
                conexao = sqlite3.connect(db_path)
                conexao.execute("DELETE FROM PRODUCT WHERE LOTE = ?", (values[Titulos[0]],))
                conexao.commit()
                conexao.close()

                del dados[selected_row]
                Window['tabela'].update(values=dados)

Window.close()
