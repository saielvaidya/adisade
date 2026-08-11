# Adisade

**A dollar saved is a dollar earned.**

Adisade is a recurring expense intelligence tool that helps users track recurring costs, understand where their money goes, and identify potential opportunities to save.

## Features

- Add, edit, and delete recurring expenses
- Weekly, monthly, and yearly expense normalization
- Monthly and yearly recurring spending metrics
- Persistent expense storage with SQLite
- Category breakdown with percentages
- Spending visualization with Chart.js
- Sort categories from highest to lowest or lowest to highest
- AI-powered recurring expense recommendations using the OpenAI API
- Real-time frontend updates without page reloads

## Tech Stack

- Python
- Flask
- SQLite
- HTML
- CSS
- JavaScript
- Chart.js
- OpenAI API

## Project Structure

```text
adisade/
├── app.py
├── expenses.py
├── analysis.py
├── ai.py
├── database.py
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── script.js
├── requirements.txt
├── README.md
└── .gitignore