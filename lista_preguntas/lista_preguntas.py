#!/usr/bin/env python3
# = ^ . ^ =
#
# Andrés Hernández (tonejito)
#
# This software is licensed under the terms of the BSD-2-Clause license
#
# https://opensource.org/licenses/BSD-2-Clause

"""
Genera un conjunto de listas con números de pregunta aleatorios

La salida es una lista de listas de enteros compatible con JSON
"""

import os
import sys
import json
import random
import argparse

# Toma los valores desde variables de entorno
DEBUG = os.environ.get("DEBUG", False)
# Número total de preguntas disponibles
PREGUNTAS = os.environ.get("PREGUNTAS", 100)
# Número máximo de preguntas a realizar
TAMAÑO = os.environ.get("TAMAÑO", 10)
# Número de diapositivas de título
IGNORA = os.environ.get("IGNORA", 1)
# Número de página de la pregunta inicial
INICIO = IGNORA + 1
# Número de página de la pregunta final
FIN = INICIO + PREGUNTAS


def parse_arguments():
    """
    Interpreta los argumentos de línea de comandos
    """
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "-n",
        "--preguntas",
        type=int,
        default=PREGUNTAS,
        help="Número total de preguntas disponibles",
    )
    parser.add_argument(
        "-s",
        "--tamaño",
        type=int,
        default=TAMAÑO,
        help="Número máximo de preguntas a realizar",
    )
    parser.add_argument(
        "-i",
        "--ignora",
        type=int,
        default=IGNORA,
        help="Número de diapositivas de título",
    )
    args = parser.parse_args()
    return args


def separa_lista(lista, num):
    """
    # https://www.geeksforgeeks.org/break-list-chunks-size-n-python/
    Separa una lista en fragmentos de tamaño 'num'
    El último fragmento puede ser de longitud menor a 'num'
    """
    for i in range(0, len(lista), num):
        yield lista[i : i + num]


def revisa_lista(lista):
    """
    Revisa la lista y regresa verdadero si algún elemento
    tiene valores consecutivos con el elemento siguiente
    """
    resultado = False
    rango = 2
    if DEBUG:
        print(".", end="", file=sys.stderr)
    for i in range(len(lista)):
        actual = lista[i]
        if i < len(lista) - 1:
            sig = lista[i + 1]
            if actual in range(sig - rango, sig + rango):
                resultado = True
    return resultado


# Código principal
if __name__ == "__main__":
    # Interpreta los argumentos de línea de comandos
    args = parse_arguments()
    # Número de página de la pregunta inicial
    INICIO = args.ignora + 1
    # Número de página de la pregunta final
    FIN = INICIO + args.preguntas

    # Genera la lista de preguntas desde un rango
    lista = list(range(INICIO, FIN))

    # Vuelve a mezclar si hay preguntas consecutivas
    while revisa_lista(lista) is True:
        random.shuffle(lista)
    if DEBUG:
        print("", file=sys.stderr)

    # Divide la lista en segmentos de tamaño fijo
    lista_separada = list(separa_lista(lista, args.tamaño))

    # Da formato e imprime el resultado
    lista_json = json.dumps(lista_separada)
    lista_json = lista_json.replace("[[", "[\n  [")
    lista_json = lista_json.replace("], [", "],\n  [")
    lista_json = lista_json.replace("]]", "]\n]")
    print(lista_json)
