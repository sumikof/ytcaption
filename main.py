import os
from flask import Flask, make_response, jsonify, request
from flask_cors import CORS
from vtt_to_srt.vtt_to_srt import vtt_to_srt
import re

import youtube_caption
from youtube_caption import vttfile_download

app = Flask(__name__)
CORS(
    app,
    supports_credentials=True
)


def caption(caption_list: list):
    index = caption_list.pop(0)
    time = caption_list.pop(0)
    hash = {
        "index": index,
        "caption": "\n".join(caption_list)
    }

    result = re.match("(.+)-->(.+)", time)
    if result:
        hash["start"] = result.group(1).strip()
        hash["end"] = result.group(2).strip()
    return hash


def captions_json(captions: list):
    hash_list = []
    try:
        for i in range(1, len(captions)):
            index = captions.index(f"{i}")
            if index != 0:
                hash_list.append(caption(captions[0:index]))
                del captions[0:index]
    except ValueError as e:
        hash_list.append(caption(captions))
    finally:
        return hash_list


@app.route('/captions/list', methods=['GET'])
def youtube_captions_list():
    video_id = request.args.get("vid")
    print(video_id)
    return jsonify(youtube_caption.get_caption_list(video_id))


@app.route('/captions/download', methods=['GET'])
def youtube_caption_download():
    video_id = request.args.get("vid")
    lang = request.args.get("lang")
    sub_option = request.args.get("sub_option")

    target_url = f'https://youtu.be/{video_id}'

    if lang != "en" and lang != "ja":
        return jsonify({'error': 'Not support language. set lang en or ja'})

    if sub_option != "--write-sub" and sub_option != "--write-auto-sub":
        return jsonify({'error': 'Not support option. set option --write-sub or --write-auto-sub'})

    vtt_path = os.path.join('/tmp', f'{video_id}.{lang}.vtt')
    srt_path = os.path.join('/tmp', f'{video_id}.{lang}.srt')

    ret_code = ''
    try:
        vttfile_download(target_url, lang, sub_option)
    except BaseException as e:
        print(f'finish youtube download retcode {e}')
        ret_code = f'{e}'

    if ret_code == '' or ret_code == '1':
        return jsonify({'error': 'error youtube douwnload'})

    if not os.path.exists(vtt_path):
        return jsonify({'error': f'not found vtt file {vtt_path}'})

    vtt_to_srt(vtt_path)
    if not os.path.exists(srt_path):
        return jsonify({'error': f'convert error srt file {srt_path}'})

    response = {"lang": lang}
    with open(srt_path, "r") as srtfile:
        captions = [s.rstrip() for s in srtfile.readlines()]
    captions = [s for s in captions if s != ""]
    response["captions"] = captions_json(captions)

    os.remove(vtt_path)
    os.remove(srt_path)
    return response


if __name__ == '__main__':
    app.run(host='localhost', port=3000, debug=True)
