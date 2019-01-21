"""
Este script se utiliza para iniciar la interfaz grafica del programa
"""
import graficos as gf
import conexion_mysql as sql
# realiza conxeion con la base de datos
CONN = sql.realizar_conexion()
if CONN == -1:
    # grafico de error si la conexion falla
    gf.error_servidor()
else:
    # grafico de conexion establecida si no falla la conexion con la base de datos
    gf.inicio(CONN)
    sql.cerrar_conexion(CONN)
