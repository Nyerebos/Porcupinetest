import openai
import pvporcupine
import pyaudio

porcu_access_key = "my api"
porcu_keyword_path = "/Erebus_en_windows_v2_2_0.ppn"
# Initialize the API key
openai.api_key = "my api"

# Initialize Porcupine wake word detection
porcupine = None
pa = None
audio_stream = None

def initialize_porcupine():
    keyword_path = porcu_keyword_path  # Path to your custom wake word file
    porcupine = pvporcupine.create(
        keywords=[keyword_path],
        access_key = porcu_access_key)
    pa = pyaudio.PyAudio()

def detect_wake_word():
    while True:
        pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
        pcm = pcm.flatten()
        keyword_index = porcupine.process(pcm)
        if keyword_index >= 0:
            print("Wake word detected!")
            return True
        else:
            return False
            print("Wai")
# Generate a response using the ChatGPT model
def generate_response(prompt):
    completions = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = completions.choices[0].text
    return message

# Greet the user
def greet_user():
    print("AI: Hello! How can I assist you today?")

# Main loop to handle user input
def main_loop():
    while True:
        prompt = input("You: ")
        response = generate_response(prompt)
        print("AI:", response)

# Initialize Porcupine wake word detection
initialize_porcupine()

# Main program flow
with pvporcupine.Porcupine(
    library_path=pvporcupine.LIBRARY_PATH,
    model_path=pvporcupine.MODEL_PATH,
    keyword_paths=[porcu_keyword_path],
) as porcupine:
    with pyaudio.PyAudio() as pa:
        audio_stream = pa.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length,
        )

        # Detect the wake word before starting the main loop
        if detect_wake_word():
            main_loop()
