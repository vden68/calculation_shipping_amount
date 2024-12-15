# from typing import Self
from typing_extensions import Self

from pydantic import BaseModel, Field, model_validator, computed_field


class InputShippingCost(BaseModel):
    distance: int = Field(gt=0, lt=10000, description="Расстояние до пункта назначения в км")
    width: int = Field(gt=0, lt=240, description="ширина груза в см")
    height: int = Field(gt=0, lt=240, description="высота грузав см")
    length: int = Field(gt=0, lt=240, description="длина груза в см")
    fragility: bool = Field(description="Хрупкий груз")
    workload: int = Field(gt=0, lt=5, default=1, description="Загруженность "
                                                             "1 - обычная"
                                                             "2 - повышенная"
                                                             "3 - высокая"
                                                             "4 - очень высокая")

    @computed_field
    def surcharge_fragility(self) -> float:
        if self.fragility:
            return 300.0
        else:
            return 0.0

    @computed_field
    def surcharge_distance(self) -> float:
        if self.distance > 30:
            return 300.0
        elif self.distance > 10:
            return 200.0
        elif self.distance > 2:
            return 100.0
        else:
            return 50.0

    @computed_field
    def surcharge_cargo_dimensions(self) -> float:
        if self.width > 100 or self.height > 100 or self.length > 100:
            return 200.0
        elif self.width < 10 and self.height < 10 and self.length < 10:
            return 100.0
        else:
            return 0.0

    @computed_field
    def surcharge_workload(self) -> float:
        if self.workload == 2:
            return 1.2
        elif self.workload == 3:
            return 1.4
        elif self.workload == 4:
            return 1.6
        else:
            return 1.0

    @model_validator(mode="after")
    def check_fragility(self) -> Self:
        if self.fragility and self.distance > 30:
            raise ValueError(
                "Хрупкие грузы нельзя возить на расстояние более 30 км"
            )
        return self
