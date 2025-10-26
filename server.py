import os
import socket
import qrcode
import werkzeug.utils
from flask import Flask, request, jsonify


# --- Helper function to get local IP ---
def get_local_ip():
    """
    Finds the local IP address of the machine.
    Connects to an external server to identify the primary network interface.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        # Fallback if the above method fails
        try:
            IP = socket.gethostbyname(socket.gethostname())
        except Exception:
            IP = '127.0.0.1'  # Last resort
    finally:
        s.close()
    return IP


# --- Flask App Initialization ---
app = Flask(__name__)

# --- Configuration ---
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- HTML, CSS, and JavaScript Front-End (Unchanged) ---
html_page = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Multi-File Upload</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: #121212;
            color: #e0e0e0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            padding: 1rem;
            box-sizing: border-box;
        }
        .container {
            background: #1e1e1e;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            text-align: center;
            width: 100%;
            max-width: 450px;
            border: 1px solid #333;
        }
        h1 {
            margin-bottom: 1.5rem;
            color: #ffffff;
            font-weight: 600;
        }
        form input[type="file"] {
            display: none;
        }
        .file-upload-label {
            display: block;
            padding: 20px;
            border: 2px dashed #444;
            border-radius: 8px;
            cursor: pointer;
            margin-bottom: 1rem;
            transition: background-color 0.3s, border-color 0.3s;
        }
        .file-upload-label:hover {
            background-color: #2a2a2a;
            border-color: #007bff;
        }
        #file-names {
            margin-bottom: 1rem;
            color: #aaa;
            font-style: italic;
            min-height: 1.2em;
            word-break: break-word;
        }
        input[type="submit"] {
            background-color: #007bff;
            color: white;
            padding: 12px 20px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 500;
            width: 100%;
            transition: background-color 0.3s;
        }
        input[type="submit"]:hover {
            background-color: #0056b3;
        }
        input[type="submit"]:disabled {
            background-color: #555;
            cursor: not-allowed;
        }
        .progress-container {
            display: none;
            margin-top: 1.5rem;
            text-align: left;
            font-size: 14px;
            color: #ddd;
        }
        progress {
            width: 100%;
            height: 10px;
            appearance: none;
            border: none;
            border-radius: 10px;
            overflow: hidden;
            margin-top: 0.5rem;
        }
        progress::-webkit-progress-bar { background-color: #333; }
        progress::-webkit-progress-value { background-color: #007bff; transition: width 0.1s ease; }
        .progress-details {
            display: flex;
            justify-content: space-between;
            font-size: 0.8rem;
            color: #aaa;
            margin-top: 0.5rem;
        }
        .message {
            margin-top: 1rem;
            padding: 0.75rem;
            border-radius: 8px;
            font-weight: 500;
            display: none; /* Hidden by default */
        }
        .message.success { background-color: rgba(40, 167, 69, 0.2); color: #28a745; }
        .message.error { background-color: rgba(220, 53, 69, 0.2); color: #dc3545; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Upload Files to PC</h1>
        <form id="upload-form">
            <label for="file" class="file-upload-label">Click to select files</label>
            <input type="file" name="files" id="file" multiple />
            <p id="file-names">No files selected</p>
            <input type="submit" value="Upload" />
        </form>
        <div class="progress-container">
            <div id="progress-text">Uploading...</div>
            <progress id="progress-bar" value="0" max="100"></progress>
            <div class="progress-details">
                <span id="size">0/0 MB</span>
                <span id="speed">0 MB/s</span>
                <span id="time-left">--:--</span>
            </div>
        </div>
        <div id="message-box" class="message"></div>
    </div>

    <script>
        const form = document.getElementById('upload-form');
        const fileInput = document.getElementById('file');
        const fileNamesDisplay = document.getElementById('file-names');
        const submitButton = form.querySelector('input[type="submit"]');
        const progressContainer = document.querySelector('.progress-container');
        const progressBar = document.getElementById('progress-bar');
        const sizeDisplay = document.getElementById('size');
        const speedDisplay = document.getElementById('speed');
        const timeLeftDisplay = document.getElementById('time-left');
        const messageBox = document.getElementById('message-box');

        let startTime;

        fileInput.addEventListener('change', () => {
            const files = fileInput.files;
            if (files.length > 0) {
                fileNamesDisplay.textContent = files.length + ' file(s) selected';
            } else {
                fileNamesDisplay.textContent = 'No files selected';
            }
        });

        form.addEventListener('submit', (e) => {
            e.preventDefault();
            if (fileInput.files.length === 0) {
                alert('Please select at least one file to upload.');
                return;
            }

            const formData = new FormData();
            for (const file of fileInput.files) {
                formData.append('files', file);
            }

            const xhr = new XMLHttpRequest();
            xhr.open('POST', '/upload', true);

            xhr.upload.addEventListener('loadstart', () => {
                progressContainer.style.display = 'block';
                messageBox.style.display = 'none';
                submitButton.disabled = true;
                startTime = Date.now();
            });

            xhr.upload.addEventListener('progress', (event) => {
                if (event.lengthComputable) {
                    const percent = (event.loaded / event.total) * 100;
                    progressBar.value = percent;

                    const totalMB = (event.total / (1024 * 1024)).toFixed(2);
                    const loadedMB = (event.loaded / (1024 * 1024)).toFixed(2);
                    sizeDisplay.textContent = `${loadedMB} / ${totalMB} MB`;

                    const elapsedTime = (Date.now() - startTime) / 1000; // in seconds
                    const speed = loadedMB / elapsedTime;
                    speedDisplay.textContent = `${speed.toFixed(2)} MB/s`;

                    if (speed > 0) {
                        const remainingMB = totalMB - loadedMB;
                        const timeLeft = remainingMB / speed;
                        const minutes = Math.floor(timeLeft / 60);
                        const seconds = Math.floor(timeLeft % 60);
                        timeLeftDisplay.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
                    }
                }
            });

            xhr.addEventListener('load', () => {
                submitButton.disabled = false;
                progressContainer.style.display = 'none';
                fileInput.value = ''; // Reset file input
                fileNamesDisplay.textContent = 'No files selected';

                let response;
                try {
                    response = JSON.parse(xhr.responseText);
                } catch (err) {
                    response = { success: false, message: 'An unknown error occurred.' };
                }

                messageBox.textContent = response.message;
                messageBox.className = 'message ' + (response.success ? 'success' : 'error');
                messageBox.style.display = 'block';
            });

            xhr.addEventListener('error', () => {
                messageBox.textContent = 'Upload failed due to a network error.';
                messageBox.className = 'message error';
                messageBox.style.display = 'block';
                submitButton.disabled = false;
                progressContainer.style.display = 'none';
            });

            xhr.send(formData);
        });
    </script>
</body>
</html>
"""


