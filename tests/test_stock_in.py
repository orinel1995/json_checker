def test_example(json_data_prepared):
    data = json_data_prepared
    assert isinstance(data, dict)


def test_doc_type(json_data_prepared):
    data = json_data_prepared
    assert data["type"] == 2
