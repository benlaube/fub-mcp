"""Tests for data processing utilities."""

import pytest
from fub_mcp.processors import DataProcessors


def test_group_by():
    """Test groupBy function."""
    data = [
        {"user": "alice", "value": 10},
        {"user": "bob", "value": 20},
        {"user": "alice", "value": 30},
    ]
    result = DataProcessors.group_by(data, "user")
    assert len(result["alice"]) == 2
    assert len(result["bob"]) == 1


def test_count_by():
    """Test countBy function."""
    data = [
        {"status": "active"},
        {"status": "active"},
        {"status": "inactive"},
    ]
    result = DataProcessors.count_by(data, "status")
    assert result["active"] == 2
    assert result["inactive"] == 1


def test_sum_by():
    """Test sumBy function."""
    data = [
        {"amount": 10.5},
        {"amount": 20.0},
        {"amount": 15.5},
    ]
    result = DataProcessors.sum_by(data, "amount")
    assert result == 46.0


def test_unique():
    """Test unique function."""
    data = [
        {"id": 1, "name": "alice"},
        {"id": 2, "name": "bob"},
        {"id": 1, "name": "alice"},
    ]
    # When key is provided, returns unique values
    result = DataProcessors.unique(data, "id")
    assert len(result) == 2
    assert 1 in result
    assert 2 in result
    
    # When no key, returns unique items
    result_items = DataProcessors.unique([1, 2, 1, 3])
    assert len(result_items) == 3


def test_aggregate():
    """Test aggregate function."""
    data = [
        {"user": "alice", "sales": 100},
        {"user": "alice", "sales": 200},
        {"user": "bob", "sales": 150},
    ]
    result = DataProcessors.aggregate(data, "user", "sales", "sum")
    assert result["alice"] == 300.0
    assert result["bob"] == 150.0

