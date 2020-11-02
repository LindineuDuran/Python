import sqlite3

conn = sqlite3.connect("ColecaoMusicas.db")

cursor = conn.cursor()

# cria uma tabela
cursor.execute("""CREATE TABLE albuns (title text, artist text, release_date text,
               publisher text, media_type text)""")

# insere alguns dados
cursor.execute("INSERT INTO albuns VALUES('Glow','Andy Hunter','7/24/2012', 'Xplore Records','MP3')")

# salva dados no banco
conn.commit()

# insere múltiplos registros de uma só vez usando o método "?", que é mais seguro
albums = [('Exodus', 'Andy Hunter', '7/9/2002', 'Sparrow Records', 'CD'),
('Until We Have Faces', 'Red', '2/1/2011', 'Essential Records', 'CD'),
('The End is Where We Begin', 'Thousand Foot Krutch', '4/17/2012', 'TFKmusic', 'CD'),
('The Good Life', 'Trip Lee', '4/10/2012', 'Reach Records', 'CD')]
cursor.executemany("INSERT INTO albuns VALUES (?,?,?,?,?)", albums)

# salva dados no banco
conn.commit()

# lista todos os registros na tabela
print("\nAqui a lista de todos os registros na tabela:\n")
for row in cursor.execute("SELECT rowid, * FROM albuns ORDER BY artist"):
    print(row)

# atualizando registros
sql = """
UPDATE albuns
SET artist = 'John Doe'
WHERE artist = 'Andy Hunter'
"""
cursor.execute(sql)
conn.commit()

# apaga registros
sql = """
DELETE FROM albuns
WHERE artist = 'John Doe'
"""
cursor.execute(sql)
conn.commit()
