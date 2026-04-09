import base64
import io
import re
from PIL import Image
import logging

logger = logging.getLogger(__name__)

def compress_image_if_needed(base64_data: str, media_type: str, max_size_kb: int = 800) -> tuple:
    """
    Compress image if it exceeds max_size_kb
    Returns: (compressed_base64_data, new_media_type, was_compressed)
    """
    try:
        # Decode base64 to bytes
        image_bytes = base64.b64decode(base64_data)
        current_size_kb = len(image_bytes) / 1024
        
        logger.info(f"Image size: {current_size_kb:.1f}KB (limit: {max_size_kb}KB)")
        
        # If under limit, return as-is
        if current_size_kb <= max_size_kb:
            logger.info("✅ Image within size limit, no compression needed")
            return base64_data, media_type, False
        
        # Open image with PIL
        img = Image.open(io.BytesIO(image_bytes))
        original_format = img.format or 'JPEG'
        
        logger.info(f"🔄 Compressing {original_format} image ({img.size[0]}x{img.size[1]})")
        
        # Convert RGBA to RGB if needed
        if img.mode == 'RGBA':
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])
            img = background
        elif img.mode not in ('RGB', 'L'):
            img = img.convert('RGB')
        
        # Start with max dimensions of 1920x1920 (good for vision models)
        max_dimension = 1920
        if max(img.size) > max_dimension:
            ratio = max_dimension / max(img.size)
            new_size = tuple(int(dim * ratio) for dim in img.size)
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            logger.info(f"📐 Resized to {img.size[0]}x{img.size[1]}")
        
        # Try progressive quality reduction
        for quality in [85, 75, 65, 55, 45]:
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG', quality=quality, optimize=True)
            compressed_bytes = buffer.getvalue()
            compressed_size_kb = len(compressed_bytes) / 1024
            
            logger.info(f"📊 Quality {quality}: {compressed_size_kb:.1f}KB")
            
            if compressed_size_kb <= max_size_kb:
                compressed_base64 = base64.b64encode(compressed_bytes).decode('utf-8')
                logger.info(f"✅ Compressed {current_size_kb:.1f}KB → {compressed_size_kb:.1f}KB (quality={quality})")
                return compressed_base64, 'image/jpeg', True
        
        # If still too large, use the last attempt
        compressed_base64 = base64.b64encode(compressed_bytes).decode('utf-8')
        final_size_kb = len(compressed_bytes) / 1024
        logger.warning(f"⚠️ Compressed to minimum: {final_size_kb:.1f}KB (may still be large)")
        return compressed_base64, 'image/jpeg', True
        
    except Exception as e:
        logger.error(f"❌ Compression failed: {e}")
        return base64_data, media_type, False


def process_messages_with_attachments(messages: list, attachments: list) -> list:
    """Enhanced version with image compression"""
    logger.info(f'🔄 process_messages_with_attachments called with {len(messages)} messages, {len(attachments)} attachments')
    
    enhanced_messages = []
    for msg in messages:
        if msg.get('role') == 'user':
            msg_attachments = attachments if msg == messages[-1] else []
            if msg_attachments:
                content_parts = []
                text_content = msg.get('content', '')
                if text_content:
                    content_parts.append({'type': 'text', 'text': text_content})
                
                for attachment in msg_attachments:
                    try:
                        if not attachment.get('isImage', False):
                            continue
                        
                        att_content = attachment.get('content', '')
                        match = re.match(r'data:([^;]+);base64,(.+)', att_content)
                        if match:
                            media_type = match.group(1)
                            image_data = match.group(2)
                            att_name = attachment.get('name', 'unknown')
                            
                            # Compress if needed
                            compressed_data, new_media_type, was_compressed = compress_image_if_needed(
                                image_data, media_type, max_size_kb=800
                            )
                            
                            status = "🗜️ (compressed)" if was_compressed else "✅ (original)"
                            logger.info(f"Added image: {att_name} {status}")
                            
                            content_parts.append({
                                'type': 'image',
                                'source': {
                                    'type': 'base64',
                                    'media_type': new_media_type,
                                    'data': compressed_data
                                }
                            })
                    except Exception as e:
                        logger.error(f"Error processing attachment: {e}")
                
                if len(content_parts) > 1:
                    enhanced_messages.append({'role': 'user', 'content': content_parts})
                elif content_parts:
                    enhanced_messages.append({'role': 'user', 'content': content_parts[0].get('text', msg.get('content', ''))})
                else:
                    enhanced_messages.append(msg)
            else:
                enhanced_messages.append(msg)
        else:
            enhanced_messages.append(msg)
    
    return enhanced_messages
