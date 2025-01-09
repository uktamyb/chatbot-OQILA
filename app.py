from flask import Flask, request, jsonify, render_template
import openai
import requests

app = Flask(__name__)

# Set your OpenAI API key here
openai.api_key = 'OPENAI_API_KEY'

# Set your Google Custom Search API key and Search Engine ID here
google_api_key = 'GOOGLE_API_KEY'
search_engine_id = 'SEARCH_ENGINE_ID'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        print(f"OpenAI response: {response}")  # Debugging line
        return jsonify({'response': response.choices[0].message['content'].strip()})
    except Exception as e:
        print(f"Error: {e}")  # Debugging line
        return jsonify({'response': 'Sorry, something went wrong.'}), 500

@app.route('/websearch', methods=['POST'])
def websearch():
    query = request.json.get('query')
    params = {
        'key': google_api_key,
        'cx': search_engine_id,
        'q': query,
    }
    try:
        response = requests.get('https://www.googleapis.com/customsearch/v1', params=params)
        response.raise_for_status()
        search_results = response.json()
        print(f"Google API response: {search_results}")  # Debugging line
        top_result = search_results['items'][0]['snippet']
        return jsonify({'results': top_result})
    except Exception as e:
        print(f"Error: {e}")  # Debugging line
        print(f"Response content: {response.content}")  # Debugging line
        return jsonify({'results': 'Sorry, something went wrong with the web search.'}), 500

if __name__ == '__main__':
    app.run(debug=True)