import os

# Store the robot's hostname in a variable
message = "Hello from %s!" % os.environ['VEHICLE_NAME']
print(message)
