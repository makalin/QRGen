# QRGen - QR Code Generator App

A simple Python application for generating QR codes. This tool allows users to quickly generate QR codes for various types of data, such as URLs, text, or contact information.

## Features

- Generate QR codes for different types of input.
- Save QR codes as image files.
- Customizable options for size, color, and error correction.

## Requirements

Before running the application, ensure you have the following installed:

- Python 3.7 or higher
- Required Python libraries:
  - `qrcode`
  - `Pillow`

To install the required libraries, run:
```bash
pip install qrcode[pil]
```

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/qr-code-app.git
```

2. Navigate to the project directory:
```bash
cd qr-code-app
```

3. Install the dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the script:
```bash
python qr-code-app.py
```

2. Follow the on-screen prompts to input the data you want to convert into a QR code.

3. Save the generated QR code as an image file.

## Example

Here is an example of generating a QR code for a URL:

1. Input:
```
Enter the URL or text: https://example.com
```

2. Output:
A QR code image is saved as `qrcode.png` in the current directory.

## Contributing

Contributions are welcome! If you find a bug or have an idea for a new feature, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
