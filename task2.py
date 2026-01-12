"""
Task 2: Dineable and Refuelable Interfaces
Interface segregation with concrete implementations and statistics tracking.
"""
from abc import ABC, abstractmethod
import unittest


class Dineable(ABC):
    """Abstract interface for dining services."""
    
    @abstractmethod
    def serve_dinner(self, car_id: int) -> None:
        """Serve dinner to passengers in the car."""
        pass


class Refuelable(ABC):
    """Abstract interface for refueling services."""
    
    @abstractmethod
    def refuel(self, car_id: int) -> None:
        """Refuel the car."""
        pass


class PeopleDinner(Dineable):
    """Dining service for human passengers."""
    
    # Class variable to track statistics across all instances
    _people_served = 0
    
    def serve_dinner(self, car_id: int) -> None:
        print(f"Serving dinner to people in car {car_id}.")
        PeopleDinner._people_served += 1
    
    @classmethod
    def get_served_count(cls) -> int:
        return cls._people_served
    
    @classmethod
    def reset_count(cls) -> None:
        cls._people_served = 0


class RobotDinner(Dineable):
    """Dining service for robot passengers."""
    
    # Class variable to track statistics across all instances
    _robots_served = 0
    
    def serve_dinner(self, car_id: int) -> None:
        print(f"Serving dinner to robots in car {car_id}.")
        RobotDinner._robots_served += 1
    
    @classmethod
    def get_served_count(cls) -> int:
        return cls._robots_served
    
    @classmethod
    def reset_count(cls) -> None:
        cls._robots_served = 0


class ElectricStation(Refuelable):
    """Charging station for electric cars."""
    
    # Class variables to track statistics across all instances
    _electric_cars_served = 0
    _total_consumption = 0
    
    def refuel(self, car_id: int, consumption: int = 0) -> None:
        print(f"Charging electric car {car_id}.")
        ElectricStation._electric_cars_served += 1
        ElectricStation._total_consumption += consumption
    
    @classmethod
    def get_served_count(cls) -> int:
        return cls._electric_cars_served
    
    @classmethod
    def get_total_consumption(cls) -> int:
        return cls._total_consumption
    
    @classmethod
    def reset_count(cls) -> None:
        cls._electric_cars_served = 0
        cls._total_consumption = 0


class GasStation(Refuelable):
    """Refueling station for gas cars."""
    
    # Class variables to track statistics across all instances
    _gas_cars_served = 0
    _total_consumption = 0
    
    def refuel(self, car_id: int, consumption: int = 0) -> None:
        print(f"Refueling gas car {car_id}.")
        GasStation._gas_cars_served += 1
        GasStation._total_consumption += consumption
    
    @classmethod
    def get_served_count(cls) -> int:
        return cls._gas_cars_served
    
    @classmethod
    def get_total_consumption(cls) -> int:
        return cls._total_consumption
    
    @classmethod
    def reset_count(cls) -> None:
        cls._gas_cars_served = 0
        cls._total_consumption = 0


# TESTS
class TestDineableAndRefuelable(unittest.TestCase):
    """Test dining and refueling services with statistics tracking."""
    
    def setUp(self):
        """Reset all counters before each test."""
        PeopleDinner.reset_count()
        RobotDinner.reset_count()
        ElectricStation.reset_count()
        GasStation.reset_count()
    
    def test_people_dinner(self):
        dinner1 = PeopleDinner()
        dinner1.serve_dinner(1)
        self.assertEqual(PeopleDinner.get_served_count(), 1)
        
        dinner1.serve_dinner(2)
        self.assertEqual(PeopleDinner.get_served_count(), 2)
    
    def test_robot_dinner(self):
        dinner1 = RobotDinner()
        dinner1.serve_dinner(3)
        self.assertEqual(RobotDinner.get_served_count(), 1)
    
    def test_electric_station(self):
        station1 = ElectricStation()
        station1.refuel(1, 25)
        self.assertEqual(ElectricStation.get_served_count(), 1)
        self.assertEqual(ElectricStation.get_total_consumption(), 25)
        
        station1.refuel(2, 30)
        self.assertEqual(ElectricStation.get_served_count(), 2)
        self.assertEqual(ElectricStation.get_total_consumption(), 55)
    
    def test_gas_station(self):
        station1 = GasStation()
        station1.refuel(4, 40)
        self.assertEqual(GasStation.get_served_count(), 1)
        self.assertEqual(GasStation.get_total_consumption(), 40)
    
    def test_multiple_instances_share_statistics(self):
        """Test that multiple instances of the same class share statistics."""
        electric1 = ElectricStation()
        electric2 = ElectricStation()
        
        electric1.refuel(1, 20)
        electric2.refuel(2, 30)
        
        # Both instances should see the same count
        self.assertEqual(ElectricStation.get_served_count(), 2)
        self.assertEqual(ElectricStation.get_total_consumption(), 50)
    
    def test_dining_without_refueling(self):
        """Test that cars can dine without affecting refuel statistics."""
        dinner = PeopleDinner()
        dinner.serve_dinner(1)
        
        self.assertEqual(PeopleDinner.get_served_count(), 1)
        self.assertEqual(ElectricStation.get_served_count(), 0)
        self.assertEqual(GasStation.get_served_count(), 0)
    
    def test_polymorphism_dineable(self):
        """Test polymorphic behavior of Dineable implementations."""
        diners: list[Dineable] = [PeopleDinner(), RobotDinner()]
        
        for i, diner in enumerate(diners, 1):
            diner.serve_dinner(i)
        
        self.assertEqual(PeopleDinner.get_served_count(), 1)
        self.assertEqual(RobotDinner.get_served_count(), 1)
    
    def test_polymorphism_refuelable(self):
        """Test polymorphic behavior of Refuelable implementations."""
        stations: list[Refuelable] = [ElectricStation(), GasStation()]
        
        for i, station in enumerate(stations, 1):
            station.refuel(i, 20)
        
        self.assertEqual(ElectricStation.get_served_count(), 1)
        self.assertEqual(GasStation.get_served_count(), 1)


if __name__ == "__main__":
    unittest.main()
