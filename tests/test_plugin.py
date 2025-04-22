import pytest
from unittest.mock import Mock, patch
from poetry.plugins import Plugin

from src.poetry_plugin_truststore.plugin import PoetryPluginTruststore


@pytest.fixture
def plugin():
    return PoetryPluginTruststore()


@pytest.fixture
def mock_poetry():
    return Mock()


@pytest.fixture
def mock_io():
    io = Mock()
    io.is_verbose.return_value = False
    return io


class TestPoetryPluginTruststore:
    def test_is_plugin_instance(self, plugin):
        assert isinstance(plugin, Plugin)

    @patch("src.poetry_plugin_truststore.plugin.truststore.inject_into_ssl")
    @patch("src.poetry_plugin_truststore.plugin.version")
    def test_activate_non_verbose(
        self, mock_version, mock_inject, plugin, mock_poetry, mock_io
    ):
        plugin.activate(mock_poetry, mock_io)

        mock_io.is_verbose.assert_called_once()
        mock_version.assert_not_called()
        mock_inject.assert_called_once()

    @patch("src.poetry_plugin_truststore.plugin.truststore.inject_into_ssl")
    @patch("src.poetry_plugin_truststore.plugin.version")
    def test_activate_verbose(
        self, mock_version, mock_inject, plugin, mock_poetry, mock_io
    ):
        mock_version.return_value = "1.2.3"
        mock_io.is_verbose.return_value = True

        plugin.activate(mock_poetry, mock_io)

        mock_io.is_verbose.assert_called_once()
        mock_version.assert_called_once_with("truststore")
        mock_inject.assert_called_once()
        mock_io.write_line.assert_called_once_with(
            "Using system cert store via Truststore 1.2.3"
        )

    @patch("src.poetry_plugin_truststore.plugin.truststore.inject_into_ssl")
    def test_activate_truststore_injection(
        self, mock_inject, plugin, mock_poetry, mock_io
    ):
        plugin.activate(mock_poetry, mock_io)
        mock_inject.assert_called_once()