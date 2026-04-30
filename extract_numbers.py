import streamlit as st
import zipfile
import re
import os
import tempfile

st.set_page_config(page_title="Shutterstock Extractor", page_icon="📸")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #111827 0%, #1f2937 45%, #312e81 100%);
    color: #f9fafb;
}

h1, h2, h3 {
    color: #f9fafb;
}

[data-testid="stFileUploader"] {
    background-color: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.18);
    border-radius: 16px;
    padding: 18px;
}

.stTextArea textarea {
    background-color: #111827;
    color: #f9fafb;
    border-radius: 12px;
}

.stDownloadButton button {
    border-radius: 999px;
    font-weight: 700;
    padding: 0.6rem 1.2rem;
}
</style>
""", unsafe_allow_html=True)

st.title("📸 Извлечение номеров Shutterstock")

uploaded_file = st.file_uploader("Загрузи ZIP с изображениями — получите список ID", type="zip")

def extract_shutterstock_numbers(folder_path):
    numbers = []

    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            # Ищем длинные числа (шуттер обычно 6+ цифр)
            matches = re.findall(r"\d{6,}", filename)
            numbers.extend(matches)

    return sorted(set(numbers))


if uploaded_file is not None:
    with st.spinner("Секунду, вытаскиваю номера..."):
        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = os.path.join(tmpdir, "files.zip")

            with open(zip_path, "wb") as f:
                f.write(uploaded_file.read())

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(tmpdir)

            numbers = extract_shutterstock_numbers(tmpdir)

        st.success(f"Готово! Найдено {len(numbers)} номеров ✨")

        result = "\n".join(numbers)

        st.download_button(
            label="📥 Скачать TXT",
            data=result,
            file_name="shutterstock_numbers.txt"
        )

st.markdown("""
<style>
.footer {
    position: fixed;
    bottom: 10px;
    right: 20px;
    font-size: 12px;
    color: rgba(255, 255, 255, 0.35);
}
</style>

<div class="footer">
Сделала Белоусова Дарья · Редакция Кладезь
</div>
""", unsafe_allow_html=True)