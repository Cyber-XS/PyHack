import argparse, pymysql, psycopg2

CREDENTIALS = [
    ("root", ""), ("root", "root"), ("mysql", "mysql"),
    ("postgres", "postgres"), ("postgres", ""), ("admin", "admin")
]

def mysql(host, port, user, password):
    try:
        pymysql.connect(host=host, port=port, user=user,
            passwd=password, connect_timeout=2,
            charset='latin1', ssl_disabled=True).close()
        return True
    except pymysql.MySQLError:
        return False

def postgres(host, port, user, password):
    try:
        psycopg2.connect(host=host, port=port, user=user, password=password, datbase="postgres", connect_timeout=2).close()
        return True
    except psycopg2.Error:
        return False

def main():
    p = argparse.ArgumentParser()
    p.add_argument("target", nargs="?", default="192.168.1.8")
    p.add_argument("--mysql-port", type=int, default=3306)
    p.add_argument("--postgres-port", type=int, default=5432)
    a = p.parse_args()

    print(f" [*] Target: {a.target} ")

    for name, port, test in [
        ("MySQL", a.mysql_port, mysql),
        ("Postgres", a.postgres_port, postgres)
    ]:

        print(f" \n [*] Testing {name} ")
        found = False

        for user, password in CREDENTIALS:
            if test(a.target, port, user, password):
                print(f" [+] {name}:{user}:{password} ")
                found = True

            if not found:
                print(f" [-] No {name} credential found ")

if __name__ == "__main__":
    main()
