from flask import Flask, request, jsonify
import requests
import json
import os

app = Flask(__name__)

# Replace with your OpenRouter API key or use environment variable
API_KEY = os.getenv("OPENROUTER_API_KEY", "<YOUR_API_KEY>")

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_input = data.get('text')
    
    if not user_input:
        return jsonify({"error": "No input provided"}), 400
    
    user_question = {
        "type": "text",
        "text": user_input
    }
    
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "model": "qwen/qwen2.5-vl-3b-instruct:free",
                "messages": [
                    {
                        "role": "user",
                        "content": [user_question]
                    }
                ],
            })
        )
        
        if response.status_code == 200:
            response_data = response.json()
            assistant_reply = response_data['choices'][0]['message']['content']
            return jsonify({"response": assistant_reply})
        else:
            error_msg = f"Request failed with status code {response.status_code}: {response.text}"
            return jsonify({"error": error_msg}), response.status_code
            
    except Exception as e:
        error_msg = f"Error processing request: {str(e)}"
        return jsonify({"error": error_msg}), 500

if __name__ == '__main__':
    app.run(debug=True)
