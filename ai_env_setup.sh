#!/bin/bash

echo "Starting environment setup for AI Coding Assistant..."

# Update and upgrade the system
echo "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python, pip, and essential tools
echo "Installing Python, pip, and essential tools..."
sudo apt install -y python3 python3-pip python3-venv build-essential

# Create a virtual environment
echo "Creating a virtual environment..."
python3 -m venv ~/ai_env

# Activate the virtual environment
source ~/ai_env/bin/activate

# Install PyTorch
echo "Installing PyTorch..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Install Hugging Face Transformers and Accelerate
echo "Installing Hugging Face Transformers and Accelerate..."
pip install transformers accelerate

# Add swap space
echo "Adding swap space..."
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# Configure Accelerate
echo "Configuring Accelerate..."
accelerate config

# Test the environment setup
echo "Testing environment setup..."
cat <<EOF > test_env.py
from transformers import AutoTokenizer, AutoModelForCausalLM

# Load the model
MODEL_NAME = "Salesforce/codegen-350M-multi"  # Use a small model for testing
print("[INFO] Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

print("[INFO] Loading model...")
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

print("[INFO] Environment setup successful!")
EOF

python3 test_env.py

# Cleanup test script
rm test_env.py

echo "Environment setup is complete! To activate the environment, run:"
echo "source ~/ai_env/bin/activate"
