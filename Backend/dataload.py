from models import *
import pandas as pd

def data_load(file_route:str):
    df = pd.read_csv(file_route)
    for _, row in df.iterrows():
        kit1 = kit(
            nome=row['nome'],
            descricao=row['descricao'],
            preco_c=row['preco_c'],
            modulos={"potencia": row['modulos_potencia'], "marca": row['modulos_marca'], "modelo": row['modulos_modelo'], "quantidade": row['modulos_quantidade'], "tipo": "Bifacial"},
            inversor={"quantidade":1,"potencia": row['inversor_potencia'], "marca": row['inversor_marca'], "modelo": row['inversor_modelo']},
            estrutura={"tipo": row['estrutura_tipo'], "marca": row['estrutura_marca'], "quantidade": row['estrutura_quantidade']},
            garantias={"painel": "12 anos", "inversor": "10 anos", "estrutura": "10 anos","instalacao": "1 ano"}
        )
        session.add(kit1)
    session.commit()

file_route = r"C:\Users\happy\Desktop\DEV\CRM-system-Happy-Energy-PROD\Backend\Database\From_CRM_System.csv"
data_load(file_route)


# 'nome'
# 'descricao'
# 'preco_c'
# 'modulos_potencia'
# 'modulos_marca'
# 'modulos_modelo'
# 'modulos_quantidade'
# 'inversor_potencia'
# 'inversor_marca'
# 'inversor_modelo'
# 'estrutura_tipo'
# 'estrutura_marca'
# 'estrutura_quantidade'
