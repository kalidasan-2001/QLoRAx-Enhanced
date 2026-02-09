import os

# Model Configuration
MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
NEW_MODEL_NAME = "tinyllama-qlorax-enhanced"

# LoRA Configuration
LORA_R = 32
LORA_ALPHA = 64
LORA_DROPOUT = 0.05
TARGET_MODULES = ["q_proj", "k_proj", "v_proj", "o_proj"]

# Training Configuration
OUTPUT_DIR = "./results"
NUM_TRAIN_EPOCHS = 1
PER_DEVICE_TRAIN_BATCH_SIZE = 4
GRADIENT_ACCUMULATION_STEPS = 4
LEARNING_RATE = 2e-4
MAX_SEQ_LENGTH = 1024

# Data Configuration
DATASET_PATH = "data/seed_data.jsonl"
