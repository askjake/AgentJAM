#!/usr/bin/env python3
"""
Custom Tool: Webcam Image Capture
Self-built by the agent for capturing and analyzing webcam images
"""

import cv2
import base64
import sys
import json
from datetime import datetime
import os

def capture_image(device='/dev/video0', output_path=None, return_base64=False):
    """
    Capture an image from webcam
    
    Args:
        device: Video device path (default: /dev/video0)
        output_path: Where to save image (optional)
        return_base64: Return base64 encoded image
    
    Returns:
        dict with status, path, base64_data (if requested)
    """
    try:
        # Open video capture
        cap = cv2.VideoCapture(device)
        
        if not cap.isOpened():
            return {
                'success': False,
                'error': f'Cannot open video device {device}'
            }
        
        # Set resolution
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        # Capture frame
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            return {
                'success': False,
                'error': 'Failed to capture frame'
            }
        
        # Generate filename if not provided
        if output_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = f'/tmp/webcam_capture_{timestamp}.jpg'
        
        # Save image
        cv2.imwrite(output_path, frame)
        
        result = {
            'success': True,
            'path': output_path,
            'device': device,
            'resolution': f'{frame.shape[1]}x{frame.shape[0]}',
            'timestamp': datetime.now().isoformat()
        }
        
        # Add base64 if requested
        if return_base64:
            with open(output_path, 'rb') as f:
                img_data = f.read()
                result['base64'] = base64.b64encode(img_data).decode('utf-8')
        
        return result
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def list_cameras():
    """List available camera devices"""
    devices = []
    for i in range(32):  # Check first 32 devices
        device = f'/dev/video{i}'
        if os.path.exists(device):
            try:
                cap = cv2.VideoCapture(device)
                if cap.isOpened():
                    devices.append({
                        'device': device,
                        'available': True
                    })
                    cap.release()
            except:
                pass
    return devices

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Webcam Capture Tool')
    parser.add_argument('--device', default='/dev/video0', help='Video device')
    parser.add_argument('--output', help='Output path')
    parser.add_argument('--list', action='store_true', help='List cameras')
    parser.add_argument('--base64', action='store_true', help='Return base64')
    
    args = parser.parse_args()
    
    if args.list:
        cameras = list_cameras()
        print(json.dumps({'cameras': cameras}, indent=2))
    else:
        result = capture_image(
            device=args.device,
            output_path=args.output,
            return_base64=args.base64
        )
        print(json.dumps(result, indent=2))
