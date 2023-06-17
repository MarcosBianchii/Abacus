# Interprete Abacus
---
## Uso

```sh
$ python3 abacus.py <archivo> [-i <indice>] [-d]
```

## Argumentos
* **archivo**: Archivo a interpretar.
* **indice**: Indice del punto de carga en base 10.
    - En caso de no especificarse ejecuta todo el archivo.
* **-d**: Flag de debug.
    - Muestra el estado del AC, el RI y su línea de código en la terminal por cada instrucción ejecutada.
    - En caso de no especificarse, no se muestra nada.
---
## Salida
* Al terminar de ejecutar el programa, se genera un nuevo archivo con el mismo nombre  pero con extensión ".ab" donde se guarda el resultado del programa ejecutado.
    - Las líneas no ejecutadas también se guardan en el archivo resultante.
---
## Comportamiento
* El programa se ejecuta hasta encontrar una instrucción con código de operación final (F). En caso de no encontrarla, se ejecuta hasta llegar al final del archivo pero no se guarda el resultado.
* Las lineas vacías son ignoradas.
---
## Tabla de traducción
* Se pueden cambiar en el código.

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
