"""Tests for quickstart/check.py — health check scenarios."""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_check_python_passes(capsys):
    """check_python should pass on the current interpreter (>= 3.10)."""
    from quickstart.check import check_python

    result = check_python()
    captured = capsys.readouterr()
    assert result is True
    assert "\u2713" in captured.out


def test_check_package_installed(capsys):
    """check_package should pass for a package that's installed."""
    from quickstart.check import check_package

    result = check_package("os")
    captured = capsys.readouterr()
    assert result is True
    assert "\u2713" in captured.out


def test_check_package_missing(capsys):
    """check_package should fail for a package that doesn't exist."""
    from quickstart.check import check_package

    result = check_package("this_package_does_not_exist_xyz")
    captured = capsys.readouterr()
    assert result is False
    assert "\u2717" in captured.out


def test_check_ollama_binary_not_found(mocker, capsys):
    """check_ollama_binary should fail when ollama isn't on PATH."""
    from quickstart.check import check_ollama_binary

    mocker.patch("shutil.which", return_value=None)
    result = check_ollama_binary()
    captured = capsys.readouterr()
    assert result is False
    assert "\u2717" in captured.out
    assert "ollama.ai" in captured.out.lower()


def test_check_ollama_binary_found(mocker, capsys):
    """check_ollama_binary should pass when ollama is on PATH."""
    from quickstart.check import check_ollama_binary

    mocker.patch("shutil.which", return_value="/usr/local/bin/ollama")
    result = check_ollama_binary()
    captured = capsys.readouterr()
    assert result is True
    assert "\u2713" in captured.out


def test_check_ollama_running_success(mocker, capsys):
    """check_ollama_running should pass when ollama.list() responds."""
    from quickstart.check import check_ollama_running

    mock_ollama = mocker.patch("quickstart.check.ollama")
    mock_ollama.list.return_value = {"models": []}

    result = check_ollama_running()
    captured = capsys.readouterr()
    assert result is True
    assert "\u2713" in captured.out


def test_check_ollama_running_failure(mocker, capsys):
    """check_ollama_running should fail when ollama.list() raises."""
    from quickstart.check import check_ollama_running

    mock_ollama = mocker.patch("quickstart.check.ollama")
    mock_ollama.list.side_effect = ConnectionError("refused")

    result = check_ollama_running()
    captured = capsys.readouterr()
    assert result is False
    assert "\u2717" in captured.out


def test_check_model_found(mocker, capsys):
    """check_model should pass when the model is in ollama.list()."""
    from quickstart.check import check_model

    mock_model = mocker.MagicMock()
    mock_model.model = "llama3.1:8b"
    mock_models = mocker.MagicMock()
    mock_models.models = [mock_model]

    mock_ollama = mocker.patch("quickstart.check.ollama")
    mock_ollama.list.return_value = mock_models

    result = check_model("llama3.1:8b")
    captured = capsys.readouterr()
    assert result is True
    assert "\u2713" in captured.out


def test_check_model_not_found(mocker, capsys):
    """check_model should fail when the model is not available."""
    from quickstart.check import check_model

    mock_model = mocker.MagicMock()
    mock_model.model = "other-model:latest"
    mock_models = mocker.MagicMock()
    mock_models.models = [mock_model]

    mock_ollama = mocker.patch("quickstart.check.ollama")
    mock_ollama.list.return_value = mock_models

    result = check_model("llama3.1:8b")
    captured = capsys.readouterr()
    assert result is False
    assert "\u2717" in captured.out
