/**
 * API client for Mirmer AI backend with SSE support.
 */

const API_BASE = '/api';

/**
 * Send message and stream 3-stage council process via Server-Sent Events.
 * 
 * @param {string} conversationId - Conversation UUID
 * @param {string} content - User message content
 * @param {Function} onEvent - Callback for each SSE event (eventType, eventData)
 * @param {string} apiKey - Optional OpenRouter API key
 * 
 * Requirements: 2.4
 */
export async function sendMessageStream(conversationId, content, onEvent, apiKey = null) {
  const response = await fetch(`${API_BASE}/conversations/${conversationId}/message/stream`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ 
      content,
      api_key: apiKey 
    }),
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  try {
    while (true) {
      const { done, value } = await reader.read();
      
      if (done) {
        break;
      }

      // Decode the chunk
      const chunk = decoder.decode(value, { stream: true });
      
      // Split by newlines to handle multiple events
      const lines = chunk.split('\n');
      
      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.slice(6); // Remove 'data: ' prefix
          
          try {
            const event = JSON.parse(data);
            onEvent(event.type, event.data || event.message);
          } catch (e) {
            console.error('Error parsing SSE event:', e);
          }
        }
      }
    }
  } finally {
    reader.releaseLock();
  }
}

/**
 * Create a new conversation.
 * 
 * @returns {Promise<Object>} Conversation object with id, title, created_at
 */
export async function createConversation() {
  const response = await fetch(`${API_BASE}/conversations`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json();
}

/**
 * List all conversations.
 * 
 * @returns {Promise<Array>} Array of conversation metadata
 */
export async function listConversations() {
  const response = await fetch(`${API_BASE}/conversations`);

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const data = await response.json();
  return data.conversations;
}

/**
 * Get a specific conversation.
 * 
 * @param {string} conversationId - Conversation UUID
 * @returns {Promise<Object>} Full conversation object
 */
export async function getConversation(conversationId) {
  const response = await fetch(`${API_BASE}/conversations/${conversationId}`);

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json();
}

export const api = {
  sendMessageStream,
  createConversation,
  listConversations,
  getConversation,
};
