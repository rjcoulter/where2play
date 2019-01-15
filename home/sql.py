import psycopg2

def execute_sql_return(sql_statement):
    conn = None
    result = None
    
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect(host="ec2-54-227-249-201.compute-1.amazonaws.com",database="d16og879vkngbj", user="wkwzplprcpgmml", password="18c147f5bd6be4aa905ebaa44fb63b04f490e3a64307d7ba3fe84aa54a723c7f")
       
        # create a new cursor
        cur = conn.cursor()
        
        # fetch data
        cur.execute(sql_statement)
        result = cur.fetchall()

        # commit the changes to the database
        conn.commit()
        
        # close communication with the database
        cur.close()
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        
    finally:
        if conn is not None:
            conn.close()
            
    return result

def execute_sql(sql_statement):
    conn = None
    
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect(host="ec2-54-227-249-201.compute-1.amazonaws.com",database="d16og879vkngbj", user="wkwzplprcpgmml", password="18c147f5bd6be4aa905ebaa44fb63b04f490e3a64307d7ba3fe84aa54a723c7f")
       
        # create a new cursor
        cur = conn.cursor()
        
        # fetch data
        cur.execute(sql_statement)

        # commit the changes to the database
        conn.commit()
        
        # close communication with the database
        cur.close()
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        
    finally:
        if conn is not None:
            conn.close()