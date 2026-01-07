from concurrent.futures import ThreadPoolExecutor
from models.openai_model import chatgpt_response
from models.gemini_model import gemini_response
from models.llama_model import llama_response
from utils.metrics import log_metrics
import time
import csv
import os
from datetime import datetime

MODEL_FUNCTIONS = {
    "ChatGPT": chatgpt_response,
    "Gemini": gemini_response,
    "LLaMA": llama_response,
}


def run_parallel(prompt):
    """Run all configured models in parallel for a single prompt.

    Returns a dict mapping model display names to their responses.
    """
    results = {}

    def call_model(model_name):
        start_time = time.time()
        try:
            response = MODEL_FUNCTIONS[model_name](prompt)
        except Exception as e:
            response = f"Error: {e}"
        elapsed = time.time() - start_time
        log_metrics(model_name, elapsed, len(response))
        return response

    with ThreadPoolExecutor(max_workers=len(MODEL_FUNCTIONS)) as executor:
        futures = {name: executor.submit(call_model, name) for name in MODEL_FUNCTIONS}
        for name, future in futures.items():
            try:
                results[name] = future.result()
            except Exception as e:
                results[name] = f"Unexpected error: {e}"

    return results


def generate_report(prompt, responses, out_path=None):
    """Generate a CSV report with the prompt and each model's response.

    Returns the path to the generated CSV file.
    """
    if out_path is None:
        out_path = os.path.join(os.path.dirname(_file_), "..", "llm_comparison_report.csv")
        out_path = os.path.abspath(out_path)

    fieldnames = ["timestamp", "prompt", "model", "response"]
    timestamp = datetime.utcnow().isoformat()

    # Ensure directory exists
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    with open(out_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for model, resp in responses.items():
            writer.writerow({
                "timestamp": timestamp,
                "prompt": prompt,
                "model": model,
                "response": resp,
            })

    return out_path