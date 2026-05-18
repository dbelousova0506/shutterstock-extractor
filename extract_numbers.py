import streamlit as st
import zipfile
import re
import os
import tempfile
from pathlib import Path

st.set_page_config(
    page_title="Shutterstock Extractor",
    page_icon="📸",
    layout="centered"
)

st.title("📸 Извлечение номеров Shutterstock")
st.write("Загрузите ZIP-архив с изображениями, а приложение соберёт длинные числовые ID из названий файлов.")

uploaded_file = st.file_uploader(
    "",
    type=["zip"]
)


def safe_extract_zip(zip_ref, extract_to):
    """
    Безопасная распаковка ZIP, чтобы файлы не могли распаковаться за пределы временной папки.
    """
    extract_to = Path(extract_to).resolve()

    for member in zip_ref.infolist():
        member_path = extract_to / member.filename
        resolved_path = member_path.resolve()

        if not str(resolved_path).startswith(str(extract_to)):
            raise ValueError("В архиве найден небезопасный путь файла.")

    zip_ref.extractall(extract_to)


def extract_shutterstock_numbers(folder_path):
    numbers = set()

    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            matches = re.findall(r"\d{6,}", filename)
            numbers.update(matches)

    return sorted(numbers, key=int)


if uploaded_file is not None:
    try:
        with st.spinner("Секунду, вытаскиваю номера..."):
            with tempfile.TemporaryDirectory() as tmpdir:
                zip_path = os.path.join(tmpdir, "files.zip")

                with open(zip_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                with zipfile.ZipFile(zip_path, "r") as zip_ref:
                    safe_extract_zip(zip_ref, tmpdir)

                numbers = extract_shutterstock_numbers(tmpdir)

        if numbers:
            st.success(f"Готово! Найдено номеров: {len(numbers)} ✨")

            result = "\n".join(numbers)

            st.text_area(
                "Найденные номера",
                value=result,
                height=250
            )

            st.download_button(
                label="📥 Скачать TXT",
                data=result,
                file_name="shutterstock_numbers.txt",
                mime="text/plain"
            )
        else:
            st.warning("Номера не найдены. Проверьте, есть ли в названиях файлов длинные числа.")

    except zipfile.BadZipFile:
        st.error("Файл не похож на корректный ZIP-архив.")
    except Exception as e:
        st.error(f"Что-то пошло не так: {e}")

st.markdown(
    "<div style='font-size:11px; color:#999; margin-top:100px;'>"
    "D. Belousova"
    "</div>",
    unsafe_allow_html=True
)
