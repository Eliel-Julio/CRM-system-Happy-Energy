from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, FLOAT, JSON
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

engine = create_engine('sqlite:///Backend/Database/crm.db')
Session = sessionmaker(bind=engine)
session = Session()
base = declarative_base()

class kit(base):
    __tablename__ = 'kits'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    preco_c = Column(FLOAT, nullable=False)
    n_modulos = Column(Integer, default=0)
    p_modulos = Column(FLOAT, default=0.0)
    inversor = Column(String, default=False)
    
    def __init__(self, nome, descricao, preco_c, n_modulos=0, inversor=False, p_modulos=0.0):
        self.nome = nome
        self.descricao = descricao
        self.preco_c = preco_c
        self.n_modulos = n_modulos
        self.inversor = inversor
        self.p_modulos = p_modulos

class cliente(base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False)
    telefone = Column(String, nullable=False)
    cidade_UF = Column(String, nullable=False)
    
    def __init__(self, nome, cpf, email, telefone, cidade_UF):
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.telefone = telefone
        self.cidade_UF = cidade_UF

class proposta(base):
    __tablename__ = 'propostas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    kit = Column(JSON, ForeignKey('kits.id'), nullable=False)
    valor_total = Column(FLOAT, nullable=False)
    
    cliente = relationship("cliente")
    kit = relationship("kit")
    
    def __init__(self, cliente_id, kit_id):
        self.cliente_id = cliente_id
        self.kit = self.kit_data(kit_id)
        self.valor_total = self.Def_valor_total()

    def Def_valor_total(self):
        return (self.kit.preco_c + (self.kit.n_modulos * 60) + 350)*1.3*1.07

    def kit_data(id):
        kit = session.query(kit).filter_by(id=id).first()
        if kit:
            return {
                "id": kit.id,
                "nome": kit.nome,
                "descricao": kit.descricao,
                "preco_c": kit.preco_c,
                "n_modulos": kit.n_modulos,
                "p_modulos": kit.p_modulos,
                "inversor": kit.inversor
            }
        return KeyError("Kit não encontrado")

base.metadata.create_all(bind=engine)