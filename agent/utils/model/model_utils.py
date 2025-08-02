from transformers import  AutoModelForCausalLM, Trainer, TrainingArguments, BitsAndBytesConfig
import torch
from tqdm import tqdm

from peft import PeftConfig, PeftModel, get_peft_model, LoraConfig, TaskType
from torch.utils.data import DataLoader

def set_eval_agent(
    model_name, 
    enable_lora=False
):

    if enable_lora:
        peft_config = PeftConfig.from_pretrained(model_name)
        base_model =  AutoModelForCausalLM.from_pretrained(peft_config.base_model_name_or_path)
        model = PeftModel.from_pretrained(base_model, model_name, device_map="auto")
    else:
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="auto"
        )
    return model

def inference(
    model, 
    tokenizer, 
    model_inputs, 
    max_new_tokens=50
):

    model_inputs.to(model.device)
    # conduct text completion
    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=max_new_tokens
    )
    output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist() 

    # parsing thinking content
    try:
        # rindex finding 151668 (</think>)
        index = len(output_ids) - output_ids[::-1].index(151668)
    except ValueError:
        index = 0

    thinking_content = tokenizer.decode(output_ids[:index], skip_special_tokens=True).strip("\n")
    content = tokenizer.decode(output_ids[index:], skip_special_tokens=True).strip("\n")

    print("thinking content:", thinking_content)
    print("content:", content)

    return content
