#!/bin/bash

set -e

echo "Checking CUDA availability..."
if ! command -v nvidia-smi &> /dev/null; then
    echo "ERROR: NVIDIA drivers not found. Please install NVIDIA drivers first."
    exit 1
fi

# Get CUDA version from nvidia-smi
CUDA_VERSION=$(nvidia-smi --query-gpu=cuda_version --format=csv,noheader | head -n 1)
CUDA_MAJOR=$(echo $CUDA_VERSION | cut -d'.' -f1)

echo "Detected CUDA version: $CUDA_VERSION"

# Install CUDA toolkit dependencies
echo "Installing CUDA toolkit dependencies..."
if [ -f /etc/os-release ]; then
    . /etc/os-release
    case $ID in
        ubuntu|debian)
            sudo apt-get update
            sudo apt-get install -y build-essential
            ;;
        rhel|centos|fedora)
            sudo yum groupinstall -y "Development Tools"
            ;;
        *)
            echo "Unsupported distribution: $ID"
            exit 1
            ;;
    esac
fi

# Install PyTorch with CUDA support
echo "Installing PyTorch with CUDA support..."
pip install torch torchvision --extra-index-url https://download.pytorch.org/whl/cu${CUDA_MAJOR}0

# Install additional GPU dependencies
echo "Installing additional GPU dependencies..."
pip install cupy-cuda${CUDA_MAJOR}0

echo "Testing GPU support..."
python -c "import torch; print('CUDA available:', torch.cuda.is_available())"

if [ $? -eq 0 ]; then
    echo "GPU support successfully installed!"
else
    echo "Error: GPU support installation failed."
    exit 1
fi