# AI发音训练器 FastAPI接口文档

## 🚀 快速开始

### 启动FastAPI服务器
```bash
# Windows
start_fastapi.bat

# macOS/Linux
cd ai-pronunciation-trainer
source venv/bin/activate
pip install -r fastapi_requirements.txt
python fastapi_server.py
```

服务器启动后访问：
- **API文档**: http://localhost:8000/docs
- **交互式文档**: http://localhost:8000/redoc
- **健康检查**: http://localhost:8000/health

## 📋 API接口列表

### 1. 发音分析 `/api/v1/pronunciation`
**POST** - 分析用户发音准确度

```json
{
  "text": "Hallo, wie geht es dir?",
  "audio_base64": "data:audio/ogg;base64,T2dnUw...",
  "language": "de"
}
```

**响应**:
```json
{
  "pronunciation_accuracy": "85",
  "ipa_transcript": "ˈhaloː viː ɡeːt ɛs diːɐ̯",
  "real_transcripts_ipa": "ˈhaloː viː ɡeːt ɛs diːɐ̯",
  "matched_transcripts_ipa": "ˈhaloː viː ɡeːt ɛs diːɐ̯",
  "pair_accuracy_category": "0 0 0 0 0",
  "is_letter_correct_all_words": "11111 111 1111 11 1111",
  "start_time": "0.0 0.5 1.0 1.5 2.0",
  "end_time": "0.5 1.0 1.5 2.0 2.5"
}
```

### 2. 文件上传发音分析 `/api/v1/pronunciation/file`
**POST** - 通过上传音频文件分析发音

```bash
curl -X POST "http://localhost:8000/api/v1/pronunciation/file" \
  -F "text=Hallo" \
  -F "language=de" \
  -F "audio_file=@recording.wav"
```

### 3. 文本转语音 `/api/v1/tts`
**POST** - 将文本转换为语音

```json
{
  "text": "Guten Tag",
  "language": "de",
  "voice_speed": 1.0
}
```

**响应**:
```json
{
  "audio_base64": "data:audio/wav;base64,UklGRn...",
  "message": "语音生成成功"
}
```

### 4. 获取练习样本 `/api/v1/sample`
**POST** - 获取指定难度的练习文本

```json
{
  "category": "0",
  "language": "de"
}
```

**响应**:
```json
{
  "real_transcript": ["Ich bin ein Student"],
  "ipa_transcript": "ɪç bɪn aɪn ʃtuˈdɛnt",
  "transcript_translation": "I am a student"
}
```

### 5. 支持的语言 `/api/v1/languages`
**GET** - 获取支持的语言列表

### 6. 难度分类 `/api/v1/categories`
**GET** - 获取难度分类信息

## 🔄 批量处理接口

### 批量发音分析 `/api/v1/batch/pronunciation`
**POST** - 批量分析多个发音

### 批量文本转语音 `/api/v1/batch/tts`
**POST** - 批量生成多个语音

## 🐍 Python客户端SDK

```python
from client_sdk import AITrainerClient

# 创建客户端
client = AITrainerClient("http://localhost:8000")

# 健康检查
status = client.health_check()

# 获取练习样本
sample = client.get_sample(category="0", language="de")

# 文本转语音
tts_result = client.text_to_speech(
    text="Hallo Welt",
    language="de",
    save_path="output.wav"
)

# 发音分析
result = client.analyze_pronunciation_file(
    text="Hallo",
    audio_file_path="recording.wav",
    language="de"
)
print(f"发音准确度: {result['pronunciation_accuracy']}%")
```

## 🌐 JavaScript客户端示例

```javascript
class AITrainerAPI {
    constructor(baseURL = 'http://localhost:8000') {
        this.baseURL = baseURL;
    }
    
    async analyzePronunciation(text, audioBase64, language = 'de') {
        const response = await fetch(`${this.baseURL}/api/v1/pronunciation`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text,
                audio_base64: audioBase64,
                language
            })
        });
        return response.json();
    }
    
    async textToSpeech(text, language = 'de') {
        const response = await fetch(`${this.baseURL}/api/v1/tts`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text,
                language,
                voice_speed: 1.0
            })
        });
        return response.json();
    }
    
    async getSample(category = '0', language = 'de') {
        const response = await fetch(`${this.baseURL}/api/v1/sample`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                category,
                language
            })
        });
        return response.json();
    }
}

// 使用示例
const api = new AITrainerAPI();

// 获取练习样本
api.getSample().then(sample => {
    console.log('练习文本:', sample.real_transcript);
});

// 文本转语音
api.textToSpeech('Hallo Welt').then(result => {
    // 播放生成的音频
    const audio = new Audio(result.audio_base64);
    audio.play();
});
```

## 🔧 参数说明

### 语言代码
- `de`: 德语
- `en`: 英语

### 难度分类
- `0`: 简单 (单词和短语)
- `1`: 中等 (短句子)
- `2`: 困难 (长句子)
- `3`: 很困难 (复杂句子)

### 音频格式
- 支持: WAV, MP3, OGG, M4A
- 采样率: 推荐16kHz或48kHz
- 单声道或立体声

## 🚨 错误处理

所有API接口都使用标准HTTP状态码：
- `200`: 成功
- `400`: 请求参数错误
- `500`: 服务器内部错误

错误响应格式：
```json
{
  "detail": "错误描述信息"
}
```

## 🔐 部署建议

### 生产环境配置
1. 修改CORS设置，指定允许的域名
2. 添加API认证 (JWT Token)
3. 启用HTTPS
4. 配置反向代理 (Nginx)
5. 设置请求限制和缓存

### Docker部署
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt
RUN pip install -r fastapi_requirements.txt

EXPOSE 8000

CMD ["python", "fastapi_server.py"]
```

现在您可以轻松地将AI发音训练器集成到任何应用中！