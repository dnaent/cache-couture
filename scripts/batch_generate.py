import json
import time
from comfy_client import queue_prompt, get_history

def load_workflow(path):
    with open(path, 'r') as f:
        return json.load(f)

def run_batch(workflow_path, prompts):
    workflow = load_workflow(workflow_path)
    
    # Typically, you'd find the node ID for the positive prompt and modify it.
    # For now, this is a placeholder batch runner structure.
    for p in prompts:
        print(f"Queueing prompt: {p}")
        # workflow["3"]["inputs"]["text"] = p # Example update
        res = queue_prompt(workflow)
        prompt_id = res['prompt_id']
        print(f"Queued, ID: {prompt_id}")
        time.sleep(2) # rate limit or wait for completion in real implementation

if __name__ == "__main__":
    print("Batch generation tool loaded.")
