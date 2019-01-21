import pymysql as sql
#Parametros de conexion - - - - - - - - -
USUARIO = "grupo3"
DB = "bgp"
PASSWORD = "grupo3"
HOST = "localhost"

def conectar(servidor, usuario, contrasena, base):
    """
    conectar: realiza la conexián a la basse de datos de MySQL
    Parámetros:
     servidor   (str):  nombre del servidor
     usuario    (str):  nombre del usuario
     contraseña (str):  contraseña del usuario
     bd         (str):  nombre de la base de datos

     Retorna: conn -- objeto de conexion a base de datos
              -1   -- cuando la conexion falla
    """
    try:
        conn = sql.connect(host=servidor, user=usuario, db=base, passwd=contrasena)
        return conn
    except:
        return -1

def realizar_conexion():
    """
     validar_conexion: realiza hasta 3 intentos la conexión de base de datos
     Parametros: ninguno

     Retorna: conn -- objeto de conexion a base de datos
              -1   -- cuando la conexion falla
    """
    #Realizar conexión a base de datos
    conn = conectar(HOST, USUARIO, PASSWORD, DB)
    #si conn==-1, la conexión falla
    return conn

def consultar_usuarios(conexion, rol="todos"):
    """
    consultar_usuarios: realiza la consulta de todos los usuarios segun el rol
    siempre y cuando la conexion sea exitosa
    Parámetros:
     conexion   (objeto):  conexion realizadaa a la base de datos
     rol   (string): admin, monitoreo, todos, por omision todos
     Retorna: lista_admins -- lista de tuplas con la idUsuario, user y password
                               [(idUsuario,user,password)]
    """
    #Selecciona el tipo de consulta a la base de datos segun el rol
    if rol == "admin":
        query = "SELECT idUsuario,user,password FROM usuarios WHERE tipo='admin'"
    elif rol == "monitoreo":
        query = "SELECT idUsuario,user,password FROM usuarios WHERE tipo='monitoreo'"
    else:
        query = "SELECT idUsuario,user,password FROM usuarios"
    #Realizar solo si la conexion es exitosa
    if conexion != -1:
        cursor = conexion.cursor()   #crear cursor
        #Ejecutar Query para seleccionar a los usuarios segun el rol
        cursor.execute(query)
        lista_usuarios = list(cursor.fetchall())
        cursor.close()  #cerrar cursor
        conexion.commit()
        return lista_usuarios

def validar_sesion(conexion, usuario, contrasena):
    """
     validar_sesion: Retorna True si el usuario existe y si la contraseña es correcta,
     caso contrario False
     Parámetros:
      conexion   (objeto):  conexion realizada a la base de datos
      usuario   (string): nombre del usuario
      contraseña (string): contraseña del usuario
     Retorna: Bool
    """
    datos_usuarios = all_users(conexion) #tupla de lista paralelas:
    usuarios = datos_usuarios[1] #lista de todos los usuarios
    contrasenas = datos_usuarios[2] #lista de todas las contraseñas
    #validar si existe el usuario ingresado
    try:
        search = usuarios.index(usuario)
    except:
        search = -1 #el usuario no existe
    if search == -1:
        #el usuario no fue encontrado
        return False
    #El usuario fue encontrado
    index_user = usuarios.index(usuario)
    passwd = contrasenas[index_user] #obtener contraseña del usuario
    #Si la contraseña es correcta True
    return passwd == contrasena

def all_users(conexion):
    """
    all_users: hace una consulta a la BD, y retorna una tupla de listas
    paralelas con las id, usuarios y contraseñas
    Parametros:
     conexion   (objeto):  conexion realizada a la base de datos
     Retorna: [id_usuarios],[usuarios],[contraseñas]
    """
    #Listas con todos los usuarios
    admins = consultar_usuarios(conexion, 'admin')
    monitoreo = consultar_usuarios(conexion, 'monitoreo')
    #Creacion de listas paralelas
    usuarios = []
    contrasenas = []
    ids_usuarios = []
    #llenar las listas paralelas con la informacion de cada usuario
    for id_u, user, pwd in admins+monitoreo:
        usuarios.append(user)
        contrasenas.append(pwd)
        ids_usuarios.append(id_u)
    #Retornar las listas paralelas en una tupla
    return ids_usuarios, usuarios, contrasenas

def all_empresas(conexion):
    """
     all_empresas: hace una consulta a la BD,
      y retorna una tupla de listas paralelas con las
     id, nombre y ASNs de las empresas
     Parámetros:
     conexion   (objeto):  conexion realizada a la base de datos
     Retorna: [ids_empresas],[nombres],[ASNs]
    """
    #Listas con todos las empresas
    empresas = consultar_empresas(conexion) #[(idEmpresa, nombre, ASN)]
    #Creacion de listas paralelas
    nombres = []
    asns = []
    ids_empresas = []
    #Llenar las listas paralelas con la informacion de cada empresa
    for id_e, nombre, asn in empresas:
        nombres.append(nombre)
        asns.append(asn)
        ids_empresas.append(id_e)
    #Retornar las listas paralelas en una tupla
    return ids_empresas, nombres, asns

