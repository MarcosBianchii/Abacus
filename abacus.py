class Archivo:
    def __init__(self, path, inicio):
        try:
            self.archivo = open(path, "r")
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: No se encontro el archivo {path}")
        
        self.lineas = [x.replace("\n", "") for x in self.archivo.readlines()]
        self.linea_actual = inicio
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.linea_actual < len(self.lineas):
            linea = self.lineas[self.linea_actual]
            self.linea_actual += 1
            return linea
        else:
            raise StopIteration

    def __getitem__(self, index):
        return self.lineas[index - 1]
    
    def __setitem__(self, index, value):
        try:
            self.lineas[index - 1] = value
        except IndexError:
            raise IndexError(f"El indice {index} no existe en el archivo {self.archivo.name}, se quizo acceder a la linea {index - 1}")

    def set_linea_actual(self, index):
        if index < 1 or index > len(self.lineas):
            raise IndexError(f"El indice {index} no existe en el archivo {self.archivo.name}, se quizo bifurcar a la linea {index - 1}")
        self.linea_actual = index

    def guardar(self):
        with open(self.archivo.name.split(".")[0] + ".ab", "w") as f:
            for linea in self.lineas:
                f.write(f"{linea}\n")
    
    def cerrar(self):
        self.archivo.close()

traduccion = {
    "0": "Carga Inmediata",
    "1": "Carga",
    "2": "Guardar",
    "3": "Sumar",
    "4": "Negar",
    "7": "Bifurcar si cero",
    "8": "Bifurcar si negativo",
    "9": "Bifurcar si positivo",
    "F": "Fin",
}


class LargoDeLineaIncorrecto(Exception):
    pass


class InterpreteAbacus:
    def __init__(self, path, inicio, debug=True):
        self.programa = Archivo(path, inicio)
        self.debug = debug
        self.acumulador = 0
        self.acciones = {
            "0": lambda x: self.carga_inmediata(int(x, 16)),
            "1": lambda x: self.carga(self.programa[int(x, 16)]),
            "2": lambda x: self.guardar(int(x, 16)),
            "3": lambda x: self.sumar(self.programa[int(x, 16)]),
            "4": lambda x: self.negar(),
            "7": lambda x: self.bifurcar(lambda: self.acumulador == 0, int(x, 16)),
            "8": lambda x: self.bifurcar(lambda: self.acumulador < 0, int(x, 16)),
            "9": lambda x: self.bifurcar(lambda: self.acumulador > 0, int(x, 16)),
            "F": lambda x: self.terminar_programa(),
        }

    def pad(self, num):
        return "".join(hex(num).split("x"))[:4].rjust(4, "0")

    def carga_inmediata(self, num):
        self.acumulador = num
        if self.acumulador >= (16**3 - 1) // 2:
            self.acumulador -= 16**3

    def carga(self, num):
        self.acumulador = num

    def guardar(self, index):
        self.programa[index] = self.pad(self.acumulador)

    def sumar(self, num):
        self.acumulador += int(num, 16)

    def negar(self):
        self.acumulador = ~self.acumulador
    
    def bifurcar(self, f, index):
        if f():
            self.programa.set_linea_actual(index)
        
    def terminar_programa(self):
        self.programa.guardar()
        raise StopIteration

    def __str__(self):
        return  "\n" + traduccion[self.programa[self.programa.linea_actual][0].upper()] + f" - {self.programa.linea_actual}\n" +\
                f"AC: {self.pad(self.acumulador)} = {self.acumulador}[10]\n" +\
                f"RI: {self.programa[self.programa.linea_actual]}"

    def ejecutar(self):
        for linea in self.programa:
            if len(linea) == 0:
                continue
            if len(linea) < 4:
                raise LargoDeLineaIncorrecto(f"Error en la linea {self.programa.linea_actual}: {linea}, largo de linea incorrecto")
                
            try:
                self.acciones.get(linea[0].upper(), None)(linea[1:4].upper())
                if self.debug:
                    print(self)

            except StopIteration:
                if self.debug:
                    print(f"{self}\n")
                break

            except TypeError:
                raise KeyError(f"Error en la linea {self.programa.linea_actual}: {linea}, no se reconoce la accion {linea[0]}")
        self.programa.cerrar()


from sys import argv

def printear_ayuda():
    print(f"\nUso: python3 {argv[0]} <archivo> [-i <inicio>] [-d]")
    print(f"  -i <inicio>: Indica el punto de carga del programa [16] (por defecto 0)")
    print(f"  -d: Muestra el estado del AC, el RI y su línea de código en la terminal en cada instrucción ejecutada (por defecto no)\n")


def conseguir_indice():
    try:
        return int(argv[argv.index("-i") + 1] if "-i" in argv else 0, 16)
    except IndexError:
        raise IndexError("No me pasaste el indice de inicio")
    except ValueError:
        raise ValueError("El indice no es un numero")


if __name__ == "__main__":
    if len(argv) < 2:
        printear_ayuda()
        exit()
    try:
        InterpreteAbacus(argv[1], conseguir_indice(), "-d" in argv).ejecutar()
    except Exception as e:
        print(e)
