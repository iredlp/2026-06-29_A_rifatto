from database.DB_connect import DBConnect
from model.customer import Customer


class DAO():
    @staticmethod
    def getAllAlbums():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select * from album
                """

        cursor.execute(query)

        for row in cursor:
            results.append(**row)

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllCountries():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                 SELECT distinct c.Country  
                    from customer c 
                 """

        cursor.execute(query)

        for row in cursor:
            results.append(row["Country"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(genere):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct c.*
                    from invoice i , customer c 
                    where c.Country =%s and  c.CustomerId =i.CustomerId    """
            cursor.execute(query, (genere,))

            for row in cursor:
                result.append(Customer(**row))

            cursor.close()
            cnx.close()
            return result

    @staticmethod
    def getFatturatoPerCliente( idC):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select sum(i.Total) as fatturato
        from invoice i , customer c 
        where  c.CustomerId =i.CustomerId and c.CustomerId =%s"""
            cursor.execute(query, (idC,))
            row = cursor.fetchone()
            #for row in cursor:
             #   result.append(row["fatturato"])

            cursor.close()
            cnx.close()
            # Se non ci sono vendite sum() restituisce None, quindi usiamo or 0
            if row and row["fatturato"] is not None:
                return float(row["fatturato"])
            return 0
           # return result

    @staticmethod
    def getArtistiPerCliente(country, idC):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """  select distinct al.ArtistId 
from customer c, invoice i, invoiceline inv, track t,album al
where c.Country =%s and  c.CustomerId =i.CustomerId and c.CustomerId =%s
and i.InvoiceId =inv.InvoiceId and inv.TrackId =t.TrackId and t.AlbumId  =al.AlbumId 
  """
            cursor.execute(query, (country,idC))

            for row in cursor:
                result.append(row["ArtistId"])

            cursor.close()
            cnx.close()
            return result