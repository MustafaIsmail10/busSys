"""
This module contains some utility functions that is used in the whole project.

"""

import math


def euclidean_distance(x1, y1, x2, y2):
    """
    This Function takes the cordinates of 2 points and return the euclidean distance between them
    """
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def dotprod(a, b):
    """
    This function gives the dot product two points
    """
    product = a["x"] * b["x"]
    product += a["y"] * b["y"]
    return product


def subtract(a, b):
    """
    This function subtracts two points
    """
    c = {}
    c["x"] = a["x"] - b["x"]
    c["y"] = a["y"] - b["y"]
    return c


def add(a, b):
    """
    This function adds two points
    """
    c = {}
    c["x"] = a["x"] + b["x"]
    c["y"] = a["y"] + b["y"]
    return c


def multiply(cons, a):
    """
    This function multiplies a point with a constant
    """
    c = {}
    c["x"] = cons * a["x"]
    c["y"] = cons * a["y"]
    return c
