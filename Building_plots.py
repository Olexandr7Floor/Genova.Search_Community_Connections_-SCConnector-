import json
import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime

def load_json(file_path):
    """
    Завантаження JSON даних з файлу.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def process_user_activity(data):
    """
    Аналіз активності користувачів за годинами.
    """
    messages = data.get("messages", [])
    user_activity = Counter()
    activity_by_hour = {hour: Counter() for hour in range(24)}
    community_activity = Counter()

    for message in messages:
        user = message.get("from", "Unknown")
        date_str = message.get("date", "")
        if date_str:
            hour = datetime.fromisoformat(date_str).hour
            user_activity[user] += 1
            activity_by_hour[hour][user] += 1
            community_activity[hour] += 1

    return user_activity, activity_by_hour, community_activity

def plot_user_activity(user_activity, activity_by_hour, output_path):
    """
    Побудова графіка активності користувачів та збереження у файл.
    """
    hours = list(range(24))
    users = list(user_activity.keys())
    user_hours = {user: [activity_by_hour[hour].get(user, 0) for hour in hours] for user in users}

    plt.figure(figsize=(12, 8))
    for user, activity in user_hours.items():
        plt.plot(hours, activity, label=user)

    plt.title('User Activity by Hour')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Number of Messages')
    plt.xticks(hours)
    plt.grid(True)
    plt.legend(loc='upper right', fontsize='small', ncol=2)
    plt.tight_layout()
    plt.savefig(output_path + "/user_activity.png")
    plt.close()

def plot_community_activity(community_activity, output_path):
    """
    Побудова графіка активності всієї спільноти та збереження у файл.
    """
    hours = list(range(24))
    community_messages = [community_activity.get(hour, 0) for hour in hours]

    plt.figure(figsize=(12, 6))
    plt.plot(hours, community_messages, label='Community Activity', color='blue', marker='o')
    plt.title('Community Activity by Hour')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Number of Messages')
    plt.xticks(hours)
    plt.grid(True)
    plt.legend(loc='upper right', fontsize='medium')
    plt.tight_layout()
    plt.savefig(output_path + "/community_activity.png")
    plt.close()

if __name__ == "__main__":
    # Шлях до JSON файлу
    file_path = 'parsed_msg.json'
    output_path = '.'  # Директорія для збереження графіків (поточна)

    # Завантаження даних
    data = load_json(file_path)
    
    # Аналіз активності
    user_activity, activity_by_hour, community_activity = process_user_activity(data)
    
    # Побудова графіка активності користувачів
    plot_user_activity(user_activity, activity_by_hour, output_path)
    
    # Побудова графіка активності спільноти
    plot_community_activity(community_activity, output_path)

    print(f"Графіки збережено в директорії: {output_path}")
