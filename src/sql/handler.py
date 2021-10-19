import sqlite3

def print_table(tb, cursor, name):
    cursor.execute("SELECT * FROM %s" % name)
    tb.commit()
    results = cursor.fetchall()

    widths = []
    columns = []
    tavnit = '|'
    separator = '+'
    index = 0

    for cd in cursor.description:
        max_col_length = max(list(map(lambda x: len(str(x[index])), results)))
        widths.append(max(max_col_length, len(cd[0])))
        columns.append(cd[0])
        index += 1

    for w in widths:
        tavnit += " %-"+"%s.%ss |" % (w,w)
        separator += '-'*w + '--+'

    print(separator)
    print(tavnit % tuple(columns))
    print(separator)
    for row in results:
        print(tavnit % row)
    print(separator)

def try_drop_table(cursor, tb_name):
    cursor.execute('SELECT count(name) FROM sqlite_master WHERE type=\'table\' AND name=\'%s\'' % tb_name)
    if cursor.fetchone()[0] == 1:
        print('DROP TABLE :%s' % tb_name)
        cursor.execute('DROP TABLE %s' % tb_name)

def add_dish_type(cursor, type_name):
    cursor.execute('INSERT INTO DishType (Name) VALUES (\'%s\')' % type_name)



con = sqlite3.connect('example.db')
cursor = con.cursor()

try_drop_table(cursor, 'DishType')
try_drop_table(cursor, 'Menu')

# Create table
cursor.execute('''CREATE TABLE DishType (
                DishTypeId  INTEGER     NOT NULL PRIMARY KEY,
                Name        text        NOT NULL
            )''')

# Create table
cursor.execute('''CREATE TABLE Menu (
                DishId      INTEGER     NOT NULL    PRIMARY KEY,
                DishType    INTEGER     NOT NULL,
                Name        text        NOT NULL,
                ShortName   text        NOT NULL,
                cost        INTEGER     NOT NULL,
                FOREIGN KEY (DishType) REFERENCES DishType (DishTypeId)
            )''')

# Insert a row of data
add_dish_type(cursor, 'ПервоеБлюдю')
add_dish_type(cursor, 'Гарнир')


# Save (commit) the changes
con.commit()

print_table(con, cursor, 'DishType')

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
con.close()