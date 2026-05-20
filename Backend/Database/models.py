from pathlib import Path
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, FLOAT, JSON, Enum
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# Garantir que o arquivo sqlite `crm.db` seja criado no mesmo diretório deste arquivo
_db_file = Path(__file__).resolve().parent / "crm.db"
engine = create_engine(f"sqlite:///{_db_file.as_posix()}")
Session = sessionmaker(bind=engine)
session = Session()
base = declarative_base()

class propriedade(base):
    __tablename__ = 'propriedades'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    valor = Column(String, nullable=False)
    tipo = Column(Enum('float', 'int', 'str', 'boolean'), nullable=False)

    def __init__(self, nome, valor, tipo):
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
    kit = Column(JSON, nullable=False)
    kit_id = Column(Integer, ForeignKey('kits.id'), nullable=False)
    valor_total = Column(FLOAT, nullable=False)

    cliente = relationship("cliente")
    kit = relationship("kit")

    def __init__(self, cliente_id, kit_id):
        self.cliente_id = cliente_id
        self.kit = self.kit_data(kit_id)
        self.kit_id = kit_id
        self.valor_total = self.Def_valor_total()

    def Def_valor_total(self):
        return (self.kit.preco_c + (self.kit.n_modulos * 60) + 350)*1.3*1.07

    def kit_data(id):
        kit_ = session.query(kit).filter_by(id=id).first()
        if kit_:
            return {
                "id": kit_.id,
                "nome": kit_.nome,
                "descricao": kit_.descricao,
                "preco_c": kit_.preco_c,
                "n_modulos": kit_.n_modulos,
                "p_modulos": kit_.p_modulos,
                "inversor": kit_.inversor
            }
        raise KeyError("Kit não encontrado")

base.metadata.create_all(bind=engine)