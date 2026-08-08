#!/usr/bin/env python3
import os
import shutil

if not os.path.exists('scripts/verify_content.py'):
    os.makedirs('scripts', exist_ok=True)
    shutil.copy('/root/.hermes/skills/web-dev/neurosurgery-digest/scripts/verify_content.py', 'scripts/verify_content.py')
print('Verify script copied')
