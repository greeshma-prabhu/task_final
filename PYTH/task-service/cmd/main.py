#!/usr/bin/env python3
"""
Task Management Service Entry Point
"""
from internal.app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
