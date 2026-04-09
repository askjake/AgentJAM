#!/usr/bin/env python3
"""
Integration script to add message summarization to intelligent_backend.py
"""

import re
import sys

def integrate_summarizer(backend_file):
    """Add message summarization integration to backend"""
    
    with open(backend_file, 'r') as f:
        content = f.read()
    
    # 1. Add import after other imports
    import_addition = """
# ============================================================================
# MESSAGE SUMMARIZATION MODULE
# ============================================================================
try:
    from message_summarizer import (
        MessageSummarizer,
        AdaptiveMessageManager,
        compress_conversation_history
    )
    
    # Initialize adaptive message manager
    _message_manager = AdaptiveMessageManager(max_context_tokens=16000)
    MESSAGE_SUMMARIZATION_ENABLED = True
    
    print('✅ Message Summarization: ENABLED')
    print('   - Strategy: Compress older messages, keep recent verbatim')
    print('   - Recent window: 10 messages')
    print('   - Compression window: 20 messages')
    print('   - Adaptive context management: ACTIVE')
    
except ImportError as e:
    MESSAGE_SUMMARIZATION_ENABLED = False
    print(f'⚠️  Message Summarization not available: {e}')
except Exception as e:
    MESSAGE_SUMMARIZATION_ENABLED = False
    print(f'❌ Message Summarization init failed: {e}')

"""
    
    # Add after logger setup
    if "logger = logging.getLogger(__name__)" in content:
        content = content.replace(
            "logger = logging.getLogger(__name__)",
            "logger = logging.getLogger(__name__)" + import_addition
        )
        print("✓ Added import section")
    
    # 2. Find and replace the build_enhanced_context function
    # Look for the specific line pattern
    search_pattern = "    recent_msgs = conv['messages'][-10:]"
    
    if search_pattern in content:
        replacement = """    # === MESSAGE SUMMARIZATION ===
    if MESSAGE_SUMMARIZATION_ENABLED and msg_count > 10:
        try:
            # Use adaptive message manager to compress history
            compressed_messages, compression_metadata = _message_manager.manage_context(
                conv['messages']
            )
            recent_msgs = compressed_messages
            
            logger.info(
                f"📊 Context management: {compression_metadata['original_message_count']} → "
                f"{compression_metadata['compressed_message_count']} messages "
                f"({compression_metadata['compression_level']} compression, "
                f"~{compression_metadata.get('tokens_saved', 0)} tokens saved)"
            )
        except Exception as e:
            logger.error(f"Summarization failed, falling back to last 10: {e}")
            recent_msgs = conv['messages'][-10:]
    else:
        # Fallback to traditional approach
        recent_msgs = conv['messages'][-10:]
    # === END SUMMARIZATION ==="""
        
        content = content.replace(search_pattern, replacement)
        print("✓ Modified build_enhanced_context function")
    else:
        print("⚠️  Could not find the exact pattern to replace")
    
    # 3. Add statistics endpoint
    stats_endpoint = """

@app.route('/api/summarization/stats', methods=['GET'])
def summarization_stats():
    \"\"\"Get message summarization statistics\"\"\"
    try:
        if not MESSAGE_SUMMARIZATION_ENABLED:
            return jsonify({
                'enabled': False,
                'message': 'Message summarization not available'
            }), 200
        
        stats = {
            'enabled': True,
            'max_context_tokens': _message_manager.max_context_tokens,
            'current_settings': {
                'recent_window': _message_manager.summarizer.recent_window,
                'compression_window': _message_manager.summarizer.compression_window,
                'max_summary_length': _message_manager.summarizer.max_summary_length
            },
            'conversations': []
        }
        
        # Get stats per conversation
        for chat_id, conv in conversations.items():
            msg_count = len(conv['messages'])
            if msg_count > 10:
                # Calculate what compression would do
                total_chars = sum(len(str(m.get('content', ''))) for m in conv['messages'])
                estimated_tokens = total_chars // 4
                
                stats['conversations'].append({
                    'chat_id': chat_id,
                    'message_count': msg_count,
                    'estimated_tokens': estimated_tokens,
                    'would_compress': estimated_tokens > _message_manager.max_context_tokens * 0.7
                })
        
        return jsonify(stats), 200
        
    except Exception as e:
        logger.error(f"Summarization stats error: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500
"""
    
    # Add before main
    if "if __name__ == '__main__':" in content:
        content = content.replace(
            "if __name__ == '__main__':",
            stats_endpoint + "\nif __name__ == '__main__':"
        )
        print("✓ Added summarization stats endpoint")
    
    return content

if __name__ == '__main__':
    backend_file = sys.argv[1] if len(sys.argv) > 1 else 'intelligent_backend.py'
    
    print(f"Integrating message summarization into {backend_file}...")
    
    modified_content = integrate_summarizer(backend_file)
    
    if modified_content:
        output_file = backend_file
        with open(output_file, 'w') as f:
            f.write(modified_content)
        print(f"\n✅ Integration complete! Modified file: {output_file}")
        print("\nChanges made:")
        print("  1. Added message summarization imports and initialization")
        print("  2. Modified build_enhanced_context() to use adaptive compression")
        print("  3. Added /api/summarization/stats endpoint")
    else:
        print("\n❌ Integration failed")
        sys.exit(1)
