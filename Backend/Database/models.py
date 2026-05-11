from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, FLOAT
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

engine = create_engine('sqlite:///crm.db')
Session = sessionmaker(bind=engine)
session = Session()
base = declarative_base()


class Usuario(base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)
    admin = Column(Boolean, default=False)
    
    def __init__(self, nome, email, senha, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.admin = admin


base.metadata.create_all(bind=engine)