
import torch
import json
import os
import WordMatching as wm
import utilsFileIO
import pronunciationTrainer
import base64
import time
import soundfile as sf
import subprocess
import numpy as np
from torchaudio.transforms import Resample
import io
import tempfile

trainer_SST_lambda = {}
trainer_SST_lambda['de'] = pronunciationTrainer.getTrainer("de")
trainer_SST_lambda['en'] = pronunciationTrainer.getTrainer("en")

transform = Resample(orig_freq=48000, new_freq=16000)


def lambda_handler(event, context):

    data = json.loads(event['body'])

    real_text = data['title']
    file_bytes = base64.b64decode(
        data['base64Audio'][22:].encode('utf-8'))
    language = data['language']

    if len(real_text) == 0:
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Credentials': "true",
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps({
                'pronunciation_accuracy': '0',
                'ipa_transcript': '',
                'real_transcripts_ipa': '',
                'matched_transcripts_ipa': '',
                'pair_accuracy_category': '',
                'is_letter_correct_all_words': '',
                'start_time': '',
                'end_time': ''
            })
        }

    try:
        with tempfile.NamedTemporaryFile(suffix=".ogg", delete=True) as tmp:
            tmp.write(file_bytes)
            tmp.flush()
            tmp_name = tmp.name
            
            # Convert OGG to WAV using FFmpeg
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as wav_tmp:
                wav_name = wav_tmp.name
                try:
                    subprocess.run([
                        'ffmpeg', '-i', tmp_name, '-acodec', 'pcm_s16le', 
                        '-ar', '48000', '-ac', '1', '-y', wav_name
                    ], check=True, capture_output=True)
                    signal, fs = sf.read(wav_name, dtype='float32')
                    
                    # Check if audio was successfully read
                    if len(signal) == 0:
                        print("Warning: Empty audio signal after conversion")
                        return json.dumps({
                            'pronunciation_accuracy': '0',
                            'ipa_transcript': '',
                            'real_transcripts_ipa': '',
                            'matched_transcripts_ipa': '',
                            'pair_accuracy_category': '',
                            'is_letter_correct_all_words': '',
                            'start_time': '',
                            'end_time': ''
                        })
                        
                except subprocess.CalledProcessError as e:
                    print(f"FFmpeg conversion failed: {e}")
                    return json.dumps({
                        'pronunciation_accuracy': '0',
                        'ipa_transcript': '',
                        'real_transcripts_ipa': '',
                        'matched_transcripts_ipa': '',
                        'pair_accuracy_category': '',
                        'is_letter_correct_all_words': '',
                        'start_time': '',
                        'end_time': ''
                    })
                    
        signal = transform(torch.Tensor(signal)).unsqueeze(0)

        result = trainer_SST_lambda[language].processAudioForGivenText(
            signal, real_text)
            
    except Exception as e:
        print(f"Error processing audio: {e}")
        return json.dumps({
            'pronunciation_accuracy': '0',
            'ipa_transcript': '',
            'real_transcripts_ipa': '',
            'matched_transcripts_ipa': '',
            'pair_accuracy_category': '',
            'is_letter_correct_all_words': '',
            'start_time': '',
            'end_time': ''
        })

    #start = time.time()
    #os.remove(random_file_name)
    #print('Time for deleting file: ', str(time.time()-start))

    start = time.time()
    real_transcripts_ipa = ' '.join(
        [word[0] for word in result['real_and_transcribed_words_ipa']])
    matched_transcripts_ipa = ' '.join(
        [word[1] for word in result['real_and_transcribed_words_ipa']])

    real_transcripts = ' '.join(
        [word[0] for word in result['real_and_transcribed_words']])
    matched_transcripts = ' '.join(
        [word[1] for word in result['real_and_transcribed_words']])

    words_real = real_transcripts.lower().split()
    mapped_words = matched_transcripts.split()

    is_letter_correct_all_words = ''
    for idx, word_real in enumerate(words_real):

        mapped_letters, mapped_letters_indices = wm.get_best_mapped_words(
            mapped_words[idx], word_real)

        is_letter_correct = wm.getWhichLettersWereTranscribedCorrectly(
            word_real, mapped_letters)  # , mapped_letters_indices)

        is_letter_correct_all_words += ''.join([str(is_correct)
                                                for is_correct in is_letter_correct]) + ' '

    pair_accuracy_category = ' '.join(
        [str(category) for category in result['pronunciation_categories']])
    print('Time to post-process results: ', str(time.time()-start))

    res = {'real_transcript': result['recording_transcript'],
           'ipa_transcript': result['recording_ipa'],
           'pronunciation_accuracy': str(int(result['pronunciation_accuracy'])),
           'real_transcripts': real_transcripts, 'matched_transcripts': matched_transcripts,
           'real_transcripts_ipa': real_transcripts_ipa, 'matched_transcripts_ipa': matched_transcripts_ipa,
           'pair_accuracy_category': pair_accuracy_category,
           'start_time': result['start_time'],
           'end_time': result['end_time'],
           'is_letter_correct_all_words': is_letter_correct_all_words}

    return json.dumps(res)
