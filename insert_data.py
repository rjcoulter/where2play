#!/usr/bin/python

# imports needed to connect to postgreSQL database
import psycopg2
import datetime

# importing the lists created from running these files
from scraper import courts, facilities
from gym_scraper import ng, afc, mem, src, ngp, p


def insert_facility_list(facility_list):
	""" insert multiple facilities into the facilities table  """
	sql = "INSERT INTO home_facility(\"F_Name\", \"Location\", \"Description\", \"Facility_Hours\", \"Facility_Phone\", \"Parking_Hours\", \"F_Type\") VALUES(%s, %s, %s, %s, %s, %s, %s)"
	conn = None
	try:
		# connect to the PostgreSQL database
		conn = psycopg2.connect(host="ec2-54-225-68-133.compute-1.amazonaws.com",database="d2ftb891msed9k", user="viuuwydegsjlob", password="f30715f358396a926ad0c5b4d6c526cdd14cbea1834c0523c7a711bae1739dde")
		# create a new cursor
		cur = conn.cursor()
		# execute the INSERT statement
		for i in facility_list:
			cur.execute(sql,i)
		# commit the changes to the database
		conn.commit()
		# close communication with the database
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()


def update_facility_list(hours, name):
	""" update facility hours """
	sql = """ UPDATE home_facility 
		SET \"Facility_Hours\" = %s
		WHERE \"F_Name\" = %s"""
	conn = None
	try:
		# connect to the PostgreSQL database
		conn = psycopg2.connect(host="ec2-54-225-68-133.compute-1.amazonaws.com",database="d2ftb891msed9k", user="viuuwydegsjlob", password="f30715f358396a926ad0c5b4d6c526cdd14cbea1834c0523c7a711bae1739dde")
		# create a new cursor
		cur = conn.cursor()
		# execute the INSERT statement
		cur.execute(sql,(hours, name))
		# commit the changes to the database
		conn.commit()
		# close communication with the database
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()


def insert_court_list(court_list):
	""" insert multiple facilities into the facilities table  """
	sql = "INSERT INTO home_court(\"id\", \"C_Name\", \"C_Type\", \"current_count\", \"facility_id\") VALUES(%s, %s, %s, %s, %s)"
	conn = None
	try:
		# connect to the PostgreSQL database
		conn = psycopg2.connect(host="ec2-54-225-68-133.compute-1.amazonaws.com",database="d2ftb891msed9k", user="viuuwydegsjlob", password="f30715f358396a926ad0c5b4d6c526cdd14cbea1834c0523c7a711bae1739dde")
		# create a new cursor
		cur = conn.cursor()
		# execute the INSERT statement
		for i in court_list:
			cur.execute(sql,i)
		
		# commit the changes to the database
		conn.commit()
		# close communication with the database
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()


if __name__ == '__main__':

	locations = [
		'450 Whitehead Rd, Charlottesville, VA 22904', #afc
		'450 Whitehead Rd, Charlottesville, VA 22904', ##afc pool
		'Carr\'s Hill Field, Charlottesville, VA 22903', #carr's hill
		'Copeley Massie Road, Charlottesville, VA, 22904', #copely
		'1112 Emmet St N, Charlottesville, VA 22903', #dell
		'210 Emmet St S, Charlottesville, VA 22903', #synder TC
		'Lambeth Field, University Way, Charlottesville, VA 22904', #lambeth
		'Nameless Field, Charlottesville, VA 22903', #nameless
		'Madison Bowl, Charlottesville, VA 22903', #madison bowl
		'210 Emmet St S, Charlottesville, VA 22903', #mem
		'510 Massie Rd, Charlottesville, VA 22903', #ngrc
		'510 Massie Rd, Charlottesville, VA 22903', #ngrc pool
		'The Park (North Grounds), Charlottesville, VA 22903', #park
		'Poplar Ridge Challenge Course Observatory Hill, Charlottesville, VA, 22904', #poplar ridge
		'505 Edgemont Rd, Charlottesville, VA 22903' #src
	]
	descriptions = [
		'AFC description',
		'AFC pool description',
		'Carr\'s hill description',
		'Copeley description',
		'The Dell description',
		'Snyder description',
		'Lambeth description',
		'Nameless description',
		'Madison Bowl description',
		'Mem Gym description',
		'NGRC description',
		'NGRC pool description',
		'Park description',
		'Poplar Ridge description',
		'SRC description'
	]
	types = [
		'Gym',
		'Gym',
		'Field',
		'Field',
		'Other Facility',
		'Other Facility',
		'Field',
		'Field',
		'Field',
		'Gym',
		'Gym',
		'Gym',
		'Field',
		'Other Facility',
		'Gym'
	]
	phones= [
		'434-924-3793',
		'434-924-3793',
		'434-924-3791',
		'434-924-3791',
		'434-924-3791',
		'434-924-3791',
		'434-924-3791',
		'434-924-3791',
		'434-924-3791',
		'434-924-6204',
		'434-924-7380',
		'434-924-7380',
		'434-924-3791',
		'434-924-3791',
		'434-982-5101',
	]

	weekday = datetime.datetime.today().weekday()

	# create the facilities list in proper insert format
	for i in range(0,len(locations)):
		facilities[i].append(locations[i])
		facilities[i].append(descriptions[i])
		if( i == 0):
			facilities[i].append(afc[weekday])
		elif(i == 1):
			facilities[i].append(p[weekday])
		elif(i == 5):
			facilities[i].append('Dusk to Midnight')
		elif( i == 9):
			facilities[i].append(mem[weekday])
		elif( i == 10):
			facilities[i].append(ng[weekday])
		elif( i == 11):
			facilities[i].append(ngp[weekday])
		elif( i == 14):
			facilities[i].append(src[weekday])
		else:
			facilities[i].append('OPEN')
		facilities[i].append(phones[i])
		facilities[i].append('varies')
		facilities[i].append(types[i])

	for i in range(0, len(facilities)):
		update_facility_list(facilities[i][3], facilities[i][0])
	
	# insert_facility_list(facilities)
	# insert_court_list(courts)

