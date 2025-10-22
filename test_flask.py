#!/usr/bin/env python3
"""
Test Flask app routes
"""

import app
from flask import Flask

# Check if the app is properly configured
print("Flask app instance:", app.app)
print("App name:", app.app.name)

# Check all routes
print("\nAll routes:")
for rule in app.app.url_map.iter_rules():
    print(f"  {rule.methods} {rule.rule} -> {rule.endpoint}")

# Check if create_recipe function exists
print(f"\ncreate_recipe function exists: {hasattr(app, 'create_recipe')}")

# Try to access the function directly
try:
    func = app.create_recipe
    print(f"create_recipe function: {func}")
except AttributeError as e:
    print(f"Error accessing create_recipe: {e}")
