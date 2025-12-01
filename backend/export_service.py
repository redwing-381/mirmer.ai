"""
Export service for generating conversation exports in various formats.

Supports:
- Markdown export with formatted conversation content
- JSON export with complete conversation data structure
- PDF export (to be implemented with WeasyPrint)

Requirements: 3.2, 3.3, 3.4
"""
import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

logger = logging.getLogger(__name__)


def validate_conversation_data(conversation: Dict[str, Any]) -> List[str]:
    """
    Validate conversation has complete data for export.
    
    Args:
        conversation: Conversation dictionary with messages
        
    Returns:
        List of warning messages for missing data (empty list if all data present)
        
    Requirements: 2.3, 2.4
    """
    warnings = []
    
    messages = conversation.get('messages', [])
    if not messages:
        warnings.append("Conversation has no messages")
        return warnings
    
    for i, msg in enumerate(messages):
        if msg.get('role') == 'assistant':
            # Check Stage 1
            stage1 = msg.get('stage1')
            if not stage1 or len(stage1) == 0:
                warnings.append(f"Message {i + 1}: Missing or empty Stage 1 data")
            
            # Check Stage 2
            stage2 = msg.get('stage2')
            if not stage2 or len(stage2) == 0:
                warnings.append(f"Message {i + 1}: Missing or empty Stage 2 data")
            
            # Check Stage 3
            stage3 = msg.get('stage3')
            if not stage3:
                warnings.append(f"Message {i + 1}: Missing Stage 3 data")
            elif not stage3.get('response') and not stage3.get('final_answer'):
                warnings.append(f"Message {i + 1}: Stage 3 has no response content")
    
    return warnings


