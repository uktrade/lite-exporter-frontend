from _decimal import Decimal


def get_total_goods_value(goods: list):
    total_value = 0
    for good in goods:
        total_value += Decimal(good["value"]).quantize(Decimal(".01"))
    return total_value
