import sqlalchemy
from select import select
from sqlalchemy import Column, create_engine, inspect, select, func, Float, Numeric
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.orm import relationship

Base = declarative_base()

class Cliente(Base):
    __tablename__ = "cliente"
    # atributos
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    cpf = Column(String)
    endereco = Column(String)

    conta = relationship(
        "Conta", back_populates="cliente", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Cliente(id={self.id}, nome={self.nome}, cpf={self.cpf}, endereco={self.endereco})"

class Conta(Base):
    __tablename__ = "conta"
    id = Column(Integer, primary_key=True)
    tipo = Column(String)
    agencia = Column(String)
    num = Column(String)
    saldo = Column(Numeric)
    id_cliente = Column(Integer, ForeignKey("cliente.id"), nullable=False)

    cliente = relationship("Cliente", back_populates="conta")

    def __repr__(self):
        return f"Conta(id={self.id}, tipo={self.tipo}, agencia={self.agencia}, num={self.num}, saldo={self.saldo})"

print(Cliente.__tablename__)
print(Conta.__tablename__)

# conexão com o banco de dados
engine = create_engine("sqlite://")

# criando as classes como tabelas no banco de dados
Base.metadata.create_all(engine)

inspetor_engine = inspect(engine)
print(inspetor_engine.has_table("cliente"))

print(inspetor_engine.get_table_names())
print(inspetor_engine.default_schema_name)

with Session(engine) as session:
    charles = Cliente(
        nome='charles',
        cpf='25436514521',
        endereco='Av. Juscelino Kubitscheck',
        conta=[Conta(tipo="Corrente",
                     agencia="2548-5",
                     num="26806-0",
                     saldo = 10.000)
               ]
    )

    erika = Cliente(
        nome='erika',
        cpf='25436547854',
        endereco='Av. Juscelino Kubitscheck',
        conta=[Conta(tipo="Poupança",
                     agencia="2548-5",
                     num="26806-0",
                     saldo=10.000)
               ]
    )

    fernanda = Cliente(
        nome='fernanda',
        cpf='25478436541',
        endereco='Av. Juscelino Kubitscheck',
        conta=[Conta(tipo="Poupança",
                     agencia="2548-5",
                     num="26806-0",
                     saldo=10.000)
               ]
    )

    # enviando para o BD (persistência de dados)
    session.add_all([charles, erika, fernanda])

    session.commit()

stmt = select(Cliente).where(Cliente.nome.in_(["charles", "fernanda"]))
print("Recuperando usuários a partir de condições de filtragem")
for cliente in session.scalars(stmt):
    print(cliente)

stmt_conta = select(Conta).where(Conta.id.in_([2]))
print("Recuperando as contas")
for conta in session.scalars(stmt_conta):
    print(conta)

stmt_order = select(Cliente).order_by(Cliente.nome.asc())
print("\n Recuperando info de maneira ordenada")
for result in session.scalars(stmt_order):
    print(result)

stmt_join = select(Cliente.nome, Cliente.cpf, Conta.tipo, Conta.agencia, Conta.num, Conta.saldo).join_from(Conta, Cliente)
print("\n")
for result in session.scalars(stmt_join):
    print(result)

connection = engine.connect()
results = connection.execute(stmt_join).fetchall()
print("\nExecutando statment a partir da connection")
for result in results:
    print(result)

stmt_count = select(func.count('*')).select_from(Cliente)
print("Total de instâncias em clientes")
for result in session.scalars(stmt_count):
    print(result)