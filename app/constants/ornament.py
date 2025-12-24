from enum import Enum


class OrnamentShape(str, Enum):
    acorn = "acorn"
    dongle = "dongle"
    soap = "soap"
    charlie = "charlie"
    candle = "candle"
    admin = "admin"


class OrnamentColor(str, Enum):
    yellow = "yellow"
    purple = "purple"
    pink = "pink"
    green = "green"
    blue = "blue"
    admin = "admin"


class PublicOrnamentShape(str, Enum):
    acorn = "acorn"
    dongle = "dongle"
    soap = "soap"
    charlie = "charlie"
    candle = "candle"


class PublicOrnamentColor(str, Enum):
    yellow = "yellow"
    purple = "purple"
    pink = "pink"
    green = "green"
    blue = "blue"
