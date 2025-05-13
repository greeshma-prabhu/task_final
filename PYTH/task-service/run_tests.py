#!/usr/bin/env python3
"""
Run tests directly without module resolution issues
"""
import sys
import os
import pytest

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Run tests
if __name__ == '__main__':
    sys.exit(pytest.main(['-v', 'tests/test_task_service.py']))
