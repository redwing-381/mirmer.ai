import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { ExternalLink, BookOpen } from 'lucide-react';
import { Helmet } from 'react-helmet';
import CodeBlock from '../components/ui/CodeBlock';
import TableOfContents from '../components/docs/TableOfContents';

/**
 * SDK Documentation Page
 * Comprehensive documentation for the Mirmer AI Python SDK
 * Follows neobrutalist design aesthetic
 */
export default function DocsPage() {
  const [activeSection, setActiveSection] = useState('installation');

  // Documentation sections for table of contents
  const sections = [
    { id: 'installation', title: 'Installation' },
    { id: 'authentication', title: 'Authentication' },
    { id: 'quick-start', title: 'Quick Start' },
    { id: 'basic-usage', title: 'Basic Usage' },
    { id: 'streaming', title: 'Streaming' },
    { id: 'async-usage', title: 'Async Usage' },
    { id: 'conversations', title: 'Conversation Management' },
    { id: 'usage-stats', title: 'Usage Statistics' },
    { id: 'error-handling', title: 'Error Handling' },
    { id: 'configuration', title: 'Configuration' },
    { id: 'api-reference', title: 'API Reference' },
  ];

  // Intersection Observer for active section tracking
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setActiveSection(entry.target.id);
          }
        });
      },
      {
        threshold: 0.3,
        rootMargin: '-100px 0px -50% 0px',
      }
    );

    sections.forEach((section) => {
      const element = document.getElementById(section.id);
      if (element) observer.observe(element);
    });

    return () => observer.disconnect();
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 relative">
      {/* Skip to Content Link for Screen Readers */}
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:px-6 focus:py-3 focus:bg-yellow-300 focus:border-4 focus:border-black focus:shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] focus:font-bold"
      >
        Skip to main content
      </a>
      
      {/* SEO Meta Tags */}
      <Helmet>
        <title>Mirmer AI Python SDK Documentation - Installation, Usage & API Reference</title>
        <meta 
          name="description" 
          content="Official Python SDK documentation for Mirmer AI multi-LLM consultation system. Learn how to install, authenticate, and use the SDK with comprehensive examples and API reference." 
        />
        <meta 
          name="keywords" 
          content="Mirmer AI, Python SDK, API documentation, multi-LLM, AI consultation, Python library, SDK tutorial, API reference, machine learning, artificial intelligence" 
        />
        <meta name="author" content="Mirmer AI" />
        <meta property="og:title" content="Mirmer AI Python SDK Documentation" />
        <meta property="og:description" content="Official Python SDK documentation with installation guide, usage examples, and complete API reference." />
        <meta property="og:type" content="website" />
        <meta property="og:url" content="https://mirmer.ai/docs" />
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content="Mirmer AI Python SDK Documentation" />
        <meta name="twitter:description" content="Official Python SDK documentation with installation guide, usage examples, and complete API reference." />
        <link rel="canonical" href="https://mirmer.ai/docs" />
        
        {/* Structured Data (JSON-LD) */}
        <script type="application/ld+json">
          {JSON.stringify({
            "@context": "https://schema.org",
            "@type": "TechArticle",
            "headline": "Mirmer AI Python SDK Documentation",
            "description": "Official Python SDK documentation for Mirmer AI multi-LLM consultation system. Installation, usage examples, and API reference.",
            "author": {
              "@type": "Organization",
              "name": "Mirmer AI",
              "url": "https://mirmer.ai"
            },
            "publisher": {
              "@type": "Organization",
              "name": "Mirmer AI",
              "url": "https://mirmer.ai"
            },
            "datePublished": "2024-01-01",
            "dateModified": new Date().toISOString().split('T')[0],
            "inLanguage": "en",
            "about": {
              "@type": "SoftwareApplication",
              "name": "Mirmer AI Python SDK",
              "applicationCategory": "DeveloperApplication",
              "operatingSystem": "Python 3.8+",
              "offers": {
                "@type": "Offer",
                "price": "0",
                "priceCurrency": "USD"
              }
            }
          })}
        </script>
      </Helmet>
      
      {/* Grid Background Pattern */}
      <div 
        className="fixed inset-0 z-0 opacity-[0.03]"
        style={{
          backgroundImage: `
            linear-gradient(to right, black 1px, transparent 1px),
            linear-gradient(to bottom, black 1px, transparent 1px)
          `,
          backgroundSize: '40px 40px',
        }}
      />
      
      {/* Navigation */}
      <nav className="bg-white border-b-4 border-black sticky top-0 z-30 relative">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link to="/" className="flex items-center gap-3">
              <img src="/favicon.png" alt="Mirmer AI Logo" className="w-8 h-8 border-2 border-black" />
              <span className="font-black text-xl">MIRMER AI</span>
            </Link>
            <Link
              to="/"
              className="px-4 py-2 bg-teal-400 border-2 border-black shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[-2px] hover:translate-y-[-2px] transition-all font-bold"
            >
              Back to Home
            </Link>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 relative z-10">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Table of Contents - Sidebar on desktop */}
          <aside className="lg:w-64 flex-shrink-0">
            <TableOfContents sections={sections} activeSection={activeSection} />
          </aside>

          {/* Documentation Content */}
          <main id="main-content" className="flex-1 max-w-4xl" role="main" aria-label="Documentation content">
            {/* Hero Section */}
            <section className="mb-16">
              <div className="bg-gradient-to-r from-teal-400 to-blue-400 border-4 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] p-8">
                <h1 className="font-black text-4xl md:text-5xl mb-4">
                  Mirmer AI Python SDK
                </h1>
                <p className="font-bold text-lg mb-6">
                  A Python client library for the Mirmer AI multi-LLM consultation system
                </p>
                <div className="flex flex-wrap gap-4">
                  <a
                    href="https://pypi.org/project/mirmer-ai/"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-2 px-6 py-3 bg-yellow-300 border-2 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[-2px] hover:translate-y-[-2px] transition-all font-bold"
                  >
                    View on PyPI <ExternalLink size={16} />
                  </a>
                </div>
              </div>
            </section>

            {/* Installation Section */}
            <Section id="installation" title="Installation">
              <p className="font-bold mb-4">
                Install the Mirmer AI SDK using pip or uv. Requires Python 3.8 or higher.
              </p>

              <h3 className="font-black text-xl mb-3">Using pip</h3>
              <CodeBlock
                code="pip install mirmerai"
                language="bash"
                title="Terminal"
              />

              <h3 className="font-black text-xl mb-3 mt-6">Using uv</h3>
              <CodeBlock
                code="uv pip install mirmerai"
                language="bash"
                title="Terminal"
              />

              <div className="mt-6 p-4 bg-blue-100 border-4 border-black">
                <p className="font-bold">
                  <strong>Requirements:</strong> Python 3.8+, httpx, pydantic, python-dateutil
                </p>
              </div>
            </Section>

            {/* Authentication Section */}
            <Section id="authentication" title="Authentication">
              <p className="font-bold mb-4">
                Authenticate with Mirmer AI using the CLI tool or programmatically with an API key.
              </p>

              <h3 className="font-black text-xl mb-3">CLI Authentication</h3>
              <p className="font-bold mb-3">
                The easiest way to authenticate is using the CLI tool, which opens a browser for Google Sign-In:
              </p>
              <CodeBlock
                code="mirmer login"
                language="bash"
                title="Terminal"
              />
              <p className="font-bold mt-3 mb-6">
                Credentials are stored in <code className="bg-gray-200 px-2 py-1 border-2 border-black">~/.mirmer/credentials.json</code>
              </p>

              <h3 className="font-black text-xl mb-3">Programmatic Authentication</h3>
              <p className="font-bold mb-3">
                Initialize the client with your API key:
              </p>
              <CodeBlock
                code={`from mirmer import Client

# Option 1: Pass API key directly
client = Client(api_key="your-api-key-here")

# Option 2: Use environment variable MIRMER_API_KEY
client = Client()

# Option 3: Use context manager for automatic cleanup
with Client(api_key="your-api-key-here") as client:
    response = client.query("Hello, world!")
    print(response.stage3.response)`}
                language="python"
                title="example.py"
              />
            </Section>

            {/* Quick Start Section */}
            <Section id="quick-start" title="Quick Start">
              <p className="font-bold mb-4">
                Get started with a simple query to the Mirmer AI council system:
              </p>
              <CodeBlock
                code={`from mirmer import Client

# Initialize client
client = Client(api_key="your-api-key")

# Send a query and get council response
response = client.query("What is the meaning of life?")

# Access Stage 1 - Individual model responses
print("Stage 1 - Individual Responses:")
for model_response in response.stage1:
    print(f"{model_response.model}: {model_response.response}")

# Access Stage 2 - Peer rankings
print("\\nStage 2 - Peer Rankings:")
for ranking in response.stage2:
    print(f"{ranking.model}: {ranking.parsed_ranking}")

# Access Stage 3 - Chairman synthesis (final answer)
print("\\nStage 3 - Chairman Synthesis:")
print(response.stage3.response)`}
                language="python"
                title="quick_start.py"
              />
              <div className="mt-4 p-4 bg-yellow-100 border-4 border-black">
                <p className="font-bold">
                  <strong>Output:</strong> The response object contains all three stages of the council process:
                  individual responses, peer rankings, and the final synthesized answer.
                </p>
              </div>
            </Section>

            {/* Basic Usage Section */}
            <Section id="basic-usage" title="Basic Usage">
              <p className="font-bold mb-4">
                The SDK provides both synchronous and asynchronous clients for different use cases.
              </p>

              <h3 className="font-black text-xl mb-3">Synchronous Client</h3>
              <CodeBlock
                code={`from mirmer import Client

# Initialize client
client = Client(api_key="your-api-key")

# Send a query
response = client.query("Explain quantum computing")

# Access the final answer
print(response.stage3.response)

# Continue the conversation
followup = client.query(
    "Can you elaborate on that?",
    conversation_id=response.conversation_id
)
print(followup.stage3.response)

# Clean up
client.close()`}
                language="python"
                title="basic_usage.py"
              />
            </Section>

            {/* Streaming Section */}
            <Section id="streaming" title="Streaming">
              <p className="font-bold mb-4">
                Stream real-time updates as each stage of the council process completes:
              </p>
              <CodeBlock
                code={`from mirmer import Client

client = Client(api_key="your-api-key")

# Stream council process updates in real-time
for update in client.stream("Explain quantum computing"):
    if update.type == "stage1_start":
        print("Stage 1: Collecting responses...")
    
    elif update.type == "stage1_complete":
        print(f"Stage 1: {len(update.data)} responses received")
    
    elif update.type == "stage2_complete":
        print("Stage 2: Rankings complete")
        # Display aggregate rankings
        for agg in update.data.get("aggregate_rankings", []):
            print(f"  {agg['model']}: {agg['average_rank']:.2f}")
    
    elif update.type == "stage3_complete":
        print("Stage 3: Final answer ready")
        print(update.data["response"])
    
    elif update.type == "error":
        print(f"Error: {update.error}")
        break

client.close()`}
                language="python"
                title="streaming.py"
              />
              <div className="mt-4 p-4 bg-green-100 border-4 border-black">
                <p className="font-bold">
                  <strong>Use Case:</strong> Streaming is perfect for building interactive UIs that show
                  progress as the council deliberates.
                </p>
              </div>
            </Section>

            {/* Async Usage Section */}
            <Section id="async-usage" title="Async Usage">
              <p className="font-bold mb-4">
                Use AsyncClient for concurrent operations and async/await syntax:
              </p>
              <CodeBlock
                code={`import asyncio
from mirmer import AsyncClient

async def main():
    # Use context manager for automatic cleanup
    async with AsyncClient(api_key="your-api-key") as client:
        # Send async query
        response = await client.query("What is machine learning?")
        print(response.stage3.response)
        
        # Multiple concurrent queries
        tasks = [
            client.query("What is AI?"),
            client.query("What is deep learning?"),
            client.query("What is neural networks?")
        ]
        responses = await asyncio.gather(*tasks)
        
        for resp in responses:
            print(resp.stage3.response)

# Run async code
asyncio.run(main())`}
                language="python"
                title="async_usage.py"
              />
            </Section>

            {/* Conversation Management Section */}
            <Section id="conversations" title="Conversation Management">
              <p className="font-bold mb-4">
                Create, list, search, and manage conversations:
              </p>

              <h3 className="font-black text-xl mb-3">Create Conversation</h3>
              <CodeBlock
                code={`from mirmer import Client

client = Client(api_key="your-api-key")

# Create a new conversation
conversation = client.create_conversation(title="AI Discussion")
print(f"Created: {conversation.id}")

# Add messages to the conversation
response = client.query("What is AI?", conversation_id=conversation.id)`}
                language="python"
                title="create_conversation.py"
              />

              <h3 className="font-black text-xl mb-3 mt-6">List Conversations</h3>
              <CodeBlock
                code={`# List all conversations
conversations = client.list_conversations()
for conv in conversations:
    print(f"- {conv.title} (ID: {conv.id})")
    print(f"  Messages: {len(conv.messages)}")`}
                language="python"
                title="list_conversations.py"
              />

              <h3 className="font-black text-xl mb-3 mt-6">Search Conversations</h3>
              <CodeBlock
                code={`# Search conversations by title or content
results = client.search_conversations("machine learning")
for conv in results:
    print(f"- {conv.title}")`}
                language="python"
                title="search_conversations.py"
              />

              <h3 className="font-black text-xl mb-3 mt-6">Get Conversation Details</h3>
              <CodeBlock
                code={`# Get full conversation with all messages
conversation = client.get_conversation(conversation_id)
print(f"Title: {conversation.title}")
for msg in conversation.messages:
    print(f"{msg.role}: {msg.content}")`}
                language="python"
                title="get_conversation.py"
              />

              <h3 className="font-black text-xl mb-3 mt-6">Delete Conversation</h3>
              <CodeBlock
                code={`# Delete a conversation
success = client.delete_conversation(conversation_id)
if success:
    print("Conversation deleted successfully")`}
                language="python"
                title="delete_conversation.py"
              />
            </Section>

            {/* Usage Statistics Section */}
            <Section id="usage-stats" title="Usage Statistics">
              <p className="font-bold mb-4">
                Monitor your API consumption and check your usage limits:
              </p>
              <CodeBlock
                code={`from mirmer import Client

client = Client(api_key="your-api-key")

# Check usage statistics
usage = client.get_usage()
print(f"Tier: {usage.tier}")
print(f"Used: {usage.queries_used_today}/{usage.daily_limit}")
print(f"Reset time: {usage.reset_time}")`}
                language="python"
                title="usage_stats.py"
              />
              <div className="mt-4 p-4 bg-purple-100 border-4 border-black">
                <p className="font-bold">
                  <strong>Tiers:</strong> Free (10 queries/day), Pro (100 queries/day), Enterprise (unlimited)
                </p>
              </div>
            </Section>

            {/* Error Handling Section */}
            <Section id="error-handling" title="Error Handling">
              <p className="font-bold mb-4">
                Handle errors gracefully with comprehensive exception types:
              </p>
              <CodeBlock
                code={`from mirmer import (
    Client,
    AuthenticationError,
    RateLimitError,
    APIError
)

client = Client(api_key="your-api-key")

try:
    response = client.query("Hello")
    print(response.stage3.response)
    
except AuthenticationError:
    print("Error: Invalid API key")
    
except RateLimitError as e:
    print(f"Error: Rate limit exceeded")
    print(f"Reset at: {e.reset_time}")
    
except APIError as e:
    print(f"Error: {e.message}")
    print(f"Status code: {e.status_code}")`}
                language="python"
                title="error_handling.py"
              />
            </Section>

            {/* Configuration Section */}
            <Section id="configuration" title="Configuration">
              <p className="font-bold mb-4">
                Customize client behavior with configuration options:
              </p>
              <CodeBlock
                code={`from mirmer import Client

client = Client(
    api_key="your-api-key",
    base_url="https://api.mirmer.ai",  # Custom API endpoint
    timeout=60.0,                       # Request timeout (seconds)
    max_retries=3                       # Max retry attempts
)`}
                language="python"
                title="configuration.py"
              />
            </Section>

            {/* API Reference Section */}
            <Section id="api-reference" title="API Reference">
              <p className="font-bold mb-6">
                Complete reference for all client methods and classes.
              </p>

              <ApiMethod
                name="Client.query"
                signature="query(message: str, conversation_id: Optional[str] = None) -> Response"
                description="Send a query to the Mirmer AI council and get the complete response."
                params={[
                  { name: 'message', type: 'str', description: 'The query message to send' },
                  { name: 'conversation_id', type: 'Optional[str]', description: 'ID of existing conversation to continue' },
                ]}
                returns="Response object containing stage1, stage2, stage3, and aggregate_rankings"
              />

              <ApiMethod
                name="Client.stream"
                signature="stream(message: str, conversation_id: Optional[str] = None) -> Iterator[StreamUpdate]"
                description="Stream real-time updates as the council process progresses."
                params={[
                  { name: 'message', type: 'str', description: 'The query message to send' },
                  { name: 'conversation_id', type: 'Optional[str]', description: 'ID of existing conversation to continue' },
                ]}
                returns="Iterator of StreamUpdate objects with type and data fields"
              />

              <ApiMethod
                name="Client.create_conversation"
                signature="create_conversation(title: str) -> Conversation"
                description="Create a new conversation."
                params={[
                  { name: 'title', type: 'str', description: 'Title for the new conversation' },
                ]}
                returns="Conversation object with id, title, created_at, and messages"
              />

              <ApiMethod
                name="Client.list_conversations"
                signature="list_conversations() -> List[Conversation]"
                description="List all conversations for the authenticated user."
                params={[]}
                returns="List of Conversation objects"
              />

              <ApiMethod
                name="Client.search_conversations"
                signature="search_conversations(query: str) -> List[Conversation]"
                description="Search conversations by title or message content."
                params={[
                  { name: 'query', type: 'str', description: 'Search query string' },
                ]}
                returns="List of matching Conversation objects"
              />

              <ApiMethod
                name="Client.get_conversation"
                signature="get_conversation(conversation_id: str) -> Conversation"
                description="Get a specific conversation with all messages."
                params={[
                  { name: 'conversation_id', type: 'str', description: 'ID of the conversation' },
                ]}
                returns="Conversation object with full message history"
              />

              <ApiMethod
                name="Client.delete_conversation"
                signature="delete_conversation(conversation_id: str) -> bool"
                description="Delete a conversation."
                params={[
                  { name: 'conversation_id', type: 'str', description: 'ID of the conversation to delete' },
                ]}
                returns="True if successful, False otherwise"
              />

              <ApiMethod
                name="Client.get_usage"
                signature="get_usage() -> Usage"
                description="Get current usage statistics and limits."
                params={[]}
                returns="Usage object with tier, queries_used_today, daily_limit, and reset_time"
              />
            </Section>

            {/* Footer */}
            <footer className="mt-16 pt-8 border-t-4 border-black">
              <div className="text-center">
                <p className="font-bold mb-4">
                  Need help? Check out our{' '}
                  <Link to="/" className="text-teal-600 hover:underline">
                    main site
                  </Link>{' '}
                </p>
              </div>
            </footer>
          </main>
        </div>
      </div>
    </div>
  );
}

