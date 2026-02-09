import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel, PeftConfig
from .config import MODEL_NAME, NEW_MODEL_NAME
import sys


def inference(prompt):
    print(f"Loading model...")
    # Load Base Model
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, device_map="cpu")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    # Load Adapter
    try:
        model = PeftModel.from_pretrained(model, NEW_MODEL_NAME)
        print(f"Loaded LoRA adapter from {NEW_MODEL_NAME}")
    except Exception as e:
        print(f"Could not load adapter: {e}. Running base model.")

    # Inference
    inputs = tokenizer(prompt, return_tensors="pt").to("cpu")
    print("Generating...")
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=100,
            do_sample=False,  # Deterministic for reproducibility
            temperature=None,
            top_p=None,
        )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response


if __name__ == "__main__":
    if len(sys.argv) > 1:
        prompt = sys.argv[1]
    else:
        prompt = "What is QLoRA?"

    print(f"Prompt: {prompt}")
    print("-" * 20)
    result = inference(prompt)
    print(result)