class ExportService:
    """Service for exporting conversations to various formats."""
    
    @staticmethod
    def export_to_markdown(conversation: Dict[str, Any]) -> str:
        """
        Export conversation to Markdown format.
        
        Args:
            conversation: Conversation dictionary with messages
            
        Returns:
            Formatted Markdown string
            
        Requirements: 3.2, 3.1, 5.4
        """
        try:
            # Validate conversation data
            warnings = validate_conversation_data(conversation)
            if warnings:
                logger.warning(f"Markdown export validation warnings for conversation {conversation.get('id')}:")
                for warning in warnings:
                    logger.warning(f"  - {warning}")
            
            lines = []
            
            # Header
            lines.append(f"# {conversation.get('title', 'Conversation')}")
            lines.append("")
            lines.append(f"**Created:** {conversation.get('created_at', 'Unknown')}")
            lines.append(f"**ID:** {conversation.get('id', 'Unknown')}")
            lines.append("")
            
            # Add warnings if any
            if warnings:
                lines.append("> **⚠️ Export Warnings:**")
                for warning in warnings:
                    lines.append(f"> - {warning}")
                lines.append("")
            
            lines.append("---")
            lines.append("")
            
            # Messages
            messages = conversation.get('messages', [])
            
            for i, message in enumerate(messages, 1):
                role = message.get('role', 'unknown')
                
                if role == 'user':
                    # User message
                    content = message.get('content', '')
                    lines.append(f"## Message {i}: User")
                    lines.append("")
                    lines.append(content)
                    lines.append("")
                    
                elif role == 'assistant':
                    # Assistant message with 3 stages
                    lines.append(f"## Message {i}: Assistant Response")
                    lines.append("")
                    
                    # Stage 1: Individual Responses
                    stage1 = message.get('stage1', [])
                    if stage1:
                        lines.append("### Stage 1: Individual Model Responses")
                        lines.append("")
                        for response in stage1:
                            model = response.get('model', 'Unknown')
                            content = response.get('response', '')
                            lines.append(f"#### {model}")
                            lines.append("")
                            lines.append(content)
                            lines.append("")
                    
                    # Stage 2: Peer Rankings
                    stage2 = message.get('stage2', [])
                    if stage2:
                        lines.append("### Stage 2: Peer Rankings")
                        lines.append("")
                        for ranking in stage2:
                            model = ranking.get('model', 'Unknown')
                            # Use 'ranking' field (full text) instead of 'rankings' list
                            ranking_text = ranking.get('ranking', '')
                            lines.append(f"#### {model}'s Rankings")
                            lines.append("")
                            lines.append(ranking_text)
                            lines.append("")
                    
                    # Stage 3: Final Synthesis
                    stage3 = message.get('stage3', {})
                    if stage3:
                        lines.append("### Stage 3: Chairman Synthesis")
                        lines.append("")
                        # Use 'response' field instead of 'final_answer'
                        final_answer = stage3.get('response', stage3.get('final_answer', ''))
                        lines.append(final_answer)
                        lines.append("")
                
                lines.append("---")
                lines.append("")
            
            return "\n".join(lines)
            
        except Exception as e:
            logger.error(f"Error exporting to Markdown: {str(e)}", exc_info=True)
            raise
    
    @staticmethod
    def export_to_json(conversation: Dict[str, Any]) -> str:
        """
        Export conversation to JSON format.
        
        Args:
            conversation: Conversation dictionary
            
        Returns:
            JSON string with complete conversation data
            
        Requirements: 3.4, 3.2, 5.4
        """
        try:
            # Validate conversation data
            warnings = validate_conversation_data(conversation)
            if warnings:
                logger.warning(f"JSON export validation warnings for conversation {conversation.get('id')}:")
                for warning in warnings:
                    logger.warning(f"  - {warning}")
            
            # Create a clean copy with all data
            export_data = {
                "id": conversation.get("id"),
                "title": conversation.get("title"),
                "created_at": conversation.get("created_at"),
                "updated_at": conversation.get("updated_at"),
                "user_id": conversation.get("user_id"),
                "messages": conversation.get("messages", []),
                "exported_at": datetime.utcnow().isoformat(),
                "validation_warnings": warnings  # Include warnings in JSON
            }
            
            # Pretty print JSON
            return json.dumps(export_data, indent=2, ensure_ascii=False)
            
        except Exception as e:
            logger.error(f"Error exporting to JSON: {str(e)}", exc_info=True)
            raise
    
    @staticmethod
    def export_to_pdf(conversation: Dict[str, Any]) -> bytes:
        """
        Export conversation to PDF format using WeasyPrint.
        
        Args:
            conversation: Conversation dictionary
            
        Returns:
            PDF file as bytes
            
        Raises:
            ValueError: If PDF generation fails or returns empty bytes
            ImportError: If WeasyPrint is not installed
            Exception: For other PDF generation errors
            
        Requirements: 3.3, 2.4, 5.4
        """
        try:
            from weasyprint import HTML
            from jinja2 import Environment, FileSystemLoader
            import os
            
            # Validate conversation data
            warnings = validate_conversation_data(conversation)
            if warnings:
                logger.warning(f"PDF export validation warnings for conversation {conversation.get('id')}:")
                for warning in warnings:
                    logger.warning(f"  - {warning}")
            
            # Get the template directory
            template_dir = os.path.join(os.path.dirname(__file__), 'templates')
            
            if not os.path.exists(template_dir):
                logger.error(f"Template directory not found: {template_dir}")
                raise ValueError(f"Template directory not found: {template_dir}")
            
            # Set up Jinja2 environment
            try:
                env = Environment(loader=FileSystemLoader(template_dir))
                template = env.get_template('conversation_pdf.html')
            except Exception as e:
                logger.error(f"Failed to load PDF template: {str(e)}", exc_info=True)
                raise ValueError(f"PDF template not found or invalid: {str(e)}")
            
            # Prepare template data
            template_data = {
                'title': conversation.get('title', 'Conversation'),
                'created_at': conversation.get('created_at', 'Unknown'),
                'conversation_id': conversation.get('id', 'Unknown'),
                'exported_at': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC'),
                'messages': conversation.get('messages', []),
                'warnings': warnings  # Pass warnings to template
            }
            
            # Render HTML
            try:
                html_content = template.render(**template_data)
            except Exception as e:
                logger.error(f"Failed to render PDF template: {str(e)}", exc_info=True)
                raise ValueError(f"PDF template rendering failed: {str(e)}")
            
            # Generate PDF
            try:
                pdf_bytes = HTML(string=html_content).write_pdf()
            except Exception as e:
                logger.error(f"WeasyPrint PDF generation failed: {str(e)}", exc_info=True)
                raise ValueError(f"PDF generation failed: {str(e)}")
            
            # Validate PDF output
            if not pdf_bytes or len(pdf_bytes) == 0:
                logger.error("PDF generation returned empty bytes")
                raise ValueError("PDF generation failed: empty output")
            
            if warnings:
                logger.info(f"✅ PDF export successful for {conversation.get('id')} ({len(pdf_bytes)} bytes, {len(warnings)} warnings)")
            else:
                logger.info(f"✅ PDF export successful for {conversation.get('id')} ({len(pdf_bytes)} bytes)")
            
            return pdf_bytes
            
        except ImportError as e:
            logger.error(f"WeasyPrint not installed: {str(e)}", exc_info=True)
            raise ImportError("WeasyPrint is required for PDF export. Install with: pip install weasyprint")
        except Exception as e:
            logger.error(f"Error exporting to PDF: {str(e)}", exc_info=True)
            raise


def generate_export_filename(conversation: Dict[str, Any], format: str) -> str:
    """
    Generate a filename for the export.
    
    Args:
        conversation: Conversation dictionary
        format: Export format ('markdown', 'json', 'pdf')
        
    Returns:
        Filename string
    """
    title = conversation.get('title', 'conversation')
    # Sanitize title for filename
    safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
    safe_title = safe_title.replace(' ', '_')[:50]  # Limit length
    
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    
    extensions = {
        'markdown': 'md',
        'json': 'json',
        'pdf': 'pdf'
    }
    
    ext = extensions.get(format, 'txt')
    
    return f"{safe_title}_{timestamp}.{ext}"
