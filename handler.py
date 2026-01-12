import runpod
from transformers import AutoModelForCausalLM, AutoProcessor, GenerationConfig
from PIL import Image
from typing import Dict, Any
import requests


# Global variables to store model and processor
model = None
processor = None


def load_model():
    """Load the Molmo model and processor globally to avoid reloading on each request"""
    global model, processor
    
    if model is None or processor is None:
        print("Loading Molmo model...")
        
        processor = AutoProcessor.from_pretrained(
            'allenai/Molmo-7B-D-0924',
            trust_remote_code=True,
            torch_dtype='auto',
            device_map='auto'
        )

        model = AutoModelForCausalLM.from_pretrained(
            'allenai/Molmo-7B-D-0924',
            trust_remote_code=True,
            torch_dtype='auto',
            device_map='auto'
        )
        print("Model loaded successfully!")


def handler(job: Dict[str, Any]) -> Dict[str, Any]:
    """
    RunPod serverless handler function
    
    Expected input format:
    {
        "input": {
            "image": "image url",
            "text": "Describe this image",
        }
    }
    """
    try:
        # Load model if not already loaded
        load_model()
        
        # Extract job input
        job_input = job.get("input", {})
        
        # Validate required inputs
        if "image" not in job_input:
            return {"error": "Missing required 'image' field in input"}
        
        # Process inputs
        inputs = processor.process(
            images=[Image.open(requests.get(job_input.get('image'), stream=True).raw)],
            text= job_input.get("text", "Describe this image")
        )
        
        # Move to device and add batch dimension
        inputs = {k: v.to(model.device).unsqueeze(0) for k, v in inputs.items()}
        
        output = model.generate_from_batch(
            inputs,
            GenerationConfig(max_new_tokens=200, stop_strings="<|endoftext|>"),
            tokenizer=processor.tokenizer
        )
        
        # Decode generated text
        generated_tokens = output[0, inputs['input_ids'].size(1):]
        generated_text = processor.tokenizer.decode(generated_tokens, skip_special_tokens=True)
        
        return {
            "output": generated_text
        }
        
    except Exception as e:
        return {"error": f"Processing failed: {str(e)}"}

# Start the Serverless function when the script is run
if __name__ == '__main__':
    runpod.serverless.start({'handler': handler })