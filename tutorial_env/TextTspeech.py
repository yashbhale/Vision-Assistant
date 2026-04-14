from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Set up the service
authenticator = IAMAuthenticator('your-ibm-api-key')
text_to_speech = TextToSpeechV1(authenticator=authenticator)
text_to_speech.set_service_url('your-service-url')

def synthesize_text(text, output_file):
    with open(output_file, 'wb') as audio_file:
        audio_file.write(
            text_to_speech.synthesize(
                text,
                voice='en-IN_Neural',  # This is an example; check IBM for exact voice codes
                accept='audio/mp3'
            ).get_result().content
        )
    print(f'Audio content written to "{output_file}"')

# Example usage
synthesize_text("Hello, this is a test message in English.", "output.mp3")
