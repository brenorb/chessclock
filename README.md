# Chess Clock App

A web-based chess clock application that tracks time for two players with a configurable global timer.

## Features
- Configurable global timer
- Individual time tracking for two players
- Pause/Resume functionality
- Percentage time usage display
- Modern, responsive UI

## Local Development

1. Create a virtual environment:
```bash
uv venv
source .venv/bin/activate  # On Unix/macOS
```

2. Install dependencies:
```bash
uv pip install -r requirements.txt
```

3. Run the development server:
```bash
python main.py
```

## Deployment

### Option 1: Deploy to Render.com (Recommended)

1. Create a new account on [Render.com](https://render.com)
2. Click "New +" and select "Web Service"
3. Connect your GitHub repository
4. Fill in the following settings:
   - Name: `chess-clock` (or your preferred name)
   - Environment: `Python`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn main:app`
   - Plan: Free

The app will be automatically deployed and you'll get a URL like `https://chess-clock.onrender.com`

### Option 2: Deploy to your own server

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run with Gunicorn:
```bash
gunicorn -c gunicorn_config.py main:app
```

## License
MIT 