# QLoRAx Enhanced: End-to-End MLOps Framework

An implementation of the QLoRAx Enhanced framework for reproducible PEFT fine-tuning.

## Structure
- **Pillar A (Data)**: `src/data_engineering/validate.py` implements quality gating.
- **Pillar B (Model)**: `src/model/train.py` (QLoRA Training), `src/model/inference.py` (CPU Inference).
- **Pillar C (MLOps)**: `.github/workflows/pipeline.yml` (7-stage CI/CD), Dockerfiles in `docker/`.
- **Pillar D (Eval)**: Integrated into pipeline and inference scripts.

## Setup
```bash
pip install -r requirements.txt
```

## Usage

### 1. Data Validation
Validate the seed data against quality heuristics (Input > 10 chars, Output > 20 chars).
```bash
python src/data_engineering/validate.py data/seed_data.jsonl
```

### 2. Training (Requires GPU)
Runs QLoRA fine-tuning on TinyLlama-1.1B.
```bash
python src/model/train.py
```

### 3. Inference (CPU Compatible)
Runs deterministic inference using the fine-tuned adapter (or base model if adapter missing).
```bash
python src/model/inference.py "What is QLoRA?"
```

### 4. Docker (Reproducibility)
Build the training factory and serving showroom images.
```bash
docker build -f docker/Dockerfile.train -t qlorax-training .
docker build -f docker/Dockerfile.serve -t qlorax-serving .
```

