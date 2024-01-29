import os
import tempfile
import whisper
import streamlit as st

def transcribe_file(file_path):
    model = whisper.load_model("medium")
    result = model.transcribe(file_path,verbose=True)
    return result["text"]

st.title('文字起こし')
st.header('概要')
st.write('音声ファイルを入れてください')

upload_file = st.file_uploader('ファイルのアップロード', type=['mp3', 'mp4', 'wav'])

if upload_file is not None:
    # 一時ファイルとして保存
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(upload_file.name)[1]) as tmp_file:
        tmp_file.write(upload_file.getvalue())
        tmp_file_path = tmp_file.name

    st.audio(upload_file)

    st.write('文字起こしです')
    if st.button('開始'):
        comment = st.empty()
        comment.write('文字起こしを開始します')
        text = transcribe_file(tmp_file_path)
        comment.write('完了しました。テキストファイルとしてダウンロードできます')
        
        # 結果を表示
        st.write(text)

        # 結果をテキストファイルに書き込み
        _, txt_file_path = tempfile.mkstemp(suffix='.txt')  # 一時ファイルの作成
        with open(txt_file_path, 'w') as txt_file:
            txt_file.write(text)

        # ダウンロード用リンクを作成
        with open(txt_file_path, 'rb') as file:
            btn = st.download_button(
                label="テキストファイルとしてダウンロード",
                data=file,
                file_name="transcription.txt",
                mime="text/plain"
            )
    os.unlink(tmp_file_path)  # 一時ファイルを削除
