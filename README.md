# Interprete Abacus

## Uso

```sh
$ python3 abacus.py <archivo> [-i <indice>] [-d]
```

## Argumentos
* **archivo**: Archivo a interpretar.
* **indice**: Indice del punto de carga en base 16.
    - En caso de no especificarse, el punto de carga es la linea 300[16].
* **-d**: Flag de debug.
    - Muestra el estado del PC, AC y RI por cada instrucción ejecutada.
    - En caso de no especificarse, no se muestra nada.
---
## Salida
* Al terminar de ejecutar el programa, se genera un nuevo archivo con el mismo nombre  pero con extensión ".ab" donde se guarda el resultado del programa ejecutado.
---
## Comportamiento
* El programa se ejecuta hasta encontrar una instrucción con código de operación final (F). En caso de no encontrarla, no se genera el archivo resultante.
* Las lineas vacías y que no comienzan con un numero hexadecimal válido de 3 dígitos son ignoradas.
* En caso de error, se detiene la ejecución del programa y se muestra por pantalla un mensage de error.
---
## Archivo ejemplo.txt
* Contiene un programa de prueba donde se suman los valores de una lista enlazada de 3 elementos. Su salida está en el archivo programa.ab.
---
## Tabla de traducción

| Código | Acción |
| ------ | ------ |
| 0 | Carga Inmediata |
| 1 | Carga desde Memoria |
| 2 | Almacenar en Memoria |
| 3 | Suma |
| 4 | Not |
| 7 | Bifurcar (AC == 0) |
| 8 | Bifurcar (AC < 0) |
| 9 | Bifurcar (AC > 0) |
| F | Fin |
