import streamlit as st
import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech.audio import AudioOutputConfig
from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer, AudioConfig

import requests, uuid, json
st.title("Scripter")
st.sidebar.title('Scripter')
st.sidebar.text("choose")
st.sidebar.title('Page Selection Menu')
page = st.sidebar.radio("Select Page:",("Translator","Audio-Text"))


if page=='Translator':
	text=st.text_area("Enter your text",value="Hi")
	target_lang=st.text_input("Enter target language", value='it')
	subscription_key = "be795affb9e0402294ae191fcb16fe9b"
	endpoint = "https://api.cognitive.microsofttranslator.com"
	location = "eastus"
	path = '/translate'
	constructed_url = endpoint + path

	params = {
	    'api-version': '3.0',
	    'to': target_lang
	}
	constructed_url = endpoint + path

	headers = {
	    'Ocp-Apim-Subscription-Key': subscription_key,
	    'Ocp-Apim-Subscription-Region': location,
	    'Content-type': 'application/json',
	    'X-ClientTraceId': str(uuid.uuid4())
	}
	body = [{
	    'text': text
	}]

	request = requests.post(constructed_url, params=params, headers=headers, json=body)
	response = request.json()

	if st.button("Submit"):
		st.write(response[0]['translations'][0]['text'])


if page=="Audio-Text":
	speech_config = speechsdk.SpeechConfig(subscription="db46884b588046fcaa37ec16b66df1ed", region="eastus")
	# file=st.file_uploader("Uploader")
	audio=st.audio("audi.wav")
	audio_config = speechsdk.audio.AudioConfig(filename="audi.wav")
	speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

	result = speech_recognizer.recognize_once()
	if st.button("Translate"):
		# Check the result
		if result.reason == speechsdk.ResultReason.RecognizedSpeech:
		    st.markdown("Recognized: {}".format(result.text))
		elif result.reason == speechsdk.ResultReason.NoMatch:
		    st.markdown("No speech could be recognized: {}".format(result.no_match_details))
		elif result.reason == speechsdk.ResultReason.Canceled:
		    cancellation_details = result.cancellation_details
		    st.markdown("Speech Recognition canceled: {}".format(cancellation_details.reason))
		    if cancellation_details.reason == speechsdk.CancellationReason.Error:
		        st.markdown("Error details: {}".format(cancellation_details.error_details))