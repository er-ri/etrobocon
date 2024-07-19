import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm
from sklearn.model_selection import train_test_split
from etrobocon.models import NvidiaModel
from etrobocon.data import transform, flip_transform, DrivingRecordDataset

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# TensorBoard, visualize the log by running: `tensorboard --logdir=runs`
writer = SummaryWriter()

# Balanced dataset, not implementated
image_paths = None
steerings = None


# Data preparation
X_train, X_val, y_train, y_val = train_test_split(
    image_paths, steerings, test_size=0.2, random_state=6
)

train_set = DrivingRecordDataset(X_train, y_train, transform, flip_transform)
val_set = DrivingRecordDataset(X_val, y_val, transform, flip_transform)

train_loader = torch.utils.data.DataLoader(train_set, batch_size=128, shuffle=True)
val_loader = torch.utils.data.DataLoader(val_set, batch_size=64, shuffle=True)

# Model, optimizer and loss function
model = NvidiaModel()
model.to(device)
optimizer = optim.Adam(model.parameters(), lr=1e-3)
criterion = nn.MSELoss()

# Training loop
num_epochs = 100
for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0

    for inputs, labels in tqdm(train_loader, desc=f"Epoch {epoch+1}/{num_epochs}"):
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()

    avg_train_loss = running_loss / len(train_loader)

    # Validation
    model.eval()
    val_loss = 0.0

    with torch.no_grad():
        for inputs, labels in val_loader:
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            val_loss += loss.item()

    avg_val_loss = val_loss / len(val_loader)

    writer.add_scalar("Loss/train", avg_train_loss, epoch)
    writer.add_scalar("Loss/val", avg_val_loss, epoch)

    print(
        f"Epoch {epoch+1}/{num_epochs}, Train Loss: {avg_train_loss:.4f}, Val Loss: {avg_val_loss:.4f}"
    )

writer.close()


# Loading and saving models
torch.save(model.state_dict(), "../model.pth")

model = NvidiaModel()
model.load_state_dict(torch.load("../model.pth"))
model.eval()
