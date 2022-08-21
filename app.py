from flask import *
import cohere
import os

app = Flask(__name__, template_folder='templates')

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html', content=get_transcripts())

@app.route('/api/v1/upload', methods=['POST'])
def upload():
    f = request.files['file']
    f.save(dst='C:\\Users\\Manav\\stuff\\ht6-2\\playground\\recordings\\' + f.filename)
    os.system('python transcriber.py ' + 'recordings/ ' + f.filename) # the space is intentional
    return render_template('home.html', content=get_transcripts())

@app.route('/api/v1/get-transcript', methods=['GET'])
def get_transcript():
    return jsonify({"transcript": get_transcript_contents(request.args.get('selected_transcript'))})

@app.route('/api/v1/get-summary', methods=['GET'])
def summarize():
    prompt = get_transcript_contents(request.args.get('selected_summary'))
    prompt += '\n The most important points to take away from the above text are:'

    approx_word_count = prompt.count(' ')
    tokens = approx_word_count // 3

    if tokens < 10:
        tokens = 10

    client = cohere.Client('', '2021-11-08') # api key removed
    response = client.generate(
        model='large',
        num_generations=1,
        prompt=prompt,
        max_tokens=tokens,
        temperature=0.3,
        frequency_penalty=0.9,
        k=0,
        p=0.75)

    return jsonify({"summary": (response.generations[0].text) + '...'})

def get_transcripts():
    transcripts_list = []
    for transcript in os.listdir('./transcripts/'):
        transcripts_list.append(transcript.replace('.txt', ''))
    return transcripts_list

def get_transcript_count():
    transcript_count = 0
    for transcript in os.listdir('./transcripts/'):
        transcript_count += 1
    return transcript_count

def get_transcript_contents(name):
    f = open('./transcripts/' + name + '.txt', 'r', encoding='utf8')
    contents = f.read()
    return contents

async def run_speech_to_text_script(filename):
    os.system('python transcriber.py ' + 'recordings/ ' + filename) # the space is intentional
    return None

if __name__ == '__main__':
    app.run()
