from packages.imports import *

openai.api_key = "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"
model = "gpt-3.5-turbo-instruct"

base_languages = {
    "spanish": {"flag": "🇪🇸",
                "description": "Embrace Spanish & Hispanic cultures from Spain's flamenco rhythms to Mexico's Día de los Muertos."},
    "french": {"flag": "🇫🇷",
               "description": "Embrace the charm of French culture, from the elegant streets of Paris to the romance of the French Riviera."},
    "mandarin": {"flag": "🇨🇳",
                 "description": "Unlock the beauty of Mandarin, delving into China's rich history and exploring its vibrant modern cities."},
    "russian": {"flag": "🇷🇺",
                "description": "Immerse yourself in Russian culture, from the grandeur of Moscow's architecture to the warmth of its people."},
    "arabic": {"flag": "🇦🇪",
               "description": "Discover the allure of Arabic, unveiling the mystique of the Middle East and its captivating traditions."},
    "hindi": {"flag": "🇮🇳",
              "description": "Embrace the vibrancy of Hindi, opening the door to India's diverse cultures and colorful festivities."},
    "portuguese": {"flag": "🇵🇹",
                   "description": "Explore the Portuguese charm, from the captivating streets of Lisbon to the lush landscapes of Brazil."},
    "japanese": {"flag": "🇯🇵",
                 "description": "Unlock the wonders of Japanese tradition, from the tranquility of tea ceremonies to the modern energy of Tokyo."},
    "korean": {"flag": "🇰🇷",
               "description": "Immerse yourself in Korean innovation, experiencing the dynamism of South Korea's thriving culture."},
}


def logged_in(f):
    @wraps(f)
    def validator(*args, **kwargs):
        if flask.session.get("email"):
            return f(*args, **kwargs)
        else:
            return flask.redirect("/")

    return validator


# FORMATTER
def response_formatter(stdin):
    pattern = r'\[(.*?)\]'
    question_answer_pairs = re.findall(pattern, stdin)

    converted_list = []
    for pair in question_answer_pairs:
        question, *answers = pair.split(',')

        sublist = [question.strip()]
        sublist.extend(answer.strip() for answer in answers)

        converted_list.append(sublist)

    return converted_list


# CHATBOT
def chatbot(text, language):
    context = '''
    The following prompt will be someone speaking in ''' + language + '''. Respond in the language they're speaking in. Keep in mind they are practicing to speak the language.
    '''

    response = openai.Completion.create(engine=model, prompt=f"{context}User:{text}\nBot:", max_tokens=100).choices[
        0].text.lstrip(string.punctuation).strip()
    return response


# PRACTICE PROBLEMS

# GRAMMAR
def grammar(amount, difficulty, concepts, language):
    prompt = ''' Return ''' + str(amount) + language + '''grammar practice problems that are a ''' + str(difficulty) + '''/10 difficulty. Here is a list of grammatical topics, you should use one for each question: ''' + concepts.replace("-", ", ").replace(".", " ") + '''
    Here is the format, note it looks like a Python list, if you use a " in the text, do \\":
    ["letter answer) QUESTION", "a) CHOICE", "b) CHOICE", "c) CHOICE", "d) CHOICE"]
    ["letter answer) QUESTION", "a) CHOICE", "b) CHOICE", "c) CHOICE", "d) CHOICE"]
    ["letter answer) QUESTION", "a) CHOICE", "b) CHOICE", "c) CHOICE", "d) CHOICE"]
    ["letter answer) QUESTION", "a) CHOICE", "b) CHOICE", "c) CHOICE", "d) CHOICE"]
    ["letter answer) QUESTION", "a) CHOICE", "b) CHOICE", "c) CHOICE", "d) CHOICE"]

    Continue until you do ''' + str(amount) + ''' questions'''

    response = openai.Completion.create(engine=model, prompt=prompt, max_tokens=800).choices[0].text.lstrip(
        string.punctuation).strip().replace("\"", "")
    return response_formatter(response)


# VOCABULARY
def vocabulary(amount, difficulty, theme, language):
    prompt = '''Return ''' + str(amount) + language + ''' vocabulary practice problems that are a ''' + str(
        difficulty) + '''/10 difficulty. The vocabulary theme should be: ''' + " ".join(theme) + '''. Make sure none of the questions are duplicates and don't let the answers for each questions be duplicates.
    Here is the format of what you should return, make sure the answers for each question are a bit similar to throw the user off—note the formatting, it is supposed to look like a Python list, so make sure the syntax works:
    ["answer (the letter) QUESTION", "a) CHOICE", "b) CHOICE", "c) CHOICE", "d) CHOICE"],
    ["answer (the letter) QUESTION", "a) CHOICE", "b) CHOICE", "c) CHOICE", "d) CHOICE"],
    ["answer (the letter) QUESTION", "a) CHOICE", "b) CHOICE", "c) CHOICE", "d) CHOICE"],
    ["answer (the letter) QUESTION", "a) CHOICE", "b) CHOICE", "c) CHOICE", "d) CHOICE"],
    ["answer (the letter) QUESTION", "a) CHOICE", "b) CHOICE", "c) CHOICE", "d) CHOICE"]

    continue until you do ''' + str(amount) + ''' questions.'''

    response = openai.Completion.create(engine=model, prompt=prompt, max_tokens=1100).choices[0].text.lstrip(
        string.punctuation).strip().replace("\"", "")
    return response_formatter(response)


# PHRASES
def culture(amount, difficulty, language, category):
    prompt = '''Return''' + str(amount) + '''problems in ''' + language + ''' to practice common language questions relating to ''' + category + ''' in ''' + language + ''' culture that are a ''' + str(
        difficulty) + '''/10 difficulty. Make sure the answers aren't just duplicates of the question, they should be a response to it. THERE CAN ONLY BE ONE POSSIBLE ANSWER FOR EACH QUESTION

    Here is an example problem:
    ["(c). ¿A qué hora nos vemos / quedamos?", "a) Al parque", "b) Quiero un pizza", "c) Manaña a las cinco", "d) Cuando quieres pasar el rato"] 

    ==========================================================================
    Here is the format:
    ["answer (the letter) QUESTION", "a) CHOICE", "b) CHOICE", "c) CHOICE", "d) CHOICE"]
    ["answer (the letter) QUESTION", "a) CHOICE", "b) CHOICE", "c) CHOICE", "d) CHOICE"]
    ["answer (the letter) QUESTION", "a) CHOICE", "b) CHOICE", "c) CHOICE", "d) CHOICE"]
    ["answer (the letter) QUESTION", "a) CHOICE", "b) CHOICE", "c) CHOICE", "d) CHOICE"]
    ["answer (the letter) QUESTION", "a) CHOICE", "b) CHOICE", "c) CHOICE", "d) CHOICE"]
    ==========================================================================

    Important Note: for each question, there should only be one reasonable choice for the question (the answer), the other choices for that question should be illogical
    '''

    response = openai.Completion.create(engine=model, prompt=prompt, max_tokens=1100).choices[0].text.lstrip(
        string.punctuation).strip().replace("\"", "")
    return response_formatter(response)
