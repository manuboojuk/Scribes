import sys
from api_02 import *

filepath = sys.argv[1]
filename = sys.argv[2]
audio_url = upload(filepath + filename)

save_transcript(audio_url, 'transcripts/' + filename)