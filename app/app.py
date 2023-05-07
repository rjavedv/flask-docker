import requests, os, uuid, json
import openai
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, redirect, url_for, request, render_template, session

app = Flask(__name__)

gorgkey = os.getenv('OAIORG')
gapikey = os.getenv('OAIKEY')
gmodel="gpt-3.5-turbo"
gsystem="You are a general purpose AI assistant."
gresponse = " "

openai.api_key = gapikey
messages = [{"role": "system", "content": gsystem}]

@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')

@app.route('/trans', methods=['GET'])
def tr_index():
	return render_template('tr_index.html')

@app.route('/trans', methods=['POST'])
def index_post():
    # Read the values from the form
    original_text = request.form['text']
    target_language = request.form['language']

    # Load the values from .env
    key = os.environ['KEY']
    endpoint = os.environ['ENDPOINT']
    location = os.environ['LOCATION']

    #print(key,location)
    # Indicate that we want to translate and the API version (3.0) and the target language
    path = '/translate?api-version=3.0'
    # Add the target language parameter
    target_language_parameter = '&to=' + target_language
    # Create the full URL
    constructed_url = endpoint + path + target_language_parameter

    # Set up the header information, which includes our subscription key
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # Create the body of the request with the text to be translated
    body = [{ 'text': original_text }]
    #print(constructed_url)

    # Make the call using post
    translator_request = requests.post(constructed_url, headers=headers, json=body)
    # Retrieve the JSON response
    translator_response = translator_request.json()
    # Retrieve the translation
    #print(translator_response)
    translated_text = translator_response[0]['translations'][0]['text']

    # Call render template, passing the translated text,
    # original text, and target language to the template
    return render_template(
        'results.html',
        translated_text=translated_text,
        original_text=original_text,
        target_language=target_language
    )

@app.route('/openai', methods=['GET'])
def oi_index():
	global gresponse
	global messages
	
	gresponse = " "
	messages.clear()
	messages.append({"role": "system", "content": gsystem})
	return render_template('oi_index.html',
			                systemtemplate=gsystem)

@app.route('/openai', methods=['POST'])
def oi_index_post():
	global messages
	global gresponse

	temp_str = request.form['reqtext']
	if temp_str:
		messages.append({"role": "user", "content": temp_str})
		#print(messages)
		lresponse = openai.ChatCompletion.create(model=gmodel, messages=messages)
		system_message = lresponse["choices"][0]["message"]
		messages.append(system_message)
		chat_transcript = ""
		for message in messages:
			if message['role'] != 'system':
				chat_transcript += message['role'] + ": " + message['content'] + "\n\n"

		#gresponse = chat_transcript
		return render_template('oi_index.html',
			                systemtemplate=gsystem,
			                sresponse=chat_transcript)	

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)