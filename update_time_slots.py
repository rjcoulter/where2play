import psycopg2
import datetime
import pytz

def initialize_slots():
    sql = "INSERT INTO home_facility(\"F_Name\", \"Location\", \"Description\", \"Facility_Hours\", \"Facility_Phone\", \"Parking_Hours\", \"F_Type\") VALUES(%s, %s, %s, %s, %s, %s, %s)"
    conn = None
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect(host="ec2-54-225-68-133.compute-1.amazonaws.com",database="d2ftb891msed9k", user="viuuwydegsjlob", password="f30715f358396a926ad0c5b4d6c526cdd14cbea1834c0523c7a711bae1739dde")
       
        # create a new cursor
        cur = conn.cursor()
        
        # fetch all courts
        cur.execute("SELECT * FROM public.home_court ORDER BY id")
        courts = cur.fetchall()

        #Insert 30 days worth of slots
        date = datetime.date.today()
        
        for i in range(0, 2):
            print("Inserting Day: ", date)
            for hour in range(6, 24):
                for half_hour in [0, 30]:
                    time = datetime.time(hour, half_hour)
                    print(time)
                    
                    for x in courts:
                        sql = "INSERT INTO home_time_slot(court_id, date, time, available, signup_count) VALUES(%s, %s, %s, %s, %s)"
                        cur.execute(sql, (x[0], date, time, True, 0))
                    
            date += datetime.timedelta(days=1)
        
        # commit the changes to the database
        conn.commit()
        
        # close communication with the database
        cur.close()
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        
    finally:
        if conn is not None:
            conn.close()
            
def update_slots():
    conn = None
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect(host="ec2-54-225-68-133.compute-1.amazonaws.com",database="d2ftb891msed9k", user="viuuwydegsjlob", password="f30715f358396a926ad0c5b4d6c526cdd14cbea1834c0523c7a711bae1739dde")
       
        # create a new cursor
        cur = conn.cursor()
        
        #Delete past day slots
        date = datetime.date.today() - datetime.timedelta(days=1)
        
        sql = "DELETE FROM home_time_slot WHERE date = %s"
        cur.execute(sql, (date, ))
        
        # commit delete changes to database
        conn.commit()
        
        # fetch all courts
        cur.execute("SELECT * FROM public.home_court ORDER BY id")
        courts = cur.fetchall()

        #Insert next new day slots
        date = datetime.date.today() + datetime.timedelta(days=1)
        
        for hour in range(6, 24):
            for half_hour in [0, 30]:
                time = datetime.time(hour, half_hour)
                print(time)
                
                for x in courts:
                    sql = "INSERT INTO home_time_slot(court_id, date, time, available, signup_count) VALUES(%s, %s, %s, %s, %s)"
                    cur.execute(sql, (x[0], date, time, True, 0))
        
        # commit insert changes to database
        conn.commit()
        
        # close communication with the database
        cur.close()
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        
    finally:
        if conn is not None:
            conn.close()
            
if __name__ == '__main__':
    #initialize_slots()
    update_slots()