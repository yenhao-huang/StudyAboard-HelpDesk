import os
import sys

# 專案根目錄 = scripts 的上一層
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

import argparse
from utils.chatbot import utils, data_utils, model_utils


def parse_args():
    parser = argparse.ArgumentParser(description="Evaluate")
    parser.add_argument("--model", type=str, default="Qwen/Qwen3-8B")
    parser.add_argument("--enable_lora", type=bool, default=False)
    parser.add_argument("--eval_batch", type=int, default=1)
    parser.add_argument("--output_dir", type=str, default="./results")
    parser.add_argument("--log_dir", type=str, default="./logs")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    output_dir, log_dir = utils.make_dir_with_timestamp(args.output_dir, args.log_dir)
    
    # Prepare the model input
    context = f"""[1] Question: who produces the most wool in the world
    Answer: Wool Global wool production is about 2 million tonnes per year, of which 60% goes into apparel. 
    Wool comprises ca 3% of the global textile market, but its value is higher owing to dying and other modifications of the material.
    [1] Australia is a leading producer of wool which is mostly from Merino sheep but has been eclipsed by China in terms of total weight.
    [30] New Zealand (2016) is the third-largest producer of wool, and the largest producer of crossbred wool. 
    Breeds such as Lincoln, Romney, Drysdale, and Elliotdale produce coarser fibers, and wool from these sheep is usually used for making carpets.
    """
    
    #query = input("Enter your query: ").strip()
    query = "who produces the most wool in the world"
    # include prompt engineer
    model_inputs, tokenizer = data_utils.data_preprocess(context, query, args.model)

    eval_agent = model_utils.set_eval_agent(
        args.model, 
        args.enable_lora,
    )

    results = model_utils.inference(
        eval_agent,
        tokenizer,
        model_inputs, 
        max_new_tokens=50
    )