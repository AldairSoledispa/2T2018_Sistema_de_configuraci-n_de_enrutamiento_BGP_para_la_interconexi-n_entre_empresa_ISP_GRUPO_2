"""
Este script se utiliza para realizar operaciones
a las direcciones ip, mascaras y log de usuarios
"""
import time as tm
import datetime as dtime


def obtener_dir_red(dir_ip, mascara):
    """
    Return la direccion de red
    la funcion obtiene la direccion de red de una ip de host segun su mascara
    Parametros:
        ip     (str):   direccion ip
        mascara(str):   mascara de subred
    """
    # separa los octetos
    octetos_ip = dir_ip.split(".")  # [xxx,xxx,xxx,xxx]
    octetos_mask = mascara.split(".")  # [xxx,xxx,xxx,xxx]
    # lista con los octetos de la direccion de red
    network = []
    for i in range(len(octetos_ip)):
        # convierte los octetos de la ip y la mascara a binario
        val_a = conv_bin(int(octetos_ip[i]))
        val_b = conv_bin(int(octetos_mask[i]))
        # realiza operacion and entre los octetos y la convierte a decimal
        operacion = operar_bin(val_a, val_b)
        operacion = conv_dec(operacion)
        # guarda el nuevo octeto
        network.append(str(operacion))
    return ".".join(network)


def operar_bin(octeto1, octeto2):
    """Return res(str): numero binario
    La funcion operacion con and bit a bit un numero binario
    Parametros:
        octeto1(str):   numero binario
        octeto2(str):   numero binario
    """
    res = ""
    # comparacion bit a bit
    for i in range(len(octeto1)):
        val_a = int(octeto1[i])
        val_b = int(octeto2[i])
        res += str(val_a and val_b)
    return res


def conv_bin(num):
    """Return numero binario de 8 bits
    la funcion convierte a binario un numero decimal
    Parametros:
        n(int):   numero decimal
    """
    binary = ""
    while num != 0:
        resul = num % 2
        binary = str(resul) + binary
        num //= 2
    return "0"*(8-len(binary)) + binary


def conv_dec(bina):
    """Return n(int):  numero decimal
    la funcion convierte a decimal un numero binario
    Parametros:
        bn(str):   numero binario
    """
    num = 0
    bina = bina[::-1]
    for i in range(len(bina)):
        num += (2**int(i))*int(bina[i])
    return num


def validar_formato_ip(ip_address):
    """Return True: ip valida, False: ip no valida
    la funcion determina si una direccion ip tiene el formato correcto
    Parametros:
        ip_Address(str):   numero binario
    """
    octetos = ip_address.split(".")
    # si no tiene 4 octetos
    if len(octetos) != 4:
        return False
    # verificar octeto por octeto
    for octeto in octetos:
        if not octeto.isdigit():
            # si el octeto no es un numero decimal
            return False
        # el octeto es decimal
        octeto = int(octeto)
        if not 0 <= octeto <= 255:
            # si el octeto no esta entre 0 y 255
            return False
    # la direccion ip es valida
    return True


def validar_asn(asn):
    """Return True: asn valido, False: asn no valido
    la funcion determina si un ASN tiene el formato correcto
    Parametros:
        asn(str):   numero de sistema autonomo
    """
    if not asn.isdigit():
        # si no es un digito
        return False
    # convertir a digito
    asn = int(asn)
    # verificar si esta entre 1 y 64512
    return 1 <= asn <= 64512


def escribir_logu(hora, usuario, mensaje):
    """Return nada
    la funcion crea un log de usuario
    Parametros:
        hora   (str):   hora en que se almacena en el log
        usuario(str):   usuario que esta usando el programa
        mensaje(str):   mensaje a escribir en el log
    """
    # abre el archivo, escribe la linea y cierra el archivo
    file = open("logs.txt", "a")
    file.write(";".join([hora, usuario, mensaje]) + "\n")
    file.close()


def hora_actualu():
    """Return st (str): hora actual formato AA-MM-DD H:M:S
    la funcion interna que devuelve la hora local en formato AA-MM-DD H:M:S
    Parametros:
        ninguno
    """
    # obtiene el tiempo actual
    tiempo = tm.time()
    # se le da el formato deseado
    s_tiempo = dtime.datetime.fromtimestamp(tiempo).strftime('%Y-%m-%d %H:%M:%S')
    return s_tiempo
