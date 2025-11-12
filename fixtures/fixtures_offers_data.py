import json
import os
from typing import Any, List
import pytest


def _get_json_filenames() -> List[str]:
    """Вспомогательная функция для получения списка JSON-файлов в папке data/."""
    data_dir = "data"
    if not os.path.exists(data_dir):
        raise FileNotFoundError(f"Папка {data_dir} не найдена.")
    return [f for f in os.listdir(data_dir) if f.endswith(".json")]


def _get_doc_number_from_file(filename: str) -> str:
    """Вспомогательная функция для извлечения doc number из файла."""
    filepath = os.path.join("data", filename)
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
        if isinstance(data, dict) and "number" in data:
            return data["number"]
        return "no_doc_number"


@pytest.fixture(scope="session")
def get_raw_data() -> list[Any]:
    """Фикстура для чтения всех JSON-файлов из папки data/."""
    data_dir = "data"
    result = []
    if not os.path.exists(data_dir):
        raise FileNotFoundError(f"Папка {data_dir} не найдена.")
    for filename in os.listdir(data_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(data_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    result.append(data)
                except json.JSONDecodeError as e:
                    raise ValueError(
                        f"Ошибка декодирования JSON в файле {filename}: {e}"
                    )
    return result


@pytest.fixture(scope="session")
def get_flow_types(get_raw_data) -> list[str]:
    """Фикстура для извлечения значений тега 'flowType' из JSON-данных."""
    flow_types = []
    for data in get_raw_data:
        if isinstance(data, dict):
            if "flowType" in data:
                flow_types.append(data["flowType"])
            else:
                flow_types.append("no_flow")
    return flow_types


@pytest.fixture(scope="session")
def get_doc_numbers(get_raw_data) -> list[str]:
    """Фикстура для извлечения значений тега 'number' из JSON-данных."""
    doc_numbers = []
    for data in get_raw_data:
        if isinstance(data, dict):
            if "number" in data:
                doc_numbers.append(data["number"])
            else:
                doc_numbers.append("no_doc_number")
    return doc_numbers


@pytest.fixture(
    params=_get_json_filenames(),
    ids=[_get_doc_number_from_file(f) for f in _get_json_filenames()],
    scope="session",
)
def json_data_prepared(request):
    """Параметризированная фикстура, возвращающая данные для каждого JSON-файла."""
    filename = request.param
    filepath = os.path.join("data", filename)
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data
