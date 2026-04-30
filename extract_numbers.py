import streamlit as st
import zipfile
import re
import os
import tempfile

st.title("📸 Извлечение номеров Shutterstock")

uploaded_file = st.file_uploader("Загрузи ZIP с изображениями", type="zip")

def extract_shutterstock_numbers(folder_path):
    numbers = []

    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            # Ищем длинные числа (шуттер обычно 6+ цифр)
            matches = re.findall(r"\d{6,}", filename)
            numbers.extend(matches)

    return sorted(set(numbers))


if uploaded_file is not None:
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