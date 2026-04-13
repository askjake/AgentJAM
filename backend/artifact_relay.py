#!/usr/bin/env python3
"""
Artifact Relay Module - Addresses diagnostic report issues
Provides multiple methods for file delivery

Author: Enhancement based on diagnostic report
Date: 2026-04-13
"""

import os
import base64
import requests
import logging
from pathlib import Path
from typing import Optional, Dict, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class ArtifactURL:
    local_url: str
    public_url: Optional[str] = None
    inline_base64: Optional[str] = None
    method: str = 'local'
    size: int = 0
    mime_type: str = 'application/octet-stream'
    
class ArtifactRelay:
    INLINE_MAX_SIZE = 500 * 1024
    CLOUD_MAX_SIZE = 100 * 1024 * 1024
    
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or self._detect_base_url()
        logger.info(f"Artifact Relay initialized: {self.base_url}")
        
    def _detect_base_url(self) -> str:
        try:
            result = os.popen("hostname -I | awk '{print $1}'").read().strip()
            if result:
                return f"http://{result}:8000"
            return "http://localhost:8000"
        except:
            return "http://localhost:8000"
    
    def get_mime_type(self, file_path: Path) -> str:
        import mimetypes
        mime_type, _ = mimetypes.guess_type(str(file_path))
        return mime_type or 'application/octet-stream'
    
    def can_inline(self, file_path: Path) -> bool:
        if not file_path.exists():
            return False
        size = file_path.stat().st_size
        mime_type = self.get_mime_type(file_path)
        is_suitable = mime_type.startswith(('image/', 'text/'))
        return is_suitable and (size <= self.INLINE_MAX_SIZE)
    
    def encode_inline(self, file_path: Path) -> Optional[str]:
        if not self.can_inline(file_path):
            return None
        try:
            mime_type = self.get_mime_type(file_path)
            with open(file_path, 'rb') as f:
                data = f.read()
            encoded = base64.b64encode(data).decode('utf-8')
            return f"data:{mime_type};base64,{encoded}"
        except Exception as e:
            logger.error(f"Failed to encode inline: {e}")
            return None
    
    def upload_to_cloud(self, file_path: Path) -> Optional[str]:
        if not file_path.exists():
            return None
        size = file_path.stat().st_size
        if size > self.CLOUD_MAX_SIZE:
            logger.warning(f"File too large: {size}")
            return None
        try:
            filename = file_path.name
            with open(file_path, 'rb') as f:
                response = requests.put(
                    f"https://transfer.sh/{filename}",
                    data=f,
                    timeout=30
                )
            if response.status_code == 200:
                public_url = response.text.strip()
                logger.info(f"Cloud relay OK: {public_url}")
                return public_url
            return None
        except Exception as e:
            logger.error(f"Cloud relay error: {e}")
            return None
    
    def get_artifact_urls(self, chat_id: str, rel_path: str, workspace: Path, use_cloud: bool = False, inline_if_possible: bool = True) -> ArtifactURL:
        full_path = (workspace / rel_path).resolve()
        if not full_path.exists():
            raise FileNotFoundError(f"Not found: {rel_path}")
        size = full_path.stat().st_size
        mime_type = self.get_mime_type(full_path)
        local_url = f"{self.base_url}/api/artifacts/{chat_id}/{rel_path}"
        inline_base64 = None
        if inline_if_possible:
            inline_base64 = self.encode_inline(full_path)
        public_url = None
        method = 'local'
        if use_cloud:
            public_url = self.upload_to_cloud(full_path)
            if public_url:
                method = 'cloud'
        if inline_base64:
            method = 'inline' if not use_cloud else f'{method}+inline'
        return ArtifactURL(local_url=local_url, public_url=public_url, inline_base64=inline_base64, method=method, size=size, mime_type=mime_type)
    
    def format_response(self, artifact_url: ArtifactURL) -> Dict[str, Any]:
        return {
            'local_url': artifact_url.local_url,
            'public_url': artifact_url.public_url,
            'inline_base64': artifact_url.inline_base64,
            'method': artifact_url.method,
            'size': artifact_url.size,
            'size_human': self._format_size(artifact_url.size),
            'mime_type': artifact_url.mime_type,
            'can_inline': artifact_url.inline_base64 is not None,
            'has_public_url': artifact_url.public_url is not None
        }
    
    @staticmethod
    def _format_size(size_bytes: int) -> str:
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"

_artifact_relay = None

def get_artifact_relay() -> ArtifactRelay:
    global _artifact_relay
    if _artifact_relay is None:
        _artifact_relay = ArtifactRelay()
    return _artifact_relay

def get_artifact_url(chat_id: str, rel_path: str, workspace: Path, use_cloud: bool = False) -> Dict[str, Any]:
    relay = get_artifact_relay()
    artifact_url = relay.get_artifact_urls(chat_id, rel_path, workspace, use_cloud=use_cloud)
    return relay.format_response(artifact_url)

if __name__ == '__main__':
    print("Artifact Relay Module - Test OK")
