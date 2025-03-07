#!/usr/bin/env python3
import json
import os
import zipfile
from datetime import datetime

def create_difypkg():
    # Read package configuration
    with open('difypkg.json', 'r') as f:
        config = json.load(f)
    
    # Create package name with version
    package_name = f"{config['name']}-{config['version']}.difypkg"
    
    # Create ZIP file
    with zipfile.ZipFile(package_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add files specified in difypkg.json
        for file in config['files']:
            if os.path.exists(file):
                zipf.write(file)
            else:
                print(f"Warning: File {file} not found")
        
        # Add difypkg.json itself
        zipf.write('difypkg.json')
    
    print(f"Created package: {package_name}")

if __name__ == '__main__':
    create_difypkg() 