# CodeAlpha Event Registration System

## Project Overview

The Event Registration System is a web application developed using Python, Flask, and SQLite. It allows users to create events, register participants, view registrations, and cancel registrations.

## Features

* Create new events.
* Register participants for events.
* Prevent duplicate registrations using email validation.
* View registered participants.
* Cancel registrations.
* Store event and registration data using SQLite.

## Technologies Used

* Python
* Flask
* SQLite
* HTML
* CSS

## Installation and Setup

1. Clone or download this repository.

2. Open the project folder in a terminal.

3. Install the required package:

   ```bash
   python -m pip install flask
   ```

4. Run the application:

   ```bash
   python app.py
   ```

5. Open your browser and visit:

   `http://127.0.0.1:5000/`

## Project Structure

```text
CodeAlpha_EventRegistration/
├── app.py
├── templates/
│   ├── index.html
│   └── registrations.html
├── .gitignore
└── README.md
```

The SQLite database is created automatically when the application starts.

## Purpose

This project was developed as part of my CodeAlpha internship to practice Python web development, database operations, and CRUD functionality.
