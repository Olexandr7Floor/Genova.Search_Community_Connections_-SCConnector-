import os
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, session
from parser_msg_telegram import load_and_filter_json
from parser_msg_discord import parse_discord_channel
from formation_text_for_ai import filter_specific_fields
import g4f  # Для інтеграції AI
from Virtual_Expert import  initialize_context, chat_with_model
from Leader_percentage_Themes_Conections import run_analysis
from Count_messages import load_json, count_user_messages, save_user_counts_to_txt
from Building_plots import process_user_activity, plot_user_activity, plot_community_activity
from diagram_generator import generate_pie_chart
from Semantic_map import read_graph_data, filter_graph_data, visualize_graph
ListController = Blueprint('ListController', __name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), )
OUTPUT_FOLDER = os.path.join(os.getcwd(), 'static')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)



@ListController.route('/run-entities-scripts', methods=['GET'])
def run_entities_scripts():
    try:
        leaders_file = os.path.join(OUTPUT_FOLDER, "leaders_analysis.txt")
        topics_file = os.path.join(OUTPUT_FOLDER, "chat_topics_percentage.txt")
        connections_file = os.path.join(OUTPUT_FOLDER, "related_persons_pairs.txt")
        run_analysis(leaders_file, topics_file, connections_file)

        input_file = os.path.join(UPLOAD_FOLDER, "parsed_msg.json")
        user_counts_file = os.path.join(OUTPUT_FOLDER, "user_message_counts.txt")
        data = load_json(input_file)
        user_counts = count_user_messages(data)
        save_user_counts_to_txt(user_counts, user_counts_file)

        user_activity, activity_by_hour, community_activity = process_user_activity(data)
        plot_user_activity(user_activity, activity_by_hour, OUTPUT_FOLDER)
        plot_community_activity(community_activity, OUTPUT_FOLDER)

        generate_pie_chart(leaders_file, OUTPUT_FOLDER)
        filtered = 0
        data, node_mentions, repeated_edges = read_graph_data(connections_file)
        filtered_nodes, filtered_data = filter_graph_data(data, node_mentions, filtered)
        visualize_graph(filtered_data, node_mentions, repeated_edges, "static/Connections")

        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@ListController.route('/run-semantic-map', methods=['GET'])
def run_semantic_map():
    try:
        output_path = os.path.join("static", "Connections.png")

        if os.path.exists(output_path):
            return jsonify({"graph": f"/{output_path}"}), 200
        else:
            return jsonify({"error": "Graph not created"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ListController.route('/read-file/<filename>', methods=['GET'])
def read_file(filename):
    try:
        file_path = os.path.join(OUTPUT_FOLDER, filename)
        if not os.path.exists(file_path):
            return jsonify({"error": "File not found"}), 404

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return jsonify({"content": content}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



UPLOAD_FOLDER = os.path.join(os.getcwd())
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'json'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@ListController.route('/', methods=["GET", "POST"])
def list_page():
    if request.method == "POST":
        if 'fileInput' not in request.files:
            flash('Файл не вибрано!')
            return redirect(url_for('ListController.list_page'))
        
        file = request.files['fileInput']
        if file.filename == '':
            flash('Файл не обрано для завантаження')
            return redirect(url_for('ListController.list_page'))
        
        if file and allowed_file(file.filename):
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
            session['uploaded_file'] = file.filename  # Зберігаємо ім'я файлу в сесії
            flash(f'Файл успішно завантажено: {file.filename}')
            return redirect(url_for('ListController.list_page'))
        else:
            flash('Файл повинен бути у форматі JSON.')
            return redirect(url_for('ListController.list_page'))
    
    return render_template('list/list.html')

@ListController.route('/run-parser', methods=['POST'])
def run_parser():
    try:
        filename = session.get('uploaded_file')
        if not filename:
            return jsonify({'error': 'Файл не було завантажено.'}), 400

        input_file = os.path.join(UPLOAD_FOLDER, filename)

        if not os.path.exists(input_file):
            return jsonify({'error': f'Файл {filename} не знайдено.'}), 404

        parsed_data = load_and_filter_json(input_file)
        
        text_for_ai = filter_specific_fields()
        
        if parsed_data:
            return jsonify(parsed_data), 200
        else:
            return jsonify({'error': 'Парсер не зміг обробити дані або повернув порожній результат.'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ListController.route('/run-discord-parser', methods=['POST'])
def run_discord_parser():
    try:
        data = request.json
        discord_token = data.get('token')
        channel_id = data.get('channel_id')
        channel_name = data.get('channel_name')

        if not all([discord_token, channel_id, channel_name]):
            return jsonify({'error': 'Всі поля (токен, ID каналу, назва каналу) обов’язкові для заповнення.'}), 400

        parsed_data = parse_discord_channel(discord_token, channel_id, channel_name)
        
        text_for_ai = filter_specific_fields()
        
        if parsed_data:
            return jsonify(parsed_data), 200
        else:
            return jsonify({'error': 'Парсер не зміг обробити дані або повернув порожній результат.'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ListController.route('/run-ai', methods=['POST'])
def run_ai():
    """
    Обробляє запити з вкладки "AI Expert".
    """
    try:
        user_query = request.json.get('query')
        uploaded_file = os.path.join(UPLOAD_FOLDER, "parsed_msg_for_ai.txt")

        if not os.path.exists(uploaded_file):
            return jsonify({"error": "Файл для аналізу не знайдено."}), 404

        with open(uploaded_file, 'r', encoding='utf-8') as f:
            message_text = f.read()

        client = g4f.Client()
        context = initialize_context(message_text)
        response = chat_with_model(client, user_query, context)

        return jsonify({"response": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
