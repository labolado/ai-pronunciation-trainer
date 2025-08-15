from flask import Flask, render_template, request, jsonify
import webbrowser
import os
from flask_cors import CORS
import json
import base64
from typing import Optional

import lambdaTTS
import lambdaSpeechToScore
import lambdaGetSample

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = '*'

rootPath = ''

# ======================== 原有Web界面路由 ========================

@app.route(rootPath+'/')
def main():
    return render_template('main.html')

@app.route(rootPath+'/getAudioFromText', methods=['POST'])
def getAudioFromText():
    event = {'body': json.dumps(request.get_json(force=True))}
    lambda_output = lambdaTTS.lambda_handler(event, [])
    
    # Extract the body from lambda response and return it directly
    if isinstance(lambda_output, dict) and 'body' in lambda_output:
        response_body = json.loads(lambda_output['body'])
        return response_body
    else:
        return lambda_output

@app.route(rootPath+'/getSample', methods=['POST'])
def getNext():
    event = {'body':  json.dumps(request.get_json(force=True))}
    lambda_output = lambdaGetSample.lambda_handler(event, [])
    
    # Extract the body from lambda response and return it directly
    if isinstance(lambda_output, dict) and 'body' in lambda_output:
        response_body = json.loads(lambda_output['body'])
        return response_body
    else:
        return lambda_output

@app.route(rootPath+'/GetAccuracyFromRecordedAudio', methods=['POST'])
def GetAccuracyFromRecordedAudio():
    print("=== GetAccuracyFromRecordedAudio called ===")
    
    try:
        request_data = request.get_json(force=True)
        print(f"Request data keys: {list(request_data.keys()) if request_data else 'None'}")
        
        if request_data:
            print(f"Title: '{request_data.get('title', '')}'")
            print(f"Language: '{request_data.get('language', '')}'")
            audio_data = request_data.get('base64Audio', '')
            print(f"Audio data length: {len(audio_data)}")
        
        event = {'body': json.dumps(request_data)}
        print("Calling lambdaSpeechToScore.lambda_handler...")
        lambda_output = lambdaSpeechToScore.lambda_handler(event, [])
        print(f"Lambda output type: {type(lambda_output)}")
        print(f"Lambda output: {lambda_output}")
        
        # Extract the body from lambda response and return it directly
        if isinstance(lambda_output, dict) and 'body' in lambda_output:
            response_body = json.loads(lambda_output['body'])
            print(f"Returning response body: {response_body}")
            return response_body
        elif isinstance(lambda_output, str):
            response_body = json.loads(lambda_output)
            return response_body
        else:
            return lambda_output
        
    except Exception as e:
        print('Error: ', str(e))
        import traceback
        traceback.print_exc()
        return {
            'pronunciation_accuracy': '0',
            'ipa_transcript': '',
            'real_transcripts_ipa': '',
            'matched_transcripts_ipa': '',
            'pair_accuracy_category': '',
            'is_letter_correct_all_words': '',
            'start_time': '',
            'end_time': ''
        }

    print("=== GetAccuracyFromRecordedAudio completed ===")

# ======================== 新增API接口路由 ========================

@app.route('/api/health')
def health_check():
    """健康检查接口"""
    return jsonify({"status": "healthy", "message": "AI发音训练器运行正常"})

@app.route('/api/info')
def api_info():
    """API信息接口"""
    return jsonify({
        "name": "AI发音训练器统一服务",
        "version": "1.0.0",
        "description": "提供Web界面和REST API的统一服务",
        "endpoints": {
            "web_ui": "http://localhost:3000/",
            "api_health": "http://localhost:3000/api/health",
            "api_pronunciation": "http://localhost:3000/api/v1/pronunciation",
            "api_tts": "http://localhost:3000/api/v1/tts",
            "api_sample": "http://localhost:3000/api/v1/sample"
        }
    })

@app.route('/api/v1/pronunciation', methods=['POST'])
def api_analyze_pronunciation():
    """
    API: 分析发音准确度
    请求格式: {"text": "文本", "audio_base64": "base64音频", "language": "de"}
    """
    try:
        data = request.get_json(force=True)
        
        # 验证必需参数
        if not data.get('text') or not data.get('audio_base64'):
            return jsonify({"error": "缺少必需参数: text 或 audio_base64"}), 400
        
        # 构造请求数据
        event_data = {
            'title': data.get('text'),
            'base64Audio': data.get('audio_base64'),
            'language': data.get('language', 'de')
        }
        
        event = {'body': json.dumps(event_data)}
        result = lambdaSpeechToScore.lambda_handler(event, [])
        
        # 解析结果
        if isinstance(result, str):
            result_data = json.loads(result)
        elif isinstance(result, dict) and 'body' in result:
            result_data = json.loads(result['body'])
        else:
            result_data = result
            
        return jsonify(result_data)
        
    except Exception as e:
        return jsonify({"error": f"发音分析失败: {str(e)}"}), 500

