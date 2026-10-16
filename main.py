import time
import random

class DigitalTwinBoat:
    """
    Represents a digital twin of a boat, reflecting its state based on sensor data.
    """
    def __init__(self, name="MyDigitalBoat"):
        self.name = name
        # Initial state of the boat
        self.fuel_level = 100.0  # Percentage
        self.engine_rpm = 0      # Revolutions per minute
        self.speed_knots = 0.0   # Knots
        self.water_temperature_c = 15.0 # Celsius
        self.latitude = 41.0082  # Istanbul's approximate latitude
        self.longitude = 28.9784 # Istanbul's approximate longitude
        self.status = "Docked"

    def update_state(self, sensor_data):
        """
        Updates the digital twin's state with new sensor readings.
        This is the core "digital twin" mechanism, mirroring the physical boat.
        """
        print(f"--- Updating {self.name} Digital Twin with new sensor data ---")
        if 'fuel_level' in sensor_data:
            self.fuel_level = max(0.0, min(100.0, sensor_data['fuel_level']))
        if 'engine_rpm' in sensor_data:
            self.engine_rpm = max(0, sensor_data['engine_rpm'])
            self.status = "Underway" if self.engine_rpm > 0 else "Docked"
        if 'speed_knots' in sensor_data:
            self.speed_knots = max(0.0, sensor_data['speed_knots'])
        if 'water_temperature_c' in sensor_data:
            self.water_temperature_c = sensor_data['water_temperature_c']
        if 'latitude' in sensor_data:
            self.latitude = sensor_data['latitude']
        if 'longitude' in sensor_data:
            self.longitude = sensor_data['longitude']

    def display_state(self):
        """
        Prints the current state of the digital twin.
        """
        print(f"\n--- {self.name} Digital Twin Current State ---")
        print(f"  Status: {self.status}")
        print(f"  Fuel Level: {self.fuel_level:.1f}%")
        print(f"  Engine RPM: {self.engine_rpm} RPM")
        print(f"  Speed: {self.speed_knots:.1f} knots")
        print(f"  Water Temp: {self.water_temperature_c:.1f}°C")
        print(f"  Location: Lat {self.latitude:.4f}, Lon {self.longitude:.4f}")
        print("------------------------------------------")

def simulate_sensor_data(current_fuel, current_rpm, current_speed, current_water_temp, current_lat, current_lon):
    """
    Simulates new sensor readings for the boat.
    In a real scenario, this data would come from actual physical sensors.
    """
    # Simulate fuel consumption
    new_fuel = current_fuel - random.uniform(0.1, 0.5) if current_rpm > 0 else current_fuel
    new_fuel = max(0.0, new_fuel)

    # Simulate engine RPM (fluctuates if running, or stays at 0)
    if current_rpm > 0:
        new_rpm = current_rpm + random.randint(-50, 50)
        new_rpm = max(500, min(3000, new_rpm)) # Keep RPM within reasonable range
    else:
        new_rpm = random.choices([0, random.randint(800, 1500)], weights=[0.8, 0.2], k=1)[0] # Small chance to start engine

    # Simulate speed based on RPM
    new_speed = new_rpm / 200.0 if new_rpm > 0 else 0.0
    new_speed = max(0.0, min(25.0, new_speed)) # Max speed 25 knots

    # Simulate water temperature (slight fluctuation)
    new_water_temp = current_water_temp + random.uniform(-0.1, 0.1)
    new_water_temp = max(5.0, min(30.0, new_water_temp))

    # Simulate movement if boat is moving
    if new_speed > 0:
        # Simple movement simulation: drift slightly
        lat_change = (new_speed / 10000.0) * random.uniform(-0.5, 0.5)
        lon_change = (new_speed / 10000.0) * random.uniform(-0.5, 0.5)
        new_lat = current_lat + lat_change
        new_lon = current_lon + lon_change
    else:
        new_lat = current_lat
        new_lon = current_lon

    return {
        'fuel_level': new_fuel,
        'engine_rpm': new_rpm,
        'speed_knots': new_speed,
        'water_temperature_c': new_water_temp,
        'latitude': new_lat,
        'longitude': new_lon
    }

if __name__ == "__main__":
    print("Starting Digital Boat Twin Simulation...")
    my_boat_twin = DigitalTwinBoat("Explorer 101")

    # Initial state display
    my_boat_twin.display_state()

    # Simulate 10 time steps (e.g., 10 minutes of operation)
    for i in range(1, 11):
        print(f"\n--- Simulation Step {i} ---")
        # Get current state for realistic simulation of changes
        current_fuel = my_boat_twin.fuel_level
        current_rpm = my_boat_twin.engine_rpm
        current_speed = my_boat_twin.speed_knots
        current_water_temp = my_boat_twin.water_temperature_c
        current_lat = my_boat_twin.latitude
        current_lon = my_boat_twin.longitude

        # Simulate new sensor data
        new_sensor_data = simulate_sensor_data(current_fuel, current_rpm, current_speed, current_water_temp, current_lat, current_lon)

        # Update the digital twin with the new data
        my_boat_twin.update_state(new_sensor_data)

        # Display the updated state of the digital twin
        my_boat_twin.display_state()

        time.sleep(1) # Simulate a 1-second interval between updates

    print("\nDigital Boat Twin Simulation Finished.")
