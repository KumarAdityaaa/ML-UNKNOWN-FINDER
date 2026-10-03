import sys

sys.path.insert(0, "dashboard")

from generate import build_dashboard


def test_dashboard_generation():
    html = build_dashboard()

    assert "<title>AI Unknown Finder Dashboard</title>" in html
    assert "Discovery" in html
    assert "Evaluation" in html
    assert "Dataset score" in html
    assert "Human evaluation score" in html
