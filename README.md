# DjangoSalesModule

## Introduction

Proyecto para la materia de HDP115, un modulo de ventas para un ERP

![imagen](https://github.com/devmariomtz/DjangoSalesModule/assets/99843020/dfa3f88e-e6c5-4eb1-9299-98928b596b8e)


### Características

* Login con roles

* Modulo de cotizaciones 

* Gestión de proveedores

* Inventario de productos

# Uso

Estos son los paso para utilizar el presente proyecto

### Usando virtualenv

Si su proyecto ya está en un virtualenv python3 existente, instale primero django ejecutando

    $ pip install django
    
Y luego ejecuta el comando `django-admin.py` para iniciar el nuevo proyecto:

    $ django-admin.py startproject \
      --template=https://github.com/devmariomtz/DjangoSalesModule/tree/main \
      --extension=py,md \
      <project_name>
      
### No virtualenv

Esto asume que `python3` está enlazado a una instalación válida de python 3 y que `pip` está instalado y `pip3` es válido
para instalar paquetes de python 3.

Se recomienda instalar dentro de virtualenv, sin embargo puedes iniciar tu proyecto sin virtualenv también.

Si no tienes django instalado para python 3 entonces ejecuta:

    $ pip3 install django
    
Y luego:

    $ python3 -m django startproject \
      --template=https://github.com/devmariomtz/DjangoSalesModule/tree/main \
      --extension=py,md \
      <project_name>
      
      
Después de eso, simplemente instale las dependencias locales, ejecute las migraciones e inicie el servidor.


# Iniciando

Primero clona el repositorio desde Github y cambia al nuevo directorio:

    $ git clone git@github.com:devmariomtz/DjangoSalesModule.git
    $ cd DjangoSalesModule
    
Active el virtualenv para su proyecto.
    
Instala las dependencias del proyecto:

    $ pip install -r requirements.txt


    
A continuación, basta con aplicar las migraciones:

    $ python manage.py migrate
    
Agrega un archivo `.env` en el root del proyecto con las siguientes variables
```
 SECRET_KEY=""
 DB_ENGINE=""
 DB_NAME=""
 DB_USER=""
 DB_PASSWORD=""
 DB_HOST=""
 DB_PORT=""
```

Ahora puede ejecutar el servidor de desarrollo:

    $ python manage.py runserver
