# Facebook Developer URL Extractor

A Python tool that automates the Facebook Sharing Debugger to extract preview information (title, description, image) for any given URL.

## Prerequisites

- Python 3.8+
- [Playwright](https://playwright.dev/python/docs/intro)

## Installation

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Install Playwright browsers:
   ```bash
   playwright install chromium
   ```

## Configuration

The script requires access to Facebook. copy the sample configuration file and fill in your credentials or cookies:

```bash
cp config_facebook_developer.json.sample config_facebook_developer.json
```

Edit `config_facebook_developer.json` with your:
- `facebook_user`: Your Facebook email.
- `facebook_password`: Your Facebook password.
- `cookies`: A list of cookie objects (can be exported using browser extensions).

## Usage

Run the script by passing the URL you want to debug:

```bash
python main.py https://www.example.com
```

Options:
- `--config`: Path to a custom config file (default: `config_facebook_developer.json`).

## Security

Sensitive files like `config_facebook_developer.json` and debug screenshots are excluded from the repository via `.gitignore`. Always use the `.sample` file as a template for sharing configuration structures.
