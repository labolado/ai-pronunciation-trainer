from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
import base64
import json
import os
import uvicorn

# 导入原有的处理模块
import lambdaTTS
import lambdaSpeechToScore
import lambdaGetSample

app = FastAPI(
    title="AI发音训练器 API",
    description="提供语音识别、发音评估和文本转语音功能的REST API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境建议指定具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 请求模型定义
class TextToSpeechRequest(BaseModel):
    text: str
    language: str = "de"  # de(德语) 或 en(英语)
    voice_speed: float = 1.0

class PronunciationRequest(BaseModel):
    text: str
    audio_base64: str  # base64编码的音频数据
    language: str = "de"

class SampleRequest(BaseModel):
    category: str = "0"  # 0:简单, 1:中等, 2:困难, 3:很困难
    language: str = "de"

class AudioFileRequest(BaseModel):
    text: str
    language: str = "de"

# 响应模型定义
class PronunciationResponse(BaseModel):
    pronunciation_accuracy: str
    ipa_transcript: str
    real_transcripts_ipa: str
    matched_transcripts_ipa: str
    pair_accuracy_category: str
    is_letter_correct_all_words: str
    start_time: str
    end_time: str

class SampleResponse(BaseModel):
    real_transcript: List[str]
    ipa_transcript: str
    transcript_translation: str

class TTSResponse(BaseModel):
    audio_base64: str
    message: str

@app.get("/")
async def root():
    """API根路径，返回基本信息"""
    return {
        "message": "AI发音训练器 FastAPI 接口",
        "version": "1.0.0",
        "endpoints": {
            "pronunciation": "/api/v1/pronunciation",
            "tts": "/api/v1/tts", 
            "sample": "/api/v1/sample",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "healthy", "message": "AI发音训练器运行正常"}

@app.post("/api/v1/pronunciation", response_model=PronunciationResponse)
async def analyze_pronunciation(request: PronunciationRequest):
    """
    分析发音准确度
    
    - **text**: 要分析的文本
    - **audio_base64**: base64编码的音频数据 (支持OGG/WAV格式)
    - **language**: 语言代码 (de=德语, en=英语)
    """
    try:
        # 构造lambda事件格式
        event = {
            'body': json.dumps({
                'title': request.text,
                'base64Audio': request.audio_base64,
                'language': request.language
            })
        }
        
        # 调用原有的处理函数
        result = lambdaSpeechToScore.lambda_handler(event, [])
        
        # 解析结果
        if isinstance(result, str):
            result_data = json.loads(result)
        else:
            result_data = result
            
        return PronunciationResponse(**result_data)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"发音分析失败: {str(e)}")

@app.post("/api/v1/pronunciation/file")
async def analyze_pronunciation_file(
    text: str,
    language: str = "de",
    audio_file: UploadFile = File(...)
):
    """
    通过上传音频文件分析发音 (支持WAV, MP3, OGG等格式)
    """
    try:
        # 读取上传的文件
        audio_content = await audio_file.read()
        
        # 转换为base64
        audio_base64 = "data:audio/ogg;base64," + base64.b64encode(audio_content).decode('utf-8')
        
        # 创建请求对象
        request = PronunciationRequest(
            text=text,
            audio_base64=audio_base64,
            language=language
        )
        
        # 调用分析函数
        return await analyze_pronunciation(request)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件处理失败: {str(e)}")

@app.post("/api/v1/tts", response_model=TTSResponse)
async def text_to_speech(request: TextToSpeechRequest):
    """
    文本转语音
    
    - **text**: 要转换的文本
    - **language**: 语言代码 (de=德语, en=英语)
    - **voice_speed**: 语音速度 (0.5-2.0)
    """
    try:
        # 构造lambda事件格式
        event = {
            'body': json.dumps({
                'text': request.text,
                'language': request.language,
                'voice_speed': request.voice_speed
            })
        }
        
        # 调用TTS处理函数
        result = lambdaTTS.lambda_handler(event, [])
        
        # 解析结果
        if isinstance(result, dict) and 'body' in result:
            result_data = json.loads(result['body'])
        elif isinstance(result, str):
            result_data = json.loads(result)
        else:
            result_data = result
            
        return TTSResponse(
            audio_base64=result_data.get('audio_base64', ''),
            message="语音生成成功"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"语音生成失败: {str(e)}")

@app.post("/api/v1/sample", response_model=SampleResponse)
async def get_sample(request: SampleRequest):
    """
    获取练习样本
    
    - **category**: 难度级别 (0=简单, 1=中等, 2=困难, 3=很困难)
    - **language**: 语言代码 (de=德语, en=英语)
    """
    try:
        # 构造lambda事件格式
        event = {
            'body': json.dumps({
                'category': request.category,
                'language': request.language
            })
        }
        
        # 调用样本生成函数
        result = lambdaGetSample.lambda_handler(event, [])
        
        # 解析结果
        if isinstance(result, dict) and 'body' in result:
            result_data = json.loads(result['body'])
        elif isinstance(result, str):
            result_data = json.loads(result)
        else:
            result_data = result
            
        return SampleResponse(**result_data)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"样本生成失败: {str(e)}")

@app.get("/api/v1/languages")
async def get_supported_languages():
    """获取支持的语言列表"""
    return {
        "languages": [
            {"code": "de", "name": "德语", "native_name": "Deutsch"},
            {"code": "en", "name": "英语", "native_name": "English"}
        ]
    }

@app.get("/api/v1/categories")
async def get_difficulty_categories():
    """获取难度分类"""
    return {
        "categories": [
            {"code": "0", "name": "简单", "description": "单词和短语"},
            {"code": "1", "name": "中等", "description": "短句子"},
            {"code": "2", "name": "困难", "description": "长句子"},
            {"code": "3", "name": "很困难", "description": "复杂句子"}
        ]
    }

# 批量处理接口
@app.post("/api/v1/batch/pronunciation")
async def batch_analyze_pronunciation(requests: List[PronunciationRequest]):
    """批量分析发音"""
    results = []
    for req in requests:
        try:
            result = await analyze_pronunciation(req)
            results.append({"success": True, "data": result})
        except Exception as e:
            results.append({"success": False, "error": str(e)})
    
    return {"results": results}

@app.post("/api/v1/batch/tts")
async def batch_text_to_speech(requests: List[TextToSpeechRequest]):
    """批量文本转语音"""
    results = []
    for req in requests:
        try:
            result = await text_to_speech(req)
            results.append({"success": True, "data": result})
        except Exception as e:
            results.append({"success": False, "error": str(e)})
    
    return {"results": results}

if __name__ == "__main__":
    print("🚀 启动 AI发音训练器 FastAPI 服务器...")
    print("📖 API文档: http://localhost:8000/docs")
    print("🔄 交互式文档: http://localhost:8000/redoc")
    
    uvicorn.run(
        "fastapi_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )