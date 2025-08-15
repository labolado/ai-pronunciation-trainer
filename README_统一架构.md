# AI发音训练器 - 统一服务架构

## 概述
AI发音训练器现在整合为单一服务器架构，同时提供Web界面和REST API接口。

## 服务地址
- **Web界面**: http://localhost:3001/
- **API文档**: http://localhost:3001/api/info

## Web界面功能
- 德语/英语发音练习
- 实时录音和播放
- 发音准确度分析
- IPA音标对比
- 练习样本生成

## API接口

### 基础接口
- `GET /api/health` - 健康检查
- `GET /api/info` - API信息和端点列表

### 核心功能API
- `POST /api/v1/pronunciation` - 发音分析
- `POST /api/v1/tts` - 文本转语音
- `POST /api/v1/sample` - 获取练习样本
- `POST /api/v1/pronunciation/file` - 文件上传发音分析

### 辅助接口
- `GET /api/v1/languages` - 支持的语言列表
- `GET /api/v1/categories` - 难度分类列表

## API使用示例

### 1. 发音分析
```bash
curl -X POST http://localhost:3001/api/v1/pronunciation \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Guten Tag",
    "audio_base64": "data:audio/ogg;base64,T2dnUw...",
    "language": "de"
  }'
```

### 2. 文本转语音
```bash
curl -X POST http://localhost:3001/api/v1/tts \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hallo Welt",
    "language": "de",
    "voice_speed": 1.0
  }'
```

### 3. 获取练习样本
```bash
curl -X POST http://localhost:3001/api/v1/sample \
  -H "Content-Type: application/json" \
  -d '{
    "category": "0",
    "language": "de"
  }'
```

### 4. 文件上传发音分析
```bash
curl -X POST http://localhost:3001/api/v1/pronunciation/file \
  -F "text=Guten Tag" \
  -F "language=de" \
  -F "audio_file=@recording.ogg"
```

## 启动服务

### 开发环境
```bash
python webApp.py
```

### Windows环境
```bash
windows_setup.bat
```

## 技术架构
- **后端**: Flask统一服务器
- **端口**: 3001
- **音频处理**: soundfile + FFmpeg
- **AI模型**: Whisper ASR + Silero TTS
- **支持格式**: OGG, WAV, MP3

## 优势
1. **简化部署**: 只需一个服务器进程
2. **统一管理**: Web界面和API共享相同逻辑
3. **便于维护**: 单一代码库，统一配置
4. **资源优化**: 减少内存和CPU占用
5. **灵活访问**: 支持浏览器直接访问和程序化调用