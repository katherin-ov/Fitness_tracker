from dataclasses import dataclass
from typing import Type, Dict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    INFO_MESSAGE: str = (
        "Тип тренировки: {0}; "
        "Длительность: {1:.3f} ч.; "
        "Дистанция: {2:.3f} км; "
        "Ср. скорость: {3:.3f} км/ч; "
        "Потрачено ккал: {4:.3f}."
    )

    def get_message(self) -> str:
        return self.INFO_MESSAGE.format(
            self.training_type,
            self.duration,
            self.distance,
            self.speed,
            self.calories)


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    action: int
    duration: float
    weight: float

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
    ) -> None:
        self.action = action
        self.weight = weight
        self.duration = duration

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            "Определите get_spent_calories в %s." % (self.__class__.__name__)
        )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_message = InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )
        return info_message


class Running(Training):
    """Тренировка: бег."""

    COEFF_1: int = 18
    COEFF_2: int = 20
    MIN_IN_HOUR: int = 60

    def get_spent_calories(self) -> float:
        return (
            (self.COEFF_1 * self.get_mean_speed() - self.COEFF_2)
            * self.weight
            / self.M_IN_KM
            * self.duration
            * self.MIN_IN_HOUR
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_1: float = 0.035
    COEFF_2: float = 0.029
    MIN_IN_HOUR: int = 60

    def __init__(
        self, action: int, duration: float, weight: float, height: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height


    def get_spent_calories(self) -> float:
        return (
            (
                self.COEFF_1 * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.COEFF_2
                * self.weight
            )
            * self.duration
            * self.MIN_IN_HOUR
        )


class Swimming(Training):
    """Тренировка: плавание."""

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: int,
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    LEN_STEP: float = 1.38
    COEFF_1:  float = 1.1
    COEFF_2: int = 2

    def get_mean_speed(self) -> float:
        return (
            (
                self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration
            )
        )

    def get_spent_calories(self) -> float:
        return (self.get_mean_speed() + self.COEFF_1) * \
            self.COEFF_2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type: Dict[str, Type[Training]] = {
        "SWM": Swimming,
        "RUN": Running,
        "WLK": SportsWalking,
    }
    return training_type[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == "__main__":
    packages = [
        ("SWM", [720, 1, 80, 25, 40]),
        ("RUN", [15000, 1, 75]),
        ("WLK", [9000, 1, 75, 180]),
    ]
    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
