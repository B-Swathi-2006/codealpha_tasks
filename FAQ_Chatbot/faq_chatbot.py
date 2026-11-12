from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

faqs = {
    "what is python":
        "Python is a beginner-friendly programming language used for web development, AI, automation and data science.",

    "what are the features of python":
        "Python is easy to learn, interpreted, object-oriented, portable and supports many libraries.",

    "what is artificial intelligence":
        "Artificial Intelligence enables computers to perform tasks that normally require human intelligence.",

    "what is machine learning":
        "Machine Learning allows computers to learn patterns from data and make predictions.",

    "what is deep learning":
        "Deep Learning is a part of Machine Learning that uses neural networks with multiple layers.",

    "what is nlp(natural language processing)":
        "NLP helps computers understand, process and work with human language.",

    "what is a chatbot":
        "A chatbot is a software application that communicates with users through text or voice.",

    "what is programming":
        "Programming is the process of writing instructions that tell a computer what to do.",

    "what is html":
        "HTML stands for HyperText Markup Language. It is used to create the structure of web pages.",

    "what is css":
        "CSS stands for Cascading Style Sheets. It is used to style and design web pages.",

    "what is javascript":
        "JavaScript is a programming language used to make web pages interactive.",

    "what is flask":
        "Flask is a lightweight Python web framework used to build web applications.",

    "what is a database":
        "A database is an organized collection of data that can be stored, accessed and managed.",

    "what is dbms":
        "DBMS stands for Database Management System. It helps users create and manage databases.",

    "what is an algorithm":
        "An algorithm is a step-by-step procedure used to solve a particular problem.",

    "what is data structure":
        "A data structure is a way of organizing and storing data efficiently.",

    "what is tensorflow":
        "TensorFlow is an open-source library used for machine learning and deep learning.",

    "what is overfitting":
        "Overfitting occurs when a machine learning model learns training data too closely and performs poorly on new data.",

    "what is supervised learning":
        "Supervised learning trains a model using labelled data.",

    "what is unsupervised learning":
        "Unsupervised learning finds patterns in data without labelled outputs."
}

greetings = {
    "hi": "Hello! 👋 How can I help you today?",
    "hello": "Hey there! 😊 What would you like to know?",
    "hey": "Hey! Ask me anything about programming, AI or technology.",
    "good morning": "Good morning! ☀️ How can I assist you?",
    "good afternoon": "Good afternoon! How can I help you?",
    "good evening": "Good evening! 😊 What would you like to learn?",
    "bye": "Goodbye! Have a great day! 👋",
    "thank you": "You're welcome! Happy to help. 😊",
    "thanks": "You're welcome!"
}

questions = list(faqs.keys())

vectorizer = TfidfVectorizer(stop_words="english")
faq_vectors = vectorizer.fit_transform(questions)


def get_answer(user_question):

    user_question = user_question.strip().lower()

    if not user_question:
        return "Please enter a question."

    # Check greetings first
    if user_question in greetings:
        return greetings[user_question]

    # NLP question matching
    user_vector = vectorizer.transform([user_question])

    scores = cosine_similarity(user_vector, faq_vectors)[0]

    best_index = scores.argmax()
    best_score = scores[best_index]

    if best_score >= 0.30:
        matched_question = questions[best_index]
        return faqs[matched_question]

    return "Sorry, I couldn't find a suitable answer. Try asking about Python, AI, Machine Learning, DBMS or programming."
