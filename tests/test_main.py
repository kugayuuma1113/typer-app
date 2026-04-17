from pathlib import Path

import pytest

from main import read_pdf

# このテストと同じフォルダ（tests/）に置く PDF の名前
TEST_PDF = Path(__file__).resolve().parent / "test.pdf"


def test_read_pdf_file_not_found():
    """パスにファイルが無いとき、read_pdf は FileNotFoundError を出すはず、というテスト。"""
    missing = Path(__file__).resolve().parent / "この名前のファイルは存在しない.pdf"
    with pytest.raises(FileNotFoundError):
        read_pdf(str(missing))


def test_read_pdf_reads_tests_pdf():
    """
    tests/test.pdf を読み、何かしら文字列が返ることを確認する。

    まだ test.pdf を置いていないときは、このテストだけスキップする（全体は失敗させない）。
    """
    if not TEST_PDF.is_file():
        pytest.skip("tests/test.pdf を追加するとこのテストが実行されます")

    text = read_pdf(str(TEST_PDF))
    assert isinstance(text, str)
    assert len(text) > 0
