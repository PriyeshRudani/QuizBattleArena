from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Category, Question
import random


class Command(BaseCommand):
    help = 'Seeds the database with categories, questions, and demo users'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting seed process...')
        
        # Create categories
        categories_data = [
            {
                'name': 'Programming Fundamentals',
                'description': 'Core programming concepts, syntax, and basic structures'
            },
            {
                'name': 'Web Development',
                'description': 'HTML, CSS, JavaScript, and web frameworks'
            },
            {
                'name': 'Database & SQL',
                'description': 'Database design, SQL queries, and data management'
            },
            {
                'name': 'Computer Networks',
                'description': 'Networking protocols, architecture, and security'
            },
            {
                'name': 'Operating Systems',
                'description': 'OS concepts, processes, memory management'
            },
            {
                'name': 'Data Structures & Algorithms',
                'description': 'Common data structures and algorithmic paradigms'
            },
            {
                'name': 'Cybersecurity',
                'description': 'Security principles, encryption, and threats'
            },
            {
                'name': 'DevOps & Cloud',
                'description': 'CI/CD, containers, cloud platforms'
            },
            {
                'name': 'Software Engineering',
                'description': 'Design patterns, best practices, and methodologies'
            },
            {
                'name': 'Tech Trivia & Innovations',
                'description': 'Tech history, companies, and innovations'
            },
        ]
        
        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories[cat_data['name']] = category
            status = 'Created' if created else 'Already exists'
            self.stdout.write(f'{status}: {category.name}')
        
        # Clear existing questions
        Question.objects.all().delete()
        self.stdout.write('Cleared existing questions')
        
        # Generate MCQ questions
        self.create_programming_fundamentals_mcqs(categories['Programming Fundamentals'])
        self.create_web_development_mcqs(categories['Web Development'])
        self.create_database_mcqs(categories['Database & SQL'])
        self.create_networks_mcqs(categories['Computer Networks'])
        self.create_os_mcqs(categories['Operating Systems'])
        self.create_dsa_mcqs(categories['Data Structures & Algorithms'])
        self.create_security_mcqs(categories['Cybersecurity'])
        self.create_devops_mcqs(categories['DevOps & Cloud'])
        self.create_software_eng_mcqs(categories['Software Engineering'])
        self.create_tech_trivia_mcqs(categories['Tech Trivia & Innovations'])
        
        # Generate coding questions
        self.create_coding_questions(categories)
        
        # Generate quick-fire questions
        self.create_quick_fire_questions(categories)
        
        # Create demo users
        self.create_demo_users()
        
        total_questions = Question.objects.count()
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {total_questions} questions!'))

    def create_programming_fundamentals_mcqs(self, category):
        questions = [
            {
                'title': 'What is a variable?',
                'question_text': 'In programming, what is a variable?',
                'options': ['A storage location with a name', 'A constant value', 'A function', 'A loop'],
                'correct_option': 0,
                'difficulty': 'EASY',
                'points': 10,
                'explanation': 'A variable is a named storage location in memory that can hold values.'
            },
            {
                'title': 'Python List Indexing',
                'question_text': 'In Python, what does list[-1] return?',
                'options': ['The first element', 'The last element', 'An error', 'None'],
                'correct_option': 1,
                'difficulty': 'EASY',
                'points': 10,
                'explanation': 'Negative indexing in Python starts from the end, with -1 being the last element.'
            },
            {
                'title': 'Loop Output',
                'question_text': 'What will this Python code output?\n\n```python\nfor i in range(3):\n    print(i)\n```',
                'options': ['0 1 2', '1 2 3', '0 1 2 3', '1 2'],
                'correct_option': 0,
                'difficulty': 'EASY',
                'points': 10,
                'explanation': 'range(3) generates numbers from 0 to 2 (3 is excluded).'
            },
            {
                'title': 'Data Types',
                'question_text': 'Which of these is NOT a primitive data type in most languages?',
                'options': ['Integer', 'Boolean', 'String', 'Array'],
                'correct_option': 3,
                'difficulty': 'MEDIUM',
                'points': 15,
                'explanation': 'Arrays are composite/collection types, not primitives. Primitives are basic single values.'
            },
            {
                'title': 'Function Return',
                'question_text': 'What does a function without a return statement return in Python?',
                'options': ['0', 'None', 'False', 'Empty string'],
                'correct_option': 1,
                'difficulty': 'EASY',
                'points': 10,
                'explanation': 'Python functions without explicit return statements return None by default.'
            },
            {
                'title': 'String Immutability',
                'question_text': 'In Python, strings are:',
                'options': ['Mutable', 'Immutable', 'Sometimes mutable', 'Dynamic'],
                'correct_option': 1,
                'difficulty': 'MEDIUM',
                'points': 15,
                'explanation': 'Python strings are immutable - they cannot be changed after creation.'
            },
            {
                'title': 'Dictionary Keys',
                'question_text': 'In Python, which of these CANNOT be used as dictionary keys?',
                'options': ['Strings', 'Tuples', 'Lists', 'Integers'],
                'correct_option': 2,
                'difficulty': 'MEDIUM',
                'points': 15,
                'explanation': 'Dictionary keys must be immutable. Lists are mutable, so they cannot be keys.'
            },
            {
                'title': 'Exception Handling',
                'question_text': 'What keyword is used to handle exceptions in Python?',
                'options': ['catch', 'except', 'handle', 'rescue'],
                'correct_option': 1,
                'difficulty': 'EASY',
                'points': 10,
                'explanation': 'Python uses try-except blocks for exception handling.'
            },
            {
                'title': 'List Comprehension',
                'question_text': 'What does [x*2 for x in range(3)] produce in Python?',
                'options': ['[0, 2, 4]', '[2, 4, 6]', '[0, 1, 2]', '[1, 2, 3]'],
                'correct_option': 0,
                'difficulty': 'MEDIUM',
                'points': 15,
                'explanation': 'List comprehension multiplies each value in range(3) [0,1,2] by 2.'
            },
            {
                'title': 'OOP Inheritance',
                'question_text': 'In OOP, inheritance allows:',
                'options': ['Code reuse', 'Polymorphism', 'Encapsulation', 'All of the above'],
                'correct_option': 3,
                'difficulty': 'MEDIUM',
                'points': 15,
                'explanation': 'Inheritance enables code reuse, supports polymorphism, and works with encapsulation.'
            },
        ]
        
        # Add more to reach 30
        easy_questions = 20
        medium_questions = 7
        hard_questions = 3
        
        for i in range(easy_questions - len([q for q in questions if q['difficulty'] == 'EASY'])):
            questions.append({
                'title': f'Programming Fundamentals Q{len(questions)+1}',
                'question_text': f'What is the purpose of a {random.choice(["loop", "function", "class", "module"])}?',
                'options': ['To organize code', 'To repeat code', 'To store data', 'All of these'],
                'correct_option': random.randint(0, 3),
                'difficulty': 'EASY',
                'points': 10,
                'explanation': 'This depends on the specific programming construct.'
            })
        
        for question_data in questions:
            Question.objects.create(
                category=category,
                question_type='MCQ',
                language='PYTHON',
                **question_data
            )
        
        self.stdout.write(f'Created {len(questions)} Programming Fundamentals MCQs')

    def create_web_development_mcqs(self, category):
        questions = [
            {
                'title': 'HTML Heading Tag',
                'question_text': 'Which HTML tag is used for the largest heading?',
                'options': ['<h6>', '<h1>', '<head>', '<header>'],
                'correct_option': 1,
                'difficulty': 'EASY',
                'points': 10,
                'explanation': '<h1> is the largest heading, <h6> is the smallest.'
            },
            {
                'title': 'CSS Box Model',
                'question_text': 'What is the correct order of the CSS box model from inside out?',
                'options': ['Content, Padding, Border, Margin', 'Margin, Border, Padding, Content', 'Content, Margin, Padding, Border', 'Padding, Content, Border, Margin'],
                'correct_option': 0,
                'difficulty': 'MEDIUM',
                'points': 15,
                'explanation': 'The CSS box model layers are: Content → Padding → Border → Margin.'
            },
            {
                'title': 'JavaScript Variable Declaration',
                'question_text': 'Which keyword creates a block-scoped variable in JavaScript?',
                'options': ['var', 'let', 'const', 'Both let and const'],
                'correct_option': 3,
                'difficulty': 'MEDIUM',
                'points': 15,
                'explanation': 'Both let and const create block-scoped variables, unlike var which is function-scoped.'
            },
            {
                'title': 'React Component',
                'question_text': 'In React, what is JSX?',
                'options': ['A JavaScript extension', 'A syntax extension for JavaScript', 'A templating language', 'A CSS preprocessor'],
                'correct_option': 1,
                'difficulty': 'MEDIUM',
                'points': 15,
                'explanation': 'JSX is a syntax extension for JavaScript that looks like HTML.'
            },
            {
                'title': 'HTTP Status Code',
                'question_text': 'What does HTTP status code 404 mean?',
                'options': ['Server error', 'Not found', 'Unauthorized', 'Success'],
                'correct_option': 1,
                'difficulty': 'EASY',
                'points': 10,
                'explanation': '404 means the requested resource was not found on the server.'
            },
        ]
        
        for i in range(25):
            questions.append({
                'title': f'Web Development Q{len(questions)+1}',
                'question_text': f'What is the purpose of {random.choice(["CSS", "HTML", "JavaScript", "React"])}?',
                'options': ['Styling', 'Structure', 'Behavior', 'Framework'],
                'correct_option': random.randint(0, 3),
                'difficulty': random.choice(['EASY', 'MEDIUM', 'HARD']),
                'points': random.choice([10, 15, 20]),
                'explanation': 'This tests knowledge of web technologies.'
            })
        
        for question_data in questions:
            Question.objects.create(
                category=category,
                question_type='MCQ',
                language='JAVASCRIPT',
                **question_data
            )
        
        self.stdout.write(f'Created {len(questions)} Web Development MCQs')

    def create_database_mcqs(self, category):
        questions = [
            {
                'title': 'SQL SELECT Statement',
                'question_text': 'Which SQL clause is used to filter results?',
                'options': ['WHERE', 'FILTER', 'HAVING', 'IF'],
                'correct_option': 0,
                'difficulty': 'EASY',
                'points': 10,
                'explanation': 'WHERE clause filters rows before grouping, HAVING filters after.'
            },
            {
                'title': 'Database Normalization',
                'question_text': 'What is the main goal of database normalization?',
                'options': ['Reduce redundancy', 'Increase speed', 'Add more tables', 'Remove indexes'],
                'correct_option': 0,
                'difficulty': 'MEDIUM',
                'points': 15,
                'explanation': 'Normalization reduces data redundancy and improves data integrity.'
            },
            {
                'title': 'JOIN Types',
                'question_text': 'Which JOIN returns all records from both tables?',
                'options': ['INNER JOIN', 'LEFT JOIN', 'RIGHT JOIN', 'FULL OUTER JOIN'],
                'correct_option': 3,
                'difficulty': 'MEDIUM',
                'points': 15,
                'explanation': 'FULL OUTER JOIN returns all records from both tables, matching when possible.'
            },
        ]
        
        for i in range(27):
            questions.append({
                'title': f'Database Q{len(questions)+1}',
                'question_text': f'What is {random.choice(["a primary key", "a foreign key", "an index", "a transaction"])}?',
                'options': ['Unique identifier', 'Reference to another table', 'Performance optimization', 'Group of operations'],
                'correct_option': random.randint(0, 3),
                'difficulty': random.choice(['EASY', 'MEDIUM', 'HARD']),
                'points': random.choice([10, 15, 20]),
                'explanation': 'This tests database concepts.'
            })
        
        for question_data in questions:
            Question.objects.create(
                category=category,
                question_type='MCQ',
                language='GENERAL',
                **question_data
            )
        
        self.stdout.write(f'Created {len(questions)} Database MCQs')

    def create_networks_mcqs(self, category):
        questions = [
            {
                'title': 'OSI Model Layers',
                'question_text': 'How many layers are in the OSI model?',
                'options': ['5', '6', '7', '8'],
                'correct_option': 2,
                'difficulty': 'EASY',
                'points': 10,
                'explanation': 'The OSI model has 7 layers from Physical to Application.'
            },
            {
                'title': 'TCP vs UDP',
                'question_text': 'Which protocol is connection-oriented?',
                'options': ['UDP', 'TCP', 'Both', 'Neither'],
                'correct_option': 1,
                'difficulty': 'EASY',
                'points': 10,
                'explanation': 'TCP is connection-oriented and ensures reliable delivery.'
            },
        ]
        
        for i in range(28):
            questions.append({
                'title': f'Networks Q{len(questions)+1}',
                'question_text': f'What is {random.choice(["IP address", "DNS", "HTTP", "Router"])}?',
                'options': ['Network identifier', 'Name resolution', 'Protocol', 'Network device'],
                'correct_option': random.randint(0, 3),
                'difficulty': random.choice(['EASY', 'MEDIUM', 'HARD']),
                'points': random.choice([10, 15, 20]),
                'explanation': 'This tests networking knowledge.'
            })
        
        for question_data in questions:
            Question.objects.create(
                category=category,
                question_type='MCQ',
                language='GENERAL',
                **question_data
            )
        
        self.stdout.write(f'Created {len(questions)} Computer Networks MCQs')

    def create_os_mcqs(self, category):
        questions = [
            {
                'title': 'Process vs Thread',
                'question_text': 'What is the main difference between a process and a thread?',
                'options': ['Threads share memory, processes don\'t', 'Processes are faster', 'Threads use more memory', 'No difference'],
                'correct_option': 0,
                'difficulty': 'MEDIUM',
                'points': 15,
                'explanation': 'Threads within a process share the same memory space.'
            },
        ]
        
        for i in range(29):
            questions.append({
                'title': f'OS Q{len(questions)+1}',
                'question_text': f'What is {random.choice(["virtual memory", "scheduling", "deadlock", "semaphore"])}?',
                'options': ['Memory management', 'Process management', 'Synchronization issue', 'Synchronization primitive'],
                'correct_option': random.randint(0, 3),
                'difficulty': random.choice(['EASY', 'MEDIUM', 'HARD']),
                'points': random.choice([10, 15, 20]),
                'explanation': 'This tests OS concepts.'
            })
        
        for question_data in questions:
            Question.objects.create(
                category=category,
                question_type='MCQ',
                language='GENERAL',
                **question_data
            )
        
        self.stdout.write(f'Created {len(questions)} Operating Systems MCQs')

    def create_dsa_mcqs(self, category):
        questions = [
            {
                'title': 'Big O Complexity',
                'question_text': 'What is the time complexity of binary search?',
                'options': ['O(n)', 'O(log n)', 'O(n log n)', 'O(1)'],
                'correct_option': 1,
                'difficulty': 'MEDIUM',
                'points': 15,
                'explanation': 'Binary search divides the search space in half each iteration: O(log n).'
            },
            {
                'title': 'Stack Operation',
                'question_text': 'Which principle does a stack follow?',
                'options': ['FIFO', 'LIFO', 'Random', 'Priority'],
                'correct_option': 1,
                'difficulty': 'EASY',
                'points': 10,
                'explanation': 'Stack follows Last In First Out (LIFO) principle.'
            },
        ]
        
        for i in range(28):
            questions.append({
                'title': f'DSA Q{len(questions)+1}',
                'question_text': f'What is the complexity of {random.choice(["insertion sort", "merge sort", "hash table lookup", "array access"])}?',
                'options': ['O(1)', 'O(log n)', 'O(n)', 'O(n²)'],
                'correct_option': random.randint(0, 3),
                'difficulty': random.choice(['EASY', 'MEDIUM', 'HARD']),
                'points': random.choice([10, 15, 20]),
                'explanation': 'This tests algorithm complexity knowledge.'
            })
        
        for question_data in questions:
            Question.objects.create(
                category=category,
                question_type='MCQ',
                language='GENERAL',
                **question_data
            )
        
        self.stdout.write(f'Created {len(questions)} DSA MCQs')

    def create_security_mcqs(self, category):
        questions = [
            {
                'title': 'Encryption Types',
                'question_text': 'Which encryption uses the same key for encryption and decryption?',
                'options': ['Asymmetric', 'Symmetric', 'Hashing', 'Public key'],
                'correct_option': 1,
                'difficulty': 'MEDIUM',
                'points': 15,
                'explanation': 'Symmetric encryption uses the same key for both operations.'
            },
        ]
        
        for i in range(29):
            questions.append({
                'title': f'Security Q{len(questions)+1}',
                'question_text': f'What is {random.choice(["SQL injection", "XSS", "CSRF", "encryption"])}?',
                'options': ['Attack vector', 'Security measure', 'Protocol', 'Algorithm'],
                'correct_option': random.randint(0, 3),
                'difficulty': random.choice(['EASY', 'MEDIUM', 'HARD']),
                'points': random.choice([10, 15, 20]),
                'explanation': 'This tests cybersecurity knowledge.'
            })
        
        for question_data in questions:
            Question.objects.create(
                category=category,
                question_type='MCQ',
                language='GENERAL',
                **question_data
            )
        
        self.stdout.write(f'Created {len(questions)} Cybersecurity MCQs')

    def create_devops_mcqs(self, category):
        questions = [
            {
                'title': 'Docker Container',
                'question_text': 'What is a Docker container?',
                'options': ['A virtual machine', 'A lightweight executable package', 'An image', 'A registry'],
                'correct_option': 1,
                'difficulty': 'MEDIUM',
                'points': 15,
                'explanation': 'Containers are lightweight packages that include application code and dependencies.'
            },
        ]
        
        for i in range(29):
            questions.append({
                'title': f'DevOps Q{len(questions)+1}',
                'question_text': f'What is {random.choice(["CI/CD", "Kubernetes", "Docker", "Jenkins"])}?',
                'options': ['Automation practice', 'Orchestration tool', 'Container platform', 'CI/CD tool'],
                'correct_option': random.randint(0, 3),
                'difficulty': random.choice(['EASY', 'MEDIUM', 'HARD']),
                'points': random.choice([10, 15, 20]),
                'explanation': 'This tests DevOps knowledge.'
            })
        
        for question_data in questions:
            Question.objects.create(
                category=category,
                question_type='MCQ',
                language='GENERAL',
                **question_data
            )
        
        self.stdout.write(f'Created {len(questions)} DevOps MCQs')

    def create_software_eng_mcqs(self, category):
        questions = [
            {
                'title': 'Agile Methodology',
                'question_text': 'What is a sprint in Agile?',
                'options': ['A race', 'A time-boxed iteration', 'A meeting', 'A deliverable'],
                'correct_option': 1,
                'difficulty': 'EASY',
                'points': 10,
                'explanation': 'A sprint is a time-boxed period (usually 2-4 weeks) for development work.'
            },
        ]
        
        for i in range(29):
            questions.append({
                'title': f'Software Eng Q{len(questions)+1}',
                'question_text': f'What is {random.choice(["SOLID", "DRY", "KISS", "YAGNI"])}?',
                'options': ['Design principle', 'Programming language', 'Framework', 'Tool'],
                'correct_option': 0,
                'difficulty': random.choice(['EASY', 'MEDIUM', 'HARD']),
                'points': random.choice([10, 15, 20]),
                'explanation': 'These are all software engineering principles.'
            })
        
        for question_data in questions:
            Question.objects.create(
                category=category,
                question_type='MCQ',
                language='GENERAL',
                **question_data
            )
        
        self.stdout.write(f'Created {len(questions)} Software Engineering MCQs')

    def create_tech_trivia_mcqs(self, category):
        questions = [
            {
                'title': 'Python Creation',
                'question_text': 'Who created Python?',
                'options': ['Linus Torvalds', 'Guido van Rossum', 'James Gosling', 'Dennis Ritchie'],
                'correct_option': 1,
                'difficulty': 'EASY',
                'points': 10,
                'explanation': 'Guido van Rossum created Python in 1991.'
            },
            {
                'title': 'Git Creator',
                'question_text': 'Who created Git?',
                'options': ['Linus Torvalds', 'Guido van Rossum', 'Brendan Eich', 'Tim Berners-Lee'],
                'correct_option': 0,
                'difficulty': 'EASY',
                'points': 10,
                'explanation': 'Linus Torvalds created Git in 2005 for Linux kernel development.'
            },
        ]
        
        for i in range(28):
            questions.append({
                'title': f'Tech Trivia Q{len(questions)+1}',
                'question_text': f'When was {random.choice(["JavaScript", "Java", "Python", "C++"])} created?',
                'options': ['1990s', '1980s', '2000s', '1970s'],
                'correct_option': random.randint(0, 3),
                'difficulty': random.choice(['EASY', 'MEDIUM']),
                'points': random.choice([10, 15]),
                'explanation': 'This tests tech history knowledge.'
            })
        
        for question_data in questions:
            Question.objects.create(
                category=category,
                question_type='MCQ',
                language='GENERAL',
                **question_data
            )
        
        self.stdout.write(f'Created {len(questions)} Tech Trivia MCQs')

    def create_coding_questions(self, categories):
        coding_questions = [
            {
                'category': categories['Programming Fundamentals'],
                'title': 'FizzBuzz Function',
                'question_text': 'Write a function that returns "Fizz" for multiples of 3, "Buzz" for multiples of 5, "FizzBuzz" for multiples of both, or the number as a string otherwise.',
                'solution_code': 'def fizzbuzz(n):\n    if n % 15 == 0:\n        return "FizzBuzz"\n    elif n % 3 == 0:\n        return "Fizz"\n    elif n % 5 == 0:\n        return "Buzz"\n    else:\n        return str(n)',
                'difficulty': 'EASY',
                'points': 20,
                'language': 'PYTHON'
            },
            {
                'category': categories['Data Structures & Algorithms'],
                'title': 'Reverse a String',
                'question_text': 'Write a function to reverse a string.',
                'solution_code': 'def reverse_string(s):\n    return s[::-1]',
                'difficulty': 'EASY',
                'points': 15,
                'language': 'PYTHON'
            },
            {
                'category': categories['Data Structures & Algorithms'],
                'title': 'Find Maximum in Array',
                'question_text': 'Write a function to find the maximum value in an array.',
                'solution_code': 'def find_max(arr):\n    return max(arr)',
                'difficulty': 'EASY',
                'points': 15,
                'language': 'PYTHON'
            },
        ]
        
        # Add more coding questions with meaningful problems
        additional_coding_problems = [
            ('Sum of Array Elements', 'Write a function that takes an array of numbers and returns their sum.', 'EASY', 20),
            ('Check Prime Number', 'Write a function that checks if a given number is prime. Return True if prime, False otherwise.', 'MEDIUM', 25),
            ('Palindrome Checker', 'Write a function that checks if a given string is a palindrome (reads the same forwards and backwards).', 'EASY', 20),
            ('Count Vowels', 'Write a function that counts the number of vowels (a, e, i, o, u) in a given string.', 'EASY', 20),
            ('Factorial Calculator', 'Write a recursive function to calculate the factorial of a number n (n!).', 'MEDIUM', 25),
            ('Fibonacci Sequence', 'Write a function that returns the nth number in the Fibonacci sequence (0, 1, 1, 2, 3, 5, 8...).', 'MEDIUM', 25),
            ('Remove Duplicates', 'Write a function that removes duplicate values from an array while maintaining order.', 'MEDIUM', 25),
            ('Binary Search', 'Implement binary search to find the index of a target value in a sorted array.', 'HARD', 30),
            ('Merge Two Sorted Arrays', 'Write a function that merges two sorted arrays into one sorted array.', 'MEDIUM', 25),
            ('Anagram Checker', 'Write a function that checks if two strings are anagrams of each other.', 'MEDIUM', 25),
            ('First Non-Repeating Character', 'Find the first non-repeating character in a string. Return the character or null if none exists.', 'MEDIUM', 25),
            ('Valid Parentheses', 'Check if a string containing only parentheses (), {}, [] is valid (properly opened and closed).', 'HARD', 30),
            ('Two Sum Problem', 'Find two numbers in an array that add up to a specific target. Return their indices.', 'MEDIUM', 25),
            ('Longest Common Prefix', 'Find the longest common prefix string amongst an array of strings.', 'MEDIUM', 25),
            ('Count Words in String', 'Write a function that counts the number of words in a given string.', 'EASY', 20),
            ('Reverse Words in String', 'Reverse the order of words in a sentence while keeping word spelling intact.', 'MEDIUM', 25),
            ('Find Missing Number', 'Given an array containing n distinct numbers from 0 to n, find the missing number.', 'MEDIUM', 25),
            ('Bubble Sort', 'Implement the bubble sort algorithm to sort an array in ascending order.', 'MEDIUM', 25),
            ('Linear Search', 'Implement linear search to find the index of a value in an array. Return -1 if not found.', 'EASY', 20),
            ('Calculate Average', 'Write a function that calculates the average of numbers in an array.', 'EASY', 20),
            ('String to Integer', 'Convert a string to an integer, handling edge cases like leading/trailing spaces and signs.', 'MEDIUM', 25),
            ('Remove Element', 'Remove all instances of a specific value from an array in-place and return the new length.', 'EASY', 20),
            ('Plus One', 'Given an array representing a non-negative integer, add one to it and return the resulting array.', 'MEDIUM', 25),
            ('Valid Palindrome', 'Check if a string is a palindrome, considering only alphanumeric characters and ignoring cases.', 'MEDIUM', 25),
            ('Implement Stack', 'Implement a basic stack data structure with push, pop, peek, and isEmpty methods.', 'HARD', 30),
            ('Implement Queue', 'Implement a basic queue data structure with enqueue, dequeue, front, and isEmpty methods.', 'HARD', 30),
            ('Rotate Array', 'Rotate an array to the right by k steps, where k is non-negative.', 'MEDIUM', 25),
        ]
        
        for i, (title, problem, difficulty, points) in enumerate(additional_coding_problems):
            cat_name = random.choice(['Programming Fundamentals', 'Data Structures & Algorithms', 'Web Development'])
            languages = ['PYTHON', 'JAVASCRIPT', 'JAVA']
            coding_questions.append({
                'category': categories[cat_name],
                'title': title,
                'question_text': problem,
                'solution_code': f'# Solution for {title}\ndef solution():\n    # Implement your solution here\n    pass',
                'difficulty': difficulty,
                'points': points,
                'language': random.choice(languages)
            })
        
        for q in coding_questions:
            Question.objects.create(
                question_type='CODE',
                explanation='Check if your solution handles all edge cases.',
                **q
            )
        
        self.stdout.write(f'Created {len(coding_questions)} Coding questions')

    def create_quick_fire_questions(self, categories):
        quick_questions = [
            {
                'category': categories['Programming Fundamentals'],
                'title': 'Python is interpreted',
                'question_text': 'True or False: Python is an interpreted language.',
                'correct_answer': 'true',
                'difficulty': 'EASY',
                'points': 5
            },
            {
                'category': categories['Web Development'],
                'title': 'HTML is a programming language',
                'question_text': 'True or False: HTML is a programming language.',
                'correct_answer': 'false',
                'difficulty': 'EASY',
                'points': 5
            },
            {
                'category': categories['Database & SQL'],
                'title': 'SQL is case sensitive',
                'question_text': 'True or False: SQL keywords are case sensitive.',
                'correct_answer': 'false',
                'difficulty': 'MEDIUM',
                'points': 8
            },
        ]
        
        # Add more meaningful quick-fire questions
        additional_quick_questions = [
            ('JavaScript is compiled', 'True or False: JavaScript is a compiled language.', 'false', 'EASY', 5, 'Programming Fundamentals'),
            ('CSS stands for', 'True or False: CSS stands for Computer Style Sheets.', 'false', 'EASY', 5, 'Web Development'),
            ('REST uses HTTP', 'True or False: REST APIs typically use HTTP methods.', 'true', 'MEDIUM', 8, 'Web Development'),
            ('Binary has two digits', 'True or False: Binary number system uses only 0 and 1.', 'true', 'EASY', 5, 'Programming Fundamentals'),
            ('Arrays are mutable in JS', 'True or False: Arrays in JavaScript are mutable.', 'true', 'EASY', 5, 'Web Development'),
            ('TCP is connectionless', 'True or False: TCP is a connectionless protocol.', 'false', 'MEDIUM', 8, 'Computer Networks'),
            ('NoSQL uses SQL', 'True or False: NoSQL databases use SQL for queries.', 'false', 'MEDIUM', 8, 'Database & SQL'),
            ('HTTPS is secure', 'True or False: HTTPS provides encrypted communication.', 'true', 'EASY', 5, 'Cybersecurity'),
            ('Git is centralized', 'True or False: Git is a centralized version control system.', 'false', 'MEDIUM', 8, 'DevOps & Cloud'),
            ('RAM is volatile', 'True or False: RAM (Random Access Memory) is volatile memory.', 'true', 'EASY', 5, 'Operating Systems'),
            ('Stack is LIFO', 'True or False: Stack follows Last In First Out (LIFO) principle.', 'true', 'EASY', 5, 'Data Structures & Algorithms'),
            ('Linux is open source', 'True or False: Linux is an open-source operating system.', 'true', 'EASY', 5, 'Operating Systems'),
            ('VPN encrypts data', 'True or False: VPN (Virtual Private Network) encrypts your internet traffic.', 'true', 'EASY', 5, 'Cybersecurity'),
            ('Docker uses VMs', 'True or False: Docker containers are the same as virtual machines.', 'false', 'MEDIUM', 8, 'DevOps & Cloud'),
            ('JSON is XML', 'True or False: JSON and XML are the same data format.', 'false', 'EASY', 5, 'Web Development'),
            ('Big O measures time', 'True or False: Big O notation only measures time complexity.', 'false', 'MEDIUM', 8, 'Data Structures & Algorithms'),
            ('Firewall blocks attacks', 'True or False: A firewall can block all cyber attacks.', 'false', 'MEDIUM', 8, 'Cybersecurity'),
            ('Agile is iterative', 'True or False: Agile is an iterative development methodology.', 'true', 'EASY', 5, 'Software Engineering'),
            ('DNS resolves domains', 'True or False: DNS converts domain names to IP addresses.', 'true', 'EASY', 5, 'Computer Networks'),
            ('MongoDB is relational', 'True or False: MongoDB is a relational database.', 'false', 'EASY', 5, 'Database & SQL'),
            ('API is interface', 'True or False: API stands for Application Programming Interface.', 'true', 'EASY', 5, 'Software Engineering'),
            ('Python uses GIL', 'True or False: Python has a Global Interpreter Lock (GIL).', 'true', 'MEDIUM', 8, 'Programming Fundamentals'),
            ('IPv6 replaces IPv4', 'True or False: IPv6 was created to replace IPv4.', 'true', 'EASY', 5, 'Computer Networks'),
            ('Encryption is hashing', 'True or False: Encryption and hashing are the same thing.', 'false', 'MEDIUM', 8, 'Cybersecurity'),
            ('CI/CD automates', 'True or False: CI/CD automates software deployment.', 'true', 'EASY', 5, 'DevOps & Cloud'),
            ('Queue is FIFO', 'True or False: Queue follows First In First Out (FIFO) principle.', 'true', 'EASY', 5, 'Data Structures & Algorithms'),
            ('SQL is declarative', 'True or False: SQL is a declarative programming language.', 'true', 'MEDIUM', 8, 'Database & SQL'),
            ('Localhost is 127', 'True or False: localhost refers to IP address 127.0.0.1.', 'true', 'EASY', 5, 'Computer Networks'),
            ('Bitcoin uses blockchain', 'True or False: Bitcoin technology uses blockchain.', 'true', 'EASY', 5, 'Tech Trivia & Innovations'),
            ('AI needs big data', 'True or False: All AI systems require massive amounts of data.', 'false', 'MEDIUM', 8, 'Tech Trivia & Innovations'),
            ('OAuth for auth', 'True or False: OAuth is an authorization protocol, not authentication.', 'true', 'MEDIUM', 8, 'Cybersecurity'),
            ('Kubernetes orchestrates', 'True or False: Kubernetes is a container orchestration platform.', 'true', 'EASY', 5, 'DevOps & Cloud'),
            ('Scrum has sprints', 'True or False: Scrum methodology uses time-boxed sprints.', 'true', 'EASY', 5, 'Software Engineering'),
            ('Cache improves speed', 'True or False: Caching can improve application performance.', 'true', 'EASY', 5, 'Software Engineering'),
            ('DDoS is attack', 'True or False: DDoS stands for Distributed Denial of Service attack.', 'true', 'EASY', 5, 'Cybersecurity'),
            ('AWS is IaaS', 'True or False: AWS provides Infrastructure as a Service (IaaS).', 'true', 'EASY', 5, 'DevOps & Cloud'),
            ('Binary tree two children', 'True or False: Every node in a binary tree must have exactly two children.', 'false', 'MEDIUM', 8, 'Data Structures & Algorithms'),
            ('HTTP is stateless', 'True or False: HTTP is a stateless protocol.', 'true', 'EASY', 5, 'Web Development'),
            ('OOP has inheritance', 'True or False: Inheritance is a core principle of Object-Oriented Programming.', 'true', 'EASY', 5, 'Programming Fundamentals'),
            ('Unit tests test units', 'True or False: Unit tests should test individual components in isolation.', 'true', 'EASY', 5, 'Software Engineering'),
            ('Deadlock requires four', 'True or False: Deadlock requires four necessary conditions to occur.', 'true', 'MEDIUM', 8, 'Operating Systems'),
            ('API REST POST create', 'True or False: In REST APIs, POST method is typically used to create resources.', 'true', 'EASY', 5, 'Web Development'),
            ('Hash table O(1)', 'True or False: Hash tables provide O(1) average time complexity for lookups.', 'true', 'MEDIUM', 8, 'Data Structures & Algorithms'),
            ('SQL injection SQLi', 'True or False: SQL injection is a type of web security vulnerability.', 'true', 'EASY', 5, 'Cybersecurity'),
            ('Cloud cheaper always', 'True or False: Cloud computing is always cheaper than on-premise infrastructure.', 'false', 'MEDIUM', 8, 'DevOps & Cloud'),
            ('Moore law doubles', 'True or False: Moore\'s Law states transistor count doubles every two years.', 'true', 'EASY', 5, 'Tech Trivia & Innovations'),
            ('Polymorphism OOP', 'True or False: Polymorphism allows objects of different types to be treated uniformly.', 'true', 'MEDIUM', 8, 'Programming Fundamentals'),
        ]
        
        for title, text, answer, difficulty, points, cat_name in additional_quick_questions:
            quick_questions.append({
                'category': categories[cat_name],
                'title': title,
                'question_text': text,
                'correct_answer': answer,
                'difficulty': difficulty,
                'points': points
            })
        
        for q in quick_questions:
            Question.objects.create(
                question_type='QUICK',
                language='GENERAL',
                explanation='Quick-fire questions test your immediate knowledge.',
                **q
            )
        
        self.stdout.write(f'Created {len(quick_questions)} Quick-fire questions')

    def create_demo_users(self):
        users_data = [
            {'username': 'alice_coder', 'email': 'alice@example.com', 'password': 'demo1234', 'points': 1500},
            {'username': 'bob_dev', 'email': 'bob@example.com', 'password': 'demo1234', 'points': 1200},
            {'username': 'charlie_eng', 'email': 'charlie@example.com', 'password': 'demo1234', 'points': 900},
            {'username': 'diana_prog', 'email': 'diana@example.com', 'password': 'demo1234', 'points': 600},
            {'username': 'eve_tech', 'email': 'eve@example.com', 'password': 'demo1234', 'points': 300},
        ]
        
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                }
            )
            if created:
                user.set_password(user_data['password'])
                user.save()
                user.profile.total_points = user_data['points']
                user.profile.save()
                self.stdout.write(f'Created demo user: {user.username}')
            else:
                self.stdout.write(f'Demo user already exists: {user.username}')
