/**
 * API client for Mirmer AI backend with SSE support.
 */

const API_BASE = import.meta.env.VITE_API_URL 
  ? `${import.meta.env.VITE_API_URL}/api` 
  : '/api';

/**
 * Get headers with user ID
 */
function getHeaders(userId) {
  return {
    'Content-Type': 'application/json',
    'X-User-Id': userId,
  };
}

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
export async function sendMessageStream(conversationId, content, onEvent, userId) {
  const response = await fetch(`${API_BASE}/conversations/${conversationId}/message/stream`, {
    method: 'POST',
    headers: getHeaders(userId),
    body: JSON.stringify({ 
      content
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
export async function createConversation(userId) {
  const response = await fetch(`${API_BASE}/conversations`, {
    method: 'POST',
    headers: getHeaders(userId),
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
export async function listConversations(userId) {
  const response = await fetch(`${API_BASE}/conversations`, {
    headers: getHeaders(userId),
  });

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
export async function getConversation(conversationId, userId) {
  const response = await fetch(`${API_BASE}/conversations/${conversationId}`, {
    headers: getHeaders(userId),
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json();
}

/**
 * Delete a conversation.
 * 
 * @param {string} conversationId - Conversation UUID
 * @returns {Promise<Object>} Success response
 */
export async function deleteConversation(conversationId, userId) {
  const response = await fetch(`${API_BASE}/conversations/${conversationId}`, {
    method: 'DELETE',
    headers: getHeaders(userId),
  });

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
  deleteConversation,
};
