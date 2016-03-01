# -*- coding: utf-8 -*-
"""
Last mod: Feb 2016
@author: Juan A. Fernández
@about: Fichero de creación de la interfaz de interacción con la relacion Matricula de la base de datos.
"""

import MySQLdb
#Doc here: http://mysql-python.sourceforge.net/MySQLdb-1.2.2/
from Matricula import *

#Variable global de para act/desactivar el modo verbose para imprimir mensajes en terminal.
v=0

'''Clase controladora de Matriculas. Que usando la clase que define el modelo de Matricula (la info en BD que de el se guarda)
ofrece una interface de gestión que simplifica y abstrae el uso.
'''
class GestorMatriculas:
    """
    Manejador de Matriculas de la base de datos.
    """

    @classmethod
    def nuevaMatricula(self, id_asignatura, id_curso, id_alumno):

        db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="smm"); #La conexión está clara.
        #query="INSERT INTO Matricula values("+"'"+nombre+"', "+ "'"+id+"');"

        #Añadimos al principio y al final una comilla simple a todos los elementos.
        id_asignatura='\''+id_asignatura+'\''
        id_curso='\''+id_curso+'\''
        id_alumno='\''+id_alumno+'\''

        query="INSERT INTO Matricula VALUES("+id_asignatura+","+id_curso+","+id_alumno+");"
        if v:
            print '\n'+query
        cursor = db.cursor()
        salida =''
        '''
        Como la ejecución de esta consulta (query) puede producir excepciones como por ejemplo que el Matricula con clave
        que estamos pasando ya exista tendremos que tratar esas excepciones y conformar una respuesta entendible.
        '''

        try:
            salida = cursor.execute(query);
        except MySQLdb.Error, e:
            # Get data from database
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
                print "Error number: "+str(e.args[0])
                salida=e.args[0]
            except IndexError:
                print "MySQL Error: %s" % str(e)

        #Efectuamos los cambios
        db.commit()
        cursor.close()
        db.close()

        if salida==1:
            return 'OK'
        if salida==1062:
            return 'Elemento duplicado'
        if salida=='1452':
            return 'Alguno de los elementos no existe'


    @classmethod
    def getMatriculas(self):
        db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="smm")
        cursor = db.cursor()

        #Sacando los acentos...........
        mysql_query="SET NAMES 'utf8'"
        cursor.execute(mysql_query)
        #-----------------------------#

        query="select * from Matricula"
        if v:
            print '\n'+query
        cursor.execute(query)
        row = cursor.fetchone()

        lista = []

        while row is not None:
            matricula = Matricula()
            matricula.id_asignatura=row[0]
            matricula.id_curso=row[1]
            matricula.id_alumno=row[2]

            lista.append(curso)
            #print row[0], row[1]
            row = cursor.fetchone()

        cursor.close()
        db.close()

        return lista

        #Una de las opciones es convertirlo en un objeto y devolverlo

    @classmethod
    def getMatricula(self, id_asignatura, id_curso, id_alumno):
        """
        Recupera TODA la información de un Matricula en concreto a través de la clave primaria, su id.
        """
        db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="smm"); #La conexión está clara.
        cursor = db.cursor()

        id_asignatura='\''+id_asignatura+'\''
        id_curso='\''+id_curso+'\''
        id_alumno='\''+id_alumno+'\''

        query="select * from Matricula where id_asignatura="+id_asignatura+" and id_curso="+id_curso+" and id_alumno="+id_alumno+";"
        if v:
            print '\n'+query
        try:
            salida = cursor.execute(query);
            row = cursor.fetchone()
        except MySQLdb.Error, e:
            # Get data from database
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
                print "Error number: "+str(e.args[0])
                #Capturamos el error:
                salida=e.args[0]
            except IndexError:
                print "MySQL Error: %s" % str(e)

        cursor.close()
        db.close()

        if salida==1:
            #Como se trata de toda la información al completo usaremos todos los campos de la clase Matricula.
            #La api del mservicio envia estos datos en JSON sin comprobar nada
            matricula = Matricula()
            matricula.id_asignatura=row[0]
            matricula.id_curso=row[1]
            matricula.id_alumno=row[2]

            return matricula
        if salida==0:
            return 'Elemento no encontrado'

    '''
    @classmethod
    def modMatricula(self, id_asignatura, id_curso, campoACambiar, nuevoValor):
        """
        Esta función permite cambiar cualquier atributo de una Matricula.
        Parámetros:
        campoACambiar: nombre del atributo que se quiere cambiar
        nuevoValor: nuevo valor que se quiere guardar en ese campo.

        Este caso puede ser delicado al tener sólo dos atributos y ambos ser claves foráneas. Por eso no permitiremos que
        se haga, para modificar la relación antes tendremos que destruirla y volverla a crear.

        """
        db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="smm"); #La conexión está clara.
        nuevoValor='\''+nuevoValor+'\''
        id_asignatura='\''+id_asignatura+'\''
        id_curso='\''+id_curso+'\''

        query="UPDATE Matricula SET "+campoACambiar+"="+nuevoValor+" WHERE id_asignatura="+id_asignatura+" and id_curso="+id_curso+";"
        if v:
            print '\n'+query

        cursor = db.cursor()
        salida =''
        '''
        #Como la ejecución de esta consulta (query) puede producir excepciones como por ejemplo que el Matricula con clave
        #que estamos pasando ya exista tendremos que tratar esas excepciones y conformar una respuesta entendible.
    '''
        try:
            salida = cursor.execute(query);
        except MySQLdb.Error, e:
            # Get data from database
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
                print "Error number: "+str(e.args[0])
                salida=e.args[0]
            except IndexError:
                print "MySQL Error: %s" % str(e)

        #Efectuamos los cambios
        db.commit()
        cursor.close()
        db.close()

        if salida==1:
            return 'OK'
        elif salida==1062:
            return 'Elemento duplicado'
        elif salida==0:
            return 'Elemento no encontrado'
    '''
    @classmethod
    def delMatricula(self, id_asignatura, id_curso, id_alumno):
        db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="smm"); #La conexión está clara.
        cursor = db.cursor()
        id_asignatura='\''+id_asignatura+'\''
        id_curso='\''+id_curso+'\''
        id_alumno='\''+id_alumno+'\''
        query="delete from Matricula where id_asignatura="+id_asignatura+" and id_curso="+id_curso+" and id_alumno="+id_alumno+";"
        if v:
            print query
        salida =''
        try:
            salida = cursor.execute(query);
        except MySQLdb.Error, e:
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
                print "Error number: "+str(e.args[0])
                salida=e.args[0]
            except IndexError:
                print "MySQL Error: %s" % str(e)

        db.commit()
        cursor.close()
        db.close()

        if salida==1:
            return 'OK'
        if salida==0:
            return 'Elemento no encontrado'