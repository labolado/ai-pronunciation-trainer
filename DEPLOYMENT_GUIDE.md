# AI Pronunciation Trainer - 部署指南

## 项目概述
AI发音训练器已成功整合为统一的Flask服务器架构，提供完整的Web界面和API服务。

## 架构变更
- **从双服务器架构整合为单一Flask服务器**
- **统一端口**: 所有服务运行在端口3000
- **集成API**: REST API端点直接集成到Flask Web服务器中
- **语言支持修复**: Whisper语音识别添加明确语言参数支持

## 快速启动

### 1. 环境准备
```bash
cd ai-pronunciation-trainer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. 启动服务器
```bash
source venv/bin/activate
python webApp.py
```

### 3. 访问应用
打开浏览器访问: http://localhost:3000/

## 技术修复

### 语音识别修复
- **问题**: Whisper模型将英语识别为中文
- **解决方案**: 在`whisper_wrapper.py`和`models.py`中添加明确的语言参数
- **文件修改**: 
  - `whisper_wrapper.py:47` - 添加language参数到transcribe调用
  - `models.py:85` - 从前端接收语言选择

### 前端API整合
- **文件**: `callbacks.js`
- **修改**: 统一所有API调用使用端口3000
- **端点**: `/pronunciation_accuracy`, `/compute_features`, `/compare_recordings`

## 项目结构
```
ai-pronunciation-trainer/
├── webApp.py           # 统一Flask服务器
├── whisper_wrapper.py  # 语音识别模块  
├── models.py          # 核心模型逻辑
├── static/js/callbacks.js  # 前端API调用
├── templates/         # HTML模板
├── venv/             # Python虚拟环境
└── requirements.txt   # 依赖列表
```

## API端点
- `GET /` - 主页面
- `POST /pronunciation_accuracy` - 发音准确度分析
- `POST /compute_features` - 音频特征计算  
- `POST /compare_recordings` - 录音对比

## 部署注意事项
1. 确保Python 3.8+环境
2. 首次运行会下载Whisper模型，需要较长时间
3. 服务器启动后会显示可用地址
4. 支持中英文语音识别

## 更新日志
- 2024-08-15: 完成双服务器到单服务器架构整合
- 2024-08-15: 修复Whisper语言识别问题
- 2024-08-15: 统一端口配置为3000
- 2024-08-15: 集成所有API端点到Flask主服务器

## GitHub仓库
https://github.com/labolado/ai-pronunciation-trainer