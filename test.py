from flask import Flask, request, jsonify, render_template
import json

app = Flask(__name__)

# 英文到中文键的映射
key_translation = {
    "in": "公称通径",
    "l": "固定式球阀长度",
    "w": "孔中心",
    "o": "法兰外径",
    "r": "水线台阶",
    "t": "法兰厚度",
    "f": "水线高度",
    "n": "孔数量规格",
    "s": "环号",
    "p": "环中心",
    "fe": "水线高度_槽深",
    "fl": "槽宽",
    "nr": "八角环槽底"
}


@app.route('/')
def index():
    # 读取本地JSON文件并获取所有sheet_name
    with open('output.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    sheet_names = [sheet['sheet_name'] for sheet in data]

    return render_template('index.html', sheet_names=sheet_names)


@app.route('/post', methods=['POST'])
def post():
    sheet_name = request.form['sheet_name']
    in_value = request.form['in']

    # 读取本地JSON文件
    with open('output.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 查找匹配的字段
    for sheet in data:
        if sheet['sheet_name'] == sheet_name:
            for item in sheet['data']:
                if item['in'] == in_value:
                    # 翻译键
                    translated_result = {key_translation.get(key, key): value for key, value in item.items() if key != 'in'}
                    response = jsonify(translated_result)
                    response.headers["Content-Type"] = "application/json; charset=utf-8"
                    return response

            return jsonify({"error": "没有找到对应的通经"})
    return jsonify({"error": "没有找到对应的名称"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8003, debug=True)
