import requests
import json
import os
from config import Config

class WhatsAppHandler:
    def __init__(self):
        self.token = Config.WHATSAPP_TOKEN
        self.phone_id = Config.WHATSAPP_PHONE_ID
        self.api_url = f"https://graph.facebook.com/v18.0/{self.phone_id}/messages"
        self.media_url = f"https://graph.facebook.com/v18.0/{self.phone_id}/media"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
    
    def send_message(self, to_phone, message):
        """Send text message"""
        payload = {
            "messaging_product": "whatsapp",
            "to": to_phone,
            "type": "text",
            "text": {"body": message}
        }
        
        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            return response.json()
        except Exception as e:
            print(f"Error sending message: {e}")
            return None
    
    def send_interactive_buttons(self, to_phone, body_text, buttons):
        """Send message with buttons (max 3 buttons)"""
        button_list = []
        for i, btn in enumerate(buttons[:3]):  # WhatsApp allows max 3 buttons
            button_list.append({
                "type": "reply",
                "reply": {
                    "id": f"btn_{i}",
                    "title": btn[:20]  # Max 20 characters
                }
            })
        
        payload = {
            "messaging_product": "whatsapp",
            "to": to_phone,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {"text": body_text},
                "action": {
                    "buttons": button_list
                }
            }
        }
        
        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            return response.json()
        except Exception as e:
            print(f"Error sending buttons: {e}")
            return None
    
    def send_interactive_list(self, to_phone, body_text, button_text, sections):
        """Send message with list (for more than 3 options)"""
        payload = {
            "messaging_product": "whatsapp",
            "to": to_phone,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {"text": body_text},
                "action": {
                    "button": button_text,
                    "sections": sections
                }
            }
        }
        
        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            return response.json()
        except Exception as e:
            print(f"Error sending list: {e}")
            return None
    
    def send_image(self, to_phone, image_path, caption=""):
        """Send image (QR code)"""
        # First upload image
        media_id = self.upload_media(image_path)
        
        if not media_id:
            return None
        
        payload = {
            "messaging_product": "whatsapp",
            "to": to_phone,
            "type": "image",
            "image": {
                "id": media_id,
                "caption": caption
            }
        }
        
        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            return response.json()
        except Exception as e:
            print(f"Error sending image: {e}")
            return None
    
    def upload_media(self, file_path):
        """Upload media to WhatsApp"""
        try:
            with open(file_path, 'rb') as f:
                files = {
                    'file': f,
                    'type': (None, 'image/jpeg'),
                    'messaging_product': (None, 'whatsapp')
                }
                headers = {"Authorization": f"Bearer {self.token}"}
                
                response = requests.post(self.media_url, headers=headers, files=files)
                result = response.json()
                return result.get('id')
        except Exception as e:
            print(f"Error uploading media: {e}")
            return None
    
    def download_media(self, media_id, save_path):
        """Download media from WhatsApp"""
        try:
            # Get media URL
            url = f"https://graph.facebook.com/v18.0/{media_id}"
            headers = {"Authorization": f"Bearer {self.token}"}
            
            response = requests.get(url, headers=headers)
            media_url = response.json().get('url')
            
            if not media_url:
                return None
            
            # Download media
            media_response = requests.get(media_url, headers=headers)
            
            with open(save_path, 'wb') as f:
                f.write(media_response.content)
            
            return save_path
        except Exception as e:
            print(f"Error downloading media: {e}")
            return None
