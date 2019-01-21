"""
Este script se utiliza para realizar la configuracion
BGP en los enrutadores
"""
def sesion_BGP(objeto_ssh, sistema_autonomo):
    """
    Habilita BGP mediante una conexion ssh, escribe en terminal del router
    Parametros:
        objeto_ssh      (ssh):  objeto  ssh
        Sistema_Autonomo(str):  numero de AS a configurar el dispositivo
    """
    ingreso_router = str("router bgp " + sistema_autonomo + "\n")
    print(ingreso_router)
    objeto_ssh.send(ingreso_router)


def configurar_Network(objeto_ssh, lista_networks):
    """
    La funcion anuncia las redes que son ingresadas como parametro de entrada
    Parametros:
        objeto_ssh      (ssh):  Objeto  ssh
        lista_Networks(lista):  Contiene una lista de strings que corresponden al
                                grupo de networks a configurar en el router.
    """
    for network in lista_networks:
        if network.strip() == "0.0.0.0":
            red = str("network " + network + "\n")
            objeto_ssh.send(red)
        else:
            red = network.split('-')
            red_y_mask = str("network "+red[0]+" mask "+red[1]+"\n")
            print(red_y_mask)
            objeto_ssh.send(red_y_mask)


def config_Vecino(objeto_ssh, ip_local, ip_vecino, as_local, as_remoto, lista_networks_l,
                  lista_networks_r, usuario, contrasena):
    """
    La funcion configura el enrutador vecino con su AS
    Parametros:
        objeto_ssh      (ssh): objeto  ssh
        ip_Vecino       (str): Dirección IP de la interfaz vecina
        AS_Local        (str): Sistema Autónomo del Router Local
        AS_Remoto       (str): Sistema Autónomo del Router Remoto
        lista_Networks(lista): contiene una lista de strings que corresponden al
                               grupo de networks a configurar en el router.
        var_Local       (str): variable indicador, separa la configuración que recibe el
                               Router local y la que recibe el remoto.
    """
    sesion_BGP(objeto_ssh, as_local)
    objeto_ssh.send("\n")
    vecino = str("neighbor " + ip_vecino + " remote-as " + as_remoto + "\n")
    objeto_ssh.send(vecino)
    configurar_Network(objeto_ssh, lista_networks_l)
    objeto_ssh.send("end\n")
    objeto_ssh.send("wr\n")
    objeto_ssh.send("\n")
    objeto_ssh.send(("ssh {}\n").format(ip_vecino))
    objeto_ssh.send(("{}\n").format(usuario))
    objeto_ssh.send(("{}\n").format(contrasena))
    objeto_ssh.send("enable \n")
    objeto_ssh.send("config t\n")
    # objeto_ssh.send("ip route 0.0.0.0 0.0.0.0 lo0 name to_core_isp \n")
    sesion_BGP(objeto_ssh, as_remoto)
    vecino_local = str("neighbor " + ip_local + " remote-as " + as_local + "\n")
    objeto_ssh.send(vecino_local)
    configurar_Network(objeto_ssh, lista_networks_r)
    print("Se configuró BGP con éxito")
