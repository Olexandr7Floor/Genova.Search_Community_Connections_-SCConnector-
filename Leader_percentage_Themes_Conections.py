import g4f
import time  # Для затримки

def initialize_context(message_text):
    """
    Завантажує текст із файлу та додає його до контексту.
    """

    # Початковий контекст для нового чату
    return [{
        "role": "system",
        "content": f"Це початковий контекст. Ось текст із файлу: {message_text}"
    }]

def chat_with_model(client, user_input, context):
    """
    Відправляє запит користувача до моделі, враховуючи наданий контекст.
    """
    # Додаємо запит користувача до контексту
    context.append({
        "role": "user",
        "content": user_input
    })

    # Відправляємо всю історію чату до моделі
    response = client.chat.completions.create(
        model="gpt-4",
        messages=context,
        temperature=1,
        max_tokens=4096,
        top_p=1,
        stream=False,
        stop=None,
    )

    # Отримуємо відповідь моделі
    assistant_response = response.choices[0].message.content

    return assistant_response

def save_response_to_file(file_name, response):
    """
    Зберігає відповідь у файл.
    """
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(response)


def run_analysis(leaders_file, topics_file, connections_file):
    # Ініціалізація клієнта
    client = g4f.Client()

    
    with open("parsed_msg_for_ai.txt", 'r', encoding='utf-8') as f:
        #message_text = json.load(f)
        message_text = f.read()
        
    queries = [
        """Визнач лідерів думок на основі завантаженого контексту. Кожному з них присвой коефіціент лідерства. Результат виведи у форматі: Особа1 - коефіціент лідерства (0 - 1) без зайвого тексту""",
        """Виведи список всіх будь-яких тем що піднімались у чаті та відсоток часу з усього чату який вони займають. Вивід у форматі: Назва Теми - відсоток чату (0%-100%) без зайвого тексту""",
        """Виведи мені ВСІ пов'язані між собою учасники в спільноті не кожен с кожним а хто з ким реально взаємодіє (ВСІ ІМЕНА В ОДНАКОВОМУ ФОРМАТІ). Вивід здійсни ненумерованим попарним списком унікальних зв'язків у вигляді: 
            Особа1; Особа2
            Особа3; Особа2
            Особа4; Особа3
            без повторів, зайвого тексту та нумерації"""
    ]
    '''
    file_names = [
        "leaders_analysis.txt",
        "chat_topics_percentage.txt",
        "related_persons_pairs.txt"
    ]'''
    file_names = [
        leaders_file,
        topics_file,
        connections_file
    ]
    for i, query in enumerate(queries, start=1):
        # Створюємо окремий контекст для кожного запиту
        context = initialize_context(message_text)
        print(f"Запит {i}: {query}")
        
        response = chat_with_model(client, query, context)
        print(f"Відповідь {i}: {response}\n")
        save_response_to_file(file_names[i-1], response)
    
    
# Основний блок
if __name__ == "__main__":
    # Ініціалізація клієнта
    client = g4f.Client()

    
    with open("parsed_msg_for_ai.txt", 'r', encoding='utf-8') as f:
        #message_text = json.load(f)
        message_text = f.read()
        
    queries = [
        "Визнач лідерів думок на основі завантаженого контексту. Кожному з них присвой коефіціент лідерства. Результат виведи у форматі: Особа1 - коефіціент лідерства (0 - 1) БЕЗ ЗАЙВОГО тексту",
        "Виведи список всіх будь-яких тем що піднімались у чаті та відсоток часу з усього чату який вони займають. Вивід у форматі: Назва Теми - відсоток чату (0%-100%) БЕЗ ЗАЙВОГО тексту",
        "Виведи мені ВСІ пов'язані між собою учасники в спільноті не кожен с кожним а хто з ким РЕАЛЬНО взаємодіє (якщо імена пусті або не містять літер записувати особа+те що є. Наприклад особа. або особа))). Вивід здійсни попарним списком унікальних зв'язків у вигляді БЕЗ НУМЕРАЦІЇ: ОсобаХ; ОсобаУ. БЕЗ повторів, зайвого тексту "
    ]

    file_names = [
        "leaders_analysis.txt",
        "chat_topics_percentage.txt",
        "related_persons_pairs.txt"
    ]
    for i, query in enumerate(queries, start=1):
        # Створюємо окремий контекст для кожного запиту
        context = initialize_context(message_text)
        print(f"Запит {i}: {query}")
        
        response = chat_with_model(client, query, context)
        print(f"Відповідь {i}: {response}\n")
        save_response_to_file(file_names[i-1], response)
