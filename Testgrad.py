import torch
import torch.optim as optim

data = torch.load("ambulance_tensor4.pt")


def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def simulate_ambulance(input_data):
    # Perform some operations on input_data to simulate the movement of the ambulance
    # Here, we'll just move 1 km in a random direction
    lat, lon = input_data[0][1], input_data[0][2]
    direction = torch.randint(0, 4, (1,)).item()
    if direction == 0:
        lat += 0.009
    elif direction == 1:
        lat -= 0.009
    elif direction == 2:
        lon += 0.009
    else:
        lon -= 0.009
    return torch.tensor([input_data[0][0], lat, lon, input_data[0][3], input_data[0][4], input_data[0][5]])


def get_response_time(simulated_pos, actual_pos):
    distance_km = manhattan_distance(simulated_pos[1], simulated_pos[2], actual_pos[0], actual_pos[1])
    response_time = distance_km / 100  # assuming 50 km/hour speed
    return response_time


total_loss = 0
for i in range(data.size()[0] - 1):
    input_data = data[i, :-1].unsqueeze(0)
    target_pos = data[i + 1, 1:3]

    simulated_pos = simulate_ambulance(input_data)
    loss = get_response_time(simulated_pos, target_pos)
    total_loss += loss

print(f"Total Loss: {total_loss.item()}")

