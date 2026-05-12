from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, FLOAT
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

engine = create_engine('sqlite:///crm.db')
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
    cpf = Column(String, nullable=False, unique=True, maxlength=11, minlength=11)
    email = Column(String, nullable=False)
    telefone = Column(String, nullable=False)
    cidade_UF = Column(String, nullable=False)
    
    def __init__(self, nome, cpf, email, telefone, cidade_UF):
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.telefone = telefone
        self.cidade_UF = cidade_UF

base.metadata.create_all(bind=engine)