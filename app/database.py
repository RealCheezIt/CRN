import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from app.config import Config

DB_PATH = Config.DATABASE_PATH

def init_db():
    """앱 시작할 때 딱 한 번 호출해서 테이블 만드는 함수"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        pw TEXT NOT NULL
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS notes (
        idx INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        title TEXT NOT NULL,
        category TEXT,
        content TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tags (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS note_tags (
        note_id INTEGER,
        tag_id INTEGER,
        FOREIGN KEY(note_id) REFERENCES notes(idx),
        FOREIGN KEY(tag_id) REFERENCES tags(id),
        PRIMARY KEY(note_id, tag_id))
        ''')
    conn.commit()
    conn.close()


def register_user(user_id, user_pw):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    hashed_pw = generate_password_hash(user_pw)  # ← 여기서 해싱
    try:
        cursor.execute('INSERT INTO users (id, pw) VALUES (?, ?)', (user_id, hashed_pw))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # 아이디 중복
    finally:
        conn.close()


def check_login(user_id, user_pw):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id=?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user is None:
        return False
    return check_password_hash(user[1], user_pw)  # user[1] = pw 컬럼(해시값)


def save_note(user_id, title, category, content):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO notes (user_id, title, category, content)
    VALUES (?, ?, ?, ?)
    ''', (user_id, title, category, content))
    conn.commit()
    conn.close()


def get_my_notes(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_note_by_id(note_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes WHERE idx = ?", (note_id,))
    row = cursor.fetchone()
    conn.close()
    return row


def update_note(note_id, user_id, title, category, content):  # edit_note → update_note로 변경
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE notes
    SET title = ?, category = ?, content = ?
    WHERE idx = ? AND user_id = ?
    ''', (title, category, content, note_id, user_id))
    conn.commit()
    conn.close()

def delete_note(note_id, user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM notes WHERE idx=? AND user_id=?', (note_id, user_id))
    conn.commit()
    conn.close()



def get_or_create_tag(cursor, tag_name):
    """연결을 새로 열지 않고, 밖에서 받은 cursor를 그대로 씀"""
    cursor.execute('SELECT id FROM tags WHERE name = ?', (tag_name,))
    row = cursor.fetchone()
    if row:
        return row[0]
    cursor.execute('INSERT INTO tags (name) VALUES (?)', (tag_name,))
    return cursor.lastrowid


def save_note_tags(note_id, tag_names):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    for name in tag_names:
        name = name.strip()
        if not name:
            continue
        tag_id = get_or_create_tag(cursor, name)   # ← 같은 cursor 넘겨줌
        cursor.execute(
            'INSERT OR IGNORE INTO note_tags (note_id, tag_id) VALUES (?, ?)',
            (note_id, tag_id)
        )
    conn.commit()
    conn.close()


def get_tags_for_note(note_id):
    """노트 하나에 붙은 태그 이름들 리스트로 리턴"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT tags.name FROM tags
        JOIN note_tags ON tags.id = note_tags.tag_id
        WHERE note_tags.note_id = ?
    ''', (note_id,))
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]


def clear_note_tags(note_id):
    """노트 수정 시 기존 태그 연결 다 지우고 새로 붙이기 위한 초기화"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM note_tags WHERE note_id = ?', (note_id,))
    conn.commit()
    conn.close()

def get_last_note_id(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        

        'SELECT idx FROM notes WHERE user_id = ? ORDER BY idx DESC LIMIT 1', (user_id,)
    )
    


    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None
