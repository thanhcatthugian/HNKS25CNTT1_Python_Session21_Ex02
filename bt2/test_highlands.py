import pytest
from bt2 import view_order_and_calc_total,high_quant
def test_calculate_total():
    test_order = [
        {"drink_id": "P1","name":"Phin Sữa Đá", "price": 35000, "quantity": 1},
        {"drink_id": "T1","name":"Trà Sen Vàng", "price": 45000, "quantity": 1}
    ]
    result = view_order_and_calc_total(test_order)
    expected = 80000
    assert result == expected

def test_invalid_quantity():
    high_quant(-5) =="InvalidQuantityError"