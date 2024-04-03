from django.shortcuts import render
from django.http import JsonResponse
import requests
import google.generativeai as genai
import markdown2

# Configure Google Generative AI
genai.configure(api_key="bhai api kyu chaiye tumko")


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

def index(request):
    if request.method == 'POST':
        user_prompt = request.POST.get('user_prompt', '')
        
        # Fetch data from the API endpoint with the user prompt
        api_url = f"https://khoj.doubtly.in/api/?q={user_prompt}"
        response = requests.get(api_url)

        if response.status_code == 200:
            data_from_api = response.json()
            # Check if API response is empty
            if data_from_api:
                # Extract text from title and description of each item and concatenate into a single string
                text_from_api = ' '.join([item.get("title", "") + " " + item.get("url", "") + " " + item.get("description", "") for item in data_from_api])
            else:
                text_from_api = ""
                print("Empty response from the API")
        else:
            text_from_api = ""
            print("Error fetching data from the API")

        # Send user prompt along with text from the API to the model
        if text_from_api:
            full_input = text_from_api + " summarize all text based on query  " + user_prompt + " and make sure you include links you recieved related to " + user_prompt + " in this input and you will not use any other links or information , you have to stick only to this data which i provided you in this input  "
        else:
            # If API response is empty or incomplete, still send some input to the model
            full_input = f" {user_prompt}. send detailed response"

        convo = model.start_chat(history=[])
        convo.send_message(full_input)
        model_response = convo.last.text

        html_model_response = markdown2.markdown(model_response)
        
        return JsonResponse({'full_input': full_input, 'html_model_response': html_model_response})
        
    return render(request, 'index.html')

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def api_response(request):
    if request.method == 'GET':
        user_query = request.GET.get('q', '')
        
        # Fetch data from the API endpoint with the user query
        api_url = f"https://khoj.doubtly.in/api/?q={user_query}"
        response = requests.get(api_url)

        if response.status_code == 200:
            data_from_api = response.json()
            # Check if API response is empty
            if data_from_api:
                # Extract text from title and description of each item and concatenate into a single string
                text_from_api = ' '.join([item.get("title", "") + " " + item.get("url", "") + " " + item.get("description", "") for item in data_from_api])
            else:
                text_from_api = ""
                print("Empty response from the API")
        else:
            text_from_api = ""
            print("Error fetching data from the API")

        # Send user query along with text from the API to the model
        if text_from_api:
            full_input = text_from_api + f" summarize all text based on query {user_query} and make sure you include links you received related to {user_query} in this input."
        else:
            # If API response is empty or incomplete, still send some input to the model
            full_input = f" {user_query}"

        convo = model.start_chat(history=[])
        convo.send_message(full_input)
        model_response = convo.last.text

        html_model_response = markdown2.markdown(model_response)

        return JsonResponse({'query': user_query, 'full_input': full_input, 'html_model_response': html_model_response})

    return JsonResponse({'error': 'Invalid request method'})
