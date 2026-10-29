import pytest
from yandex import Ya_Disk


import pytest
from yandex import Ya_Disk


@pytest.mark.parametrize(
    ("size_bytes", "expected_result"),
    [
        (500, "500.00 B"),
        (1024, "1.00 KB"),
        (1048576, "1.00 MB"),
    ],
)
def test_human_size_returns_readable_size(
    size_bytes: int,
    expected_result: str,
) -> None:
    result = Ya_Disk.human_size(size_bytes)

    assert result == expected_result

@pytest.mark.parametrize('name_file', ['passed.txt', 'passed-2.txt'])
def test_chek_file_returns_path_for_existing_file(name_file: str, tmp_path):
    file_path = tmp_path / name_file

    file_path.write_text("mode=test", encoding="utf-8")

    result = Ya_Disk.chek_file(file_path)

    assert result.exists()
    assert result.is_file()
    assert result == file_path




def test_chek_file_raises_file_not_found_for_missing_file(tmp_path):
    file_path = tmp_path / 'non_passed.txt'
    with pytest.raises(FileNotFoundError):
        Ya_Disk.chek_file(file_path)


@pytest.fixture
def fake_client(monkeypatch):
    client = Ya_Disk("fake-token")

    def fake_check_url_GET(url_API):
        return {
            "total_space": 1073741824,
            "used_space": 1048576,
        }

    monkeypatch.setattr(client, "check_url_GET", fake_check_url_GET)

    return client


def test_get_resourse_formats_disk_space(fake_client):
    result = fake_client.get_resourse("/v1/disk")

    assert "1.00 GB" in result
    assert "1.00 MB" in result


def test_get_url_to_load_file_returns_href_and_method(monkeypatch):
    client = Ya_Disk("fake-token")

    def fake_check_url_GET(url_API, params=None):
        return {
            "href": "https://fake-upload-url",
            "method": "PUT",
        }

    monkeypatch.setattr(client, "check_url_GET", fake_check_url_GET)

    result = client.get_url_to_load_file(
        "/v1/disk/resources/upload",
        "/test/file.txt",
    )

    assert result == ("https://fake-upload-url", "PUT")
