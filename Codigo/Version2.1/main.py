import graficos as gf
import conexion_mysql as sql

""" 
Retorna grafico de error de conexion en caso de fallar la conexion con la base de datos 
o retorna el grafico de inicio para continuar a configurar los enrutadores.

"""
conn=sql.realizar_conexion() #Si existe conexion con la base de datos devuelve la direccion hexagecimal caso contrario devuevle -1
if conn==-1:
    gf.error_servidor()
else:
    gf.inicio(conn)
    sql.cerrar_conexion(conn)
