"""
Message Summarization for Conversation History
Implements sliding window + summarization to preserve context
"""

import logging
from typing import List
from datetime import datetime

from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage, ToolMessage

logger = logging.getLogger(__name__)


class ConversationSummarizer:
    """Implements sliding window + summarization to preserve old context"""
    
    def __init__(
        self,
        max_recent_messages: int = 50,
        summarize_threshold: int = 100,
        aggressive_threshold: int = 150
    ):
        """
        Args:
            max_recent_messages: Keep this many recent messages at full fidelity
            summarize_threshold: Start summarizing when message count exceeds this
            aggressive_threshold: More aggressive summarization above this
        """
        self.max_recent = max_recent_messages
        self.summarize_threshold = summarize_threshold
        self.aggressive_threshold = aggressive_threshold
    
    def summarize_messages(self, messages: List[BaseMessage]) -> List[BaseMessage]:
        """
        Apply summarization strategy to messages.
        Returns: Compressed message list with summary + recent messages
        """
        if len(messages) <= self.summarize_threshold:
            # No summarization needed
            return messages
        
        logger.info(f"📊 Summarizing conversation: {len(messages)} messages")
        
        # Split messages into "old" (to summarize) and "recent" (keep full)
        num_to_summarize = len(messages) - self.max_recent
        old_messages = messages[:num_to_summarize]
        recent_messages = messages[num_to_summarize:]
        
        # Create summary
        summary = self._create_summary(old_messages, aggressive=(len(messages) > self.aggressive_threshold))
        
        # Create summary message
        summary_msg = SystemMessage(
            content=f"[CONVERSATION HISTORY SUMMARY - {len(old_messages)} messages compressed]\n\n{summary}",
            additional_kwargs={"compressed_message_count": len(old_messages)}
        )
        
        result = [summary_msg] + recent_messages
        
        logger.info(f"✅ Compressed {len(messages)} → {len(result)} messages")
        logger.info(f"   Summary covers {len(old_messages)} old messages")
        logger.info(f"   Kept {len(recent_messages)} recent messages at full fidelity")
        
        return result
    
    def _create_summary(self, messages: List[BaseMessage], aggressive: bool = False) -> str:
        """Create a structured summary of older messages"""
        
        # Categorize messages
        user_messages = []
        assistant_messages = []
        tool_calls = []
        tool_results = []
        
        for msg in messages:
            if isinstance(msg, HumanMessage):
                content = self._extract_content(msg)
                if content and len(content.strip()) > 0:
                    user_messages.append(content)
            elif isinstance(msg, AIMessage):
                content = self._extract_content(msg)
                if content and len(content.strip()) > 0:
                    assistant_messages.append(content)
                # Track tool usage
                if hasattr(msg, 'tool_calls') and msg.tool_calls:
                    for tc in msg.tool_calls:
                        tool_name = tc.get('name', 'unknown')
                        tool_calls.append(tool_name)
            elif isinstance(msg, ToolMessage):
                content = self._extract_content(msg)
                tool_results.append(content[:200] if content else "")
        
        # Build summary
        summary_parts = []
        
        # User interaction summary
        if user_messages:
            summary_parts.append(f"**User Requests ({len(user_messages)} total):**")
            if aggressive:
                # Very aggressive: just count and show first/last
                summary_parts.append(f"- First: {user_messages[0][:150]}...")
                if len(user_messages) > 1:
                    summary_parts.append(f"- [... {len(user_messages)-2} more requests ...]")
                    summary_parts.append(f"- Last: {user_messages[-1][:150]}...")
            else:
                # Keep more detail
                for i, msg in enumerate(user_messages[:5]):  # First 5
                    summary_parts.append(f"- {msg[:200]}...")
                if len(user_messages) > 5:
                    summary_parts.append(f"- [... {len(user_messages)-5} more requests ...]")
        
        # Assistant response summary
        if assistant_messages:
            summary_parts.append(f"\n**Assistant Responses ({len(assistant_messages)} total):**")
            # Keep last few responses as they contain important context
            for msg in assistant_messages[-3:]:
                summary_parts.append(f"- {msg[:250]}...")
        
        # Tool usage summary
        if tool_calls:
            unique_tools = list(set(tool_calls))
            summary_parts.append(f"\n**Tools Used:** {', '.join(unique_tools)} ({len(tool_calls)} total calls)")
        
        # Metadata
        summary_parts.append(f"\n**Compressed:** {len(messages)} messages at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return "\n".join(summary_parts)
    
    def _extract_content(self, msg: BaseMessage) -> str:
        """Extract text content from message"""
        if isinstance(msg.content, str):
            return msg.content
        elif isinstance(msg.content, list):
            # Handle multi-modal content
            text_parts = []
            for item in msg.content:
                if isinstance(item, dict):
                    if item.get("type") == "text":
                        text_parts.append(item.get("text", ""))
                elif isinstance(item, str):
                    text_parts.append(item)
            return " ".join(text_parts)
        return str(msg.content)


# Singleton instance
_summarizer = None


def get_summarizer() -> ConversationSummarizer:
    """Get or create the conversation summarizer singleton"""
    global _summarizer
    if _summarizer is None:
        _summarizer = ConversationSummarizer(
            max_recent_messages=50,      # Keep last 50 messages
            summarize_threshold=100,      # Start at 100 messages
            aggressive_threshold=150      # More aggressive at 150+
        )
    return _summarizer
