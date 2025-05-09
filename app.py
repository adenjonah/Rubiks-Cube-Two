from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = 'rubikscubesecret'  # Set a secret key for session

# Load quiz data
with open('quiz.json', 'r') as f:
    quiz_data = json.load(f)

# Load module data
with open('modules.json', 'r') as f:
    modules_data = json.load(f)

# Function to initialize or reset session data
def reset_session_data():
    session.clear()
    session['progress'] = {
        'modules': {},
        'mini_quizzes': {},
        'final_quiz_attempted': False,
        'final_quiz_score': 0
    }
    if 'quiz_results' in session:
        session.pop('quiz_results')
    if 'mini_quiz_results' in session:
        session.pop('mini_quiz_results')
    if 'current_module' in session:
        session.pop('current_module')
    if 'current_page' in session:
        session.pop('current_page')
    session.modified = True
    print("DEBUG: Session data reset")

# Server restart timestamp to detect when the server has been restarted
server_start_time = os.path.getmtime(__file__)

@app.route('/')
def home():
    # Check if progress exists or if server was restarted
    if 'progress' not in session or 'server_start_time' not in session or session.get('server_start_time') != server_start_time:
        reset_session_data()
        session['server_start_time'] = server_start_time
        print("DEBUG: Server restart detected or new session - data has been reset")
    
    # Don't reset progress when visiting home page
    # Only reset current location info
    if 'quiz_results' in session:
        session.pop('quiz_results')
    if 'current_module' in session:
        session.pop('current_module')
    if 'current_page' in session:
        session.pop('current_page')
    
    # Calculate module progress for display
    modules_progress = []
    for module in modules_data['modules']:
        module_id = str(module['id'])
        module_progress = {
            'id': module['id'],
            'title': module['title'],
            'completed': False,
            'pages_completed': 0,
            'total_pages': len(module['pages']),
            'mini_quiz_completed': False,
            'progress_percent': 0
        }
        
        # Check if module pages are in progress/completed
        if module_id in session['progress']['modules']:
            module_progress['pages_completed'] = len(session['progress']['modules'][module_id])
            module_progress['progress_percent'] = int((module_progress['pages_completed'] / module_progress['total_pages']) * 100)
        
        # Check if mini quiz is completed
        if module_id in session['progress']['mini_quizzes']:
            module_progress['mini_quiz_completed'] = True
            
        # Module is fully completed if all pages and mini quiz are done
        if (module_progress['pages_completed'] == module_progress['total_pages'] and 
            module_progress['mini_quiz_completed']):
            module_progress['completed'] = True
            
        modules_progress.append(module_progress)
    
    return render_template('home.html', 
                          modules_data=modules_data,
                          modules_progress=modules_progress,
                          progress=session['progress'])

@app.route('/learn/<int:module_id>/<int:page_id>')
def learn(module_id, page_id):
    # Check if server was restarted
    if 'server_start_time' not in session or session.get('server_start_time') != server_start_time:
        reset_session_data()
        session['server_start_time'] = server_start_time
        print("DEBUG: Server restart detected in learn route - data has been reset")
        return redirect(url_for('home'))
        
    # Store current module and page in session
    session['current_module'] = module_id
    session['current_page'] = page_id
    
    # Get module information
    module = modules_data['modules'][module_id - 1]
    
    # Initialize progress tracking if it doesn't exist
    if 'progress' not in session:
        reset_session_data()
    
    # Mark current page as viewed/completed
    if str(module_id) not in session['progress']['modules']:
        session['progress']['modules'][str(module_id)] = {}
    
    # Store timestamp to track when page was completed
    session['progress']['modules'][str(module_id)][str(page_id)] = {
        'completed': True,
        'timestamp': str(os.path.getmtime(__file__))  # Using file modification time as timestamp
    }
    
    # Check if page exists
    if page_id > len(module['pages']):
        # If page doesn't exist, go to mini quiz
        return redirect(url_for('mini_quiz', module_id=module_id, question_id=1))
    
    # Get page information
    page = module['pages'][page_id - 1]
    
    next_page = page_id + 1
    
    # Calculate module progress percentage
    pages_completed = len(session['progress']['modules'].get(str(module_id), {}))
    total_pages = len(module['pages'])
    progress_percent = int((pages_completed / total_pages) * 100)
    
    return render_template('learn.html', 
                          module=module, 
                          page=page, 
                          module_id=module_id, 
                          page_id=page_id,
                          next_page=next_page,
                          progress_percent=progress_percent)

@app.route('/mini_quiz/<int:module_id>/<int:question_id>', methods=['GET', 'POST'])
def mini_quiz(module_id, question_id):
    # Check if server was restarted
    if 'server_start_time' not in session or session.get('server_start_time') != server_start_time:
        reset_session_data()
        session['server_start_time'] = server_start_time
        print("DEBUG: Server restart detected in mini_quiz route - data has been reset")
        return redirect(url_for('home'))
        
    # Get module information
    module = modules_data['modules'][module_id - 1]
    modules_length = len(modules_data['modules'])
    
    # Initialize progress tracking if it doesn't exist
    if 'progress' not in session:
        reset_session_data()
    
    # Make sure mini quiz exists for this module
    if 'mini_quiz' not in module or not module['mini_quiz']:
        # If no mini quiz, go to next module or final quiz
        if module_id < len(modules_data['modules']):
            return redirect(url_for('learn', module_id=module_id + 1, page_id=1))
        else:
            return redirect(url_for('quiz', question_id=1))
    
    # Check if question exists
    if question_id > len(module['mini_quiz']):
        # If no more questions, mark mini quiz as completed and go to next module or final quiz
        session['progress']['mini_quizzes'][str(module_id)] = {
            'completed': True,
            'timestamp': str(os.path.getmtime(__file__))
        }
        
        if module_id < len(modules_data['modules']):
            return redirect(url_for('learn', module_id=module_id + 1, page_id=1))
        else:
            return redirect(url_for('quiz', question_id=1))
    
    # Get question information
    question = module['mini_quiz'][question_id - 1]
    
    # Process form submission
    feedback = None
    is_correct = False
    
    if request.method == 'POST':
        if question['type'] == 'multiple_select':
            # For multiple select, get all selected answers
            user_answers = request.form.getlist('answer')
            correct_answers = question['correct_answers']
            
            # Check if the selected answers match the correct answers exactly
            is_correct = set(user_answers) == set(correct_answers)
        else:
            # For multiple choice or fill in the blank
            user_answer = request.form.get('answer')
            is_correct = user_answer == question['correct_answer']
        
        # Store answer in session
        if 'mini_quiz_results' not in session:
            session['mini_quiz_results'] = {}
        
        if str(module_id) not in session['mini_quiz_results']:
            session['mini_quiz_results'][str(module_id)] = {}
        
        if question['type'] == 'multiple_select':
            session['mini_quiz_results'][str(module_id)][str(question_id)] = {
                'question': question['question'],
                'user_answer': request.form.getlist('answer'),
                'correct_answers': question['correct_answers'],
                'correct': is_correct,
                'explanation': question.get('explanation', '')
            }
        else:
            session['mini_quiz_results'][str(module_id)][str(question_id)] = {
                'question': question['question'],
                'user_answer': request.form.get('answer'),
                'correct_answer': question['correct_answer'],
                'correct': is_correct,
                'explanation': question.get('explanation', '')
            }
        
        # Show feedback rather than redirecting
        feedback = True
    
    return render_template('mini_quiz.html', 
                          module=module, 
                          question=question, 
                          module_id=module_id, 
                          question_id=question_id,
                          feedback=feedback,
                          is_correct=is_correct,
                          modules_length=modules_length)

@app.route('/quiz/<int:question_id>', methods=['GET', 'POST'])
def quiz(question_id):
    # Check if server was restarted
    if 'server_start_time' not in session or session.get('server_start_time') != server_start_time:
        reset_session_data()
        session['server_start_time'] = server_start_time
        print("DEBUG: Server restart detected in quiz route - data has been reset")
        return redirect(url_for('home'))
        
    # Clear quiz results if starting from question 1
    if question_id == 1 and request.method == 'GET':
        if 'quiz_results' in session:
            session.pop('quiz_results')
    
    # Make sure question exists and is not beyond the max question
    total_questions = len(quiz_data['quiz_questions'])
    if question_id > total_questions:
        # If no more questions, go to results
        return redirect(url_for('quiz_results'))

    # Initialize quiz_results in session if it doesn't exist
    if 'quiz_results' not in session:
        session['quiz_results'] = {}
    
    # Get question information
    question = quiz_data['quiz_questions'][question_id - 1]
    
    # Process form submission
    if request.method == 'POST':
        # Get the user's answer
        answer = request.form.get('answer')
        
        # Validate that an answer was provided
        if not answer:
            return render_template('quiz.html', 
                                  question=question, 
                                  question_id=question_id, 
                                  total_questions=total_questions,
                                  error="Please provide an answer before continuing")
        
        is_correct = answer == question['correct_answer']
        
        # Store answer in session
        session['quiz_results'][str(question_id)] = {
            'question': question['question'],
            'user_answer': answer,
            'correct_answer': question['correct_answer'],
            'correct': is_correct,
            'explanation': question.get('explanation', '')
        }
        
        # Save the session to ensure data is stored
        session.modified = True
        
        # Redirect to next question or results
        if question_id < total_questions:
            return redirect(url_for('quiz', question_id=question_id + 1))
        else:
            return redirect(url_for('quiz_results'))
    
    # Check if this question has already been answered (in case user navigates back)
    previous_answer = session['quiz_results'].get(str(question_id), {}).get('user_answer', '')
    
    return render_template('quiz.html', 
                          question=question, 
                          question_id=question_id, 
                          total_questions=total_questions,
                          previous_answer=previous_answer)

@app.route('/quiz_results')
def quiz_results():
    # Check if server was restarted
    if 'server_start_time' not in session or session.get('server_start_time') != server_start_time:
        reset_session_data()
        session['server_start_time'] = server_start_time
        print("DEBUG: Server restart detected in quiz_results route - data has been reset")
        return redirect(url_for('home'))
        
    # Make sure quiz results exist
    if 'quiz_results' not in session:
        return redirect(url_for('quiz', question_id=1))
    
    results = session['quiz_results']
    
    # If no results or incomplete quiz, redirect to the appropriate question
    if not results:
        return redirect(url_for('quiz', question_id=1))
    
    # Find the first unanswered question, if any
    total_questions = len(quiz_data['quiz_questions'])
    for i in range(1, total_questions + 1):
        if str(i) not in results:
            return redirect(url_for('quiz', question_id=i))
    
    # Debug info
    print("DEBUG: Quiz results from session:", results)
    
    # Check how many questions were actually answered
    answered_count = len(results)
    
    # Calculate correct answers - make sure to properly count
    correct_answers = 0
    for result in results.values():
        if result.get('correct', False):
            correct_answers += 1
    
    print(f"DEBUG: Answered count: {answered_count}, Correct answers: {correct_answers}")
    
    # Calculate score based on answered questions
    if answered_count > 0:
        score = (correct_answers / answered_count) * 100
    else:
        score = 0
    
    # Update progress to mark final quiz as attempted
    if 'progress' not in session:
        reset_session_data()
    
    session['progress']['final_quiz_attempted'] = True
    session['progress']['final_quiz_score'] = score
    
    # Log incorrect answers to server console
    print("\n----- QUIZ RESULTS - INCORRECT ANSWERS -----")
    incorrect_count = 0
    for q_id, result in results.items():
        if not result.get('correct', False):
            incorrect_count += 1
            print(f"Question {q_id}: {result['question']}")
            print(f"  User's answer: {result['user_answer']}")
            print(f"  Correct answer: {result['correct_answer']}")
            print("--------------------------------------------")
    
    if incorrect_count == 0 and answered_count > 0:
        print("Perfect score! No incorrect answers.")
    else:
        print(f"Total incorrect: {incorrect_count} out of {answered_count} answered (total quiz: {len(quiz_data['quiz_questions'])})")
    print("----------------------------------------------\n")
    
    return render_template('quiz_results.html', 
                          results=results, 
                          score=score, 
                          total_questions=answered_count,
                          correct_answers=correct_answers)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) 