# Rubik's Cube Solver Tutorial

A Flask web application that teaches users how to solve a Rubik's Cube through step-by-step instructions and interactive quizzes.

## Features

- Step-by-step learning modules on solving a Rubik's Cube
- Bite-sized pages with easy-to-understand content
- Mini-quizzes at the end of each learning module
- Comprehensive final quiz to test overall knowledge
- Quiz results with performance statistics

## Project Structure

- `app.py`: Main Flask application
- `modules.json`: Content for learning modules
- `quiz.json`: Questions for the final quiz
- `static/`: Static files (CSS, JavaScript)
- `templates/`: HTML templates

## Installation

1. Clone the repository:
```
git clone https://github.com/yourusername/Rubiks-Cube-Solver.git
cd Rubiks-Cube-Solver
```

2. Create a virtual environment and activate it:
```
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install the required packages:
```
pip install -r requirements.txt
```

## Usage

1. Run the Flask application:
```
python app.py
```

2. Open your web browser and go to:
```
http://localhost:5000
```

3. Navigate through the learning modules and take quizzes to test your knowledge.

## Development

- The learning content is stored in `modules.json`
- Quiz questions are stored in `quiz.json`
- Edit these files to modify the content

## License

This project is open source, feel free to use and modify it. 