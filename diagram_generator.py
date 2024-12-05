import matplotlib.pyplot as plt
import os

def generate_pie_chart(file_path: str, output_dir: str = ".") -> None:
    """
    Читає дані з файлу та створює кругову діаграму.
    
    :param file_path: Шлях до файлу з даними.
    :param output_dir: Директорія для збереження графіку.
    """
    # Перевірка існування файлу
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл за шляхом {file_path} не знайдено.")

    # Читання даних з файлу
    labels = []
    sizes = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            if '-' in line:
                label, size = line.split('-')
                labels.append(label.strip())
                sizes.append(float(size.strip()))
    
    # Створення кругової діаграми
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)

    # Зробити коло рівним, щоб графік був круглим
    ax.axis('equal')

    # Заголовок графіку
    plt.title('Leaders Analysis: Opinion Leaders')

    # Збереження графіку
    output_file = os.path.join(output_dir, "leaders_analysis_pie_chart.png")
    plt.savefig(output_file)
    print(f"Графік збережено у файл: {output_file}")


if __name__ == "__main__":

    # Ввід даних для роботи функції
    input_file = input("Введіть шлях до файлу з даними: ").strip()
    output_directory = input("Введіть шлях до директорії для збереження графіку (або залиште порожнім для поточної директорії): ").strip()

    # Якщо користувач не ввів шлях до директорії, використовується поточна
    #output_directory = output_directory if output_directory else "."

    # Виклик функції
    generate_pie_chart(input_file, output_directory)