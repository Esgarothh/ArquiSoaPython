import psycopg2


class BaseDeDatos:
    def __init__(self):
        self.host = "silly.db.elephantsql.com"
        self.port = 5432
        self.user = "sjpzdvmw"
        self.password = "d5QoAfziB_lNBjSxGl_UC5cxPs1PM3LY"
        self.conn = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password
            )
            print("Connected to ElephantSQL")
        except psycopg2.Error as e:
            print("Error connecting to ElephantSQL:", e)

    def close(self):
        if self.conn:
            self.conn.close()
            print("Connection to ElephantSQL closed")

    def execute_query(self, query, params=None):
        try:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            results = cursor.fetchall()
            return results
        except psycopg2.Error as e:
            print("Error executing query:", e)

    def get_usuario(self, rut):
        query = "SELECT * FROM usuarios WHERE rut = %s;"
        params = (rut,)
        results = self.execute_query(query, params)
        return results

    def get_receta(self, receta_id):
        query = "SELECT * FROM recetas WHERE id = %s;"
        params = (receta_id,)
        results = self.execute_query(query, params)
        return results

    def get_hora(self, hora_id):
        query = "SELECT * FROM horas WHERE id = %s;"
        params = (hora_id,)
        results = self.execute_query(query, params)
        return results

    def get_test(self, id):
        query = "SELECT * FROM test WHERE id = %s;"
        params = (id,)
        results = self.execute_query(query, params)
        return results
