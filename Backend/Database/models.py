from pathlib import Path
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, FLOAT, JSON, Enum
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime as dt

# Garantir que o arquivo sqlite `crm.db` seja criado no mesmo diretório deste arquivo
_db_file = Path(__file__).resolve().parent / "crm.db"
engine = create_engine(f"sqlite:///{_db_file.as_posix()}")
Session = sessionmaker(bind=engine)
session = Session()
base = declarative_base()

def produto(list:list, t=1):
    for v in list:t*=v
    return t

class propriedade(base):
    __tablename__ = 'propriedades'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False, unique=True)
    valor = Column(String, nullable=False)
    tipo = Column(Enum('float', 'int', 'str', 'boolean'), nullable=False)

    def __init__(self, nome, valor, tipo):
        if tipo not in ('float', 'int', 'str', 'boolean'):
            raise KeyError(f"Incorect type description <<{tipo}>> , pleas entry on off ('float', 'int', 'str', 'boolean')")
        self.nome = nome
        self.tipo = tipo
        self.set_valor(valor)

    def __repr__(self):
        return f"<Propriedade(nome='{self.nome}', valor='{self.valor}', tipo='{self.tipo}')>"
    
    def set_valor(self, valor):
        match self.tipo:    
            case 'float':
                try:
                    self.valor = float(valor)
                    return self.valor
                except ValueError:
                    raise ValueError("Valor deve ser um número para tipo Float")
            case 'int':                
                try:
                    self.valor = int(valor)
                    return self.valor
                except ValueError:
                    raise ValueError("Valor deve ser um número para tipo Int")
            case 'str':                
                try:
                    self.valor = str(valor)
                    return self.valor
                except ValueError:
                    raise ValueError("Valor deve ser uma string para tipo Str")
            case 'boolean':                
                try:
                    self.valor = bool(valor)
                    return self.valor
                except ValueError:
                    raise ValueError("Valor deve ser um booleano para tipo Boolean")

class kit(base):
    __tablename__ = 'kits'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    preco_c = Column(FLOAT, nullable=False)
    modulos_json = Column(JSON, nullable=False)
    inversor_json = Column(JSON, nullable=False)
    estrutura_json = Column(JSON, nullable=False)
    garantias_json = Column(JSON, nullable=False)
    

    # "modulos": {"potencia": 610, "marca": "WEG", "modelo": "615 Wp - WEG BIFACIAL", "quantidade": 12, "area": 2.39*1.14},
    # "inversor":{"potencia": 5.0, "marca": "WEG", "modelo": "SIW 200G M050 W00"    , "quantidade": 1, "tipo": "Monofásico"},
    # "estrutura": {"tipo": "Fibrocimento", "marca": "WEG", "quantidade": 12},

    def __init__(self, nome, descricao, preco_c, modulos:dict, inversor:dict, estrutura:dict, garantias:dict):
        for key in ("potencia", "marca", "modelo", "quantidade", "tipo"):
            if key not in modulos.keys():raise KeyError(f"A chave obrigatória '{key}' está faltando no dicionário modulos!")
        for key in ("potencia","marca", "modelo", "quantidade"):
            if key not in inversor.keys():raise KeyError(f"A chave obrigatória '{key}' está faltando no dicionário inversor!")
        for key in ("tipo", "marca", "quantidade"):
            if key not in estrutura.keys():raise KeyError(f"A chave obrigatória '{key}' está faltando no dicionário estrutura!")
        for key in ("painel", "inversor", "estrutura", "instalacao"):
            if key not in garantias.keys():raise KeyError(f"A chave obrigatória '{key}' está faltando no dicionário garantias!")
        self.modulos_json = modulos
        self.inversor_json = inversor
        self.estrutura_json = estrutura
        self.garantias_json = garantias

        self.nome = nome
        self.descricao = descricao
        self.preco_c = preco_c

class cliente(base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False)
    telefone = Column(String, nullable=False)
    cidade_uf = Column(String, nullable=False)
    endereco = Column(String, nullable=True)

    def __init__(self, nome:String, cpf:String, email:String, telefone:String, cidade_uf:String, endereco:String):
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.telefone = telefone
        self.cidade_uf = cidade_uf
        self.endereco = endereco

class proposta(base):
    __tablename__ = 'propostas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    kit_id = Column(Integer, ForeignKey('kits.id'), nullable=False)
    valor_total = Column(FLOAT, nullable=False)
    data = Column(String, nullable=False)

    kit_json = Column(JSON, nullable=False)
    cliente_json = Column(JSON, nullable=False)
    consts = Column(JSON, nullable=False)

    cliente_rel = relationship("cliente")
    kit_rel = relationship("kit")

    prazoprazo_instalacao = Column(Integer,nullable=False)
    consdicao_pgto = Column(String,nullable=False)
    validade_proposta = Column(Integer,nullable=False)
    forma_pgto = Column(String,nullable=False)

    def __init__(self, cliente_id, kit_id,prazo_instalacao:int=60, consdicao_pgto:str='', validade_proposta:int=30,forma_pgto:str=''):
        self.kit_id = kit_id
        self.kit_json = self.kit_data(kit_id)

        self.cliente_id = cliente_id
        self.cliente_json = self.cliente_data(cliente_id)

        self.consts = {obj.nome:obj.valor for obj in session.query(propriedade).all()}
        self.valor_total = self.Def_valor_total()
        self.data = dt.today().strftime("%d/%m/%Y")

        self.prazoprazo_instalacao = prazo_instalacao
        self.consdicao_pgto = consdicao_pgto
        self.validade_proposta = validade_proposta
        self.forma_pgto = forma_pgto

    def Def_valor_total(self,instal=60, extra=350 , rates={"margim":0.3,"tax":0.07, "commission":0.00}):
        return (self.kit_json["preco_c"] + (self.kit_json["modulos_json"]["quantidade"] * instal) + extra)*produto([1+t for t in rates.values()])

    def cliente_data(self, id_):
        cliente_=session.query(cliente).filter_by(id=id_).first()
        if cliente_:
            c = cliente_.__dict__
            c.pop('_sa_instance_state',None)
            return c
        raise KeyError("Cliente não encontrado")

    def kit_data(self, id_):
        kit_ = session.query(kit).filter_by(id=id_).first()
        if kit_:
            k = kit_.__dict__
            k.pop('_sa_instance_state',None)
            return k
        raise KeyError("Kit não encontrado")

base.metadata.create_all(bind=engine)