@app.route('/api/v1/tts', methods=['POST'])
def api_text_to_speech():
    """
    API: 文本转语音
    请求格式: {"text": "文本", "language": "de", "voice_speed": 1.0}
    """
    try:
        data = request.get_json(force=True)
        
        if not data.get('text'):
            return jsonify({"error": "缺少必需参数: text"}), 400
        
        # 构造请求数据
        event_data = {
            'text': data.get('text'),
            'language': data.get('language', 'de'),
            'voice_speed': data.get('voice_speed', 1.0)
        }
        
        event = {'body': json.dumps(event_data)}
        result = lambdaTTS.lambda_handler(event, [])
        
        # 解析结果
        if isinstance(result, str):
            result_data = json.loads(result)
        elif isinstance(result, dict) and 'body' in result:
            result_data = json.loads(result['body'])
        else:
            result_data = result
            
        return jsonify({
            "audio_base64": result_data.get('audio_base64', ''),
            "message": "语音生成成功"
        })
        
    except Exception as e:
        return jsonify({"error": f"语音生成失败: {str(e)}"}), 500

@app.route('/api/v1/sample', methods=['POST'])
def api_get_sample():
    """
    API: 获取练习样本
    请求格式: {"category": "0", "language": "de"}
    """
    try:
        data = request.get_json(force=True)
        
        # 构造请求数据
        event_data = {
            'category': data.get('category', '0'),
            'language': data.get('language', 'de')
        }
        
        event = {'body': json.dumps(event_data)}
        result = lambdaGetSample.lambda_handler(event, [])
        
        # 解析结果
        if isinstance(result, str):
            result_data = json.loads(result)
        elif isinstance(result, dict) and 'body' in result:
            result_data = json.loads(result['body'])
        else:
            result_data = result
            
        return jsonify(result_data)
        
    except Exception as e:
        return jsonify({"error": f"样本生成失败: {str(e)}"}), 500

@app.route('/api/v1/languages')
def api_get_languages():
    """API: 获取支持的语言列表"""
    return jsonify({
        "languages": [
            {"code": "de", "name": "德语", "native_name": "Deutsch"},
            {"code": "en", "name": "英语", "native_name": "English"}
        ]
    })

@app.route('/api/v1/categories')
def api_get_categories():
    """API: 获取难度分类"""
    return jsonify({
        "categories": [
            {"code": "0", "name": "简单", "description": "单词和短语"},
            {"code": "1", "name": "中等", "description": "短句子"},
            {"code": "2", "name": "困难", "description": "长句子"},
            {"code": "3", "name": "很困难", "description": "复杂句子"}
        ]
    })

# 文件上传支持
@app.route('/api/v1/pronunciation/file', methods=['POST'])
def api_analyze_pronunciation_file():
    """
    API: 通过上传音频文件分析发音
    """
    try:
        # 获取文本和语言参数
        text = request.form.get('text')
        language = request.form.get('language', 'de')
        
        if not text:
            return jsonify({"error": "缺少必需参数: text"}), 400
        
        # 获取上传的文件
        if 'audio_file' not in request.files:
            return jsonify({"error": "缺少音频文件"}), 400
            
        audio_file = request.files['audio_file']
        if audio_file.filename == '':
            return jsonify({"error": "未选择文件"}), 400
        
        # 读取文件内容并转换为base64
        audio_content = audio_file.read()
        audio_base64 = "data:audio/ogg;base64," + base64.b64encode(audio_content).decode('utf-8')
        
        # 调用发音分析
        event_data = {
            'title': text,
            'base64Audio': audio_base64,
            'language': language
        }
        
        event = {'body': json.dumps(event_data)}
        result = lambdaSpeechToScore.lambda_handler(event, [])
        
        # 解析结果
        if isinstance(result, str):
            result_data = json.loads(result)
        elif isinstance(result, dict) and 'body' in result:
            result_data = json.loads(result['body'])
        else:
            result_data = result
            
        return jsonify(result_data)
        
    except Exception as e:
        return jsonify({"error": f"文件处理失败: {str(e)}"}), 500


if __name__ == "__main__":
    language = 'de'
    print("Starting AI Pronunciation Trainer...")
    print("Current directory:", os.getcwd())
    print("Server will be available at: http://127.0.0.1:3000/")
    print("Loading models... This may take a few minutes on first run.")
    
    try:
        app.run(host="0.0.0.0", port=3000, debug=True)
    except Exception as e:
        print(f"Failed to start server: {e}")