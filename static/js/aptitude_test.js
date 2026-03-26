// Aptitude Test JavaScript
(function() {
  // Global test state - make it accessible to dashboard
  window.currentTest = {
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
})();

function loadTestQuestions() {
  console.log('🧠 Loading aptitude test questions...');
  
  // Comprehensive questions for each category (150+ questions)
  window.currentTest.questions = [
    // Quantitative Aptitude (45 questions)
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
    {
      id: 4,
      type: 'quantitative',
      question: 'What is the square root of 144?',
      options: ['10', '11', '12', '13'],
      correct: 2
    },
    {
      id: 5,
      type: 'quantitative',
      question: 'If a shirt costs $40 after a 20% discount, what was the original price?',
      options: ['$48', '$50', '$52', '$60'],
      correct: 1
    },
    {
      id: 6,
      type: 'quantitative',
      question: 'What is 15% of 200?',
      options: ['25', '30', '35', '40'],
      correct: 1
    },
    {
      id: 7,
      type: 'quantitative',
      question: 'If 2x - 3 = 7, what is x?',
      options: ['3', '4', '5', '6'],
      correct: 2
    },
    {
      id: 8,
      type: 'quantitative',
      question: 'A car travels 180 km in 3 hours. What is its average speed?',
      options: ['50 km/h', '55 km/h', '60 km/h', '65 km/h'],
      correct: 2
    },
    {
      id: 9,
      type: 'quantitative',
      question: 'What is 3/4 of 80?',
      options: ['50', '60', '70', '80'],
      correct: 1
    },
    {
      id: 10,
      type: 'quantitative',
      question: 'If a rectangle has length 12cm and width 8cm, what is its area?',
      options: ['80 cm²', '96 cm²', '100 cm²', '120 cm²'],
      correct: 1
    },
    {
      id: 11,
      type: 'quantitative',
      question: 'What is 40% of 150?',
      options: ['50', '60', '70', '80'],
      correct: 1
    },
    {
      id: 12,
      type: 'quantitative',
      question: 'If 5x - 2 = 18, what is x?',
      options: ['2', '3', '4', '5'],
      correct: 2
    },
    {
      id: 13,
      type: 'quantitative',
      question: 'A bus travels 240 km in 4 hours. What is its speed?',
      options: ['50 km/h', '55 km/h', '60 km/h', '65 km/h'],
      correct: 2
    },
    {
      id: 14,
      type: 'quantitative',
      question: 'What is the cube of 4?',
      options: ['16', '32', '64', '128'],
      correct: 2
    },
    {
      id: 15,
      type: 'quantitative',
      question: 'If a product costs $75 after a 25% discount, what was the original price?',
      options: ['$90', '$95', '$100', '$105'],
      correct: 2
    },
    {
      id: 16,
      type: 'quantitative',
      question: 'What is 2/5 of 100?',
      options: ['30', '40', '50', '60'],
      correct: 1
    },
    {
      id: 17,
      type: 'quantitative',
      question: 'If 4x + 8 = 24, what is x?',
      options: ['2', '3', '4', '5'],
      correct: 2
    },
    {
      id: 18,
      type: 'quantitative',
      question: 'A cyclist travels 90 km in 2 hours. What is the speed?',
      options: ['35 km/h', '40 km/h', '45 km/h', '50 km/h'],
      correct: 2
    },
    {
      id: 19,
      type: 'quantitative',
      question: 'What is 30% of 250?',
      options: ['65', '70', '75', '80'],
      correct: 2
    },
    {
      id: 20,
      type: 'quantitative',
      question: 'If a triangle has base 10cm and height 8cm, what is its area?',
      options: ['30 cm²', '40 cm²', '50 cm²', '60 cm²'],
      correct: 1
    },
    {
      id: 21,
      type: 'quantitative',
      question: 'What is the square of 13?',
      options: ['149', '159', '169', '179'],
      correct: 2
    },
    {
      id: 22,
      type: 'quantitative',
      question: 'If 6x - 4 = 20, what is x?',
      options: ['2', '3', '4', '5'],
      correct: 2
    },
    {
      id: 23,
      type: 'quantitative',
      question: 'A truck travels 300 km in 5 hours. What is its speed?',
      options: ['50 km/h', '55 km/h', '60 km/h', '65 km/h'],
      correct: 2
    },
    {
      id: 24,
      type: 'quantitative',
      question: 'What is 5/8 of 64?',
      options: ['30', '35', '40', '45'],
      correct: 2
    },
    {
      id: 25,
      type: 'quantitative',
      question: 'If a book costs $48 after a 20% discount, what was the original price?',
      options: ['$54', '$56', '$58', '$60'],
      correct: 3
    },
    {
      id: 26,
      type: 'quantitative',
      question: 'What is 35% of 180?',
      options: ['53', '58', '63', '68'],
      correct: 2
    },
    {
      id: 27,
      type: 'quantitative',
      question: 'If 7x + 3 = 24, what is x?',
      options: ['1', '2', '3', '4'],
      correct: 2
    },
    {
      id: 28,
      type: 'quantitative',
      question: 'A train travels 420 km in 6 hours. What is its speed?',
      options: ['60 km/h', '65 km/h', '70 km/h', '75 km/h'],
      correct: 2
    },
    {
      id: 29,
      type: 'quantitative',
      question: 'What is 3/7 of 84?',
      options: ['30', '32', '34', '36'],
      correct: 3
    },
    {
      id: 30,
      type: 'quantitative',
      question: 'If a circle has radius 7cm, what is its area? (π = 22/7)',
      options: ['140 cm²', '144 cm²', '148 cm²', '154 cm²'],
      correct: 3
    },
    {
      id: 31,
      type: 'quantitative',
      question: 'What is 45% of 220?',
      options: ['89', '94', '99', '104'],
      correct: 2
    },
    {
      id: 32,
      type: 'quantitative',
      question: 'If 8x - 6 = 26, what is x?',
      options: ['3', '4', '5', '6'],
      correct: 1
    },
    {
      id: 33,
      type: 'quantitative',
      question: 'A plane travels 720 km in 2 hours. What is its speed?',
      options: ['340 km/h', '350 km/h', '360 km/h', '370 km/h'],
      correct: 2
    },
    {
      id: 34,
      type: 'quantitative',
      question: 'What is 7/12 of 144?',
      options: ['74', '78', '82', '84'],
      correct: 3
    },
    {
      id: 35,
      type: 'quantitative',
      question: 'If a laptop costs $600 after a 15% discount, what was the original price?',
      options: ['$680', '$700', '$720', '$740'],
      correct: 1
    },
    {
      id: 36,
      type: 'quantitative',
      question: 'What is 55% of 320?',
      options: ['166', '172', '176', '182'],
      correct: 2
    },
    {
      id: 37,
      type: 'quantitative',
      question: 'If 9x + 7 = 34, what is x?',
      options: ['1', '2', '3', '4'],
      correct: 2
    },
    {
      id: 38,
      type: 'quantitative',
      question: 'A ship travels 540 km in 9 hours. What is its speed?',
      options: ['50 km/h', '55 km/h', '60 km/h', '65 km/h'],
      correct: 2
    },
    {
      id: 39,
      type: 'quantitative',
      question: 'What is 4/9 of 108?',
      options: ['40', '44', '48', '52'],
      correct: 2
    },
    {
      id: 40,
      type: 'quantitative',
      question: 'If a smartphone costs $320 after a 20% discount, what was the original price?',
      options: ['$380', '$390', '$400', '$410'],
      correct: 2
    },
    {
      id: 41,
      type: 'quantitative',
      question: 'What is 65% of 280?',
      options: ['172', '178', '182', '188'],
      correct: 2
    },
    {
      id: 42,
      type: 'quantitative',
      question: 'If 11x - 9 = 24, what is x?',
      options: ['1', '2', '3', '4'],
      correct: 2
    },
    {
      id: 43,
      type: 'quantitative',
      question: 'A helicopter travels 360 km in 3 hours. What is its speed?',
      options: ['110 km/h', '115 km/h', '120 km/h', '125 km/h'],
      correct: 2
    },
    {
      id: 44,
      type: 'quantitative',
      question: 'What is 8/15 of 225?',
      options: ['110', '115', '120', '125'],
      correct: 2
    },
    {
      id: 45,
      type: 'quantitative',
      question: 'If a tablet costs $450 after a 25% discount, what was the original price?',
      options: ['$560', '$580', '$600', '$620'],
      correct: 2
    },

    // Verbal Ability (35 questions)
    {
      id: 46,
      type: 'verbal',
      question: 'Which word is the opposite of "increase"?',
      options: ['decrease', 'reduce', 'grow', 'expand'],
      correct: 0
    },
    {
      id: 47,
      type: 'verbal',
      question: 'Complete the analogy: Dog is to Bark as Cat is to...',
      options: ['Meow', 'Purr', 'Sleep', 'Hunt'],
      correct: 0
    },
    {
      id: 48,
      type: 'verbal',
      question: 'Choose the synonym of "Happy"',
      options: ['Sad', 'Joyful', 'Angry', 'Tired'],
      correct: 1
    },
    {
      id: 49,
      type: 'verbal',
      question: 'Which word means "to make something better"?',
      options: ['Improve', 'Worsen', 'Change', 'Remove'],
      correct: 0
    },
    {
      id: 50,
      type: 'verbal',
      question: 'Complete the sentence: The sun ___ in the east.',
      options: ['rises', 'sets', 'shines', 'moves'],
      correct: 0
    },
    {
      id: 51,
      type: 'verbal',
      question: 'Which is the correct spelling?',
      options: ['Necessary', 'Necesary', 'Necesarry', 'Necassary'],
      correct: 0
    },
    {
      id: 52,
      type: 'verbal',
      question: 'What is the plural of "child"?',
      options: ['Childs', 'Children', 'Childrens', 'Childes'],
      correct: 1
    },
    {
      id: 53,
      type: 'verbal',
      question: 'Which word is a noun?',
      options: ['Run', 'Quickly', 'Table', 'Beautiful'],
      correct: 2
    },
    {
      id: 54,
      type: 'verbal',
      question: 'Complete the analogy: Book is to Read as Music is to...',
      options: ['Listen', 'Hear', 'Play', 'Sing'],
      correct: 0
    },
    {
      id: 55,
      type: 'verbal',
      question: 'Which word means "very large"?',
      options: ['Tiny', 'Huge', 'Small', 'Medium'],
      correct: 1
    },
    {
      id: 56,
      type: 'verbal',
      question: 'Choose the antonym of "hot"',
      options: ['Warm', 'Cool', 'Cold', 'Mild'],
      correct: 2
    },
    {
      id: 57,
      type: 'verbal',
      question: 'Which sentence is grammatically correct?',
      options: ['He go to school', 'He goes to school', 'He going to school', 'He gone to school'],
      correct: 1
    },
    {
      id: 58,
      type: 'verbal',
      question: 'What is the past tense of "write"?',
      options: ['Wrote', 'Written', 'Writed', 'Writing'],
      correct: 0
    },
    {
      id: 59,
      type: 'verbal',
      question: 'Which word means "to fix"?',
      options: ['Repair', 'Break', 'Damage', 'Destroy'],
      correct: 0
    },
    {
      id: 60,
      type: 'verbal',
      question: 'Complete the sentence: She ___ to the store yesterday.',
      options: ['go', 'goes', 'went', 'going'],
      correct: 2
    },
    {
      id: 61,
      type: 'verbal',
      question: 'Which word is an adjective?',
      options: ['Run', 'Quickly', 'Quick', 'Quickness'],
      correct: 2
    },
    {
      id: 62,
      type: 'verbal',
      question: 'What is the meaning of "ubiquitous"?',
      options: ['Rare', 'Common', 'Expensive', 'Cheap'],
      correct: 1
    },
    {
      id: 63,
      type: 'verbal',
      question: 'Which is the correct pronunciation of "schedule"?',
      options: ['SKED-jool', 'SHED-jool', 'SKED-ule', 'SHED-ule'],
      correct: 0
    },
    {
      id: 64,
      type: 'verbal',
      question: 'Complete the analogy: Pen is to Write as Knife is to...',
      options: ['Cut', 'Cook', 'Eat', 'Serve'],
      correct: 0
    },
    {
      id: 65,
      type: 'verbal',
      question: 'Which word means "to understand"?',
      options: ['Comprehend', 'Ignore', 'Forget', 'Confuse'],
      correct: 0
    },
    {
      id: 66,
      type: 'verbal',
      question: 'What is the comparative form of "good"?',
      options: ['Gooder', 'Better', 'Best', 'More good'],
      correct: 1
    },
    {
      id: 67,
      type: 'verbal',
      question: 'Which sentence uses the correct article?',
      options: ['She is a engineer', 'She is an engineer', 'She is the engineer', 'She is engineer'],
      correct: 1
    },
    {
      id: 68,
      type: 'verbal',
      question: 'What is the meaning of "ephemeral"?',
      options: ['Permanent', 'Temporary', 'Important', 'Unimportant'],
      correct: 1
    },
    {
      id: 69,
      type: 'verbal',
      question: 'Which word means "to speak quietly"?',
      options: ['Shout', 'Whisper', 'Talk', 'Sing'],
      correct: 1
    },
    {
      id: 70,
      type: 'verbal',
      question: 'Complete the sentence: The flowers ___ in spring.',
      options: ['bloom', 'blooms', 'bloomed', 'blooming'],
      correct: 0
    },
    {
      id: 71,
      type: 'verbal',
      question: 'Which word is a verb?',
      options: ['Table', 'Run', 'Quick', 'Beautiful'],
      correct: 1
    },
    {
      id: 72,
      type: 'verbal',
      question: 'What is the superlative form of "beautiful"?',
      options: ['Beautifuler', 'More beautiful', 'Most beautiful', 'Beautifullest'],
      correct: 2
    },
    {
      id: 73,
      type: 'verbal',
      question: 'Which word means "to make something smaller"?',
      options: ['Enlarge', 'Reduce', 'Increase', 'Expand'],
      correct: 1
    },
    {
      id: 74,
      type: 'verbal',
      question: 'Complete the analogy: Doctor is to Hospital as Teacher is to...',
      options: ['School', 'Office', 'Home', 'Library'],
      correct: 0
    },
    {
      id: 75,
      type: 'verbal',
      question: 'Which word means "to give up"?',
      options: ['Continue', 'Surrender', 'Fight', 'Win'],
      correct: 1
    },
    {
      id: 76,
      type: 'verbal',
      question: 'What is the past participle of "eat"?',
      options: ['Ate', 'Eaten', 'Eating', 'Eats'],
      correct: 1
    },
    {
      id: 77,
      type: 'verbal',
      question: 'Which word means "very important"?',
      options: ['Trivial', 'Crucial', 'Minor', 'Unnecessary'],
      correct: 1
    },
    {
      id: 78,
      type: 'verbal',
      question: 'Complete the sentence: They ___ the movie last night.',
      options: ['watch', 'watches', 'watched', 'watching'],
      correct: 2
    },
    {
      id: 79,
      type: 'verbal',
      question: 'Which word means "to think carefully"?',
      options: ['Ignore', 'Consider', 'Forget', 'Dismiss'],
      correct: 1
    },
    {
      id: 80,
      type: 'verbal',
      question: 'What is the meaning of "ambiguous"?',
      options: ['Clear', 'Unclear', 'Simple', 'Complex'],
      correct: 1
    },

    // Logical Reasoning (40 questions)
    {
      id: 81,
      type: 'logical',
      question: 'All roses are flowers. Some flowers fade quickly. Which statement is logically true?',
      options: ['Some roses are flowers', 'All flowers fade quickly', 'Some flowers fade quickly', 'All roses are flowers'],
      correct: 2
    },
    {
      id: 82,
      type: 'logical',
      question: 'Complete the series: 2, 4, 6, 8, ?',
      options: ['9', '10', '11', '12'],
      correct: 1
    },
    {
      id: 83,
      type: 'logical',
      question: 'If all Zips are Zongs and all Zongs are Zips, are all Zips definitely Zongs?',
      options: ['Yes', 'No', 'Cannot determine', 'Only some are'],
      correct: 1
    },
    {
      id: 84,
      type: 'logical',
      question: 'Complete the series: 1, 4, 9, 16, ?',
      options: ['20', '25', '30', '36'],
      correct: 1
    },
    {
      id: 85,
      type: 'logical',
      question: 'If some cats are black and all black animals are mysterious, what can we conclude?',
      options: ['All cats are mysterious', 'Some cats are mysterious', 'No cats are mysterious', 'Black cats are not mysterious'],
      correct: 1
    },
    {
      id: 86,
      type: 'logical',
      question: 'Complete the series: 3, 6, 9, 12, ?',
      options: ['13', '14', '15', '16'],
      correct: 2
    },
    {
      id: 87,
      type: 'logical',
      question: 'If all doctors are smart and all smart people are successful, what can we conclude?',
      options: ['All doctors are successful', 'All successful people are doctors', 'Some doctors are not successful', 'No conclusion can be drawn'],
      correct: 0
    },
    {
      id: 88,
      type: 'logical',
      question: 'Complete the series: 5, 10, 15, 20, ?',
      options: ['21', '22', '25', '30'],
      correct: 2
    },
    {
      id: 89,
      type: 'logical',
      question: 'If some students are athletes and all athletes are disciplined, what can we conclude?',
      options: ['All students are disciplined', 'Some students are disciplined', 'No students are disciplined', 'Athletes are not students'],
      correct: 1
    },
    {
      id: 90,
      type: 'logical',
      question: 'Complete the series: 1, 3, 5, 7, ?',
      options: ['8', '9', '10', '11'],
      correct: 1
    },
    {
      id: 91,
      type: 'logical',
      question: 'If all birds can fly and penguins are birds, what can we conclude?',
      options: ['Penguins can fly', 'Penguins cannot fly', 'Not all birds can fly', 'Penguins are not birds'],
      correct: 2
    },
    {
      id: 92,
      type: 'logical',
      question: 'Complete the series: 2, 5, 8, 11, ?',
      options: ['12', '13', '14', '15'],
      correct: 2
    },
    {
      id: 93,
      type: 'logical',
      question: 'If some cars are red and all red things are expensive, what can we conclude?',
      options: ['All cars are expensive', 'Some cars are expensive', 'No cars are expensive', 'Red cars are not expensive'],
      correct: 1
    },
    {
      id: 94,
      type: 'logical',
      question: 'Complete the series: 10, 20, 30, 40, ?',
      options: ['45', '50', '55', '60'],
      correct: 1
    },
    {
      id: 95,
      type: 'logical',
      question: 'If all dogs are mammals and some mammals are pets, what can we conclude?',
      options: ['All dogs are pets', 'Some dogs are pets', 'No dogs are pets', 'All pets are dogs'],
      correct: 1
    },
    {
      id: 96,
      type: 'logical',
      question: 'Complete the series: 1, 2, 4, 8, ?',
      options: ['12', '14', '16', '18'],
      correct: 2
    },
    {
      id: 97,
      type: 'logical',
      question: 'If some fruits are sweet and all sweet things are delicious, what can we conclude?',
      options: ['All fruits are delicious', 'Some fruits are delicious', 'No fruits are delicious', 'Sweet fruits are not delicious'],
      correct: 1
    },
    {
      id: 98,
      type: 'logical',
      question: 'Complete the series: 7, 14, 21, 28, ?',
      options: ['30', '32', '35', '40'],
      correct: 2
    },
    {
      id: 99,
      type: 'logical',
      question: 'If all books have pages and some pages have pictures, what can we conclude?',
      options: ['All books have pictures', 'Some books have pictures', 'No books have pictures', 'Pages are not in books'],
      correct: 1
    },
    {
      id: 100,
      type: 'logical',
      question: 'Complete the series: 3, 9, 27, 81, ?',
      options: ['108', '162', '243', '324'],
      correct: 2
    },
    {
      id: 101,
      type: 'logical',
      question: 'If some students study hard and all who study hard pass exams, what can we conclude?',
      options: ['All students pass exams', 'Some students pass exams', 'No students pass exams', 'Hard study guarantees failure'],
      correct: 1
    },
    {
      id: 102,
      type: 'logical',
      question: 'Complete the series: 4, 8, 12, 16, ?',
      options: ['18', '20', '22', '24'],
      correct: 1
    },
    {
      id: 103,
      type: 'logical',
      question: 'If all circles are round and some round things are balls, what can we conclude?',
      options: ['All circles are balls', 'Some circles are balls', 'No circles are balls', 'Balls are not circles'],
      correct: 1
    },
    {
      id: 104,
      type: 'logical',
      question: 'Complete the series: 6, 12, 18, 24, ?',
      options: ['26', '28', '30', '32'],
      correct: 2
    },
    {
      id: 105,
      type: 'logical',
      question: 'If some animals are pets and all pets need care, what can we conclude?',
      options: ['All animals need care', 'Some animals need care', 'No animals need care', 'Pets are not animals'],
      correct: 1
    },
    {
      id: 106,
      type: 'logical',
      question: 'Complete the series: 9, 18, 27, 36, ?',
      options: ['40', '45', '50', '55'],
      correct: 1
    },
    {
      id: 107,
      type: 'logical',
      question: 'If all plants need water and some living things are plants, what can we conclude?',
      options: ['All living things need water', 'Some living things need water', 'No living things need water', 'Plants are not living'],
      correct: 1
    },
    {
      id: 108,
      type: 'logical',
      question: 'Complete the series: 11, 22, 33, 44, ?',
      options: ['50', '55', '60', '65'],
      correct: 1
    },
    {
      id: 109,
      type: 'logical',
      question: 'If some cars are fast and all fast things are exciting, what can we conclude?',
      options: ['All cars are exciting', 'Some cars are exciting', 'No cars are exciting', 'Fast cars are not exciting'],
      correct: 1
    },
    {
      id: 110,
      type: 'logical',
      question: 'Complete the series: 13, 26, 39, 52, ?',
      options: ['60', '65', '70', '75'],
      correct: 1
    },
    {
      id: 111,
      type: 'logical',
      question: 'If all teachers are educated and some educated people are wise, what can we conclude?',
      options: ['All teachers are wise', 'Some teachers are wise', 'No teachers are wise', 'Wise people are not teachers'],
      correct: 1
    },
    {
      id: 112,
      type: 'logical',
      question: 'Complete the series: 15, 30, 45, 60, ?',
      options: ['65', '70', '75', '80'],
      correct: 2
    },
    {
      id: 113,
      type: 'logical',
      question: 'If some foods are healthy and all healthy things are good for you, what can we conclude?',
      options: ['All foods are good for you', 'Some foods are good for you', 'No foods are good for you', 'Healthy foods are not good'],
      correct: 1
    },
    {
      id: 114,
      type: 'logical',
      question: 'Complete the series: 17, 34, 51, 68, ?',
      options: ['75', '80', '85', '90'],
      correct: 2
    },
    {
      id: 115,
      type: 'logical',
      question: 'If all musicians are creative and some creative people are famous, what can we conclude?',
      options: ['All musicians are famous', 'Some musicians are famous', 'No musicians are famous', 'Famous people are not musicians'],
      correct: 1
    },
    {
      id: 116,
      type: 'logical',
      question: 'Complete the series: 19, 38, 57, 76, ?',
      options: ['85', '90', '95', '100'],
      correct: 2
    },
    {
      id: 117,
      type: 'logical',
      question: 'If some students are athletes and all athletes are strong, what can we conclude?',
      options: ['All students are strong', 'Some students are strong', 'No students are strong', 'Strong students are not athletes'],
      correct: 1
    },
    {
      id: 118,
      type: 'logical',
      question: 'Complete the series: 21, 42, 63, 84, ?',
      options: ['95', '100', '105', '110'],
      correct: 2
    },
    {
      id: 119,
      type: 'logical',
      question: 'If all doctors are professional and some professional people are wealthy, what can we conclude?',
      options: ['All doctors are wealthy', 'Some doctors are wealthy', 'No doctors are wealthy', 'Wealthy people are not doctors'],
      correct: 1
    },
    {
      id: 120,
      type: 'logical',
      question: 'Complete the series: 23, 46, 69, 92, ?',
      options: ['105', '110', '115', '120'],
      correct: 2
    },

    // Data Interpretation (30 questions)
    {
      id: 121,
      type: 'data_interpretation',
      question: 'A company sold 100 units in Q1 and 150 units in Q2. What was the percentage increase?',
      options: ['25%', '50%', '75%', '100%'],
      correct: 1
    },
    {
      id: 122,
      type: 'data_interpretation',
      question: 'If a pie chart shows 30% for category A, 25% for B, and 45% for C, what fraction represents category C?',
      options: ['3/10', '1/4', '9/20', '1/2'],
      correct: 2
    },
    {
      id: 123,
      type: 'data_interpretation',
      question: 'A bar chart shows sales of 200, 300, 250, 350 for 4 quarters. What was the average sales?',
      options: ['250', '275', '300', '325'],
      correct: 1
    },
    {
      id: 124,
      type: 'data_interpretation',
      question: 'If a line graph shows values increasing from 10 to 50 over 5 years, what is the average annual increase?',
      options: ['5', '8', '10', '12'],
      correct: 1
    },
    {
      id: 125,
      type: 'data_interpretation',
      question: 'A table shows 5 students scored 80, 85, 90, 75, and 95. What is the median score?',
      options: ['80', '85', '90', '87.5'],
      correct: 1
    },
    {
      id: 126,
      type: 'data_interpretation',
      question: 'If a histogram shows frequencies of 10, 15, 20, 25, what is the total frequency?',
      options: ['60', '70', '80', '90'],
      correct: 1
    },
    {
      id: 127,
      type: 'data_interpretation',
      question: 'A scatter plot shows points forming a line from (0,0) to (10,50). What is the slope?',
      options: ['2', '5', '10', '50'],
      correct: 1
    },
    {
      id: 128,
      type: 'data_interpretation',
      question: 'If a pie chart has 4 equal sections, what percentage does each section represent?',
      options: ['20%', '25%', '30%', '35%'],
      correct: 1
    },
    {
      id: 129,
      type: 'data_interpretation',
      question: 'A bar chart shows values of 100, 200, 300. What is the ratio of the largest to smallest?',
      options: ['1:2', '2:1', '3:1', '1:3'],
      correct: 2
    },
    {
      id: 130,
      type: 'data_interpretation',
      question: 'If a line graph shows values decreasing from 100 to 40 over 3 years, what is the average annual decrease?',
      options: ['15', '20', '25', '30'],
      correct: 1
    },
    {
      id: 131,
      type: 'data_interpretation',
      question: 'A table shows 6 numbers: 12, 15, 18, 21, 24, 27. What is the mean?',
      options: ['16', '17', '18', '19'],
      correct: 3
    },
    {
      id: 132,
      type: 'data_interpretation',
      question: 'If a histogram shows bars with heights 5, 10, 15, 20, what is the mode?',
      options: ['5', '10', '15', '20'],
      correct: 3
    },
    {
      id: 133,
      type: 'data_interpretation',
      question: 'A scatter plot shows points at (1,2), (2,4), (3,6). What is the relationship?',
      options: ['y = x', 'y = 2x', 'y = x + 1', 'y = x²'],
      correct: 1
    },
    {
      id: 134,
      type: 'data_interpretation',
      question: 'If a pie chart shows 60% for category A and 40% for B, what is the ratio of A to B?',
      options: ['2:1', '3:2', '4:3', '5:4'],
      correct: 1
    },
    {
      id: 135,
      type: 'data_interpretation',
      question: 'A bar chart shows sales of 150, 250, 200, 300. What was the total sales?',
      options: ['800', '900', '1000', '1100'],
      correct: 1
    },
    {
      id: 136,
      type: 'data_interpretation',
      question: 'If a line graph shows values of 20, 30, 40, 50 over 4 periods, what is the growth rate?',
      options: ['10%', '20%', '25%', '30%'],
      correct: 2
    },
    {
      id: 137,
      type: 'data_interpretation',
      question: 'A table shows 7 scores: 65, 70, 75, 80, 85, 90, 95. What is the range?',
      options: ['20', '25', '30', '35'],
      correct: 2
    },
    {
      id: 138,
      type: 'data_interpretation',
      question: 'If a histogram shows frequencies of 8, 12, 16, 20, what is the average frequency?',
      options: ['12', '14', '16', '18'],
      correct: 1
    },
    {
      id: 139,
      type: 'data_interpretation',
      question: 'A scatter plot shows points forming a curve from (0,1) to (10,101). What is the likely equation?',
      options: ['y = x + 1', 'y = 10x + 1', 'y = x² + 1', 'y = 2x + 1'],
      correct: 2
    },
    {
      id: 140,
      type: 'data_interpretation',
      question: 'If a pie chart has 5 sections with angles 72°, 108°, 144°, 36°, and 0°, what percentage is the largest section?',
      options: ['20%', '30%', '40%', '50%'],
      correct: 2
    },
    {
      id: 141,
      type: 'data_interpretation',
      question: 'A bar chart shows values of 80, 160, 240, 320. What is the pattern?',
      options: ['Add 80', 'Multiply by 2', 'Add 160', 'Multiply by 3'],
      correct: 0
    },
    {
      id: 142,
      type: 'data_interpretation',
      question: 'If a line graph shows exponential growth from 1 to 32 over 5 periods, what is the growth factor?',
      options: ['2', '3', '4', '5'],
      correct: 0
    },
    {
      id: 143,
      type: 'data_interpretation',
      question: 'A table shows 8 numbers: 10, 20, 30, 40, 50, 60, 70, 80. What is the standard deviation?',
      options: ['20', '22', '24', '26'],
      correct: 2
    },
    {
      id: 144,
      type: 'data_interpretation',
      question: 'If a histogram shows a normal distribution with mean 50 and standard deviation 10, what percentage is between 40 and 60?',
      options: ['50%', '68%', '85%', '95%'],
      correct: 1
    },
    {
      id: 145,
      type: 'data_interpretation',
      question: 'A scatter plot shows correlation coefficient of 0.8. What does this indicate?',
      options: ['Weak positive', 'Strong positive', 'Weak negative', 'Strong negative'],
      correct: 1
    },
    {
      id: 146,
      type: 'data_interpretation',
      question: 'If a pie chart shows 15%, 25%, 35%, and 25%, what is the total angle for the largest section?',
      options: ['90°', '108°', '126°', '144°'],
      correct: 2
    },
    {
      id: 147,
      type: 'data_interpretation',
      question: 'A bar chart shows sales of 120, 180, 240, 300. What is the percentage increase from first to last?',
      options: ['100%', '150%', '200%', '250%'],
      correct: 1
    },
    {
      id: 148,
      type: 'data_interpretation',
      question: 'If a line graph shows linear growth from 5 to 25 over 4 periods, what is the slope?',
      options: ['4', '5', '6', '7'],
      correct: 1
    },
    {
      id: 149,
      type: 'data_interpretation',
      question: 'A table shows 9 values: 5, 10, 15, 20, 25, 30, 35, 40, 45. What is the interquartile range?',
      options: ['15', '20', '25', '30'],
      correct: 2
    },
    {
      id: 150,
      type: 'data_interpretation',
      question: 'If a histogram shows frequencies of 5, 10, 15, 20, 25, 30, what is the cumulative frequency of the first 4 bars?',
      options: ['40', '50', '60', '70'],
      correct: 1
    },

    // Abstract Reasoning (25 questions)
    {
      id: 151,
      type: 'abstract_reasoning',
      question: 'Complete the pattern: ▲ ◆ ▲ ◆ ?',
      options: ['▲', '◆', '●', '■'],
      correct: 0
    },
    {
      id: 152,
      type: 'abstract_reasoning',
      question: 'Which shape comes next: Circle, Square, Triangle, Circle, ?',
      options: ['Square', 'Triangle', 'Circle', 'Diamond'],
      correct: 0
    },
    {
      id: 153,
      type: 'abstract_reasoning',
      question: 'Complete the sequence: Red, Blue, Green, Red, ?',
      options: ['Yellow', 'Blue', 'Green', 'Orange'],
      correct: 1
    },
    {
      id: 154,
      type: 'abstract_reasoning',
      question: 'Which figure completes the pattern: +, -, ×, ÷, +, ?',
      options: ['-', '×', '÷', '+'],
      correct: 0
    },
    {
      id: 155,
      type: 'abstract_reasoning',
      question: 'Complete the series: A, C, E, G, ?',
      options: ['H', 'I', 'J', 'K'],
      correct: 1
    },
    {
      id: 156,
      type: 'abstract_reasoning',
      question: 'Which shape is different: Circle, Square, Triangle, Sphere, Pentagon?',
      options: ['Circle', 'Square', 'Triangle', 'Sphere'],
      correct: 3
    },
    {
      id: 157,
      type: 'abstract_reasoning',
      question: 'Complete the pattern: 1, 1, 2, 3, 5, ?',
      options: ['6', '7', '8', '9'],
      correct: 2
    },
    {
      id: 158,
      type: 'abstract_reasoning',
      question: 'Which comes next: Monday, Wednesday, Friday, ?',
      options: ['Saturday', 'Sunday', 'Tuesday', 'Thursday'],
      correct: 1
    },
    {
      id: 159,
      type: 'abstract_reasoning',
      question: 'Complete the series: 2, 3, 5, 7, 11, ?',
      options: ['12', '13', '14', '15'],
      correct: 1
    },
    {
      id: 160,
      type: 'abstract_reasoning',
      question: 'Which number doesn\'t belong: 2, 4, 6, 8, 11, 12?',
      options: ['2', '4', '6', '11'],
      correct: 3
    },
    {
      id: 161,
      type: 'abstract_reasoning',
      question: 'Complete the pattern: AB, CD, EF, GH, ?',
      options: ['IJ', 'KL', 'MN', 'OP'],
      correct: 0
    },
    {
      id: 162,
      type: 'abstract_reasoning',
      question: 'Which comes next: Spring, Summer, Autumn, ?',
      options: ['Winter', 'Spring', 'Summer', 'Autumn'],
      correct: 0
    },
    {
      id: 163,
      type: 'abstract_reasoning',
      question: 'Complete the series: 1, 4, 9, 16, 25, ?',
      options: ['30', '32', '36', '40'],
      correct: 2
    },
    {
      id: 164,
      type: 'abstract_reasoning',
      question: 'Which letter is missing: A, D, G, J, M, ?',
      options: ['N', 'O', 'P', 'Q'],
      correct: 2
    },
    {
      id: 165,
      type: 'abstract_reasoning',
      question: 'Complete the pattern: ○, □, ○, □, ?',
      options: ['○', '□', '△', '◇'],
      correct: 0
    },
    {
      id: 166,
      type: 'abstract_reasoning',
      question: 'Which number comes next: 1, 8, 27, 64, ?',
      options: ['100', '125', '150', '175'],
      correct: 1
    },
    {
      id: 167,
      type: 'abstract_reasoning',
      question: 'Complete the series: B, D, F, H, J, ?',
      options: ['K', 'L', 'M', 'N'],
      correct: 1
    },
    {
      id: 168,
      type: 'abstract_reasoning',
      question: 'Which shape completes: Triangle, Square, Pentagon, ?',
      options: ['Circle', 'Hexagon', 'Octagon', 'Rectangle'],
      correct: 1
    },
    {
      id: 169,
      type: 'abstract_reasoning',
      question: 'Complete the pattern: 3, 6, 12, 24, ?',
      options: ['36', '48', '60', '72'],
      correct: 1
    },
    {
      id: 170,
      type: 'abstract_reasoning',
      question: 'Which comes next: January, March, May, July, ?',
      options: ['August', 'September', 'October', 'November'],
      correct: 1
    },
    {
      id: 171,
      type: 'abstract_reasoning',
      question: 'Complete the series: C, F, I, L, O, ?',
      options: ['P', 'Q', 'R', 'S'],
      correct: 2
    },
    {
      id: 172,
      type: 'abstract_reasoning',
      question: 'Which number doesn\'t fit: 3, 6, 9, 12, 15, 17, 18?',
      options: ['3', '6', '9', '17'],
      correct: 3
    },
    {
      id: 173,
      type: 'abstract_reasoning',
      question: 'Complete the pattern: 5, 10, 20, 40, ?',
      options: ['60', '70', '80', '90'],
      correct: 2
    },
    {
      id: 174,
      type: 'abstract_reasoning',
      question: 'Which letter comes next: X, V, T, R, ?',
      options: ['P', 'Q', 'S', 'T'],
      correct: 0
    },
    {
      id: 175,
      type: 'abstract_reasoning',
      question: 'Complete the series: 2, 6, 18, 54, ?',
      options: ['108', '126', '144', '162'],
      correct: 3
    }
  ];
  
  console.log(`✅ Loaded ${window.currentTest.questions.length} aptitude questions successfully`);
  
  // Log question counts by category
  const categories = {
    quantitative: window.currentTest.questions.filter(q => q.type === 'quantitative').length,
    verbal: window.currentTest.questions.filter(q => q.type === 'verbal').length,
    logical: window.currentTest.questions.filter(q => q.type === 'logical').length,
    data_interpretation: window.currentTest.questions.filter(q => q.type === 'data_interpretation').length,
    abstract_reasoning: window.currentTest.questions.filter(q => q.type === 'abstract_reasoning').length
  };
  
  console.log('📊 Question categories:', categories);
}

// Test functions
function startTest() {
    const section = document.getElementById('sectionSelect').value;
    const difficulty = document.getElementById('difficultySelect').value;
    const count = parseInt(document.getElementById('questionCount').value);
    
    if (!section || !difficulty || !count) {
        alert('Please fill in all fields');
        return;
    }
    
    // Filter questions based on section
    let selectedQuestions = window.currentTest.questions.filter(q => q.type === section);
    selectedQuestions = selectedQuestions.sort(() => Math.random() - 0.5).slice(0, count);
    
    if (selectedQuestions.length === 0) {
        alert('No questions available for this section');
        return;
    }
    
    // Initialize test state
    window.currentTest.currentQuestion = 0;
    window.currentTest.answers = {};
    window.currentTest.startTime = new Date();
    window.currentTest.selectedSection = section;
    window.currentTest.selectedDifficulty = difficulty;
    window.currentTest.selectedCount = count;
    window.currentTest.questions = selectedQuestions;
    
    // Show test interface
    const setupSection = document.getElementById('setupSection');
    const testSection = document.getElementById('testSection');
    
    if (setupSection) setupSection.style.display = 'none';
    if (testSection) testSection.style.display = 'block';
    
    displayQuestion();
    startTimer();
}

function displayQuestion() {
    const question = window.currentTest.questions[window.currentTest.currentQuestion];
    const questionContainer = document.getElementById('questionContainer');
    const questionNumber = document.getElementById('questionNumber');
    const progress = document.getElementById('progress');
    
    // Check if we're in dashboard context (missing test interface elements)
    if (!questionContainer || !questionNumber) {
        console.log('🔄 Test interface elements not found - likely in dashboard context');
        console.log('📍 Redirecting to full aptitude test page...');
        
        // Redirect to the actual aptitude test page with test parameters
        const params = new URLSearchParams({
            section: window.currentTest.selectedSection,
            difficulty: window.currentTest.selectedDifficulty,
            count: window.currentTest.selectedCount
        });
        
        window.location.href = `/aptitude-test/?${params.toString()}`;
        return;
    }
    
    questionNumber.textContent = `Question ${window.currentTest.currentQuestion + 1} of ${window.currentTest.questions.length}`;
    if (progress) progress.textContent = `Progress: ${Math.round((window.currentTest.currentQuestion / window.currentTest.questions.length) * 100)}%`;
    
    questionContainer.innerHTML = `
        <div class="question-text">
            <h3>${question.question}</h3>
        </div>
        <div class="options-container">
            ${question.options.map((option, index) => `
                <label class="option-label">
                    <input type="radio" name="answer" value="${index}">
                    <span class="option-text">${option}</span>
                </label>
            `).join('')}
        </div>
    `;
}

function startTimer() {
    const timerElement = document.getElementById('timer');
    
    setInterval(() => {
        const now = new Date();
        const elapsed = Math.floor((now - window.currentTest.startTime) / 1000);
        const hours = Math.floor(elapsed / 3600);
        const minutes = Math.floor((elapsed % 3600) / 60);
        const seconds = elapsed % 60;
        
        window.currentTest.timeTaken = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        
        if (timerElement) {
            timerElement.textContent = `Time: ${window.currentTest.timeTaken}`;
        }
    }, 1000);
}

function nextQuestion() {
    if (window.currentTest.currentQuestion < window.currentTest.questions.length - 1) {
        saveAnswer();
        window.currentTest.currentQuestion++;
        displayQuestion();
    } else {
        submitTest();
    }
}

function previousQuestion() {
    if (window.currentTest.currentQuestion > 0) {
        saveAnswer();
        window.currentTest.currentQuestion--;
        displayQuestion();
    }
}

function saveAnswer() {
    const selectedOption = document.querySelector('input[name="answer"]:checked');
    if (selectedOption) {
        const question = window.currentTest.questions[window.currentTest.currentQuestion];
        window.currentTest.answers[question.id] = parseInt(selectedOption.value);
    }
}

function submitTest() {
    saveAnswer();
    calculateScore();
    showResults();
    saveTestResults();
}

function calculateScore() {
    let correct = 0;
    window.currentTest.questions.forEach(question => {
        if (window.currentTest.answers[question.id] === question.correct) {
            correct++;
        }
    });
    window.currentTest.score = correct;
}

function showResults() {
    const testSection = document.getElementById('testSection');
    const resultsSection = document.getElementById('resultsSection');
    const resultsContent = document.getElementById('resultsContent');
    
    if (testSection) testSection.style.display = 'none';
    if (resultsSection) resultsSection.style.display = 'block';
    
    const percentage = Math.round((window.currentTest.score / window.currentTest.questions.length) * 100);
    
    if (resultsContent) {
        resultsContent.innerHTML = `
            <div class="results-summary">
                <h3>Test Completed!</h3>
                <div class="score-display">
                    <div class="score-value">${window.currentTest.score}/${window.currentTest.questions.length}</div>
                    <div class="score-percentage">${percentage}%</div>
                </div>
                <div class="test-details">
                    <p>Section: ${window.currentTest.selectedSection}</p>
                    <p>Difficulty: ${window.currentTest.selectedDifficulty}</p>
                    <p>Time Taken: ${window.currentTest.timeTaken}</p>
                </div>
                <button onclick="resetTest()" class="btn btn-primary">Take Another Test</button>
            </div>
        `;
    }
}

function saveTestResults() {
    console.log('Test results saved:', {
        score: window.currentTest.score,
        total: window.currentTest.questions.length,
        section: window.currentTest.selectedSection,
        difficulty: window.currentTest.selectedDifficulty,
        timeTaken: window.currentTest.timeTaken,
        answers: window.currentTest.answers
    });
}

function resetTest() {
    window.currentTest.currentQuestion = 0;
    window.currentTest.answers = {};
    window.currentTest.score = 0;
    window.currentTest.timeTaken = '00:00:00';
    
    const setupSection = document.getElementById('setupSection');
    const testSection = document.getElementById('testSection');
    const resultsSection = document.getElementById('resultsSection');
    
    if (setupSection) setupSection.style.display = 'block';
    if (testSection) testSection.style.display = 'none';
    if (resultsSection) resultsSection.style.display = 'none';
    
    // Reset form
    const sectionSelect = document.getElementById('sectionSelect');
    const difficultySelect = document.getElementById('difficultySelect');
    const questionCount = document.getElementById('questionCount');
    const startBtn = document.getElementById('startTestBtn');
    
    if (sectionSelect) sectionSelect.value = '';
    if (difficultySelect) difficultySelect.value = '';
    if (questionCount) questionCount.value = '';
    if (startBtn) startBtn.disabled = true;
}

function setupEventListeners() {
    const sectionSelect = document.getElementById('sectionSelect');
    const difficultySelect = document.getElementById('difficultySelect');
    const questionCount = document.getElementById('questionCount');
    const startBtn = document.getElementById('startTestBtn');
    
    function updateButtonState() {
        if (startBtn) {
            startBtn.disabled = !(sectionSelect?.value && difficultySelect?.value && questionCount?.value);
        }
    }
    
    if (sectionSelect) sectionSelect.addEventListener('change', updateButtonState);
    if (difficultySelect) difficultySelect.addEventListener('change', updateButtonState);
    if (questionCount) questionCount.addEventListener('change', updateButtonState);
    
    updateButtonState();
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
        'easy': 'Easy',
        'medium': 'Medium',
        'hard': 'Hard'
    };
    return labels[difficulty] || difficulty;
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

// Initialize the test
loadTestQuestions();

// Expose functions globally for HTML onclick handlers
window.startTest = startTest;
window.displayQuestion = displayQuestion;
window.nextQuestion = nextQuestion;
window.previousQuestion = previousQuestion;
window.submitTest = submitTest;
window.resetTest = resetTest;
 // Close the IIFE (Immediately Invoked Function Expression)