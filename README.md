# Facebook Developer URL Extractor

A Python tool that automates the Facebook Sharing Debugger to extract preview information (title, description, image) for any given URL.

## Prerequisites

- Python 3.8+
- [Playwright](https://playwright.dev/python/docs/intro)

## Quick Start (Installation & Setup)

To set up the project automatically, run the installation script for your environment:

### Windows
```batch
install.bat
```

### Linux / Git Bash
```bash
bash ./install.sh
```

These scripts will:
1. Create a virtual environment (`.venv`).
2. Install all dependencies from `requirements.txt`.
3. Install the required Playwright browsers (chromium).

## Configuration

The script requires Facebook credentials or cookies. Copy the sample configuration file and fill in your details:

```bash
cp config_facebook_developer.json.sample config_facebook_developer.json
```

Edit `config_facebook_developer.json` with:
- `facebook_user`: Your Facebook username/email.
- `facebook_password`: Your Facebook password.
- `cookies`: A list of cookie objects (recommended for avoiding 2FA issues).

## Usage

You can run the tool using the provided simplified execution scripts:

### Windows
```batch
run.bat https://www.example.com
```

### Linux / Git Bash
```bash
./run.sh https://www.example.com
```

### Direct Execution
If you have the virtual environment active:
```bash
python main.py <URL>
```

## Testing

To run the unit and integration tests:

```bash
./test.sh
```

## Global Command (Windows)

You can also use the `fb_developer_extractor` command from anywhere if you have added `c:\scripts\bin` to your system PATH.

## Security & Local Configuration

- **Sensitive Data**: Your `config_facebook_developer.json` and screenshots are kept safe and are not tracked by Git.
- **Local Rules**: This project uses `.git/info/exclude` for privacy. No public `.gitignore` is included to maintain a clean project structure.
- **Context**: More detailed project context can be found in `CONTEXT.md` (which is also excluded from Git).
