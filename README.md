# Państwa-Miasta Letter Drawing App

A single-page Flask application for drawing random letters for the "Państwa-Miasta" (Countries-Cities) game.

## Features

- Draw random letters from the English alphabet
- Display currently drawn letter prominently
- Show all previously used letters below the button
- Beautiful, centered UI design
- Fully self-contained single-page application

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## How to Use

1. Click the "Wylosuj literę" (Draw letter) button to randomly select a letter
2. The letter will be displayed in large font in the center
3. Previously drawn letters will appear below the button
4. Each letter can only be drawn once per session

## Technology Stack

- Flask (Python web framework)
- HTML5
- CSS3
- JavaScript (Vanilla)
