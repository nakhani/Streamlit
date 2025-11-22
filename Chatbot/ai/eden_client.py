# ai/eden_client.py
import os
import requests
import streamlit as st  # برای نمایش خطا در UI

class EdenClient:
    def __init__(self, api_key: str = None, provider: str = "openai", model: str = "gpt-4o-mini"):
        self.api_key = api_key or os.getenv("EDENAI_API_KEY")
        self.provider = provider
        self.model = model
        self.base = "https://api.edenai.run/v2/text"

    def chat(self, messages):
        """
        messages: list of dicts [{'role': 'user'|'assistant'|'system', 'content': '...'}]
        """
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "providers": self.provider,
            "model": self.model,          # اضافه کردن مدل
            "text": messages[-1]["content"],
            "temperature": 0.7,
            "max_tokens": 512,
        }

        try:
            r = requests.post(f"{self.base}/chat", json=payload, headers=headers, timeout=60)
            r.raise_for_status()
            data = r.json()

            # EdenAI پاسخ را در ساختار provider-specific برمی‌گرداند
            if self.provider in data and "generated_text" in data[self.provider]:
                return data[self.provider]["generated_text"]
            else:
                st.error(f"Unexpected response format: {data}")
                return "Sorry, unexpected response format."

        except requests.exceptions.RequestException as e:
            st.error(f"API connection failed: {e}")
            return "Sorry, connection error."
