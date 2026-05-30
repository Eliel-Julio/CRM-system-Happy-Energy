import render

if __name__ == "__main__":
    dados={
    "id": 5,
     "nome": "Jailson",
    "endereco": "",
    "descricao": "24 MÓDULO FOTOVOLTAICO 615 Wp - WEG BIFACIAL \n01 INVERSOR FOTOVOLTAICO SIW200G M105 W1, Inversor Monofásico 220 V \nESTRUTURA DE FIXAÇÃO LAJE \nKIT COMPLETO DE INSTALAÇÃO",
    "data": "2026-04-30",
    "telefone": "",
    "email": "",
    "potencia_kit": 14.76,
    "cidade-uf":"Petrolina",
    "CONSTS": {
        "CONST_IRRAD": 139,
        "CONST_FATOR_DIURNO": 0.5,
        "CONST_TUSDgd": 0.2,
        "CRECIMENTO_ANUAL_CONSUMO": 0.2,
        "DECRESCIMO_GERACAO": 0.0081,
        "TARIFA_INICIAL": 1.22,
        "TARIFA_INFLACAO_ANUAL": 0.08,
        "MANUTENCAO_INFLACAO_ANUAL": 0.03
    },
    "valor": 32767.62,
    "garantias": {"painel": "12 anos", "inversor": "10 anos", "estrutura": "10 anos", "instalacao": "1 ano"},
    "prazo_instalacao": 60,
    "forma_pagamento": "",
    "condicao_pagamento": "",
    "retorno_investimento": "1 ano e 3 meses",
    "modulos": {"potencia": 615 , "marca": "WEG", "modelo": "615 Wp - WEG BIFACIAL", "quantidade": 24, "area": 2.39*1.14},
    "inversor":{"potencia": 10.5, "marca": "WEG", "modelo": "SIW200G M105 W1", "quantidade": 1, "tipo": "Monofásico 380 V"},
    "estrutura": {"tipo": "Laje", "marca": "WEG", "quantidade": 24},
    "CONSUMO_MES_INICIAL": 24*615*0.139*0.8,
    "validade_proposta": "30 dias"
    }
    render.render_proposta(dados).save()
    # print(render.tousand_separator(8167.20))