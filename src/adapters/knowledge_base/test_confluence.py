
import datetime
from unittest.mock import MagicMock, patch

from pydantic import HttpUrl

from src.adapters.knowledge_base.confluence import ConfluenceConnector
from src.models.knowledge_base import KnowledgeBaseArticle


def get_mock_confluence_connector():
    """
    Creates a mock ConfluenceConnector for testing purposes.
    """
    with patch("src.adapters.knowledge_base.confluence.Confluence") as mock_confluence_client:
        connector = ConfluenceConnector(
            url="http://fake-confluence.com",
            api_key="fake_api_key",
            space_key="FAKE",
            username="fake_user",
        )
        connector.confluence = mock_confluence_client
        return connector

def test_convert_to_article():
    """
    Test suite for the _convert_to_article method.
    """
    # Arrange
    connector = get_mock_confluence_connector()
    mock_page_content = {
        "id": "12345",
        "title": "Test Page",
        "body": {"storage": {"value": "<p>This is a test page.</p>"}},
        "_links": {"webui": "/display/FAKE/Test+Page"},
        "space": {"key": "FAKE", "name": "Fake Space"},
        "version": {"when": "2025-07-08T10:00:00.000Z"},
    }

    expected_article = KnowledgeBaseArticle(
        id="12345",
        source="Confluence",
        title="Test Page",
        content="<p>This is a test page.</p>",
        url=HttpUrl("http://fake-confluence.com/wiki/display/FAKE/Test+Page"),
        service="FAKE",
        owner_team="Fake Space",
        last_updated=datetime.datetime(2025, 7, 8, 10, 0, 0, tzinfo=datetime.timezone.utc),
    )

    print(expected_article)

    # Act
    article = connector._convert_to_article(mock_page_content)
    print(article)

    # Assert
    assert article.model_dump() == expected_article.model_dump()

def test_fetch_articles_success():
    """
    Test suite for the fetch_articles method.
    """
    # Arrange
    connector = get_mock_confluence_connector()
    mock_page_summary = {"id": "12345"}
    mock_page_content = {
        "id": "12345",
        "title": "Test Page",
        "body": {"storage": {"value": "<p>This is a test page.</p>"}},
        "_links": {"webui": "/display/FAKE/Test+Page"},
        "space": {"key": "FAKE", "name": "Fake Space"},
        "version": {"when": "2025-07-08T10:00:00.000Z"},
    }

    connector.confluence.get_all_pages_from_space.return_value = [mock_page_summary]
    connector.confluence.get_page_by_id.return_value = mock_page_content

    # Act
    articles = connector.fetch_articles()

    # Assert
    assert len(articles) == 1
    assert articles[0].title == "Test Page"
    connector.confluence.get_all_pages_from_space.assert_called_once_with("FAKE")
    connector.confluence.get_page_by_id.assert_called_once_with("12345", expand="body.storage,version,space")

def test_fetch_articles_api_error():
    """
    Test that fetch_articles handles ApiError gracefully.
    """
    # Arrange
    connector = get_mock_confluence_connector()
    from atlassian.errors import ApiError
    connector.confluence.get_all_pages_from_space.side_effect = ApiError("Fake API Error", response=MagicMock(status_code=404))

    # Act
    articles = connector.fetch_articles()

    # Assert
    assert len(articles) == 0