def establecer_sesion(conexion, usuario):
    """
     establecer_sesion: genera una variable de sesión con el usuario y contraseña ingresados
     Parámetros:
      conexion   (objeto):  conexion realizada a la base de datos
      usuario   (string): nombre del usuario
      contraseña (string): contraseña del usuario
     Retorna: {'id':<id_usuario>,'username': <usuario>} -- diccionario
    """
    #Se crean las listas con la informacion de los usuarios
    id_usuarios, usuarios, contrasenas = all_users(conexion)
    search = usuarios.index(usuario) #busca el indice del usuario
    #retorna un diccionario con las claves id,username. Variable de sesion.
    return {'id':id_usuarios[search], 'username': usuarios[search], 'password':contrasenas[search]}

def consultar_devices_empresa(conexion):
    """
     consultar_devices_empresa: realiza la consulta de todos los dispositivos
     donde existe el usuario y en una empresa especifica
     siempre y cuando la conexión sea exitosa
     Parámetros:
      conexion   (objeto):  conexion realizadaa a la base de datos
      sesion   (diccionario): variable de sesion con las claves id y user
      id_empresa  (string): id de la empresa a consultar los dispositivos donde esta el usuario
     Retorna: lista_dispositivos
     -- lista de tuplas con la idDispositivo, nombre, gateway del dispositivo
                               [(idDispositivo, nombre, gateway)]
    """
    cursor = conexion.cursor()   #crear cursor
    #Seleccionan los dispositivos de la empresa y a los que pertenece
    query = "SELECT dispositivos.idDispositivo,dispositivos.nombre,dispositivos.gateway FROM dispositivos"
    cursor.execute(query)
    lista_dispositivos = list(cursor.fetchall())
    cursor.close()  #cerrar cursor
    conexion.commit()
    return lista_dispositivos

def consultar_interfaces(conexion, id_dispositivo):
    """
     consultar_interfaces: realiza la consulta de todas las interfaces de un dispositivo
     siempre y cuando la conexioó sea exitosa
     Parámetros:
      conexion   (objeto):  conexion realizadaa a la base de datos
      id_empresa  (string): id del dispositivo

     Retorna: lista_interfaces -- lista de tuplas con el nombre, ipAddress, mascara del dispositivo
                               [(nombre, ipAddress, mascara)]
    """
    cursor = conexion.cursor()   #crear cursor
    #Seleccionan todas las interfaces del dispositivo
    query = "SELECT nombre,ipAddress,mascara FROM interfaces WHERE idDispositivo='{}'".format(id_dispositivo)
    cursor.execute(query)
    lista_interfaces = list(cursor.fetchall())
    cursor.close()  #cerrar cursor
    conexion.commit()
    return lista_interfaces

def consultar_empresas(conexion):
    """
     consultar_empresas: realiza la consulta de todas las empresas
     siempre y cuando la conexión sea exitosa
     Parametros:
      conexion   (objeto):  conexion realizadaa a la base de datos

     Retorna: lista_empresas -- lista de tuplas con la idEmpresa, nombre,ASN
                               [(idEmpresa, nombre, ASN)]
    """
    cursor = conexion.cursor()   #crear cursor
    #Query donde se seleccionan todas las empresas existentes
    query = "SELECT idEmpresa,nombre,ASN FROM empresa"
    cursor.execute(query)
    lista_empresas = list(cursor.fetchall())
    cursor.close()  #cerrar cursor
    conexion.commit()
    return lista_empresas

def buscar_id_dispositivo(nombre, id_empresa, conexion):
    """
     buscar_id_dispositivo: busca el dispositivo según el nombre y la id de empresa
     siempre y cuando la conexión sea exitosa
     Parámetros:
      conexion   (objeto):  conexion realizadaa a la base de datos

     Retorna: lista_empresas -- lista de tuplas con la idEmpresa, nombre,ASN
                               [(idEmpresa, nombre, ASN)]
    """
    cursor = conexion.cursor()   #crear cursor
    #Seleccionan todas las empresas existentes
    query = "SELECT idDispositivo FROM dispositivos WHERE nombre='{}' AND empresa ='{}'".format(nombre, id_empresa)
    cursor.execute(query)
    lista_dispositivo = list(cursor.fetchall())
    cursor.close()  #cerrar cursor
    conexion.commit()
    return lista_dispositivo[0][0]

def buscar_ip_dispositivo(nombre, id_empresa, conexion):
    """
     buscar_dispositivo: busca el dispositivo segun el nombre y la id de empresa
     siempre y cuando la conexión sea exitosa
     Parámetros:
      conexion   (objeto):  conexion realizadaa a la base de datos

     Retorna: lista_empresas -- lista de tuplas con la idEmpresa, nombre,ASN
                               [(idEmpresa, nombre, ASN)]
    """
    cursor = conexion.cursor()   #crear cursor
    #Se seleccionan todas las empresas existentes
    query = "SELECT gateway FROM dispositivos WHERE nombre='{}' AND empresa ='{}'".format(nombre, id_empresa)
    cursor.execute(query)
    lista_dispositivo = list(cursor.fetchall())
    cursor.close()  #cerrar cursor
    conexion.commit()
    return lista_dispositivo[0][0]

def cerrar_conexion(conexion):
    """
     cerrar_conexion: realiza el cierre de la conexión de MySQL
      Parámetros:
        conexion (objeto):  conexion realizada a la base de datos
     Retorna: nada
    """
    conexion.close()
