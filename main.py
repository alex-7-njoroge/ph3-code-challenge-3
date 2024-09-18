import psycopg2
from concert import Concert
from venue import Venue
from band import Band

# Establish the connection
conn = psycopg2.connect(
    dbname="concerts",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)

# Example usage:

# For Concert methods
concert = Concert(1)  # Assuming concert with id 1 exists
print(concert.band(conn))
print(concert.venue(conn))
print(concert.hometown_show(conn))
print(concert.introduction(conn))

#For Venue methods
venue = Venue(1)  # Assuming venue with id 1 exists
print(venue.concerts(conn))
print(venue.bands(conn))
print(venue.concert_on('2024-09-21', conn))
print(venue.most_frequent_band(conn))

#For Band methods
band = Band(1)  # Assuming band with id 1 exists
print(band.concerts(conn))
print(band.venues(conn))
band.play_in_venue('Madison Square Garden', '2024-12-31', conn)
print(band.all_introductions(conn))
print(Band.most_performances(conn))

# Don't forget to close the connection
conn.close()