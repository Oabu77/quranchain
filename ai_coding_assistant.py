#!/usr/bin/env python3

from transformers import AutoTokenizer, AutoModelForCausalLM
import requests
import subprocess
import os
import torch
import json
import logging
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

# Configuration
MODEL_NAME = "Salesforce/codegen-350M-multi"
OFFLOAD_FOLDER = "./offload_weights"
LOG_FILE = "ai_feedback_log.txt"
API_BASE_URL = "http://localhost:5000"

# Ensure directories
os.makedirs(OFFLOAD_FOLDER, exist_ok=True)

# Logging
logging.basicConfig(
    filename="ai_coding_assistant.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Load model and tokenizer
print("[INFO] Loading tokenizer and model... This may take a moment.")
logging.info("Loading tokenizer and model.")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float32,
    device_map="auto",
    offload_folder=OFFLOAD_FOLDER
)

# Auto-completion for CLI input
generators = ["Python", "JavaScript", "HTML", "CSS", "SQL", "Markdown", "Kubernetes", "Dockerfile", "JSON", "AI"]
generator_completer = WordCompleter(generators)

templates = {
    "Python": ["hello_world", "rest_api"],
    "HTML": ["basic_page", "form_page"],
    "CSS": ["basic_styles", "responsive_styles"],
    # Add more templates here
}
template_completer = WordCompleter(list(templates.keys()))


# API Integration
def connect_to_api(endpoint, method="GET", data=None):
    """Connect to the TemplateService API."""
    try:
        url = f"{API_BASE_URL}/{endpoint}"
        response = requests.request(method, url, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to connect to API: {e}")
        logging.error(f"API Connection Error: {e}")
        return None


# Local AI Code Generation
def generate_code(task_description, language="Python"):
    """Generate code locally using the model."""
    print(f"\n[INFO] Generating {language} code for task locally...")
    prompt = f"# Task: {task_description}\n# Language: {language}\n"
    inputs = tokenizer.encode(prompt, return_tensors="pt").to("cpu")
    outputs = model.generate(inputs, max_length=512, temperature=0.7)
    code = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print("\n[INFO] Generated Code Locally:\n")
    print(code)
    return code


# API-Enhanced Functionality
def generate_code_with_api(generator_name, template_name, params=None):
    """Generate code using TemplateService API."""
    print(f"\n[INFO] Generating code via API ({generator_name}: {template_name})...")
    response = connect_to_api("generate_template", method="POST", data={
        "generator_name": generator_name,
        "template_name": template_name,
        "params": params or {}
    })
    if response and "template" in response:
        code = response["template"]
        print("\n[INFO] Generated Code via API:\n")
        print(code)
        return code
    else:
        print("[ERROR] Failed to generate code via API.")
        return None


def save_code_with_api(generator_name, template_name, params=None):
    """Save code using the TemplateService API."""
    print(f"\n[INFO] Saving code via API ({generator_name}: {template_name})...")
    response = connect_to_api("save_template", method="POST", data={
        "generator_name": generator_name,
        "template_name": template_name,
        "params": params or {}
    })
    if response and "file_path" in response:
        file_path = response["file_path"]
        print(f"\n[INFO] Code saved to {file_path} via API.")
        return file_path
    else:
        print("[ERROR] Failed to save code via API.")
        return None


def interactive_menu():
    """Interactive CLI Menu."""
    while True:
        print("\nAI Coding Assistant Menu:")
        print("1. Generate Code Locally")
        print("2. Generate Code via API")
        print("3. Save Code via API")
        print("4. Exit")
        choice = input("Choose an option (1-4): ")
        if choice == "1":
            task = input("Enter the programming task description:\n> ")
            language = input("Enter the programming language (default: Python):\n> ") or "Python"
            code = generate_code(task, language)
        elif choice == "2":
            generator_name = prompt("Enter the generator name:\n> ", completer=generator_completer)
            template_name = prompt("Enter the template name:\n> ", completer=template_completer)
            params = input("Enter additional parameters as JSON (or leave blank):\n> ")
            try:
                params = json.loads(params) if params else {}
            except json.JSONDecodeError:
                print("[ERROR] Invalid JSON format for parameters.")
                params = {}
            generate_code_with_api(generator_name, template_name, params)
        elif choice == "3":
            generator_name = prompt("Enter the generator name:\n> ", completer=generator_completer)
            template_name = prompt("Enter the template name:\n> ", completer=template_completer)
            params = input("Enter additional parameters as JSON (or leave blank):\n> ")
            try:
                params = json.loads(params) if params else {}
            except json.JSONDecodeError:
                print("[ERROR] Invalid JSON format for parameters.")
                params = {}
            save_code_with_api(generator_name, template_name, params)
        elif choice == "4":
            print("[INFO] Exiting AI Coding Assistant.")
            break
        else:
            print("[ERROR] Invalid choice. Please try again.")


def main():
    """Main program loop."""
    print("Welcome to the Advanced AI Coding Assistant!")
    interactive_menu()


if __name__ == "__main__":
    main()
