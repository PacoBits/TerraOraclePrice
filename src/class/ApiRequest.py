import requests, json
from requests.models import Response
from logger import logger
from excepciones import ImposibleObtenerToken, ImposibleAuth



class ApiRequest:
    """Clase base para conectarse a una API REST
    
    Note
    ----
        N/A
    Parameters
    ----------
    sectoken : bool
        Indica si la API esta securizada o no
    log : bool
        indica si hay log y trazas
    ficherolog : str
        ruta y fichero de log en el que escribir
    loglevel : int
        Indica el nivel de log a partir del cual se escriben las trazas    
    host : str
        host de la api sin la / del final

    Attributes Clase
    ----------
    N/A
    
    Attributes
    ----------
    sectoken : bool
        Indica si la API esta securizada, por defecto false.
    token : str
        Token para realizar las conexiones
    secendpoint : str
        endponint para obtener el token de seguridad
    secpayload : str
        payload para obtener la seguridad: usuario y clave
    secheaders : str
        headers para obtener la seguridad
    tokenparser : str
         nombre del token devuelto al autorizarse
    tokenrequest : str
        nombre del token al hacer las peticiones   
    host : str
        host de la api sin la / del final
    logger: Clase logger
        Instancia a la clase logger para escribir 
    authheader : str
        header de auth si corresponde enviarlo                   
    """
    authheader=""
    sectoken=False # si la api usa token de sguridad o no
    token="" #token de seguridad
    secendpoint="" # endpoint para obtener la seguridad
    secpayload="" # payload para obtener la seguridad: usuario y clave
    secheaders=""  # headers para obtener la seguridad
    tokenparser="" # nombre del token devuelto al autorizarse
    tokenrequest=""# nombre del token al hacer las peticiones
    host=""# host de la api
    def __init__(self, sectoken, log,   ficherolog ,loglevel,host):        
        self.logger=logger(ficherolog,loglevel)
        if log==False: #Por defecto la clase logger arranca como true
            self.logger=False
        if not(sectoken==True or sectoken==False):
            self.sectoken=False
        else:
            self.sectoken=sectoken
        self.host= host   

    def settokenname(self,tparser,trequest):
        """Establece el nombre de lostoken para las request y para buscarlo cuando se recibe.

        Parameters
        ----------
        tparser : str
            nombre del token devuelto al autorizarse
        trequest : str  
            nombre del token al hacer las peticiones  
        
        """
        self.tokenparser=tparser #token 
        self.tokenrequest=trequest


    def _log(self,texto,level):
        """Escribe en el log

        Parameters
        ----------
        texto : str
            Texto a escribir en el log
        level : int  
            Nivel de severidad del log a escribir. Solo se escribe si esta variable supera al self.log valor
        
        """
        if self.logger:
            self.logger.hazlog((str(type(self))+texto),level)


    def _ProcessResponse(self,r):
        """Procesa la respuesta de  un request

        Parameters
        ----------
        r : request
            respuesta de la peticion request
        Returns -  Se debe validar con isinstance
        ----------
        r : request
            respuesta de la peticion request (si todo ha ido bien)    
        r : int
            returncode  de la peticion request (si ha habido problemas)    
        
        """
        
        if r.status_code == 200:
            self._log ("_ProcessResponse: Ok",4)
            return r
        else:
            self._log ("_ProcessResponse: Ha habido error en: " +r.url+ " con  codigo: "+str(r.status_code) + " con Error: "+ r.text,1)
            return r.status_code

    def setAuthVars(self,endpoint,payload, headers):
        """ establece las varaibles de seguridad necesarias para el request de autorizacion

        Parameters
        ----------
        endpoint : str
            endponint para obtener el token de seguridad
        payload : json
            payload para obtener la seguridad: usuario y clave
        headers : json
            headers para obtener la seguridad
        
        """
        self.secendpoint=endpoint
        self.secpayload=payload
        self.secheaders=headers

    def Auth(self):
        """ Realiza la Auth y guarda el token

        Returns
        ----------
        Bool : -
            Indica si ha sido posible o no hacer la Auth. False si hay status code distinto de 200
        Excepctions:
        
        --------- 
        ImposibleObtenerToken : En caso de que haya un fallo no espeerado        
        
        """
        r=self._ProcessResponse(requests.post(self.host+self.secendpoint, headers = self.secheaders,json = self.secpayload))   
        if isinstance(r,int):
            self._log ("Auth: No es posible hacer la Authenticicacion",1)
            return False
        else:
            self._log ("Auth: Autentificacion Correcta, ",1)
            y=json.loads(r.text)
            try:
                self.token=(y[self.tokenparser])
            except:
                self._log ("Auth: Imposible recoger la variable token: " +self.tokenparser+ " del Json response, ",1)
                raise ImposibleObtenerToken
            return True
    def CargaJsonFichero(self,archivo):
        """Lee un fichero json y lo carga en una variable

        Parameters
        ----------
        archivo: str
            Fichero donde se encuentra un json

        Returns
        ----------
        json : _
            objeto json con el fichero cargado
        """
        with open(archivo) as json_file:
            return json.load(json_file) 
    
    def _validsec(self):
        """ funcion que define si es necesario añadir un token de seguridad a las peticiones request en base a la confgiuracion de la clase
        """         
        if self.sectoken:
            if not self.token:
                if  not self.Auth():
                    raise ImposibleAuth
            self.authheader={self.tokenrequest : self.token}  

    def EjecutaRequest(self,funcion, parametros,payload):
        """ Funcion que ejecuta un request segun los parametros que se indican
        La funciona control la gestion de la uth en el caso de que la haya.
        
        Parameters
        ----------
        parametros : lista
             su longitud es variable ya que cada funcion requiere un numero de parametros. el nonce siempre va en la posicion 2        
             - parametros[1] es el header
        funcion : string
            nombre de la funcion que se llamara  

        Returns -  Se debe validar con isinstance
        ----------
        r : request
            respuesta de la peticion request (si todo ha ido bien)    
        r : int
            returncode  de la peticion request (si ha habido problemas)   

        """
        self._log ("EjecutaRequest: Llamado ",4)
        try :
            endpoint=parametros[0]
        except:
            endpoint=""
        try :
            header=parametros[1]
        except:
            header={}           
        self._validsec()
        if isinstance(self.authheader,dict):
            header.update(self.authheader)
        
        # antes del return tenemos que comprobar si ha devuelto un 401
        if payload=="":
            r=self._ProcessResponse(funcion(endpoint,headers=header))        
        else:
            r=self._ProcessResponse(funcion(endpoint,headers=header,json=payload))        
        if isinstance(r,int):
            self._log ("EjecutaRequest: Respondio con codigo "+ str(r),4)
            if r==401:
                #si es un 401 debo reautorizar el token
                self.token=""
                self._validsec()
                return funcion(headers=header)                                  
            else:
                # ha fallado por algun motivo desconocido
                self._log ("EjecutaRequest: Error no contemplado: "+ str(r),1)
                p=Response()
                p.status_code=int(r)
                p.code = "error"
                p.url=endpoint
                p.error_type = "error"                
                p._content = b"Fallo ya indicado en el mensaje anterior"                
                return p
        else:
            # Todo fue bien        
            return r


 
   
   