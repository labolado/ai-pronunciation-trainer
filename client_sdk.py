import requests
import base64
import json
from typing import Optional

class AITrainerClient:
    """AI发音训练器Python客户端"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
    
    def health_check(self) -> dict:
        """健康检查"""
        response = self.session.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()
    
    def analyze_pronunciation(
        self, 
        text: str, 
        audio_file_path: str, 
        language: str = "de"
    ) -> dict:
        """
        分析发音准确度
        
        Args:
            text: 要分析的文本
            audio_file_path: 音频文件路径
            language: 语言代码 (de/en)
        """
        # 读取音频文件并转换为base64
        with open(audio_file_path, 'rb') as f:
            audio_content = f.read()
        
        audio_base64 = "data:audio/ogg;base64," + base64.b64encode(audio_content).decode('utf-8')
        
        payload = {
            "text": text,
            "audio_base64": audio_base64,
            "language": language
        }
        
        response = self.session.post(
            f"{self.base_url}/api/v1/pronunciation",
            json=payload
        )
        response.raise_for_status()
        return response.json()
    
    def analyze_pronunciation_file(
        self, 
        text: str, 
        audio_file_path: str, 
        language: str = "de"
    ) -> dict:
        """
        通过文件上传分析发音
        """
        with open(audio_file_path, 'rb') as f:
            files = {"audio_file": f}
            data = {
                "text": text,
                "language": language
            }
            
            response = self.session.post(
                f"{self.base_url}/api/v1/pronunciation/file",
                files=files,
                data=data
            )
            response.raise_for_status()
            return response.json()
    
    def text_to_speech(
        self, 
        text: str, 
        language: str = "de", 
        voice_speed: float = 1.0,
        save_path: Optional[str] = None
    ) -> dict:
        """
        文本转语音
        
        Args:
            text: 要转换的文本
            language: 语言代码
            voice_speed: 语音速度
            save_path: 保存音频文件的路径 (可选)
        """
        payload = {
            "text": text,
            "language": language,
            "voice_speed": voice_speed
        }
        
        response = self.session.post(
            f"{self.base_url}/api/v1/tts",
            json=payload
        )
        response.raise_for_status()
        result = response.json()
        
        # 如果指定了保存路径，保存音频文件
        if save_path and result.get("audio_base64"):
            audio_data = base64.b64decode(result["audio_base64"].split(',')[1])
            with open(save_path, 'wb') as f:
                f.write(audio_data)
            result["saved_to"] = save_path
        
        return result
    
    def get_sample(self, category: str = "0", language: str = "de") -> dict:
        """
        获取练习样本
        
        Args:
            category: 难度级别 (0-3)
            language: 语言代码
        """
        payload = {
            "category": category,
            "language": language
        }
        
        response = self.session.post(
            f"{self.base_url}/api/v1/sample",
            json=payload
        )
        response.raise_for_status()
        return response.json()
    
    def get_supported_languages(self) -> dict:
        """获取支持的语言"""
        response = self.session.get(f"{self.base_url}/api/v1/languages")
        response.raise_for_status()
        return response.json()
    
    def get_difficulty_categories(self) -> dict:
        """获取难度分类"""
        response = self.session.get(f"{self.base_url}/api/v1/categories")
        response.raise_for_status()
        return response.json()

# 使用示例
if __name__ == "__main__":
    # 创建客户端
    client = AITrainerClient("http://localhost:8000")
    
    try:
        # 健康检查
        health = client.health_check()
        print("✅ 服务器状态:", health)
        
        # 获取练习样本
        sample = client.get_sample(category="0", language="de")
        print("📝 练习样本:", sample["real_transcript"])
        
        # 文本转语音示例
        tts_result = client.text_to_speech(
            text="Hallo, wie geht es dir?",
            language="de",
            save_path="output.wav"
        )
        print("🔊 语音生成:", tts_result["message"])
        
        # 发音分析示例 (需要音频文件)
        # pronunciation_result = client.analyze_pronunciation_file(
        #     text="Hallo",
        #     audio_file_path="recording.wav",
        #     language="de"
        # )
        # print("📊 发音评分:", pronunciation_result["pronunciation_accuracy"])
        
    except Exception as e:
        print(f"❌ 错误: {e}")