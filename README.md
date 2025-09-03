# HKI Slideshow

A Python-based slideshow application that displays images and videos from a specified folder.

## Features

- Displays images (PNG, JPG, JPEG, BMP, GIF) and videos (MP4, MOV, AVI)
- **Randomized order**: Media files are displayed in random order
- **Continuous loop**: When all files have been shown, the order is re-randomized and the slideshow continues
- Automatic scaling and panning for videos
- Keyboard controls for navigation

## Setup

The project uses a virtual environment to manage dependencies. The setup is automated through the `run_slideshow.sh` script.

### Requirements

- Python 3.12 or higher
- macOS (tested on macOS with Apple Silicon)

### Dependencies

- pygame==2.6.1
- moviepy==1.0.3
- numpy==2.3.2
- pillow==11.3.0

## Usage

1. Make sure you have a folder with images and/or videos
2. Run the slideshow:

```bash
./run_slideshow.sh /path/to/your/media/folder
```

### First Run

On the first run, the script will automatically:

- Create a virtual environment if it doesn't exist
- Install all required dependencies from `requirements.txt`
- Start the slideshow

### Controls

- **ESC**: Exit the slideshow
- The slideshow will automatically advance through media files

## Project Structure

```
hki-slideshow/
├── run_slideshow.sh    # Main launcher script
├── slideshow.py        # Python slideshow application
├── requirements.txt    # Python dependencies
├── venv/              # Virtual environment (auto-created)
└── README.md          # This file
```

## Troubleshooting

If you encounter issues:

1. Make sure the `run_slideshow.sh` script has execute permissions:

   ```bash
   chmod +x run_slideshow.sh
   ```

2. If the virtual environment gets corrupted, delete the `venv/` folder and run the script again:

   ```bash
   rm -rf venv
   ./run_slideshow.sh /path/to/media/folder
   ```

3. Make sure you have Python 3.12+ installed:
   ```bash
   python3 --version
   ```
