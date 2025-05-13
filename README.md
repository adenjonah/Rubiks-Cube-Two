# Rubik's Cube Solver Tutorial

A Flask web application that teaches users how to solve a Rubik's Cube through step-by-step instructions and interactive quizzes.

## Features

- Step-by-step learning modules on solving a Rubik's Cube
- Bite-sized pages with easy-to-understand content
- Mini-quizzes at the end of each learning module
- Comprehensive final quiz to test overall knowledge
- Quiz results with performance statistics

## Requirements

- Python 3.6 or higher
- pip (Python package installer)

## Installation and Setup

### macOS

1. Clone the repository:
```
git clone https://github.com/yourusername/Rubiks-Cube-Two.git
cd Rubiks-Cube-Two
```

2. Create a virtual environment and activate it:
```
python3 -m venv venv
source venv/bin/activate
```

3. Install the required packages:
```
pip install -r requirements.txt
```

4. Run the Flask application:
```
python app.py
```

5. Open your web browser and go to:
```
http://localhost:5000
```

### Windows

1. Clone the repository:
```
git clone https://github.com/yourusername/Rubiks-Cube-Two.git
cd Rubiks-Cube-Two
```

2. Create a virtual environment and activate it:
```
python -m venv venv
venv\Scripts\activate
```

3. Install the required packages:
```
pip install -r requirements.txt
```

4. Run the Flask application:
```
python app.py
```

5. Open your web browser and go to:
```
http://localhost:5000
```

## Troubleshooting

### macOS
- If you encounter a "command not found" error for Python, try using `python3` instead of `python`
- If you have permission issues, try using `sudo pip install -r requirements.txt`

### Windows
- Make sure Python is added to your PATH environment variable
- If the virtual environment activation fails, try running PowerShell as administrator and execute: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- If you're using Command Prompt, use `venv\Scripts\activate.bat`

## Usage

Navigate through the learning modules and take quizzes to test your knowledge on solving a Rubik's Cube.

## Development

- The learning content is stored in `modules.json`
- Quiz questions are stored in `quiz.json`
- Edit these files to modify the content

## License

This project is open source, feel free to use and modify it. 