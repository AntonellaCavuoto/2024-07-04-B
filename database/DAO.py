from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(row["id"],
                          row["Name"],
                          row["Capital"],
                          row["Lat"],
                          row["Lng"],
                          row["Area"],
                          row["Population"],
                          row["Neighbors"]))

            cursor.close()
            cnx.close()
        return result

    # @staticmethod
    # def get_all_sightings():
    #     cnx = DBConnect.get_connection()
    #     result = []
    #     if cnx is None:
    #         print("Connessione fallita")
    #     else:
    #         cursor = cnx.cursor(dictionary=True)
    #         query = """select *
    #                 from sighting s
    #                 order by `datetime` asc """
    #         cursor.execute(query)
    #
    #         for row in cursor:
    #             result.append(Sighting(**row))
    #         cursor.close()
    #         cnx.close()
    #     return result

    @staticmethod
    def getYears():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct year(s.`datetime`) as year
                        from sighting s 
                        order by year(s.`datetime`) asc """
            cursor.execute(query)

            for row in cursor:
                result.append(row["year"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getStates(year):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """ select distinct s2.Name as state
                        from sighting s, state s2 
                        where s.state = s2.id 
                        and year(s.`datetime`) = %s
                        order by s2.Name asc"""
            cursor.execute(query, (year, ))

            for row in cursor:
                result.append(row["state"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getNodes(state, year):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select s.*
                        from sighting s, state s2 
                        where s2.Name = %s and s2.id = s.state 
                        and year(s.`datetime`) = %s"""
            cursor.execute(query, (state, year))

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getEdges(state1, year1, state2, year2, idMap):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select s1.id as id1, s2.id as id2
                        from (select s.*
                        from sighting s, state s2 
                        where s2.Name = %s and s2.id = s.state 
                        and year(s.`datetime`) = %s) s1, (
                        select s.*
                        from sighting s, state s2 
                        where s2.Name = %s and s2.id = s.state 
                        and year(s.`datetime`) = %s) s2
                        where s1.id < s2.id and s1.shape = s2.shape 
                        order by s1.id, s2.id"""
            cursor.execute(query, (state1, year1, state2, year2))

            for row in cursor:
                result.append((idMap[row["id1"]], idMap[row["id2"]]))
            cursor.close()
            cnx.close()
        return result