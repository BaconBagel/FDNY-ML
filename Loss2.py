import torch
from torch import nn
from torch.optim import SGD
import time
import tensorboard
from torch.utils.tensorboard import SummaryWriter

writer = SummaryWriter(log_dir='logs')

data = torch.load("ambulance_tensor4.pt")

# Define hyperparameters
num_epochs = 10
learning_rate = 0.001

# Define model architecture
model = nn.Sequential(
    nn.Linear(6, 16),
    nn.ReLU(),
    nn.Linear(16, 2)
)

# Define loss function
criterion = nn.L1Loss()

# Define optimizer
optimizer = SGD(model.parameters(), lr=learning_rate)

# Train the model
for epoch in range(num_epochs):
    total_loss = 0
    for i in range(len(data) - 1):
        print(len(data),i)
        # Get input data and target
        data = abs(data.float())
        input_data = abs(data[i, :-1])
        target = data[i + 1, 1:3]
 

        # Calculate Manhattan distance
        distance = torch.abs(target - input_data[1:3]).sum()


        # Calculate estimated time
        estimated_time = distance / 50  # assuming 50 km/h

        # Get model output
        output = model(input_data.unsqueeze(0))

        # Calculate loss
        loss = criterion(output.squeeze(), target)

        # Backpropagation
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

        # Log the loss after each epoch
        writer.add_scalar('Loss', total_loss, epoch)

        # Log the distribution of the model parameters after each epoch
        for name, param in model.named_parameters():
            writer.add_histogram(name, param, epoch)

    if epoch % 1  == 0:
        print(f"Epoch {epoch + 1}, Total Loss: {total_loss:.4f}")

# Update the position of the ambulance
current_position = torch.tensor([data[0, 1], data[0, 2]])

writer.close()

for i in range(len(data) - 1):
    input_data = data[i, :-1]
    target = data[i + 1, 1:3]

    # Calculate Manhattan distance
    distance = torch.abs(target - current_position).sum()
    print(target)

    # Calculate estimated time
    estimated_time = distance / 50  # assuming 50 km/h

    # Get model output
    output = model(input_data.unsqueeze(0))

    # Update the position of the ambulance
    current_position = current_position + (output.squeeze() * estimated_time)

    print(f"Updated position of ambulance after incident {i + 1}: {current_position}")
    time.sleep(2)
