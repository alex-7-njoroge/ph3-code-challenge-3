import psycopg2

class Concert:
    def __init__(self, concert_id):
        self.concert_id = concert_id

    def band(self, conn):
        query = """
        SELECT band.* FROM band
        JOIN concerts ON concerts.band_id = band.id
        WHERE concerts.id = %s
        """
        with conn.cursor() as cur:
            cur.execute(query, (self.concert_id,))
            return cur.fetchone()

    def venue(self, conn):
        query = """
        SELECT venue.* FROM venue
        JOIN concerts ON concerts.venue_id = venue.id
        WHERE concerts.id = %s
        """
        with conn.cursor() as cur:
            cur.execute(query, (self.concert_id,))
            return cur.fetchone()

    def hometown_show(self, conn):
        query = """
        SELECT band.hometown, venue.city 
        FROM concerts
        JOIN band ON concerts.band_id = band.id
        JOIN venue ON concerts.venue_id = venue.id
        WHERE concerts.id = %s
        """
        with conn.cursor() as cur:
            cur.execute(query, (self.concert_id,))
            result = cur.fetchone()
            return result[0] == result[1]

    def introduction(self, conn):
        query = """
        SELECT band.name, band.hometown, venue.city
        FROM concerts
        JOIN band ON concerts.band_id = band.id
        JOIN venue ON concerts.venue_id = venue.id
        WHERE concerts.id = %s
        """
        with conn.cursor() as cur:
            cur.execute(query, (self.concert_id,))
            result = cur.fetchone()
            return f"Hello {result[2]}!!!!! We are {result[0]} and we're from {result[1]}"