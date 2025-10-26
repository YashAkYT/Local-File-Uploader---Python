# Local-File-Uploader---Python

![alt text](https://img.shields.io/badge/Python-3.7+-blue.svg)
![alt text](https://img.shields.io/badge/Flask-2.x-black.svg)
![alt text](https://img.shields.io/badge/License-MIT-green.svg)

A simple, fast, and reliable web-based utility to upload files from any device (like a phone) to your PC over your local network. It solves the common problem of inconsistent and slow file transfers from mobile to desktop by leveraging your Wi-Fi's full speed.

The application starts a local web server on your PC and instantly displays a QR code. Simply scan the code with your phone to open the upload page and start sending files.

(Feel free to replace this with your own screenshot or a GIF of the app in action!)

✨ Features

Cross-Platform: Works with any device that has a web browser (Android, iPhone, macOS, Linux).

Multi-File Upload: Select and upload multiple files at once.

Real-time Progress: Monitor upload speed, percentage complete, transfer size, and estimated time remaining.

QR Code for Easy Access: No more typing IP addresses! The server generates and displays a QR code on startup for instant access from your phone.

Automatic File Renaming: Prevents overwriting files. If photo.jpg exists, a new file will be saved as photo (1).jpg.

Blazing Fast: Uses your local Wi-Fi network directly, ensuring the fastest possible transfer speeds.

Zero Configuration: No need for accounts, pairing, or complex setup.

One-Click Start: Includes a .bat script for Windows to set up the environment and run the server with a single click.

Lightweight & Private: No external services involved. Your files never leave your local network.

🤔 Why Use This Over Quick Share / AirDrop?

While services like Quick Share and AirDrop are convenient, they can be unreliable. They often default to a slow Bluetooth connection for phone-to-PC transfers, even on a fast Wi-Fi network. This tool guarantees that the transfer will always use your fast Wi-Fi connection, making it perfect for large files like videos.

Feature	Local File Uploader	Quick Share / AirDrop
Speed	✅ Consistently Fast (Uses Wi-Fi)	⚠️ Unreliable (Often defaults to slow Bluetooth)
Compatibility	✅ Universal (Any browser)	❌ Platform-locked (Android/Windows or Apple)
Setup	✅ Scan QR Code	✅ Automatic Discovery
Privacy	✅ 100% Local	✅ Generally Secure
🚀 Getting Started

You can get the server running in under a minute.

Requirements

Python 3.7+

Quick Install & Run (Windows)

The easiest way to get started on Windows is to use the included batch script.

Download the Code:

Click the green Code button on this GitHub page and select Download ZIP.

Extract the ZIP file to a folder on your computer.

Run the Starter Script:

Navigate into the folder and simply double-click the start.bat file.

That's it! The script will automatically:

Create a Python virtual environment.

Install the required libraries.

Start the web server.

Open a QR code image on your screen.

Scan the QR code with your phone's camera, open the link, and start uploading!

Manual Installation (All Platforms)

If you're not on Windows or prefer to set it up manually:

Clone the repository:

code
Bash
download
content_copy
expand_less
git clone https://github.com/your-username/local-file-uploader.git
cd local-file-uploader

Create and activate a virtual environment:

code
Bash
download
content_copy
expand_less
# For Windows
python -m venv venv
.\venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

Install the required packages:

code
Bash
download
content_copy
expand_less
pip install -r requirements.txt

Run the server:

code
Bash
download
content_copy
expand_less
python server.py

A QR code image named server_address_qr.png will be created in the folder. Open it and scan it with your phone.

🛠️ How It Works

Backend: A lightweight web server built with Flask (a Python micro-framework). It handles the file uploads and the logic for renaming files.

Frontend: A single, self-contained HTML page with vanilla CSS and JavaScript. It uses XMLHttpRequest (XHR) to handle the file upload process and display real-time progress without needing a page refresh.

QR Code Generation: The qrcode Python library is used to generate the QR code from the server's local IP address upon startup.

💡 Future Improvements

Add a dark/light mode toggle.

Create a simple gallery to view/download uploaded files from the browser.

Dockerize the application for even easier deployment.

Add an optional password protection feature.

📄 License

This project is licensed under the MIT License. See the LICENSE file for details.
