from sqlalchemy import text
from models import engine

def column_exists(conn, table, column):
	res = conn.execute(text(f"PRAGMA table_info('{table}')")).fetchall()
	cols = [r[1] for r in res]
	return column in cols

def run():
	with engine.connect() as conn:
		# Checar e adicionar pricing_variables
		if not column_exists(conn, 'propostas', 'pricing_variables'):
			print('Adicionando coluna pricing_variables...')
			conn.execute(text("ALTER TABLE propostas ADD COLUMN pricing_variables TEXT NOT NULL DEFAULT '{""instal_mod"": 60, ""extra"": 350}'"))
		else:
			print('Coluna pricing_variables já existe.')

		# Checar e adicionar rates
		if not column_exists(conn, 'propostas', 'rates'):
			print('Adicionando coluna rates...')
			conn.execute(text("ALTER TABLE propostas ADD COLUMN rates TEXT NOT NULL DEFAULT '{""margim"": 0.3, ""tax"": 0.07, ""commission"": 0.0}'"))
		else:
			print('Coluna rates já existe.')

		# Mostrar colunas atuais
		cols = conn.execute(text("PRAGMA table_info('propostas')")).fetchall()
		print('Colunas atuais em propostas:')
		for c in cols:
			print('-', c[1])


if __name__ == '__main__':
	run()

