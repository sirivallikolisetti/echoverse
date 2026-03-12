import requests
import logging

logging.basicConfig(level=logging.INFO)

HF_TOKEN = "YOUR_HUGGINGFACE_TOKEN"  # Replace with your token
API_URL = "https://api-inference.huggingface.co/models/ibm-granite/granite-13b-chat"

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

def query_ibm_granite(prompt: str) -> str:
    payload = {
        "inputs": prompt,
        "options": {"wait_for_model": True}
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        result = response.json()

        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"]
        elif isinstance(result, dict) and "generated_text" in result:
            return result["generated_text"]
        else:
            logging.warning("Unexpected response format from Hugging Face API.")
            return "⚠ The model did not return any text."
    except Exception as e:
        logging.error(f"Error in query_ibm_granite: {e}")
        return "❌ An error occurred while querying the model."
