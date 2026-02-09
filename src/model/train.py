
import torch
import os
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig,
    TrainingArguments,
)
from peft import LoraConfig, prepare_model_for_kbit_training, get_peft_model
from trl import SFTTrainer
from datasets import load_dataset
from .config import (
    MODEL_NAME, NEW_MODEL_NAME, LORA_R, LORA_ALPHA, LORA_DROPOUT,
    TARGET_MODULES, OUTPUT_DIR, NUM_TRAIN_EPOCHS,
    PER_DEVICE_TRAIN_BATCH_SIZE, LEARNING_RATE, MAX_SEQ_LENGTH, DATASET_PATH
)

def formatting_prompts_func(example):
    output_texts = []
    for messages in example['messages']:
        # Simple ChatML-like format or similar
        text = ''
        for msg in messages:
            role = msg['role']
            content = msg['content']
            text += f'<|{role}|>\n{content}</s>\n'
        output_texts.append(text)
    return output_texts

def train():
    print(f'Starting Training for {MODEL_NAME}...')
    
    # 1. Load Dataset
    data_files = {'train': DATASET_PATH}
    dataset = load_dataset('json', data_files=data_files, split='train')

    # 2. BitsAndBytes Config (4-bit NF4)
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type='nf4',
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
    )

    # 3. Load Base Model
    device_map = 'auto' 
    
    try:
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            quantization_config=bnb_config,
            device_map=device_map,
            trust_remote_code=True
        )
    except Exception as e:
        print(f'Warning: Quantization failed ({e}). Loading in 32-bit (CPU fallback).')
        model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, trust_remote_code=True)


    model.config.use_cache = False
    model.config.pretraining_tp = 1

    # 4. Load Tokenizer
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = 'right'

    # 5. PEFT Config
    peft_config = LoraConfig(
        lora_alpha=LORA_ALPHA,
        lora_dropout=LORA_DROPOUT,
        r=LORA_R,
        bias='none',
        task_type='CAUSAL_LM',
        target_modules=TARGET_MODULES
    )

    # 6. Training Arguments
    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        num_train_epochs=NUM_TRAIN_EPOCHS,
        per_device_train_batch_size=PER_DEVICE_TRAIN_BATCH_SIZE,
        gradient_accumulation_steps=4,
        optim='paged_adamw_32bit',
        save_steps=25,
        logging_steps=25,
        learning_rate=LEARNING_RATE,
        weight_decay=0.001,
        fp16=False,
        bf16=False, 
        max_grad_norm=0.3,
        max_steps=-1,
        warmup_ratio=0.03,
        group_by_length=True,
        lr_scheduler_type='constant',
        report_to='tensorboard'
    )

    # 7. Trainer
    trainer = SFTTrainer(
        model=model,
        train_dataset=dataset,
        peft_config=peft_config,
        formatting_func=formatting_prompts_func, # Use the formatting function
        max_seq_length=MAX_SEQ_LENGTH,
        tokenizer=tokenizer,
        args=training_args,
        packing=False,
    )

    # 8. Train
    print('Training...')
    trainer.train()
    
    # 9. Save Model
    print('Saving model...')
    trainer.model.save_pretrained(NEW_MODEL_NAME)
    print('Done.')

if __name__ == '__main__':
    train()

