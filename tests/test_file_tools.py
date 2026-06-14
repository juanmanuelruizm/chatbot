import dataclasses

import pytest

from chatbot.config import settings
from chatbot.tools import file_tools


@pytest.fixture()
def sandbox(tmp_path, monkeypatch):
    """Apunta el sandbox de file_tools a un directorio temporal aislado."""
    scoped = dataclasses.replace(settings, allowed_base_dir=tmp_path.resolve())
    monkeypatch.setattr(file_tools, "settings", scoped)
    return tmp_path


def test_write_and_read_roundtrip(sandbox):
    target = sandbox / "nota.txt"
    file_tools.write_file(str(target), "hola mundo")
    assert file_tools.read_file(str(target)) == "hola mundo"


def test_read_missing_file_returns_error(sandbox):
    result = file_tools.read_file(str(sandbox / "no_existe.txt"))
    assert "not found" in result


def test_list_directory_lists_entries(sandbox):
    (sandbox / "a.txt").write_text("a")
    (sandbox / "b.txt").write_text("b")
    listing = file_tools.list_directory(str(sandbox))
    assert "a.txt" in listing
    assert "b.txt" in listing


def test_path_outside_sandbox_is_denied(sandbox):
    with pytest.raises(PermissionError):
        file_tools._safe_resolve("/etc/passwd")


def test_sibling_prefix_path_is_denied(sandbox):
    # Un directorio hermano con el mismo prefijo no debe burlar el sandbox.
    sibling = str(sandbox) + "-evil/secret.txt"
    with pytest.raises(PermissionError):
        file_tools._safe_resolve(sibling)


def test_write_creates_intermediate_dirs(sandbox):
    nested = sandbox / "sub" / "dir" / "f.txt"
    file_tools.write_file(str(nested), "x")
    assert nested.read_text() == "x"
