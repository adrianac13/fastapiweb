from data.modelo.usuario import Usuario


class DaoUsuario:
    def get_all(self, db) -> list[Usuario]:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM viajes")

        viajes_en_db = cursor.fetchall()
        viajes = []
        for reserva in viajes_en_db:
            nuevo_usuario = Usuario(
                reserva["id"], reserva["nombre_reserva"], reserva["destino"], reserva["duracion"], reserva["presupuesto"], reserva["fecha_reserva"],
            )
            viajes.append(nuevo_usuario)
        cursor.close()
        return viajes

    def insert(self, db, nombre_reserva: str, destino: str, duracion: str, presupuesto: float, fecha_reserva: str):
        cursor = db.cursor()
        sql = "INSERT INTO viajes (nombre_reserva, destino, duracion, presupuesto, fecha_reserva) VALUES (%s, %s, %s, %s, %s)"
        data = (nombre_reserva, destino, duracion, presupuesto, fecha_reserva)
        cursor.execute(sql, data)
        db.commit()
        cursor.close()

    def update(self, db, id: int, nombre_reserva: str, destino: str, duracion: str, presupuesto: float, fecha_reserva: str):
        cursor = db.cursor()
        sql = "UPDATE viajes SET nombre_reserva = %s, destino = %s, duracion = %s, presupuesto = %s, fecha_reserva = %s WHERE id = %s"
        data = (nombre_reserva, destino, duracion, presupuesto, fecha_reserva, id)
        cursor.execute(sql, data)
        db.commit()
        cursor.close()

    def delete(self, db, id: int):
        cursor = db.cursor()
        sql = "DELETE FROM viajes WHERE id = %s"
        data = (id,)
        cursor.execute(sql, data)
        db.commit()
        cursor.close()
