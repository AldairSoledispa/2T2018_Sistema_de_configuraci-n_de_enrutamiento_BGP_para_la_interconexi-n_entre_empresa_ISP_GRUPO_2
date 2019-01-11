"""

Habilita BGP mediante una conexion ssh, escribe en terminal del router
Parametros:
    objeto_ssh      (ssh):  objeto  ssh
    Sistema_Autonomo(str):  numero de AS a configurar el dispositivo

"""
def sesion_BGP(objeto_ssh,Sistema_Autonomo):
    
    ingreso_Router=str("router bgp "+Sistema_Autonomo+"\n")
    print(ingreso_Router)
    objeto_ssh.send(ingreso_Router)

"""

Return True or False 

La funcion permite comparar un String para saber si es estamos configurando el router local o el remoto
Parametros:
    Local_OR_Remoto  (str):  variable a comparar 

"""

def es_Local(Local_OR_Remoto):
    if Local_OR_Remoto.lower().strip()=="local":
        return True
    else:
        return False

"""

La funcion anuncia las redes que son ingresadas como parametro de entrada
Parametros:
    objeto_ssh      (ssh):  Objeto  ssh
    lista_Networks(lista):  Contiene una lista de strings que corresponden al
                            grupo de networks a configurar en el router.

"""

def configurar_Network(objeto_ssh,lista_Networks):
    for network in lista_Networks:
        if(network.strip()=="0.0.0.0"):
            red=str("network "+ network+"\n")
            objeto_ssh.send(red)
        else:
            red=network.split('-')
            red_Y_mask=str("network "+red[0]+" mask "+red[1]+"\n")
            print (red_Y_mask)
            objeto_ssh.send(red_Y_mask)


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


def config_Vecino(objeto_ssh,ip_local,ip_Vecino,AS_Local,AS_Remoto,lista_NetworksL,lista_NetworksR,usuario,contraseña):
    sesion_BGP(objeto_ssh,AS_Local)
    objeto_ssh.send("\n")
    vecino=str("neighbor " +ip_Vecino+ " remote-as "+AS_Remoto+"\n")
    objeto_ssh.send(vecino)
    configurar_Network(objeto_ssh,lista_NetworksL)

    objeto_ssh.send("end\n")
    objeto_ssh.send("wr\n")
    objeto_ssh.send("\n")
        
    objeto_ssh.send(("ssh {}\n").format(ip_Vecino))
    objeto_ssh.send(("{}\n").format(usuario))
    objeto_ssh.send(("{}\n").format(contraseña))

    
    objeto_ssh.send("enable \n")
    objeto_ssh.send("config t\n")
        
    ##objeto_ssh.send("ip route 0.0.0.0 0.0.0.0 lo0 name to_core_isp \n")
    sesion_BGP(objeto_ssh,AS_Remoto)
    vecino_Local=str("neighbor " +ip_local+ " remote-as "+AS_Local+"\n")
    objeto_ssh.send(vecino_Local)
    configurar_Network(objeto_ssh,lista_NetworksR)
    print("Se configuró BGP con éxito")