// Section component for consistent styling
function Section({ id, title, children }) {
  return (
    <section id={id} className="mb-16 scroll-mt-24">
      <h2 className="font-black text-3xl mb-6 pb-2 border-b-4 border-black">
        {title}
      </h2>
      <div className="space-y-4">{children}</div>
    </section>
  );
}

// API Method component for API reference
function ApiMethod({ name, signature, description, params, returns }) {
  return (
    <div className="mb-8 p-6 bg-white border-4 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
      <h4 className="font-black text-xl mb-2">{name}</h4>
      <code className="block bg-gray-100 border-2 border-black p-3 mb-4 font-mono text-sm overflow-x-auto">
        {signature}
      </code>
      <p className="font-bold mb-4">{description}</p>
      
      {params.length > 0 && (
        <>
          <h5 className="font-black text-lg mb-2">Parameters:</h5>
          <ul className="list-none space-y-2 mb-4">
            {params.map((param, idx) => (
              <li key={idx} className="ml-4">
                <code className="bg-yellow-100 px-2 py-1 border-2 border-black font-mono text-sm">
                  {param.name}
                </code>
                <span className="font-bold text-sm text-gray-600 ml-2">
                  ({param.type})
                </span>
                <span className="font-bold ml-2">- {param.description}</span>
              </li>
            ))}
          </ul>
        </>
      )}
      
      <h5 className="font-black text-lg mb-2">Returns:</h5>
      <p className="font-bold ml-4">{returns}</p>
    </div>
  );
}
