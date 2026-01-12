"""
Task 3: Composition, IoC and Dependency Injection
CarStation class composed of Queue, Dineable, and Refuelable components.
"""
from dataclasses import dataclass
from typing import Optional
import unittest
import sys
import os

# Import from task1 and task2
sys.path.insert(0, os.path.dirname(__file__))
from task1 import Queue, ListQueue
from task2 import Dineable, Refuelable, PeopleDinner, RobotDinner, ElectricStation, GasStation


@dataclass
class Car:
    """Represents a car with its properties."""
    id: int
    type: str  # "ELECTRIC" or "GAS"
    passengers: str  # "PEOPLE" or "ROBOTS"
    is_dining: bool
    consumption: int


class CarStation:
    """
    Car service station composed of dining, refueling, and queue components.
    Uses Dependency Injection for flexibility and testability.
    """
    
    def __init__(
        self,
        refueling_service: Refuelable,
        dining_service: Optional[Dineable] = None,
        queue: Optional[Queue[Car]] = None
    ):
        """
        Initialize CarStation with injected dependencies.
        
        Args:
            refueling_service: The refueling service (Electric or Gas)
            dining_service: Optional dining service (People or Robot)
            queue: Optional queue implementation (defaults to ListQueue)
        """
        self.refueling_service = refueling_service
        self.dining_service = dining_service
        self.queue: Queue[Car] = queue if queue else ListQueue[Car]()
    
    def add_car(self, car: Car) -> None:
        """Add a car to the station's queue."""
        self.queue.enqueue(car)
    
    def serve_cars(self) -> None:
        """
        Process all cars in the queue.
        Serves dinner if needed and requested, then refuels each car.
        """
        while not self.queue.is_empty():
            car = self.queue.dequeue()
            if car is None:
                break
            
            # Serve dinner if car wants dining and we have dining service
            if car.is_dining and self.dining_service:
                self.dining_service.serve_dinner(car.id)
            
            # Refuel the car
            if hasattr(self.refueling_service, 'refuel'):
                # Check if refuel accepts consumption parameter
                import inspect
                sig = inspect.signature(self.refueling_service.refuel)
                if len(sig.parameters) > 1:
                    self.refueling_service.refuel(car.id, car.consumption)
                else:
                    self.refueling_service.refuel(car.id)
    
    def get_queue_size(self) -> int:
        """Return the current queue size."""
        return self.queue.size()


# TESTS
class TestCarStation(unittest.TestCase):
    """Test CarStation with composition and dependency injection."""
    
    def setUp(self):
        """Reset all service counters before each test."""
        PeopleDinner.reset_count()
        RobotDinner.reset_count()
        ElectricStation.reset_count()
        GasStation.reset_count()
    
    def test_add_car_to_station(self):
        """Test adding cars to the station queue."""
        station = CarStation(
            refueling_service=ElectricStation(),
            dining_service=PeopleDinner()
        )
        
        car1 = Car(1, "ELECTRIC", "PEOPLE", True, 25)
        car2 = Car(2, "ELECTRIC", "PEOPLE", False, 30)
        
        station.add_car(car1)
        station.add_car(car2)
        
        self.assertEqual(station.get_queue_size(), 2)
    
    def test_serve_cars_with_dining(self):
        """Test serving cars that want dining."""
        station = CarStation(
            refueling_service=ElectricStation(),
            dining_service=PeopleDinner()
        )
        
        car1 = Car(1, "ELECTRIC", "PEOPLE", True, 25)
        car2 = Car(2, "ELECTRIC", "PEOPLE", True, 30)
        
        station.add_car(car1)
        station.add_car(car2)
        station.serve_cars()
        
        self.assertEqual(station.get_queue_size(), 0)
        self.assertEqual(ElectricStation.get_served_count(), 2)
        self.assertEqual(PeopleDinner.get_served_count(), 2)
        self.assertEqual(ElectricStation.get_total_consumption(), 55)
    
    def test_serve_cars_without_dining(self):
        """Test serving cars that don't want dining."""
        station = CarStation(
            refueling_service=GasStation(),
            dining_service=RobotDinner()
        )
        
        car1 = Car(1, "GAS", "ROBOTS", False, 40)
        car2 = Car(2, "GAS", "ROBOTS", False, 35)
        
        station.add_car(car1)
        station.add_car(car2)
        station.serve_cars()
        
        self.assertEqual(GasStation.get_served_count(), 2)
        self.assertEqual(RobotDinner.get_served_count(), 0)  # No dining requested
        self.assertEqual(GasStation.get_total_consumption(), 75)
    
    def test_serve_mixed_dining_preferences(self):
        """Test serving cars with mixed dining preferences."""
        station = CarStation(
            refueling_service=ElectricStation(),
            dining_service=PeopleDinner()
        )
        
        car1 = Car(1, "ELECTRIC", "PEOPLE", True, 20)
        car2 = Car(2, "ELECTRIC", "PEOPLE", False, 25)
        car3 = Car(3, "ELECTRIC", "PEOPLE", True, 30)
        
        station.add_car(car1)
        station.add_car(car2)
        station.add_car(car3)
        station.serve_cars()
        
        self.assertEqual(ElectricStation.get_served_count(), 3)
        self.assertEqual(PeopleDinner.get_served_count(), 2)  # Only 2 wanted dining
    
    def test_station_without_dining_service(self):
        """Test station that has no dining service."""
        station = CarStation(
            refueling_service=GasStation(),
            dining_service=None
        )
        
        car1 = Car(1, "GAS", "PEOPLE", True, 45)  # Wants dining but station has none
        
        station.add_car(car1)
        station.serve_cars()
        
        self.assertEqual(GasStation.get_served_count(), 1)
        self.assertEqual(PeopleDinner.get_served_count(), 0)
    
    def test_dependency_injection_flexibility(self):
        """Test that different implementations can be injected."""
        # Electric station with people dining
        station1 = CarStation(
            refueling_service=ElectricStation(),
            dining_service=PeopleDinner()
        )
        
        # Gas station with robot dining
        station2 = CarStation(
            refueling_service=GasStation(),
            dining_service=RobotDinner()
        )
        
        car1 = Car(1, "ELECTRIC", "PEOPLE", True, 20)
        car2 = Car(2, "GAS", "ROBOTS", True, 40)
        
        station1.add_car(car1)
        station2.add_car(car2)
        
        station1.serve_cars()
        station2.serve_cars()
        
        self.assertEqual(ElectricStation.get_served_count(), 1)
        self.assertEqual(GasStation.get_served_count(), 1)
        self.assertEqual(PeopleDinner.get_served_count(), 1)
        self.assertEqual(RobotDinner.get_served_count(), 1)
    
    def test_empty_queue_serve(self):
        """Test serving when queue is empty."""
        station = CarStation(
            refueling_service=ElectricStation(),
            dining_service=PeopleDinner()
        )
        
        station.serve_cars()  # Should not crash
        self.assertEqual(station.get_queue_size(), 0)


if __name__ == "__main__":
    unittest.main()
