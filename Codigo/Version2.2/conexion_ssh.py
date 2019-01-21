"""
Este script se utiliza para realizar la conexion
ssh con los routers
"""
import paramiko
import conexion_mysql as sql
import funciones_Sesion_BGP2 as BGP
# import ConfiguracionBGP.Base_de_Datos.conexion_mysql
HOST_LOOPBACK = str('192.168.101.12')
HOST_LOCAL = str("192.168.101.11")
HOST_REMOTO = str("209.165.200.1")


def conexion_ssh(host, user_dispo, password_dispo):
    """Returna objeto_ssh si la conexion se establece de lo contrario -1 si falla
    La funcion realiza conexion a ssh con el router a configurar
    parametros:
        ip            (str):  direccion IP del dispositivo
        user_Dispo    (str):  usuario del dispositivo
        password_Dispo(str):  contrasena del dispositivo
    """
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=host, port=22, username=user_dispo, password=password_dispo)
        objeto_ssh = ssh_client.invoke_shell()
        print("Conexion ssh realizada con exito\n")
        return objeto_ssh
    except:
        return -1


def iniciar_configuracion(objeto_ssh):
    """
    la funcion permite iniciar una configuracion del router
    Parametros:
        objeto_ssh    (ssh): objeto de conexion ssh
        hostname_Dispo(str): nombre del dispositivo
    """
    objeto_ssh.send("enable\n")
    objeto_ssh.send("configure terminal\n")


def guardar_configuracion(objeto_ssh):
    """
    La funcion guarda en memoria las configuraciones realizadas
    Parametros:
        objeto_ssh(ssh): objeto de conexion ssh
    """
    objeto_ssh.send("end\n")
    objeto_ssh.send("wr\n")
    objeto_ssh.send('\n')
