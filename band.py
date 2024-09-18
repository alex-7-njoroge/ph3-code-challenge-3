class Band:
    def __init__(self, band_id):
        self.band_id = band_id

    def concerts(self, conn):
        query = "SELECT * FROM concerts WHERE band_id = %s"
        with conn.cursor() as cur:
            cur.execute(query, (self.band_id,))
            return cur.fetchall()

    def venues(self, conn):
        query = """
        SELECT DISTINCT venue.* FROM venue
        JOIN concerts ON concerts.venue_id = venue.id
        WHERE concerts.band_id = %s
        """
        with conn.cursor() as cur:
            cur.execute(query, (self.band_id,))
            return cur.fetchall()

    def play_in_venue(self, venue_title, date, conn):
        # Get the next available ID
        query_get_max_id = "SELECT COALESCE(MAX(id), 0) + 1 FROM concerts"
        with conn.cursor() as cur:
            cur.execute(query_get_max_id)
            new_id = cur.fetchone()[0]

        # Insert a new concert with the new ID
        query_insert = """
        INSERT INTO concerts (id, band_id, venue_id, date)
        SELECT %s, %s, venue.id, %s
        FROM venue
        WHERE venue.title = %s
        """
        with conn.cursor() as cur:
            cur.execute(query_insert, (new_id, self.band_id, date, venue_title))
            conn.commit()

    def all_introductions(self, conn):
        query = """
        SELECT band.name, band.hometown, venue.city 
        FROM concerts
        JOIN band ON concerts.band_id = band.id
        JOIN venue ON concerts.venue_id = venue.id
        WHERE concerts.band_id = %s
        """
        with conn.cursor() as cur:
            cur.execute(query, (self.band_id,))
            introductions = cur.fetchall()
            return [
                f"Hello {intro[2]}!!!!! We are {intro[0]} and we're from {intro[1]}"
                for intro in introductions
            ]

    @staticmethod
    def most_performances(conn):
        query = """
        SELECT band.*, COUNT(concerts.id) AS num_performances
        FROM concerts
        JOIN band ON concerts.band_id = band.id
        GROUP BY band.id
        ORDER BY num_performances DESC
        LIMIT 1
        """
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchone()