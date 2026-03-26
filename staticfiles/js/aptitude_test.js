// Aptitude Test JavaScript
(function() {
    let currentTest = {
        questions: [],
        currentQuestion: 0,
        answers: {},
        startTime: null,
        timeTaken: '00:00:00',
        selectedSection: '',
        selectedDifficulty: '',
        selectedCount: 0
    };

    // Initialize test
    document.addEventListener('DOMContentLoaded', function() {
        console.log('🧠 Aptitude test script loaded');
        loadTestQuestions();
        setupEventListeners();
    });

function loadTestQuestions() {
    // Sample questions for each category
    currentTest.questions = [
        // Quantitative (10 questions)
        {
            id: 1,
            type: 'quantitative',
            question: 'What is 25% of 80?',
            options: ['10', '15', '20', '25'],
            correct: 2
        },
        {
            id: 2,
            type: 'quantitative',
            question: 'If 3x + 7 = 28, what is x?',
            options: ['5', '6', '7', '8'],
            correct: 1
        },
        {
            id: 3,
            type: 'quantitative',
            question: 'A train travels 120 km in 2 hours. What is its speed?',
            options: ['40 km/h', '50 km/h', '60 km/h', '70 km/h'],
            correct: 2
        },
        // Verbal (10 questions)
        {
            id: 11,
            type: 'verbal',
            question: 'Which word is the opposite of "increase"?',
            options: ['decrease', 'reduce', 'grow', 'expand'],
            correct: 0
        },
        {
            id: 12,
            type: 'verbal',
            question: 'Complete the analogy: Dog is to Bark as Cat is to...',
            options: ['Meow', 'Purr', 'Sleep', 'Hunt'],
            correct: 0
        },
        {
            id: 13,
            type: 'verbal',
            question: 'Choose the synonym of "Happy"',
            options: ['Sad', 'Joyful', 'Angry', 'Tired'],
            correct: 1
        },
        // Logical Reasoning (10 questions)
        {
            id: 21,
            type: 'logical',
            question: 'All roses are flowers. Some flowers fade quickly. Which statement is logically true?',
            options: ['Some roses are flowers', 'All flowers fade quickly', 'Some flowers fade quickly', 'All roses are flowers'],
            correct: 2
        },
        {
            id: 22,
            type: 'logical',
            question: 'Complete the series: 2, 4, 6, 8, ?',
            options: ['9', '10', '11', '12'],
            correct: 1
        },
        {
            id: 23,
            type: 'logical',
            question: 'If all Zips are Zongs and all Zongs are Zips, are all Zips definitely Zongs?',
            options: ['Yes', 'No', 'Cannot determine', 'Only some are'],
            correct: 1
        },
        // Data Interpretation (10 questions)
        {
            id: 31,
            type: 'data_interpretation',
            question: 'A company sold 100 units in Q1 and 150 units in Q2. What was the percentage increase?',
            options: ['25%', '50%', '75%', '100%'],
            correct: 1
        },
        {
            id: 32,
            type: 'data_interpretation',
            question: 'If sales increased from 200 to 300, what is the growth rate?',
            options: ['20%', '33%', '50%', '100%'],
            correct: 2
        },
        // Abstract Reasoning (10 questions)
        {
            id: 41,
            type: 'abstract_reasoning',
            question: 'What comes next in the sequence: 2, 4, 8, 16, ?',
            options: ['20', '24', '32', '64'],
            correct: 2
        },
        {
            id: 42,
            type: 'abstract_reasoning',
            question: 'If all Bloops are Razzies and all Razzies are Bloops, are all Bloops definitely Razzies?',
            options: ['Yes', 'No', 'Some are', 'None are'],
            correct: 1
        }
    ];
    
    console.log(`✅ Loaded ${currentTest.questions.length} sample questions`);
}

function setupEventListeners() {
    // Setup form listeners
    const sectionSelect = document.getElementById('sectionSelect');
    const difficultySelect = document.getElementById('difficultySelect');
    const questionCountSelect = document.getElementById('questionCount');
    const startBtn = document.getElementById('startTestBtn');
    
    if (sectionSelect) {
        sectionSelect.addEventListener('change', validateForm);
    }
    if (difficultySelect) {
        difficultySelect.addEventListener('change', validateForm);
    }
    if (questionCountSelect) {
        questionCountSelect.addEventListener('change', validateForm);
    }
    if (startBtn) {
        startBtn.addEventListener('click', startTest);
    }
    
    // Navigation buttons
    const prevBtn = document.getElementById('prevQuestion');
    const nextBtn = document.getElementById('nextQuestion');
    const submitBtn = document.getElementById('submitTest');
    
    if (prevBtn) {
        prevBtn.addEventListener('click', previousQuestion);
    }
    if (nextBtn) {
        nextBtn.addEventListener('click', nextQuestion);
    }
    if (submitBtn) {
        submitBtn.addEventListener('click', submitTest);
    }
    
    console.log('✅ Event listeners attached');
}

function validateForm() {
    const section = document.getElementById('sectionSelect').value;
    const difficulty = document.getElementById('difficultySelect').value;
    const count = document.getElementById('questionCount').value;
    const startBtn = document.getElementById('startTestBtn');
    const info = document.getElementById('setupInfo');
    
    if (section && difficulty && count) {
        startBtn.disabled = false;
        info.innerHTML = '<i class="fas fa-check-circle" style="color: var(--success);"></i> Ready to start! Click Start Aptitude Test.';
    } else {
        startBtn.disabled = true;
        info.innerHTML = '<i class="fas fa-info-circle"></i> Select section and difficulty to enable Start.';
    }
}

function startTest() {
    const section = document.getElementById('sectionSelect').value;
    const difficulty = document.getElementById('difficultySelect').value;
    const count = parseInt(document.getElementById('questionCount').value);
    
    if (!section || !difficulty || !count) {
        alert('Please select all options');
        return;
    }
    
    // Store test configuration
    currentTest.selectedSection = section;
    currentTest.selectedDifficulty = difficulty;
    currentTest.selectedCount = count;
    currentTest.startTime = new Date();
    
    // Filter questions based on section
    let filteredQuestions = currentTest.questions.filter(q => q.type === section);
    
    // Take only the requested number of questions
    currentTest.questions = filteredQuestions.slice(0, Math.min(count, filteredQuestions.length));
    
    if (currentTest.questions.length === 0) {
        alert('No questions available for this section');
        return;
    }
    
    // Update UI
    document.getElementById('setupSection').style.display = 'none';
    document.getElementById('testSection').style.display = 'block';
    
    // Set badges
    document.getElementById('selectedSection').textContent = getSectionLabel(section);
    document.getElementById('selectedDifficulty').textContent = getDifficultyLabel(difficulty);
    document.getElementById('selectedCount').textContent = `${count} Questions`;
    
    // Start timer
    startTimer(count * 60); // 1 minute per question
    
    // Display first question
    displayQuestion();
    
    console.log(`🚀 Test started: ${section} - ${difficulty} - ${count} questions`);
}

function getSectionLabel(section) {
    const labels = {
        'quantitative': 'Quantitative Aptitude',
        'verbal': 'Verbal Ability',
        'logical': 'Logical Reasoning',
        'data_interpretation': 'Data Interpretation',
        'abstract_reasoning': 'Abstract Reasoning'
    };
    return labels[section] || section;
}

function getDifficultyLabel(difficulty) {
    const labels = {
        'easy': 'Beginner',
        'medium': 'Intermediate',
        'hard': 'Advanced',
        'mixed': 'Mixed'
    };
    return labels[difficulty] || difficulty;
}

function startTimer(seconds) {
    let timeRemaining = seconds;
    const timerDisplay = document.getElementById('timerDisplay');
    
    const timerInterval = setInterval(() => {
        const minutes = Math.floor(timeRemaining / 60);
        const secs = timeRemaining % 60;
        timerDisplay.textContent = `Time Left: ${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
        
        if (timeRemaining <= 0) {
            clearInterval(timerInterval);
            submitTest();
        }
        
        timeRemaining--;
    }, 1000);
}

function displayQuestion() {
    if (currentTest.currentQuestion >= currentTest.questions.length) {
        showResults();
        return;
    }
    
    const question = currentTest.questions[currentTest.currentQuestion];
    const questionContainer = document.getElementById('questionContainer');
    const optionsContainer = document.getElementById('optionsContainer');
    const progressContainer = document.getElementById('progressIndicator');
    
    // Update progress
    progressContainer.innerHTML = `
        <i class="fas fa-chart-line"></i> Progress: ${currentTest.currentQuestion + 1}/${currentTest.questions.length} answered
        <div class="progress-bar">
            <div class="progress-fill" style="width: ${((currentTest.currentQuestion + 1) / currentTest.questions.length * 100)}%"></div>
        </div>
    `;
    
    // Display question
    questionContainer.innerHTML = `
        <div class="question-container">
            <div class="question-header">
                <span class="question-type">${getCategoryLabel(question.type)}</span>
                <span class="question-number">Question ${currentTest.currentQuestion + 1}</span>
            </div>
            <div class="question-text">${question.question}</div>
        </div>
    `;
    
    // Display options
    optionsContainer.innerHTML = '';
    question.options.forEach((option, index) => {
        const optionElement = document.createElement('div');
        optionElement.className = 'answer-option';
        optionElement.innerHTML = `
            <input type="radio" name="answer" value="${index}" id="option${index}">
            <label for="option${index}">${option}</label>
        `;
        optionsContainer.appendChild(optionElement);
    });
    
    // Add event listeners to new options
    document.querySelectorAll('.answer-option').forEach(option => {
        option.addEventListener('click', function() {
            selectAnswer(this);
        });
    });
    
    // Update navigation buttons
    updateNavigationButtons();
}

function getCategoryLabel(type) {
    const labels = {
        'quantitative': 'Quantitative',
        'verbal': 'Verbal',
        'logical': 'Logical Reasoning',
        'data_interpretation': 'Data Interpretation',
        'abstract_reasoning': 'Abstract Reasoning'
    };
    return labels[type] || type;
}

function selectAnswer(optionElement) {
    // Clear previous selection
    document.querySelectorAll('.answer-option').forEach(opt => {
        opt.classList.remove('selected');
    });
    
    // Mark new selection
    optionElement.classList.add('selected');
    const radio = optionElement.querySelector('input[type="radio"]');
    radio.checked = true;
    
    // Store answer
    const question = currentTest.questions[currentTest.currentQuestion];
    currentTest.answers[question.id] = parseInt(radio.value);
}

function previousQuestion() {
    if (currentTest.currentQuestion > 0) {
        currentTest.currentQuestion--;
        displayQuestion();
    }
}

function nextQuestion() {
    if (currentTest.currentQuestion < currentTest.questions.length - 1) {
        currentTest.currentQuestion++;
        displayQuestion();
    }
}

function updateNavigationButtons() {
    const prevBtn = document.getElementById('prevQuestion');
    const nextBtn = document.getElementById('nextQuestion');
    const submitBtn = document.getElementById('submitTest');
    
    prevBtn.style.display = currentTest.currentQuestion === 0 ? 'none' : 'inline-block';
    nextBtn.style.display = currentTest.currentQuestion === currentTest.questions.length - 1 ? 'none' : 'inline-block';
    submitBtn.style.display = currentTest.currentQuestion === currentTest.questions.length - 1 ? 'inline-block' : 'none';
}

function submitTest() {
    // Calculate time taken
    const endTime = new Date();
    const timeDiff = endTime - currentTest.startTime;
    const hours = Math.floor(timeDiff / 3600000);
    const minutes = Math.floor((timeDiff % 3600000) / 60000);
    const seconds = Math.floor((timeDiff % 60000) / 1000);
    currentTest.timeTaken = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    
    // Calculate scores by category
    const scores = calculateScores();
    
    // Submit to backend
    submitTestResults(scores);
}

function calculateScores() {
    const scores = {
        quantitative: 0,
        verbal: 0,
        logical: 0,
        data_interpretation: 0,
        abstract_reasoning: 0
    };
    
    currentTest.questions.forEach(question => {
        const userAnswer = currentTest.answers[question.id];
        const correctAnswer = question.correct;
        
        if (userAnswer === correctAnswer) {
            scores[question.type]++;
        }
    });
    
    return scores;
}

function submitTestResults(scores) {
    const testData = {
        scores: scores,
        max_score: currentTest.questions.length,
        time_taken: currentTest.timeTaken,
        difficulty_level: currentTest.selectedDifficulty
    };
    
    fetch('/api/submit-aptitude-test/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(testData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            showResults(data);
        } else {
            alert('Error: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error submitting test:', error);
        // Show results even if backend fails
        showResults({
            scores: scores,
            total_score: Object.values(scores).reduce((a, b) => a + b, 0),
            max_score: currentTest.questions.length,
            percentage: Math.round((Object.values(scores).reduce((a, b) => a + b, 0) / currentTest.questions.length) * 100)
        });
    });
}

function showResults(data) {
    const testSection = document.getElementById('testSection');
    const resultsSection = document.getElementById('resultsSection');
    const resultsContent = document.getElementById('resultsContent');
    
    // Hide test section, show results
    testSection.style.display = 'none';
    resultsSection.style.display = 'block';
    
    resultsContent.innerHTML = `
        <div class="score-breakdown">
            <h3>Score Breakdown by Topic:</h3>
            <div class="score-grid">
                <div class="score-item">
                    <h4>Quantitative</h4>
                    <div class="score">${data.scores.quantitative}/${data.max_score}</div>
                    <div class="percentage">${calculatePercentage(data.scores.quantitative, data.max_score)}%</div>
                </div>
                <div class="score-item">
                    <h4>Verbal</h4>
                    <div class="score">${data.scores.verbal}/${data.max_score}</div>
                    <div class="percentage">${calculatePercentage(data.scores.verbal, data.max_score)}%</div>
                </div>
                <div class="score-item">
                    <h4>Logical Reasoning</h4>
                    <div class="score">${data.scores.logical}/${data.max_score}</div>
                    <div class="percentage">${calculatePercentage(data.scores.logical, data.max_score)}%</div>
                </div>
                <div class="score-item">
                    <h4>Data Interpretation</h4>
                    <div class="score">${data.scores.data_interpretation}/${data.max_score}</div>
                    <div class="percentage">${calculatePercentage(data.scores.data_interpretation, data.max_score)}%</div>
                </div>
                <div class="score-item">
                    <h4>Abstract Reasoning</h4>
                    <div class="score">${data.scores.abstract_reasoning}/${data.max_score}</div>
                    <div class="percentage">${calculatePercentage(data.scores.abstract_reasoning, data.max_score)}%</div>
                </div>
            </div>
        </div>
        
        <div class="overall-score">
            <h3>Overall Performance</h3>
            <div class="score-circle">
                <div class="score-value">${data.percentage}%</div>
                <div class="score-label">${data.total_score}/${data.max_score}</div>
            </div>
            <p class="performance-text">${getPerformanceLevel(data.percentage)}</p>
        </div>
    `;
}

function calculatePercentage(score, maxScore) {
    return maxScore > 0 ? Math.round((score / maxScore) * 100) : 0;
}

function getPerformanceLevel(percentage) {
    if (percentage >= 80) return 'Excellent! 🌟';
    if (percentage >= 60) return 'Good! 👍';
    if (percentage >= 40) return 'Average! 👌';
    return 'Needs Improvement! 📚';
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

})(); // Close the IIFE (Immediately Invoked Function Expression)
