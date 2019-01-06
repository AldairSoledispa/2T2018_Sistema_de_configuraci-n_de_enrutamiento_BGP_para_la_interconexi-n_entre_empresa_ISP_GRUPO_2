import paramiko
import conexion_mysql as sql
import funciones_Sesion_BGP2 as BGP

# import ConfiguracionBGP.Base_de_Datos.conexion_mysql

HOST_Loopback=str('192.168.100.254')
HOST_Local=str("192.168.101.11")
HOST_Remoto=str("209.165.200.1")

# ===============================================================================
# conexion_ssh: realiza la conexión a ssh con el Router a configurar
# Parametros:
# ip   (str):  dirección IP del dispositivo
# user_Dispo    (str):  usuario del dispositivo
# password_Dispo (str):  contraseña del dispositivo
#
# Retorna: objeto_ssh -- objeto de conexion ssh
#          -1   -- cuando la conexion falla
# -------------------------------------------------------------------------------

def conexion_ssh(host,user_Dispo,password_Dispo):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoADDPolicy())
        ssh.connect(host, port=22, username=user_Dispo, password = password_Dispo)
        objeto_ssh = ssh.invoke_shell()
        print("Conexion ssh realizada con exito\n")
        return(objeto_ssh)
    except:
        return -1


# ===============================================================================
# iniciar_Configuracion: Permite inicar una configuración
# Parametros:
# objeto_ssh   (ssh): objeto de conexión ssh
# hostname_Dispo   (str):  nombre del dispositivo
#
# -------------------------------------------------------------------------------

def iniciar_Configuracion(objeto_ssh):
    objeto_ssh.send("enable\n")
    objeto_ssh.send("configure terminal\n")

# ===============================================================================
# guardar_Configuracion: guarda en memoria las configuraciones realizadas
# Parametros:
# objeto_ssh   (ssh): objeto de conexión ssh
#
# -------------------------------------------------------------------------------

def guardar_Configuracion(objeto_ssh):
    objeto_ssh.send("end\n")
    objeto_ssh.send("wr\n")
    objeto_ssh.send('\n')

#===============================================================================
#config_Plantilla_Basica: configuración básica de un router
#Parametros:
# objeto_ssh   (ssh):  objeto tipo ssh
# hostname_Dispo    (str):  nombre del dispositivo
#
#-------------------------------------------------------------------------------

def config_Plantilla_Basica(objeto_ssh, hostname_Dispo, conexion):
    iniciar_Configuracion(objeto_ssh)
    nombre_Host=str("hostname "+hostname_Dispo+"\n")
    objeto_ssh.send(nombre_Host)
    objeto_ssh.send("ip domain-name fiec.espol.edu.ec\n")
    objeto_ssh.send("ip name-server 192.168.1.17\n")
    objeto_ssh.send("ip name-server 192.168.1.19\n")
    id_usuarios, usuarios, contraseñas = sql.all_users(conexion)
    for i in range(len(usuarios)):
        user = usuarios[i]
        passwd = contraseñas[i]
        objeto_ssh.send("username {} privilege 15 secret {}\n".format(user,passwd))
    objeto_ssh.send("banner motd #ACCESO SOLO A PERSONAL AUTORIZADO#\n")
    objeto_ssh.send("line vty 0 4\n")
    objeto_ssh.send("transport input all\n")
    objeto_ssh.send("login local\n")
    objeto_ssh.send("exec-timeout 3 3\n")
    objeto_ssh.send("logging synchronous\n")
    objeto_ssh.send("line console 0\n")
    objeto_ssh.send("transport output all\n")
    objeto_ssh.send("login local\n")
    objeto_ssh.send("exec-timeout 3 3\n")
    objeto_ssh.send("logging synchronous\n")
    guardar_Configuracion(objeto_ssh)


# ===============================================================================
# configurar_Interfaces: configura IP y Mask  en las interfaces del router.
# Parametros:
# objeto_ssh   (ssh):  objeto tipo ssh
# id_empresa (int):  identificador del dispositivo
# usuario(str): nombre del usuario
# contraseña (str): contraseña del usuario
#  .encode('ascii')
# -------------------------------------------------------------------------------

def configurar_Interfaces(objeto_ssh, nom_empresa, nom_Dispo_Especifico, usuario, contraseña):
    conex_BD = sql.validar_conexion()
    config_Plantilla_Basica(objeto_ssh, nom_Dispo_Especifico)
    sesion = sql.establecer_sesion(conex_BD, usuario, contraseña)
    id_empresas, nombres, ASNs = sql.all_empresas(conex_BD)

    try:
        id_empresa = ""
        id_Dispo_Especifico = ""
        for i in range(len(nombres)):
            if (nombres[i] == nom_empresa.strip()):
                id_empresa = id_empresas[i]

        list_Dispositivos = sql.consultar_devices_empresa(conex_BD, sesion, id_empresa)
        for id_Dispositivo, nom_Dispositivo, gateway_Dispo in list_Dispositivos:
            if (nom_Dispositivo == nom_Dispo_Especifico.strip()):
                id_Dispo_Especifico = id_Dispositivo

        lista_Interfaces_Dispo = sql.consultar_interfaces(conex_BD, id_Dispo_Especifico)

        for interfaz in lista_Interfaces_Dispo:
            nom_Interfaz = str("int " + interfaz[0] + "\n")
            ip_Interfaz = str(interfaz[1])
            mascara_Interfaz = str(interfaz[2] + "\n")
            ip_Adress = str("ip address " + ip_Interfaz + " " + mascara_Interfaz)

            objeto_ssh.send(nom_Interfaz)
            objeto_ssh.send(ip_Adress)
            objeto_ssh.send("no shutdown\n")
            objeto_ssh.send("exit\n")
    except:
        print("Empresa o dispositivo incorrectos")
    guardar_Configuracion(objeto_ssh)
    print(nom_empresa + "->" + nom_Dispo_Especifico + "\nInterfaces configuradas con éxito")


# #============================================================================================
# #
# #                                        Pruebas
# #
# #============================================================================================
# conn = sql.realizar_conexion()
# if conn==-1:
#     print("nel")
# else:
#     listaL= ["192.168.101.0"]
#     listaR= ["0.0.0.0"]
#     tn1=conexion_ssh(HOST_Local,"admin","admin")
#     iniciar_Configuracion(tn1)
#     BGP.config_Vecino(tn1, "209.165.200.2","209.165.200.1", "65000","65001",listaL,listaR,"admin","admin")
#     guardar_Configuracion(tn1)
#     sql.cerrar_conexion(conn)




