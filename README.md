# Local File Uploader

A simple web application to transfer files from your phone to your PC over the local network. It runs a lightweight server on your PC and provides a simple upload page, accessible by scanning a QR code.

This tool was created to be a more reliable alternative to services like Quick Share or AirDrop, which can be slow and inconsistent for phone-to-PC transfers. This uploader guarantees the use of your high-speed Wi-Fi connection, making it ideal for large files.

## Features

-   **QR Code Access:** Instantly access the upload page by scanning a QR code. No need to type IP addresses.
-   **High-Speed Transfers:** Utilizes your local Wi-Fi network for maximum transfer speed.
-   **Multi-File Upload:** Select and upload multiple files simultaneously.
-   **Real-time Progress:** See the upload percentage, speed, and estimated time remaining.
-   **No Overwriting:** Automatically renames new files if a file with the same name already exists (e.g., `image.png` becomes `image (1).png`).
-   **Cross-Platform:** Works on any device with a modern web browser.

## Installation & Usage

First, clone the repository to your local machine:

```bash
git clone https://github.com/YashAkYT/Local-File-Uploader---Python.git
cd Local-File-Uploader---Python
```

### For Windows Users

The easiest method is to use the included batch script.

Simply **double-click the `start.bat` file**.

It will automatically create a virtual environment, install the necessary dependencies, start the server, and display the QR code for you to scan.

### For macOS & Linux Users

Open your terminal and run the following commands:

```bash
# 1. Create a virtual environment
python3 -m venv venv

# 2. Activate the environment
source venv/bin/activate

# 3. Install the required packages
pip install -r requirements.txt

# 4. Run the server
python server.py
```

After running the server, a QR code image (`server_address_qr.png`) will be saved in the project directory. Open the image and scan it with your phone to begin uploading files.
