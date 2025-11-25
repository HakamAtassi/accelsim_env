import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import accelerate

# Load model 
model_name = "Qwen/Qwen3-0.6B"  # or try smaller ones like "facebook/opt-1.3b"

# Load Tokenizer
print("Loading tokenizer and model...")
tokenizer = AutoTokenizer.from_pretrained(model_name)

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,      # Use float16 for lower memory
    device_map="auto",               # Automatically use available GPU(s)
    output_attentions = True,
    return_dict = True
)

####################
## ADD SOME HOOKS ##
####################

# Make some modifications to the model
for i, layer in enumerate(model.model.layers):
    layer.self_attn.register_forward_hook(
        lambda module, input, output, i=i: print(f"At layer {i}")
    )

model.lm_head.register_forward_hook(lambda module, input, output: print("Decode complete..."))
#print(model)

model.model.layers = model.model.layers[0:4] # labotomize the model



##########################
## PERFORM FORWARD PASS ##
##########################


prompt = "A Zebra is"
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

outputs = model.generate(
    **inputs,
    max_new_tokens=50,
    temperature=0.7,
    top_p=0.9,
    do_sample=True,
    output_attentions=True,
)

generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(generated_text)