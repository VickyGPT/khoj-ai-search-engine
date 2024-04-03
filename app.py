import requests
import google.generativeai as genai

# Example usage
user_prompt = input("Enter your prompt: ")

# Fetch data from the API endpoint with the user prompt
api_url = f"https://khoj.doubtly.in/api/?q={user_prompt}"
response = requests.get(api_url)

if response.status_code == 200:
    data_from_api = response.json()
    # Extract text from title and description of each item and concatenate into a single string
    text_from_api = ' '.join([item.get("title", "") + " " + item.get("description", "") for item in data_from_api])
else:
    print("Error fetching data from the API")

genai.configure(api_key="AIzaSyCAfb-AR2QMVBA3TQXSS560jtXc-NJoFkI")

# Set up the model
generation_config = {
    "temperature": 1,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

def chat_with_model(user_prompt):
    full_input = text_from_api + " summarize all text based on query " + user_prompt
    convo = model.start_chat(history=[])
    convo.send_message(full_input)
    return convo.last.text

response = chat_with_model(user_prompt)
print("Model response:", response)
