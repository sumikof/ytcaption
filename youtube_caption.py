import youtube_dl
import google_oauth_cred


def get_caption_list(video_id: str):
    youtube = google_oauth_cred.get_oauth_cred()
    request = youtube.captions().list(
        part="snippet",
        videoId=video_id,
    )
    return request.execute()


def vttfile_download(target_url: str, lang: str, sub_option: str):
    youtube_dl.main(
        ['--sub-lang', lang, sub_option, '--skip-download', '--sub-format', 'vtt',
         '-o' '/tmp/%(id)s',
         target_url])


if __name__ == '__main__':
    print(get_caption_list('_CIHLJHVoN8'))
