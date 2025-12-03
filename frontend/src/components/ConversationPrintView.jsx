import React, { useEffect } from 'react';
import './ConversationPrintView.css';

/**
 * Print-optimized view of a conversation for PDF export.
 * Renders conversation with all stages in a format suitable for printing.
 * 
 * Requirements: 1.2, 1.3, 3.2, 3.3
 */
export default function ConversationPrintView({ conversation, onClose, autoPrint = true }) {
  useEffect(() => {
    if (autoPrint) {
      // Small delay to ensure rendering is complete
      const timer = setTimeout(() => {
        window.print();
      }, 500);
      
      return () => clearTimeout(timer);
    }
  }, [autoPrint]);

  // Handle after print (close the view)
  useEffect(() => {
    const handleAfterPrint = () => {
      if (onClose) {
        onClose();
      }
    };

    window.addEventListener('afterprint', handleAfterPrint);
    return () => window.removeEventListener('afterprint', handleAfterPrint);
  }, [onClose]);

  if (!conversation) {
    return (
      <div className="print-view-error">
        <p>Error: No conversation data available</p>
      </div>
    );
  }

  // Debug: Log conversation data
  console.log('ConversationPrintView - Full conversation:', conversation);
  console.log('ConversationPrintView - Messages count:', conversation.messages?.length);
  conversation.messages?.forEach((msg, idx) => {
    if (msg.role === 'assistant') {
      console.log(`Message ${idx}:`, {
        hasStage1: !!msg.stage1,
        stage1Count: msg.stage1?.length,
        hasStage2: !!msg.stage2,
        stage2Count: msg.stage2?.length,
        hasStage3: !!msg.stage3,
      });
    }
  });

  const formatDate = (dateString) => {
    if (!dateString) return 'Unknown';
    try {
      return new Date(dateString).toLocaleString();
    } catch {
      return dateString;
    }
  };

  return (
    <div className="conversation-print-view">
      {/* Header with metadata */}
      <header className="print-header">
        <h1>{conversation.title || 'Conversation'}</h1>
        <div className="print-metadata">
          <p><strong>Created:</strong> {formatDate(conversation.created_at)}</p>
          <p><strong>Conversation ID:</strong> {conversation.id}</p>
          <p><strong>Exported:</strong> {new Date().toLocaleString()}</p>
        </div>
      </header>

      {/* Messages */}
      <div className="print-messages">
        {conversation.messages && conversation.messages.map((message, index) => (
          <div key={index} className={`print-message print-message-${message.role}`}>
            {message.role === 'user' ? (
              // User message
              <div className="print-user-message">
                <h2>Message {index + 1}: User</h2>
                <div className="print-content">
                  {message.content}
                </div>
              </div>
            ) : (
              // Assistant message with 3 stages
              <div className="print-assistant-message">
                <h2>Message {index + 1}: Assistant Response</h2>

                {/* Stage 1: Individual Responses */}
                {message.stage1 && message.stage1.length > 0 ? (
                  <div className="print-stage print-stage-1">
                    <h3>Stage 1: Individual Model Responses</h3>
                    {message.stage1.map((response, idx) => (
                      <div key={idx} className="print-model-response">
                        <h4>{response.model || 'Unknown Model'}</h4>
                        <div className="print-content">
                          {response.response || 'No response'}
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="print-stage print-stage-1">
                    <h3>Stage 1: Individual Model Responses</h3>
                    <p className="print-warning">⚠️ Stage 1 data not available</p>
                  </div>
                )}

                {/* Stage 2: Peer Rankings */}
                {message.stage2 && message.stage2.length > 0 ? (
                  <div className="print-stage print-stage-2">
                    <h3>Stage 2: Peer Rankings</h3>
                    {message.stage2.map((ranking, idx) => (
                      <div key={idx} className="print-model-ranking">
                        <h4>{ranking.model || 'Unknown Model'}'s Rankings</h4>
                        <div className="print-content">
                          {ranking.ranking || 'No ranking'}
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="print-stage print-stage-2">
                    <h3>Stage 2: Peer Rankings</h3>
                    <p className="print-warning">⚠️ Stage 2 data not available</p>
                  </div>
                )}

                {/* Stage 3: Final Synthesis */}
                {message.stage3 && (message.stage3.response || message.stage3.final_answer) ? (
                  <div className="print-stage print-stage-3">
                    <h3>Stage 3: Chairman Synthesis</h3>
                    <div className="print-content">
                      {message.stage3.response || message.stage3.final_answer}
                    </div>
                  </div>
                ) : (
                  <div className="print-stage print-stage-3">
                    <h3>Stage 3: Chairman Synthesis</h3>
                    <p className="print-warning">⚠️ Stage 3 data not available</p>
                  </div>
                )}
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Footer */}
      <footer className="print-footer">
        <p>Generated by Mirmer AI - Multi-LLM Consultation System</p>
      </footer>

      {/* Screen-only close button */}
      {onClose && (
        <button className="print-close-button" onClick={onClose}>
          Close Print View
        </button>
      )}
    </div>
  );
}
