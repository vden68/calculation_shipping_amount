from app.schemas import InputShippingCost


class ShippingCost:
    """ """

    def __init__(self):
        """ """
        self.price_1_km = 10.0
        self.min_price = 400.0
        pass

    def shipping_cost(self, input_data: InputShippingCost):
        """ """
        shipping_price = (self.price_1_km * input_data.distance
                          + input_data.surcharge_fragility
                          + input_data.surcharge_distance
                          + input_data.surcharge_cargo_dimensions) * input_data.surcharge_workload

        if shipping_price <= self.min_price:
            shipping_price = self.min_price
        return shipping_price
