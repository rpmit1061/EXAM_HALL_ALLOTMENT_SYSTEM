import psycopg2
conn = psycopg2.connect("host=localhost dbname=gpcs user=postgres password=12345")
cur = conn.cursor()


def getenrollment_no(limit):
    cur.execute("SELECT enrollment_no FROM studentdata where paper_type='Theory'"
                " and replace(paper_code,'''' ,'' )=%s limit %s", [limit])
    rollnumber = cur.fetchall()
    return rollnumber