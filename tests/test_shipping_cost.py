import allure
import pytest
from pydantic import  ValidationError

from app.schemas import InputShippingCost
from app.shipping_cost import ShippingCost


test_data = [
    (InputShippingCost(distance=10, width=10, height=10, length=10, fragility=False, workload=1), 400.0),
    (InputShippingCost(distance=10, width=10, height=10, length=10, fragility=True, workload=1), 500.0),
    (InputShippingCost(distance=25, width=10, height=10, length=10, fragility=False, workload=1), 450.0),
    (InputShippingCost(distance=35, width=10, height=10, length=10, fragility=False, workload=2), 780.0),
    (InputShippingCost(distance=25, width=10, height=10, length=10, fragility=False, workload=3), 630.0),
    (InputShippingCost(distance=25, width=10, height=10, length=10, fragility=False, workload=4), 720.0),
    (InputShippingCost(distance=25, width=105, height=10, length=10, fragility=False, workload=1), 650.0),
    (InputShippingCost(distance=25, width=10, height=105, length=10, fragility=False, workload=1), 650.0),
    (InputShippingCost(distance=25, width=10, height=10, length=105, fragility=False, workload=1), 650.0),
    (InputShippingCost(distance=25, width=5, height=5, length=5, fragility=False, workload=1), 550.0),
    (InputShippingCost(distance=25, width=5, height=50, length=50, fragility=False, workload=1), 450.0)
]

validation_data = [
    (35, 10, 10, 10, True, 1),
    (-35, 10, 10, 10, False, 1),
    (10001, 10, 10, 10, True, 1),
    (0, 10, 10, 10, True, 1),
    (10, 10, 10, 10, 5, 1),
    (10, 10, 10, 10, False, 10),
    (10, 0, 10, 10, True, 1),
    (10, 10, 0, 10, False, 1),
    (10, 10, 10, 0, True, 1),
    (10, 10, 10, 10, True, 0),
    (10, 250, 10, 10, False, 1),
    (10, 10, 250, 10, True, 1),
    (10, 10, 10, 250, False, 1)

]

@allure.epic("shipping_cost")
@allure.title("Тестирование shipping_cost.py с данными (test_data)")
@pytest.mark.parametrize("input_data, shipping_price", test_data)
def test_shipping_cost(input_data, shipping_price):
    shipping_cost = ShippingCost().shipping_cost(input_data=input_data)
    print("shipping_cost=" + str(shipping_cost))
    assert shipping_cost == shipping_price

@allure.epic("shipping_cost")
@allure.title("Тестирование валидации данных shipping_cost.py с данными (validation_data)")
@pytest.mark.parametrize("distance, width, height, length, fragility, workload", validation_data)
def test_validation_data(distance, width, height, length, fragility, workload):
    except_validation_data = False
    try:
        validation_data = InputShippingCost(distance=distance, width=width, height=height,
                                        length=length, fragility=fragility, workload=workload)
    except ValidationError as e:
        print(str(e.json()))
        except_validation_data = True
    assert except_validation_data



