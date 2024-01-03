# Copypasta

**Copypasta** is a simple web application built using FastAPI, designed to help you manage and interact with files stored on a server. It provides various features for uploading, previewing, and deleting files, as well as generating Base64 representations of files. This README will guide you through setting up and using the Copypasta tool.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

Copypasta offers the following features:

1. **File Upload**: Upload files to the server, with support for multiple file uploads.
2. **Base64 Encoding**: Convert files into Base64-encoded strings. It also supports converting into UTF16-LE (for Powershell -ec commands)
3. **Preview**: Preview the content of text-based files.
4. **File Deletion**: Delete files from the server.
5. **File Size Display**: Display file sizes in a user-friendly format (e.g., B, KB, MB, GB).
6. **MD5 Hash Storage**: Shows MD5 hashes for files under a certain size to verify data integrity.

## Prerequisites

Before you begin, ensure you meet the following requirements:

- Python3 installed on your system
- pip package manager

## Installation

Copypasta supports running locally via python or running in a container via Docker

### Running Locally

1. Clone the repository
2. Navigate to the repository folder
   - *(Optional)* Create a virtual environment
   - *(Optional)* Activate the virtual environment
3. pip install -r requirements.txt
4. python copypasta.py

By default, it will host on http://0.0.0.0:8080. This can be changed in variables.py.

### Running in Docker
1. clone the repository
2. cd into the repository folder
3. docker build -t copypasta .
4. docker-compose up -d

## Usage

`python copypasta.py`
or
`docker build -t copypasta .`
`docker-compose up -d`

## Contributing

- Written by [WJDigby](https://github.com/WJDigby) and stylized by [Quaid DeLacluyse](https://github.com/ezra-buckingham/copypasta)
- The functionality and design was improved and refactored by me.

## License

This project is licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html).

For the full license text, please see [LICENSE](LICENSE).