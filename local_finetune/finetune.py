from unsloth import FastLanguageModel
import torch
from trl import SFTTrainer
from transformers import TrainingArguments
from unsloth import is_bfloat16_supported
from datasets import load_dataset

# --------------------------------------------------------------------
# Step 1: Global Configuration
# --------------------------------------------------------------------
max_seq_length = 3096
load_in_4bit = True

dtype = torch.float16 if torch.cuda.is_available() else torch.float32

# Model name from UnsloTh repository
model_name = "unsloth/Meta-Llama-3.1-8B"

# --------------------------------------------------------------------
# Step 2: Load Pre-Trained Model and Tokenizer
# --------------------------------------------------------------------
print(f"Loading model '{model_name}'...")
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name=model_name,
    max_seq_length=max_seq_length,
    dtype=dtype,
    load_in_4bit=load_in_4bit,
)

# Apply PEFT (Parameter-Efficient Fine-Tuning)
model = FastLanguageModel.get_peft_model(
    model,
    r=16,  # LoRA rank; suggested values are 8, 16, etc.
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                    "gate_proj", "up_proj", "down_proj"],
    lora_alpha=16,
    lora_dropout=0,
    bias="none",
    use_gradient_checkpointing="unsloth",
    random_state=3407,
    
    use_rslora=False,  # Rank stabilized LoRA disabled
    loftq_config=None,  # LoftQ disabled
)

# --------------------------------------------------------------------
# Step 3: Load and Prepare the Dataset
# --------------------------------------------------------------------
print("Loading dataset...")

# Example: We have a single instruct JSONL file with lines like:
#   { "instruction": "Explain X", "input": "...", "output": "..." }
# Hugging Face Datasets can load .jsonl files with `load_dataset("json", data_files=...)`
dataset = load_dataset(
    "json",
    data_files="data_instruct.jsonl",  # <-- your instruct dataset
    split="train"  # Put all data in one split
)

# Create a train/validation split (e.g., 80%/20%)
split_dataset = dataset.train_test_split(test_size=0.2, seed=42)
train_dataset = split_dataset["train"]
eval_dataset = split_dataset["test"]

print(f"Train samples: {len(train_dataset)} | Validation samples: {len(eval_dataset)}")

# Tokenization Function
def tokenize_function(examples):
    """
    Build a prompt from 'instruction' and 'input', then tokenize 'output' as labels.
    """
    instructions = examples["instruction"]
    contexts = examples["input"]
    outputs = examples["output"]

    # Build a prompt for each example:
    # e.g. "Instruction: <instruction>\nInput: <input>\nAnswer:"
    # If `input` is empty, skip that line.
    full_prompts = []
    for instr, ctx in zip(instructions, contexts):
        if ctx.strip():
            full_prompts.append(f"Instruction: {instr}\nInput: {ctx}\nAnswer:")
        else:
            full_prompts.append(f"Instruction: {instr}\nAnswer:")

    # Tokenize the prompt
    model_inputs = tokenizer(
        full_prompts,
        max_length=max_seq_length // 2,
        truncation=True,
        padding="max_length",
    )

    # Tokenize the output
    labels = tokenizer(
        outputs,
        max_length=max_seq_length // 2,
        truncation=True,
        padding="max_length",
    )["input_ids"]

    model_inputs["labels"] = labels
    return model_inputs

print("Tokenizing train dataset...")
tokenized_train_dataset = train_dataset.map(
    tokenize_function,
    batched=True,
    remove_columns=["instruction", "input", "output"]  # remove old columns
)

print("Tokenizing validation dataset...")
tokenized_eval_dataset = eval_dataset.map(
    tokenize_function,
    batched=True,
    remove_columns=["instruction", "input", "output"]
)

train_dataset = tokenized_train_dataset
eval_dataset = tokenized_eval_dataset

# --------------------------------------------------------------------
# Step 4: Set Up SFTTrainer for Fine-Tuning
# --------------------------------------------------------------------
trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=train_dataset,
    dataset_text_field="text",  # Not actually used here, but required by SFTTrainer
    max_seq_length=max_seq_length,
    dataset_num_proc=2,
    packing=False,
    args=TrainingArguments(
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        warmup_steps=5,
        max_steps=60,  # Set for 60 training steps or adjust as needed
        learning_rate=2e-4,
        fp16=not is_bfloat16_supported(),
        bf16=is_bfloat16_supported(),
        logging_steps=1,
        optim="adamw_8bit",
        weight_decay=0.01,
        lr_scheduler_type="linear",
        seed=3407,
        output_dir="outputs",
        report_to="none",  # set to "wandb" or "tensorboard" if desired
    ),
)

# --------------------------------------------------------------------
# Step 5: Fine-Tune the Model
# --------------------------------------------------------------------
print("Starting fine-tuning...")
trainer.train()

# --------------------------------------------------------------------
# Step 6: Save the Fine-Tuned Model
# --------------------------------------------------------------------
print("Saving fine-tuned model...")
trainer.save_model("./fine_tuned_model")
tokenizer.save_pretrained("./fine_tuned_model")
print("Fine-tuning completed successfully!")

# --------------------------------------------------------------------
# Step 7: Test the Fine-Tuned Model (Optional)
# --------------------------------------------------------------------
def generate_sample_text(prompt="Hello, my name is Ollama."):
    """
    Test the fine-tuned model by generating a response to a prompt.
    """
    print("\nLoading the fine-tuned model for testing...")
    fine_tuned_model, fine_tuned_tokenizer = FastLanguageModel.from_pretrained(
        model_name="./fine_tuned_model",
        max_seq_length=max_seq_length,
        dtype=dtype,
        load_in_4bit=load_in_4bit
    )

    input_ids = fine_tuned_tokenizer.encode(prompt, return_tensors="pt")
    if torch.cuda.is_available():
        fine_tuned_model = fine_tuned_model.cuda()
        input_ids = input_ids.cuda()

    outputs = fine_tuned_model.generate(
        input_ids,
        max_length=100,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        temperature=0.8
    )

    output_text = fine_tuned_tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"Generated Text:\n{output_text}\n")

# Uncomment to test text generation:
# generate_sample_text()
