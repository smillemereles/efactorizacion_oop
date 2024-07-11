import tkinter as tk 
from tkinter import messagebox 
import heapq

class Nodo:
    def __init__(self, posicion, costo_g, costo_h, padre):
        self.posicion = posicion
        self.costo_g = costo_g
        self.costo_h = costo_h
        self.costo_f = costo_g + costo_h
        self.padre = padre

    def __lt__(self, otro):
        return self.costo_f < otro.costo_f

class Mapa:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.grid = [[0 for _ in range(columnas)] for _ in range(filas)]

    def set_celda(self, fila, columna, valor):
        self.grid[fila][columna] = valor

    def get_celda(self, fila, columna):
        return self.grid[fila][columna]

    def es_valido(self, fila, columna):
        return 0 <= fila < self.filas and 0 <= columna < self.columnas

    def obtener_vecinos(self, nodo):
        vecinos = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nueva_fila, nueva_columna = nodo.posicion[0] + dx, nodo.posicion[1] + dy
            if self.es_valido(nueva_fila, nueva_columna):
                terreno = self.get_celda(nueva_fila, nueva_columna)
                if terreno == 0:
                    costo = 1
                elif terreno == 2:
                    costo = 3
                elif terreno == 3:
                    costo = 5
                else:
                    continue
                vecinos.append(((nueva_fila, nueva_columna), costo))
        return vecinos

class CalculadoraRutas:
    @staticmethod
    def heuristica(a, b):
        return abs(b[0] - a[0]) + abs(b[1] - a[1])

    @staticmethod
    def a_estrella(mapa, inicio, objetivo):
        nodo_inicial = Nodo(inicio, 0, CalculadoraRutas.heuristica(inicio, objetivo), None)
        lista_abierta = [nodo_inicial]
        conjunto_cerrado = set()

        while lista_abierta:
            nodo_actual = heapq.heappop(lista_abierta)

            if nodo_actual.posicion == objetivo:
                camino = []
                while nodo_actual:
                    camino.append(nodo_actual.posicion)
                    nodo_actual = nodo_actual.padre
                return camino[::-1]

            conjunto_cerrado.add(nodo_actual.posicion)

            for posicion_vecino, costo_vecino in mapa.obtener_vecinos(nodo_actual):
                if posicion_vecino in conjunto_cerrado:
                    continue

                vecino = Nodo(posicion_vecino,
                              nodo_actual.costo_g + costo_vecino,
                              CalculadoraRutas.heuristica(posicion_vecino, objetivo),
                              nodo_actual)

                if vecino not in lista_abierta:
                    heapq.heappush(lista_abierta, vecino)
                else:
                    idx = lista_abierta.index(vecino)
                    if lista_abierta[idx].costo_g > vecino.costo_g:
                        lista_abierta[idx] = vecino
                        heapq.heapify(lista_abierta)

        return None

class InterfazBuscadorRutas:
    def __init__(self, maestro):
        self.maestro = maestro
        self.maestro.title("Calculadora de Rutas")
        self.mapa = Mapa(20, 20)
        self.inicio = None
        self.objetivo = None
        self.tamano_celda = 30

        self.lienzo = tk.Canvas(self.maestro, width=600, height=600)
        self.lienzo.pack()

        self.dibujar_cuadricula()

        self.lienzo.bind("<Button-1>", self.al_hacer_clic)
        
        self.boton_limpiar = tk.Button(self.maestro, text="Limpiar", command=self.limpiar_mapa)
        self.boton_limpiar.pack()
        
        self.boton_encontrar_ruta = tk.Button(self.maestro, text="Encontrar Ruta", command=self.encontrar_ruta)
        self.boton_encontrar_ruta.pack()

    def dibujar_cuadricula(self):
        for i in range(self.mapa.filas):
            for j in range(self.mapa.columnas):
                x1 = j * self.tamano_celda
                y1 = i * self.tamano_celda
                x2 = x1 + self.tamano_celda
                y2 = y1 + self.tamano_celda
                self.lienzo.create_rectangle(x1, y1, x2, y2, fill="white", outline="gray")

    def al_hacer_clic(self, evento):
        columna = evento.x // self.tamano_celda
        fila = evento.y // self.tamano_celda
        
        if not self.inicio:
            self.inicio = (fila, columna)
            self.colorear_celda(fila, columna, "green")
        elif not self.objetivo:
            self.objetivo = (fila, columna)
            self.colorear_celda(fila, columna, "red")
        else:
            if self.mapa.get_celda(fila, columna) == 0:
                self.mapa.set_celda(fila, columna, 1)
                self.colorear_celda(fila, columna, "black")
            else:
                self.mapa.set_celda(fila, columna, 0)
                self.colorear_celda(fila, columna, "white")

    def colorear_celda(self, fila, columna, color):
        x1 = columna * self.tamano_celda
        y1 = fila * self.tamano_celda
        x2 = x1 + self.tamano_celda
        y2 = y1 + self.tamano_celda
        self.lienzo.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

    def limpiar_mapa(self):
        self.mapa = Mapa(20, 20)
        self.inicio = None
        self.objetivo = None
        self.dibujar_cuadricula()

    def encontrar_ruta(self):
        if not self.inicio or not self.objetivo:
            messagebox.showerror("Error", "Por favor, seleccione un punto de inicio y un punto final.")
            return

        camino = CalculadoraRutas.a_estrella(self.mapa, self.inicio, self.objetivo)
        if camino:
            for fila, columna in camino[1:-1]:
                self.colorear_celda(fila, columna, "yellow")
        else:
            messagebox.showinfo("Resultado", "No se encontró un camino.")

def main():
    raiz = tk.Tk()
    app = InterfazBuscadorRutas(raiz)
    raiz.mainloop()

if __name__ == "__main__":
    main()