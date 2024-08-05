import psycopg2


def get_balances():
    conn = psycopg2.connect(database="postgres",
                        host="aws-0-sa-east-1.pooler.supabase.com",
                        user="postgres.yuduhfwulcdmflcsinwp",
                        password="DevGenius@123",
                        port="6543")

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM balances")
    balances = cursor.fetchall()
    conn.close()
    return balances

