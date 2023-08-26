import utils

def connect_to_database(name='database.db'):
	import sqlite3
	return sqlite3.connect(name, check_same_thread=False)

def init_db(connection):
	cursor = connection.cursor()

	cursor.execute('''
		CREATE TABLE IF NOT EXISTS users (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			username TEXT NOT NULL UNIQUE,
			password TEXT NOT NULL,
			balance REAL NOT NULL DEFAULT 0.0
		)
	''')

	connection.commit()


def add_user(connection, username, password):
    cursor = connection.cursor()
    hashed_password = utils.hash_password(password)
    query = '''INSERT INTO users (username, password) VALUES (?, ?)'''
    cursor.execute(query, (username, hashed_password))
    connection.commit()

def get_user(connection, username):
    cursor = connection.cursor()
    query = '''SELECT * FROM users WHERE username = ?'''
    cursor.execute(query, (username,))
    return cursor.fetchone()


def get_all_users(connection):
	cursor = connection.cursor()
	query = 'SELECT * FROM users'
	cursor.execute(query)
	return cursor.fetchall()

def seed_admin_user(connection):
    admin_username = 'admin'
    admin_password = 'admin'

    # Check if admin user exists
    admin_user = get_user(connection, admin_username)
    if not admin_user:
        add_user(connection, admin_username, admin_password)
        print("Admin user seeded successfully.")

def init_gadget_table(connection):
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gadgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            image_url TEXT,
            is_sold BOOLEAN DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    connection.commit()


def add_gadget(connection, user_id, title, description, price, image_url=None):
    cursor = connection.cursor()
    query = '''INSERT INTO gadgets (user_id, title, description, price, image_url) VALUES (?, ?, ?, ?, ?)'''
    cursor.execute(query, (user_id, title, description, price, image_url))
    connection.commit()

#*****************************************************************
# A function that checks if the item is sold 
def is_gadget_sold(connection, gadget_id):
    cursor = connection.cursor()
    query = '''SELECT is_sold FROM gadgets WHERE id = ?'''
    cursor.execute(query, (gadget_id,))
    return cursor.fetchone()[0]
#***************************************************************** 

def get_gadget(connection, gadget_id):
    cursor = connection.cursor()
    query = '''SELECT * FROM gadgets WHERE id = ?'''
    cursor.execute(query, (gadget_id,))
    return cursor.fetchone()

def get_user_gadgets(connection, user_id):
    cursor = connection.cursor()
    query = '''SELECT * FROM gadgets WHERE user_id = ?'''
    cursor.execute(query, (user_id,))
    return cursor.fetchall()

def get_all_gadgets(connection):
    cursor = connection.cursor()
    query = '''SELECT * FROM gadgets'''
    cursor.execute(query)
    return cursor.fetchall()

def mark_gadget_as_sold(connection, gadget_id):
    cursor = connection.cursor()

    # Retrieve gadget information
    gadget_query = '''SELECT price, user_id FROM gadgets WHERE id = ?'''
    cursor.execute(gadget_query, (gadget_id,))
    gadget_data = cursor.fetchone()

    if gadget_data:
        gadget_price, user_id = gadget_data

        # Update gadget as sold
        update_query = '''UPDATE gadgets SET is_sold = 1 WHERE id = ?'''
        cursor.execute(update_query, (gadget_id,))
        connection.commit()

        # Update owner's balance
        update_balance_query = '''UPDATE users SET balance = balance + ? WHERE id = ?'''
        cursor.execute(update_balance_query, (gadget_price, user_id))
        connection.commit()


def init_comments_table(connection):
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gadget_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            text TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (gadget_id) REFERENCES gadgets (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    connection.commit()
    

def add_comment(connection, gadget_id, user_id, text):
    cursor = connection.cursor()
    query = '''INSERT INTO comments (gadget_id, user_id, text) VALUES (?, ?, ?)'''
    cursor.execute(query, (gadget_id, user_id, text))
    connection.commit()

def get_comments_for_gadget(connection, gadget_id):
    cursor = connection.cursor()
    query = '''
        SELECT  users.username, comments.text, comments.timestamp
        FROM comments
        JOIN users ON comments.user_id = users.id
        WHERE comments.gadget_id = ?
    '''
    cursor.execute(query, (gadget_id,))
    return cursor.fetchall()