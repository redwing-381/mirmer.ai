import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import ConversationPrintView from '../ConversationPrintView';

/**
 * Tests for ConversationPrintView component
 * Requirements: 1.2, 1.3, 3.2, 3.3
 */
describe('ConversationPrintView', () => {
  const mockConversation = {
    id: 'test-123',
    title: 'Test Conversation',
    created_at: '2024-01-01T00:00:00Z',
    messages: [
      {
        role: 'user',
        content: 'Hello, this is a test question'
      },
      {
        role: 'assistant',
        stage1: [
          { model: 'Model A', response: 'Response from Model A' },
          { model: 'Model B', response: 'Response from Model B' }
        ],
        stage2: [
          { model: 'Model A', ranking: 'Model B is better because...' },
          { model: 'Model B', ranking: 'Model A is better because...' }
        ],
        stage3: {
          response: 'Final synthesis from chairman'
        }
      }
    ]
  };

  it('renders conversation title and metadata', () => {
    render(
      <ConversationPrintView 
        conversation={mockConversation} 
        onClose={vi.fn()}
        autoPrint={false}
      />
    );

    expect(screen.getByText('Test Conversation')).toBeInTheDocument();
    expect(screen.getByText(/Conversation ID:/)).toBeInTheDocument();
    expect(screen.getByText(/test-123/)).toBeInTheDocument();
  });

  it('renders user messages', () => {
    render(
      <ConversationPrintView 
        conversation={mockConversation} 
        onClose={vi.fn()}
        autoPrint={false}
      />
    );

    expect(screen.getByText('Hello, this is a test question')).toBeInTheDocument();
  });

  it('renders all three stages for assistant messages', () => {
    render(
      <ConversationPrintView 
        conversation={mockConversation} 
        onClose={vi.fn()}
        autoPrint={false}
      />
    );

    // Stage 1
    expect(screen.getByText('Stage 1: Individual Model Responses')).toBeInTheDocument();
    expect(screen.getByText('Model A')).toBeInTheDocument();
    expect(screen.getByText('Response from Model A')).toBeInTheDocument();

    // Stage 2
    expect(screen.getByText('Stage 2: Peer Rankings')).toBeInTheDocument();
    expect(screen.getByText(/Model A's Rankings/)).toBeInTheDocument();

    // Stage 3
    expect(screen.getByText('Stage 3: Chairman Synthesis')).toBeInTheDocument();
    expect(screen.getByText('Final synthesis from chairman')).toBeInTheDocument();
  });

  it('handles missing conversation data gracefully', () => {
    render(
      <ConversationPrintView 
        conversation={null} 
        onClose={vi.fn()}
        autoPrint={false}
      />
    );

    expect(screen.getByText(/Error: No conversation data available/)).toBeInTheDocument();
  });

  it('renders close button when onClose is provided', () => {
    const onClose = vi.fn();
    render(
      <ConversationPrintView 
        conversation={mockConversation} 
        onClose={onClose}
        autoPrint={false}
      />
    );

    expect(screen.getByText('Close Print View')).toBeInTheDocument();
  });
});
