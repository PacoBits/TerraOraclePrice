import time,json
from excepciones import DatosIncompletos,SaldoInsuficiente




class logger:
    """Clase para escribir en un fichero de log
    Note
    ----
    No hereda de nadie.

    Parameters
    ----------
    ficherolog : str
        nombre del fichero (puede incluir la ruta) donde se escribe el log
    loglevel : int
        el nivel a partir de la cual se escribiran mensajes que superen dicho nivel

    Attributes
    ----------
    ficherolog : str
        nombre del fichero (puede incluir la ruta) donde se escribe el log
    loglevel : int
        el nivel a partir de la cual se escribiran mensajes que superen dicho nivel
    log : bool
        Indica si esta activo el logging    
    """
    
    def __init__(self, ficherolog,loglevel):
        self.log=True 
        """ indica si la clase escribe mensajes en pantalla o no """

        if not loglevel:
            self.loglevel=1 
        else:
            self.loglevel=loglevel
        if not ficherolog:
            self.ficherolog='salida_defecto.txt'
        else:
            self.ficherolog=ficherolog
        self.fw= None
        

    def __del__(self):         
        if self.fw:                         
            self.fw.close()
            self.fw=None
# === NuevoLog ===        
    def NuevoLog(self,fichero):
        """
        Abre un nuevo fichero de log

        Parameters
        ----------
        ficherolog : str
            nombre del fichero (puede incluir la ruta) donde se escribe el log    
        """    
        if self.fw:                  
            self.fw.close()
            self.fw=None
        self.ficherolog=fichero

# === hazlog ===
    def hazlog(self,texto,level):
        """
        Escribe el mensaje en el log si el level lo permite

        Parameters
        ----------
        texto : str
            nombre del fichero (puede incluir la ruta) donde se escribe el log    
        level : int
            nivel del mensaje    
        """
        if self.log:
            if (level<=self.loglevel):
                if not self.fw:                    
                    self.fw = open(self.ficherolog,'a')
                    self.fw.write(str(type(self))+'_log: Abierto Fichero: '+self.ficherolog+ '\n')
                    
                print(texto)
                self.fw.write(texto+ '\n')
                self.fw.flush()
                