# --- Flask Server Logic ---
@app.route('/')
def index():
    return html_page


@app.route('/upload', methods=['POST'])
def upload_files():
    uploaded_files = request.files.getlist('files')
    if not uploaded_files or uploaded_files[0].filename == '':
        return jsonify({'success': False, 'message': 'No files selected for upload.'}), 400

    try:
        count = len(uploaded_files)
        for file in uploaded_files:
            if file.filename != '':
                filename = werkzeug.utils.secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

                # --- Rename file if it exists ---
                if os.path.exists(filepath):
                    name, extension = os.path.splitext(filename)
                    counter = 1
                    while os.path.exists(filepath):
                        new_filename = f"{name} ({counter}){extension}"
                        filepath = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
                        counter += 1

                file.save(filepath)

        return jsonify({'success': True, 'message': f'Successfully uploaded {count} file(s)!'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'An error occurred: {e}'}), 500


if __name__ == '__main__':
    PORT = 5000
    local_ip = get_local_ip()
    server_url = f"http://{local_ip}:{PORT}"

    # --- Generate and show QR code ---
    print("=" * 50)
    print(f"Server is starting...")
    print(f"Scan the QR code with your phone or navigate to:")
    print(f"==> {server_url} <==")
    print("=" * 50)

    qr_img = qrcode.make(server_url)
    qr_img_path = 'server_address_qr.png'
    qr_img.save(qr_img_path)

    # Open the QR code image automatically (works on Windows, macOS, and Linux)
    try:
        if os.name == 'nt':  # Windows
            os.startfile(qr_img_path)
        elif os.uname().sysname == 'Darwin':  # macOS
            os.system(f'open {qr_img_path}')
        else:  # Linux
            os.system(f'xdg-open {qr_img_path}')
    except Exception as e:
        print(f"\nCould not open QR code image automatically: {e}")
        print("Please open 'server_address_qr.png' manually.")

    # --- Run Flask Server ---
    app.run(host='0.0.0.0', port=PORT, debug=False)