class Error(Exception):
    """Clase base para excepciones en el módulo."""
    def __init__(self, codigo, message):
       # Call the base class constructor with the parameters it needs
        super(Error, self).__init__(message)

class FalloTX(Exception):
    """Excepcion indica fallo de transaccion """   
    def __init__(self, expresion, mensaje):
        super(FalloTX, self).__init__(mensaje)
        self.expresion = expresion
        self.mensaje = mensaje

class DatosIncompletos(Exception):
    """Excepcion indica datos incompletos por lo que no se puede ejecutgar una transaccion """   
    def __init__(self, expresion, mensaje):
        super(DatosIncompletos, self).__init__(mensaje)
        self.expresion = expresion
        self.mensaje = mensaje      

class ProblemasDominio(Exception):
    """Excepcion indica que existen problemas para registrar un dominio, posiblemente por no ser valido """   
    def __init__(self, expresion, mensaje):
        super(ProblemasDominio, self).__init__(mensaje)
        self.expresion = expresion
        self.mensaje = mensaje      

class SaldoInsuficiente(Exception):
    """Excepcion indica que hay menos saldo del que se quiere enviar en la cuenta """   
    def __init__(self, mensaje):
        super(SaldoInsuficiente, self).__init__(mensaje)        
        self.mensaje = mensaje 

class DominioYaRegistrado(Exception):
    """Excepcion indica que el dominio ya esta registrado y no se puedo continuar con el registro """   
    def __init__(self, mensaje):
        super(DominioYaRegistrado, self).__init__(mensaje)        
        self.mensaje = mensaje 


class ProblemaNodoETH(Exception):
    """Excepcion indica que no hay conexion con el nodo ETH """   
    def __init__(self, mensaje):
        super(ProblemaNodoETH, self).__init__(mensaje)        
        self.mensaje = mensaje         

class AddressNovalida(Exception):
    """Excepcion indica que la direccion de ethereum no es valida """   
    def __init__(self, mensaje):
        super(AddressNovalida, self).__init__(mensaje)        
        self.mensaje = mensaje


class ImposibleEsperarTX(Exception):
    """Excepcion indica que habia orden de esperar la ejecusion de una transaccion sin reintetarla, pero esto no es posible debido a fallos con el nonce o underprice. 
    Habitualmente  producidos por la ejecucion en paralelo del proceso"""   
    def __init__(self, expresion, mensaje):
        super(ImposibleEsperarTX, self).__init__(mensaje)
        self.expresion = expresion
        self.mensaje = mensaje

class ImposibleObtenerToken(Exception):
    """Excepcion indica que habia orden de esperar la ejecusion de una transaccion sin reintetarla, pero esto no es posible debido a fallos con el nonce o underprice. 
    Habitualmente  producidos por la ejecucion en paralelo del proceso"""   
    def __init__(self, expresion, mensaje):
        super(ImposibleObtenerToken, self).__init__(mensaje)
        self.expresion = expresion
        self.mensaje = mensaje

class ImposibleAuth(Exception):
    """Excepcion indica que no ha sido posible realizar la auth de la api"""   
    def __init__(self, expresion, mensaje):
        super(ImposibleAuth, self).__init__(mensaje)
        self.expresion = expresion
        self.mensaje = mensaje

class ImposibleSetAddress(Exception):
    """Excepcion indica que la direccion de ethereum no es valida """   
    def __init__(self, mensaje):
        super(ImposibleSetAddress, self).__init__(mensaje)        
        self.mensaje = mensaje        

class ImposibleSetResolver(Exception):
    """Excepcion indica que la direccion de ethereum no es valida """   
    def __init__(self, mensaje):
        super(ImposibleSetResolver, self).__init__(mensaje)        
        self.mensaje = mensaje  
class TransAndDelegatedConflicto(Exception):
    """Excepcion indica que la direccion de ethereum no es valida """   
    def __init__(self, mensaje):
        super(TransAndDelegatedConflicto, self).__init__(mensaje)        
        self.mensaje = mensaje  
class AccionBBDDNoDefinida(Exception):
    """Excepcion indica que no se encuentra esas accion en la base de datos por lo que no se puede ejecutar ninguna logica """   
    def __init__(self, mensaje):
        super(AccionBBDDNoDefinida, self).__init__(mensaje)        
        self.mensaje = mensaje  
class DominioExpirado(Exception):
    """Excepcion indica que el dominio ha expirado """   
    def __init__(self, mensaje):
        super(DominioExpirado, self).__init__(mensaje)        
        self.mensaje = mensaje
class DominioLibre(Exception):
    """Excepcion indica que el dominio esta libre"""   
    def __init__(self, mensaje):
        super(DominioLibre, self).__init__(mensaje)        
        self.mensaje = mensaje          
class ImposibleSetMC(Exception):
    """Excepcion indica que no se puede estables un Multicoin al dominio"""   
    def __init__(self, mensaje):
        super(ImposibleSetMC, self).__init__(mensaje)        
        self.mensaje = mensaje 
class ImposibleSetText(Exception):
    """Excepcion indica que no se puede estables un Multicoin al dominio"""   
    def __init__(self, mensaje):
        super(ImposibleSetText, self).__init__(mensaje)        
        self.mensaje = mensaje 
class AutoGestionSCNoActiva(Exception):
    """Excepcion indica que se debe tener la autogestionactiva de SC"""   
    def __init__(self, mensaje):
        super(ImposibleSetText, self).__init__(mensaje)        
        self.mensaje = mensaje         



        

        