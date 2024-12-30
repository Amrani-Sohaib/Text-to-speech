#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=======================================================================
Fine-Tuning Ollama-Style Models with Hugging Face Transformers
=======================================================================

Usage:
------
1. Install the necessary dependencies (if you have not already):
       pip install transformers datasets torch accelerate

2. Update the 'model_name' variable with the name of the Ollama model 
   you want to fine-tune. For example:
       model_name = "ollama/ollama-model-name"

3. Provide your dataset path in the load_dataset function if you have 
   a local or Hugging Face dataset. For instance:
       dataset = load_dataset("path_to_your_dataset")

4. Adjust the hyperparameters in TrainingArguments (like batch_size,
   learning rate, etc.) according to your hardware and project needs.

5. Run the script:
       python fine_tune_ollama.py

6. After training completes, your fine-tuned model and tokenizer will 
   be saved in the './ollama-fine-tuned' folder (you can change this 
   path in the script).

7. Use the final section's sample code to load and test the model.
   Try generating text with it to verify the fine-tuning results.
"""

import torch
from transformers import (AutoModelForCausalLM, 
                          AutoTokenizer, 
                          Trainer, 
                          TrainingArguments)
from datasets import load_dataset

# --------------------------------------------------------------------
# Step 1: Global Configuration
# --------------------------------------------------------------------
# Explanation:
#  - max_seq_length: Controls how many tokens (words/pieces) from the 
#    text will be processed at once by the model.
#  - dtype: Chooses float16 if there's a GPU present (for memory
#    efficiency), otherwise defaults to float32.
#  - load_in_4bit: If True, attempts to load the model in 4-bit 
#    precision (quantization), significantly reducing VRAM usage.
# --------------------------------------------------------------------
max_seq_length = 2048
dtype = torch.float16 if torch.cuda.is_available() else torch.float32
load_in_4bit = True

# Replace "ollama/ollama-model-name" with the actual model you want to fine-tune.
model_name = "ollama/ollama-model-name"

# --------------------------------------------------------------------
# Step 2: Load Pre-Trained Model and Tokenizer
# --------------------------------------------------------------------
# Explanation:
#  - from_pretrained():
#      Downloads (if needed) and initializes the model weights.
#  - torch_dtype is set to dtype for precision.
#  - quantization_config is used if we want 4-bit loading.
#  - trust_remote_code=True allows custom modeling code from Hugging Face
#    repos.
# --------------------------------------------------------------------
print(f"Loading model '{model_name}'...")
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=dtype,
    quantization_config={"load_in_4bit": load_in_4bit} if load_in_4bit else None,
    trust_remote_code=True,
)

print(f"Loading tokenizer for '{model_name}'...")
tokenizer = AutoTokenizer.from_pretrained(model_name)

# --------------------------------------------------------------------
# Step 3: Load and Prepare the Dataset
# --------------------------------------------------------------------
# Explanation:
#  - load_dataset(): Loads a dataset, either from a local path or from 
#    Hugging Face Hub.
#  - For demonstration, we're expecting the dataset to have a column 
#    named "text". Adjust as needed.
# --------------------------------------------------------------------
print("Loading dataset...")
# Replace "path_to_your_dataset" with the actual path or name of your dataset.
dataset = load_dataset("path_to_your_dataset")

print("Tokenizing dataset...")

def tokenize_function(examples):
    """
    Tokenize the input text using the model's tokenizer.
    - Truncation: Cuts off text longer than max_seq_length.
    - Padding: Ensures each input is padded to max_seq_length, 
      so that they align in shape.
    """
    return tokenizer(
        examples["text"],        # Adjust if your column name is different
        truncation=True,
        max_length=max_seq_length,
        padding="max_length"
    )

# Map the tokenize function to each split of the dataset
tokenized_datasets = dataset.map(tokenize_function, batched=True)

# --------------------------------------------------------------------
# Step 4: Split the Dataset into Training and Validation
# --------------------------------------------------------------------
# Explanation:
#  - train_dataset: The subset used for updating model weights.
#  - eval_dataset: The subset used for monitoring overfitting and 
#    progress during training.
# --------------------------------------------------------------------
train_dataset = tokenized_datasets["train"]
eval_dataset = tokenized_datasets["validation"]

# --------------------------------------------------------------------
# Step 5: Set Up Training Arguments
# --------------------------------------------------------------------
# Explanation of Key Params:
#  - output_dir: Where final model checkpoints and logs are stored.
#  - evaluation_strategy: How often to evaluate (e.g. "steps", "epoch").
#  - save_steps: Save a checkpoint every 'save_steps' training steps.
#  - fp16: Enable mixed precision to speed up training on GPUs.
# --------------------------------------------------------------------
training_args = TrainingArguments(
    output_dir="./ollama-fine-tuned",  # Folder for checkpoints/models
    evaluation_strategy="steps",       # Evaluate every X steps
    per_device_train_batch_size=4,     # Adjust based on GPU memory
    per_device_eval_batch_size=4,      # Adjust based on GPU memory
    gradient_accumulation_steps=4,     # Accumulate gradients for bigger effective batch size
    num_train_epochs=3,                # Number of full passes through the training data
    save_steps=500,                    # Save model checkpoint every 500 steps
    save_total_limit=2,                # Keep only 2 recent checkpoints to save disk space
    learning_rate=5e-5,                # Typical fine-tuning learning rate
    weight_decay=0.01,                 # Regularization
    logging_dir="./logs",              # Directory for logs
    fp16=True if torch.cuda.is_available() else False,
)

# --------------------------------------------------------------------
# Step 6: Initialize the Trainer
# --------------------------------------------------------------------
# Explanation:
#  - The Trainer class simplifies the training loop, handling forward
#    pass, backward pass, gradient updates, logging, and evaluation.
# --------------------------------------------------------------------
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    tokenizer=tokenizer,
)

# --------------------------------------------------------------------
# Step 7: Fine-Tune the Model
# --------------------------------------------------------------------
# Explanation:
#  - trainer.train() performs the actual fine-tuning, iterating over 
#    the dataset multiple times (epochs).
# --------------------------------------------------------------------
print("Starting fine-tuning...")
trainer.train()

# --------------------------------------------------------------------
# Step 8: Save the Fine-Tuned Model and Tokenizer
# --------------------------------------------------------------------
# Explanation:
#  - After training, we save the updated model weights and the tokenizer.
# --------------------------------------------------------------------
print("Saving fine-tuned model...")
trainer.save_model("./ollama-fine-tuned")
tokenizer.save_pretrained("./ollama-fine-tuned")
print("Fine-tuning completed successfully!")

# --------------------------------------------------------------------
# Step 9: Usage Example - Generating Text
# --------------------------------------------------------------------
# Explanation:
#  - Demonstrates how to load the fine-tuned model and generate text.
#  - This section is optional and can be used as a reference or run 
#    after training to verify the model works.
# --------------------------------------------------------------------
def generate_sample_text(prompt="Hello, my name is Ollama."):
    """
    Loads the fine-tuned model from the saved directory and generates
    text based on the provided prompt.
    """
    print("\nLoading the fine-tuned model and tokenizer for testing...")
    fine_tuned_model = AutoModelForCausalLM.from_pretrained("./ollama-fine-tuned")
    fine_tuned_tokenizer = AutoTokenizer.from_pretrained("./ollama-fine-tuned")
    
    print(f"Generating text for the prompt: '{prompt}'")
    input_ids = fine_tuned_tokenizer.encode(prompt, return_tensors="pt")
    
    # Move input to GPU if available
    if torch.cuda.is_available():
        fine_tuned_model = fine_tuned_model.cuda()
        input_ids = input_ids.cuda()

    # Generate text
    output_ids = fine_tuned_model.generate(
        input_ids,
        max_length=100,          # Adjust to control output length
        do_sample=True,          # Enable sampling for more varied outputs
        top_k=50,                # Restrict the sampling to top-k tokens
        top_p=0.95,              # Nucleus sampling
        temperature=0.8          # Adjust temperature to control randomness
    )
    
    # Decode output tokens
    output_text = fine_tuned_tokenizer.decode(output_ids[0], skip_special_tokens=True)
    print(f"Generated Text:\n{output_text}\n")

# Uncomment to test text generation right after fine-tuning:
# generate_sample_text()
