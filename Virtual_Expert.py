import g4f

def initialize_context(message_text):
    """
    Створює початковий контекст із текстом для моделі.
    """
    return [{
        "role": "system",
        "content": f"Це початковий контекст. Ось текст із файлу: {message_text}"
    }]

def chat_with_model(client, user_input, context):
    """
    Відправляє запит користувача до моделі, враховуючи наданий контекст.
    """
    context.append({
        "role": "user",
        "content": user_input
    })

    response = client.chat.completions.create(
        model="gpt-4",
        messages=context,
        temperature=1,
        max_tokens=4096,
        top_p=1,
        stream=False,
        stop=None,
    )

    return response.choices[0].message.content

# Основний блок
if __name__ == "__main__":
    # Ініціалізація клієнта
    client = g4f.Client()

    # Завантажуємо текст повідомлень
    message_text = """
    Ваш великий текст тут...
    """

    # Один запит для аналізу
    user_query = "Ваш запит тут..."  # Введіть свій запит у цю змінну

    # Контекст із тексту
    context = initialize_context(message_text)

    # Виконання запиту
    response = chat_with_model(client, user_query, context)

    # Виведення результату
    print(f"Результат запиту:\n{response}")
