
# Crear entorno
```sh
python3 -m venv venv
```


# Activar en Ubuntu
```sh
source venv/bin/activate
```

# instalar dependencia 
```sh
pip install -r requirements.txt
```

# generar archivo requeriment 

```sh

pip freeze > requirements.txt
```


# ejecutar proyecto
```sh
export FLASK_APP=run.py
flask run
```