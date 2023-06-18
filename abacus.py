from csv import reader
from sys import argv


def pad(num, n):
    return "".join(num.split("x"))[4-n:4].rjust(n, "0").upper()


class Programa:
    def __init__(self, path, inicio):
        if len(inicio) > 3 or int(inicio, 16) > int("999", 16):
            raise ValueError(f"El punto de carga ({inicio}) es mayor a 999[16]")
        if int(inicio, 16) < 0:
            raise ValueError(f"El punto de carga ({inicio}) debe ser un número positivo")

        try:
            archivo = open(path)
            self.memoria = {i[0]:i[1] for i in reader(archivo, delimiter=" ") if len(i) > 1}
            self.nombre_archivo = archivo.name
            archivo.close()
        except FileNotFoundError:
            raise FileNotFoundError(f"No se encontró el archivo {path}")
        
        self.linea_actual = inicio
        self.linea_anterior = ""

    def __iter__(self):
        return self
    
    def __next__(self):
        try:
            ri = self.memoria[self.linea_actual]
        except KeyError:
            raise StopIteration
        self.linea_anterior = self.linea_actual
        self.linea_actual = pad(hex(int(self.linea_actual, 16) + 1), 3)
        return ri        

    def __getitem__(self, index):
        index = pad(hex(int(index, 16)), 3)
        ri = self.memoria.get(index, None)
        if ri is None:
            raise IndexError(f"Se quizo acceder a la linea {index} y no existe")
        return ri
    
    def __setitem__(self, index, value):
        self.memoria.update({index: value})

    def set_linea_actual(self, index):
        self.linea_actual = index

    def guardar(self):
        with open(self.nombre_archivo.split(".")[0] + ".ab", "w") as f:
            linea_anterior = ""
            for i in sorted(self.memoria.items()):
                try:
                    if linea_anterior != pad(hex(int(i[0], 16) - 1), 3) and linea_anterior != "":
                        f.write("...\n")
                except ValueError:
                    continue
                f.write(f"{i[0]} {i[1]}\n")
                linea_anterior = i[0]


traduccion = {
    "0": "Carga Inmediata",
    "1": "Carga",
    "2": "Guardado",
    "3": "Suma",
    "4": "Negación",
    "7": "Bifurca si cero",
    "8": "Bifurca si negativo",
    "9": "Bifurca si positivo",
    "F": "Fín",
}


class InterpreteAbacus:
    def __init__(self, path, inicio="300", debug=False):
        self.programa = Programa(path, inicio)
        self.acumulador = 0
        self.debug = debug
        self.acciones = {
            "0": lambda x: self.carga_inmediata(int(x, 16)),
            "1": lambda x: self.carga(int(self.programa[x], 16)),
            "2": lambda x: self.guardar(x),
            "3": lambda x: self.sumar(int(self.programa[x], 16)),
            "4": lambda x: self.negar(),
            "7": lambda x: self.bifurcar(lambda: self.acumulador == 0, x),
            "8": lambda x: self.bifurcar(lambda: self.acumulador < 0, x),
            "9": lambda x: self.bifurcar(lambda: self.acumulador > 0, x),
            "F": lambda x: self.terminar_programa(),
        }

    def ac_pad(self, num):
        b = bin(num*1 if num < 0 else num)
        b = b[b.index("b")+1:].rjust(16, "0" if num >= 0 else "1")
        return hex(int(b, 2))[2:].rjust(4, "0").upper()

    def verificar_acumulador(self, n):
        if self.acumulador >= (16**n - 1) // 2:
            self.acumulador -= 16**n

    def carga_inmediata(self, num):
        self.acumulador = num
        self.verificar_acumulador(3)

    def carga(self, num):
        self.acumulador = num
        self.verificar_acumulador(4)

    def guardar(self, index):
        self.programa[index] = self.ac_pad(self.acumulador)

    def sumar(self, num):
        self.acumulador += num
        self.verificar_acumulador(4)

    def negar(self):
        self.acumulador = ~self.acumulador
    
    def bifurcar(self, f, index):
        if f():
            self.programa.set_linea_actual(index)
        
    def terminar_programa(self):
        self.programa.guardar()
        raise StopIteration

    def __str__(self):
        return  f"\n{traduccion[self.programa[self.programa.linea_anterior][0].upper()]}\n" +\
                f" PC: {self.programa.linea_anterior}\n" +\
                f" RI: {self.programa[self.programa.linea_anterior]}\n" +\
                f" AC: {self.ac_pad(self.acumulador)}"

    def ejecutar(self):
        for ri in self.programa:
            if len(ri) < 4:
                raise ValueError(f"El largo de la linea {self.programa.linea_anterior} que contiene {ri} es incorrecto")
                
            try:
                self.acciones[ri[0].upper()](ri[1:4].upper())
                if self.debug:
                    print(self)

            except StopIteration:
                if self.debug:
                    print(f"{self}\n")
                break

            except KeyError:
                raise KeyError(f"No se reconoce el código de acción de {ri} en la linea {self.programa.linea_anterior}")


def printear_ayuda():
    print(f"\nUso: python3 {argv[0]} <archivo> [-i <inicio>] [-d]")
    print(f"  <archivo>:   Archivo con el programa a ejecutar")
    print(f"  -i <inicio>: Indica el punto de carga del programa [16] (por defecto 300)")
    print(f"  -d:          Muestra el estado del AC, el RI y su línea de código en la terminal en cada instrucción ejecutada (por defecto no)\n")


def conseguir_indice():
    try:
        return argv[argv.index("-i") + 1] if "-i" in argv else "300"
    except IndexError:
        raise IndexError("No me pasaste el índice de inicio")


if __name__ == "__main__":
    if len(argv) < 2:
        printear_ayuda()
        exit()
    try:
        InterpreteAbacus(argv[1], conseguir_indice(), "-d" in argv).ejecutar()
    except Exception as e:
        print(e)
