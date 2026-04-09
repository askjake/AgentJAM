#!/usr/bin/env python3
"""
Message Summarization Strategy for Intelligent Backend
Compresses older messages rather than dropping them entirely.
"""

import json
import logging
from typing import List, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class MessageSummarizer:
    """
    Implements intelligent message compression strategy:
    - Keeps recent messages verbatim
    - Compresses older messages into summaries
    - Maintains critical context (tool calls, decisions, etc.)
    """
    
    def __init__(
        self,
        recent_window: int = 10,
        compression_window: int = 20,
        max_summary_length: int = 200
    ):
        """
        Initialize the summarizer.
        
        Args:
            recent_window: Number of most recent messages to keep verbatim
            compression_window: Number of older messages to compress
            max_summary_length: Maximum length for each compressed message
        """
        self.recent_window = recent_window
        self.compression_window = compression_window
        self.max_summary_length = max_summary_length
        
    def compress_messages(
        self,
        messages: List[Dict[str, Any]],
        preserve_tool_calls: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Compress message history intelligently.
        
        Returns:
            - Recent messages (verbatim)
            - Compressed older messages
            - System summaries of ancient history
        """
        if len(messages) <= self.recent_window:
            # No compression needed
            return messages
        
        # Split messages into segments
        total_msgs = len(messages)
        
        # Calculate boundaries
        recent_start = max(0, total_msgs - self.recent_window)
        compression_start = max(0, recent_start - self.compression_window)
        
        # Segment 1: Ancient history (oldest) - create high-level summary
        ancient_msgs = messages[:compression_start]
        
        # Segment 2: Middle history - compress individual messages
        middle_msgs = messages[compression_start:recent_start]
        
        # Segment 3: Recent history - keep verbatim
        recent_msgs = messages[recent_start:]
        
        compressed_history = []
        
        # Add ancient history summary if exists
        if ancient_msgs:
            ancient_summary = self._create_conversation_summary(ancient_msgs)
            compressed_history.append({
                'role': 'system',
                'content': f"[CONVERSATION SUMMARY - {len(ancient_msgs)} messages]\n{ancient_summary}",
                'timestamp': ancient_msgs[-1].get('timestamp', ''),
                'is_summary': True,
                'original_message_count': len(ancient_msgs)
            })
        
        # Compress middle messages individually
        for msg in middle_msgs:
            compressed_msg = self._compress_single_message(msg, preserve_tool_calls)
            compressed_history.append(compressed_msg)
        
        # Add recent messages verbatim
        compressed_history.extend(recent_msgs)
        
        logger.info(
            f"📊 Message compression: {total_msgs} → {len(compressed_history)} "
            f"({len(ancient_msgs)} summarized, {len(middle_msgs)} compressed, "
            f"{len(recent_msgs)} verbatim)"
        )
        
        return compressed_history
    
    def _compress_single_message(
        self,
        message: Dict[str, Any],
        preserve_tool_calls: bool = True
    ) -> Dict[str, Any]:
        """
        Compress a single message while preserving key information.
        """
        role = message.get('role', 'user')
        content = message.get('content', '')
        tool_calls = message.get('tool_calls', [])
        
        # Extract key information
        compressed_msg = {
            'role': role,
            'timestamp': message.get('timestamp', ''),
            'is_compressed': True
        }
        
        # Compress content
        if len(content) > self.max_summary_length:
            # Extract key phrases and concepts
            compressed_content = self._extract_key_content(content)
            compressed_msg['content'] = f"[COMPRESSED] {compressed_content}"
            compressed_msg['original_length'] = len(content)
        else:
            compressed_msg['content'] = content
        
        # Preserve tool calls if requested (they contain important context)
        if preserve_tool_calls and tool_calls:
            tool_summary = self._summarize_tool_calls(tool_calls)
            compressed_msg['content'] += f"\n[Tools: {tool_summary}]"
            compressed_msg['tool_calls'] = tool_calls
        
        return compressed_msg
    
    def _extract_key_content(self, content: str) -> str:
        """
        Extract key content from a message.
        Focuses on:
        - Questions
        - Commands
        - Key facts
        - Decisions
        """
        lines = content.split('\n')
        key_parts = []
        
        # Look for questions
        questions = [line for line in lines if '?' in line]
        if questions:
            key_parts.append(questions[0].strip())
        
        # Look for commands/requests (starts with action verbs)
        action_verbs = ['find', 'search', 'create', 'update', 'delete', 'check', 
                       'list', 'show', 'get', 'set', 'run', 'execute', 'deploy']
        commands = [
            line for line in lines 
            if any(line.lower().strip().startswith(verb) for verb in action_verbs)
        ]
        if commands:
            key_parts.append(commands[0].strip())
        
        # If no specific patterns found, take first and last sentences
        if not key_parts:
            sentences = [s.strip() for s in content.split('.') if s.strip()]
            if sentences:
                if len(sentences) == 1:
                    key_parts.append(sentences[0])
                else:
                    key_parts.append(sentences[0])
                    if sentences[-1] != sentences[0]:
                        key_parts.append(sentences[-1])
        
        extracted = ' ... '.join(key_parts)
        
        # Truncate to max length if still too long
        if len(extracted) > self.max_summary_length:
            extracted = extracted[:self.max_summary_length - 3] + '...'
        
        return extracted or content[:self.max_summary_length]
    
    def _summarize_tool_calls(self, tool_calls: List[Dict[str, Any]]) -> str:
        """
        Create a brief summary of tool calls.
        """
        if not tool_calls:
            return ""
        
        tool_names = [tc.get('function', {}).get('name', 'unknown') 
                     for tc in tool_calls]
        
        if len(tool_names) == 1:
            return tool_names[0]
        elif len(tool_names) <= 3:
            return ', '.join(tool_names)
        else:
            return f"{', '.join(tool_names[:2])}, +{len(tool_names)-2} more"
    
    def _create_conversation_summary(
        self,
        messages: List[Dict[str, Any]]
    ) -> str:
        """
        Create a high-level summary of a conversation segment.
        """
        user_messages = [m for m in messages if m.get('role') == 'user']
        assistant_messages = [m for m in messages if m.get('role') == 'assistant']
        
        # Extract topics
        topics = self._extract_topics(messages)
        
        # Count tool usage
        all_tool_calls = []
        for msg in assistant_messages:
            all_tool_calls.extend(msg.get('tool_calls', []))
        
        tool_names = set(
            tc.get('function', {}).get('name', 'unknown')
            for tc in all_tool_calls
        )
        
        # Build summary
        summary_parts = [
            f"Conversation covered: {', '.join(topics) if topics else 'general discussion'}",
            f"{len(user_messages)} user messages, {len(assistant_messages)} responses"
        ]
        
        if tool_names:
            summary_parts.append(f"Tools used: {', '.join(sorted(tool_names))}")
        
        return ' | '.join(summary_parts)
    
    def _extract_topics(
        self,
        messages: List[Dict[str, Any]]
    ) -> List[str]:
        """
        Extract main topics from messages using simple keyword extraction.
        """
        # Common technical topics
        topic_keywords = {
            'deployment': ['deploy', 'deployment', 'release'],
            'errors': ['error', 'bug', 'issue', 'problem', 'fail'],
            'database': ['database', 'db', 'sql', 'query'],
            'api': ['api', 'endpoint', 'rest', 'graphql'],
            'kubernetes': ['k8s', 'kubernetes', 'pod', 'deployment', 'service'],
            'logs': ['log', 'logs', 'logging'],
            'monitoring': ['monitor', 'metrics', 'alert'],
            'configuration': ['config', 'configure', 'settings'],
            'analysis': ['analyze', 'analysis', 'investigate']
        }
        
        detected_topics = set()
        
        for msg in messages:
            content = msg.get('content', '').lower()
            for topic, keywords in topic_keywords.items():
                if any(keyword in content for keyword in keywords):
                    detected_topics.add(topic)
        
        return list(detected_topics)[:3]  # Return top 3 topics


class AdaptiveMessageManager:
    """
    Adaptive message manager that adjusts compression based on context length.
    """
    
    def __init__(self, max_context_tokens: int = 16000):
        self.max_context_tokens = max_context_tokens
        self.summarizer = MessageSummarizer()
    
    def manage_context(
        self,
        messages: List[Dict[str, Any]],
        system_prompt: str = ""
    ) -> tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """
        Manage message context to stay within token limits.
        
        Returns:
            (managed_messages, metadata)
        """
        # Estimate token count (rough: 1 token ≈ 4 chars)
        total_chars = sum(len(str(m.get('content', ''))) for m in messages)
        total_chars += len(system_prompt)
        estimated_tokens = total_chars // 4
        
        metadata = {
            'original_message_count': len(messages),
            'estimated_tokens': estimated_tokens,
            'compression_applied': False,
            'compression_level': 'none'
        }
        
        # If under limit, return as-is
        if estimated_tokens < self.max_context_tokens * 0.7:  # 70% threshold
            return messages, metadata
        
        # Apply compression
        logger.info(
            f"⚠️  Context approaching limit: {estimated_tokens}/{self.max_context_tokens} tokens"
        )
        
        # Adjust compression parameters based on how much we need to compress
        if estimated_tokens > self.max_context_tokens * 0.9:
            # Aggressive compression
            self.summarizer.recent_window = 5
            self.summarizer.compression_window = 10
            metadata['compression_level'] = 'aggressive'
        elif estimated_tokens > self.max_context_tokens * 0.8:
            # Moderate compression
            self.summarizer.recent_window = 8
            self.summarizer.compression_window = 15
            metadata['compression_level'] = 'moderate'
        else:
            # Light compression
            self.summarizer.recent_window = 10
            self.summarizer.compression_window = 20
            metadata['compression_level'] = 'light'
        
        compressed_messages = self.summarizer.compress_messages(messages)
        
        metadata['compression_applied'] = True
        metadata['compressed_message_count'] = len(compressed_messages)
        
        # Recalculate tokens
        compressed_chars = sum(len(str(m.get('content', ''))) for m in compressed_messages)
        metadata['compressed_estimated_tokens'] = compressed_chars // 4
        metadata['tokens_saved'] = estimated_tokens - metadata['compressed_estimated_tokens']
        
        logger.info(
            f"✅ Compression complete: {metadata['original_message_count']} → "
            f"{metadata['compressed_message_count']} messages, "
            f"saved ~{metadata['tokens_saved']} tokens"
        )
        
        return compressed_messages, metadata


# Export convenience function for easy integration
def compress_conversation_history(
    messages: List[Dict[str, Any]],
    recent_window: int = 10,
    compression_window: int = 20
) -> List[Dict[str, Any]]:
    """
    Convenience function for quick message compression.
    
    Usage:
        compressed = compress_conversation_history(messages)
    """
    summarizer = MessageSummarizer(
        recent_window=recent_window,
        compression_window=compression_window
    )
    return summarizer.compress_messages(messages)


if __name__ == '__main__':
    # Test the summarizer
    test_messages = [
        {'role': 'user', 'content': 'How do I deploy to production?', 'timestamp': '2024-01-01T10:00:00'},
        {'role': 'assistant', 'content': 'To deploy to production, you should first...', 'timestamp': '2024-01-01T10:01:00'},
        {'role': 'user', 'content': 'What about the database migrations?', 'timestamp': '2024-01-01T10:02:00'},
        {'role': 'assistant', 'content': 'Database migrations should be...', 'timestamp': '2024-01-01T10:03:00', 'tool_calls': [{'function': {'name': 'run_migration'}}]},
    ] * 10  # 40 messages total
    
    compressed = compress_conversation_history(test_messages)
    print(f"Original: {len(test_messages)} messages")
    print(f"Compressed: {len(compressed)} messages")
    print("\nSample compressed message:")
    print(json.dumps(compressed[0], indent=2))
