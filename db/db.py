
from vk.vkuser import VKUser


def create_base(conn):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS label_base(
        label_id INTEGER PRIMARY KEY,
        name_label VARCHAR(100));
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS candidate_base(
        vk_id INTEGER PRIMARY KEY UNIQUE,
        name_lastname VARCHAR(100) NOT NULL,
        label_id INTEGER REFERENCES label_base(label_id))
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS photo_base(
        photo_id SERIAL PRIMARY KEY,
        photo INTEGER NOT NULL,
        vk_id INTEGER REFERENCES candidate_base(vk_id));
        """)


def candidates_upload(conn, data):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO candidate_base(vk_id, name_lastname, label_id)
        VALUES(%s, %s, %s)
        RETURNING vk_id;
        """, (data['user_id'], data['user_name'], 1))
        return cur.fetchone()[0]


def add_label(conn, names_label):
    for i, j in enumerate(names_label):
        with conn.cursor() as cur:
            cur.execute(""" 
            INSERT INTO label_base(label_id , name_label) VALUES (%s,%s);
            """, (i+1, j))


def photo_upload(conn, photo, vk_id):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO photo_base(photo, vk_id)
        VALUES(%s, %s)
        RETURNING  photo, vk_id;
        """, (photo['photo'], vk_id))


def bot_request(conn):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT cb.name_lastname, cb.vk_id, pb.photo FROM candidate_base cb LEFT JOIN 
        photo_base pb ON pb.vk_id=cb.vk_id
        WHERE label_id = %s;
        """, (1, ))
        return cur.fetchmany(3)


def get_list_elect(conn):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT name_lastname, vk_id FROM candidate_base WHERE label_id = %s;
        """, (3, ))
        return cur.fetchall()


def delete_data(conn):
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM photo_base;
        DELETE FROM candidate_base;
        DELETE FROM label_base
        """)


def get_data(conn):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT FROM photo_base;
        SELECT FROM candidate_base;
        SELECT FROM label_base
        """)
        return cur.fetchone()


def update_label_2(conn, id):
    with conn.cursor() as cur:
        cur.execute("""
        UPDATE candidate_base SET label_id = %s WHERE vk_id = %s;
        """, (2, id))
        conn.commit()


def update_label_3(conn, id):
    with conn.cursor() as cur:
        cur.execute("""
        UPDATE candidate_base SET label_id = %s WHERE  vk_id = %s;
        """, (3, id))
        conn.commit()


def bd_data(conn, token, id):
    create_base(conn)
    names_label = ['Отсутствует', 'Пропустить', 'Избранное']
    vk = VKUser(token, id)
    data_db = vk.get_list_users()
    if get_data(conn) is None:
        add_label(conn, names_label)
        for data in data_db:
            d_id = candidates_upload(conn, data)
            for i in data['photos']:
                photo_upload(conn, i, d_id)
    else:
        delete_data(conn)
        add_label(conn, names_label)
        for data in data_db:
            d_id = candidates_upload(conn, data)
            for i in data['photos']:
                photo_upload(conn, i, d_id)
