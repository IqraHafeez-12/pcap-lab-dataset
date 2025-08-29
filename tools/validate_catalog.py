#!/usr/bin/env python3
import json, sys
from jsonschema import validate, ValidationError, SchemaError

if len(sys.argv) < 3:
    print("Usage: python3 tools/validate_catalog.py <catalog.json> <schema.json>")
    sys.exit(1)

catalog_path = sys.argv[1]
schema_path = sys.argv[2]

with open(catalog_path, "r") as f:
    catalog = json.load(f)

with open(schema_path, "r") as f:
    schema = json.load(f)

try:
    validate(instance=catalog, schema=schema)
    print("✅ Catalog is valid")
except (ValidationError, SchemaError) as e:
    print("❌ Schema error:", e.message)
    sys.exit(2)
