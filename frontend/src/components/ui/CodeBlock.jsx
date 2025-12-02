import { useState } from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { tomorrow } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { Copy, Check } from 'lucide-react';

/**
 * CodeBlock component with macOS-style window and copy functionality
 * Follows neobrutalist design with bold borders and shadows
 */
export default function CodeBlock({ 
  code, 
  language = 'python', 
  title = 'Terminal',
  showLineNumbers = false 
}) {
  const [copied, setCopied] = useState(false);

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      // Fallback for older browsers
      const textArea = document.createElement('textarea');
      textArea.value = code;
      textArea.style.position = 'fixed';
      textArea.style.left = '-999999px';
      document.body.appendChild(textArea);
      textArea.select();
      try {
        document.execCommand('copy');
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
      } catch (err) {
        console.error('Failed to copy:', err);
      } finally {
        document.body.removeChild(textArea);
      }
    }
  };

  return (
    <div className="w-full my-6">
      {/* macOS Window Container */}
      <div 
        className="border-4 border-black bg-white shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] overflow-hidden"
        role="region"
        aria-label={`Code example: ${title}`}
      >
        {/* macOS Title Bar */}
        <div className="bg-gray-200 border-b-4 border-black px-4 py-3 flex items-center justify-between">
          {/* macOS Traffic Lights */}
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-red-500 border-2 border-black"></div>
            <div className="w-3 h-3 rounded-full bg-yellow-400 border-2 border-black"></div>
            <div className="w-3 h-3 rounded-full bg-green-500 border-2 border-black"></div>
          </div>
          
          {/* Window Title */}
          <div className="flex-1 text-center">
            <span className="font-bold text-sm">{title}</span>
          </div>

          {/* Copy Button */}
          <button
            onClick={copyToClipboard}
            className="flex items-center gap-2 px-3 py-1 bg-yellow-300 border-2 border-black shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[-2px] hover:translate-y-[-2px] transition-all font-bold text-sm focus:outline-none focus:ring-4 focus:ring-blue-500 focus:ring-offset-2"
            aria-label={copied ? 'Code copied to clipboard' : 'Copy code to clipboard'}
            aria-live="polite"
          >
            {copied ? (
              <>
                <Check size={16} />
                <span className="hidden sm:inline">Copied!</span>
              </>
            ) : (
              <>
                <Copy size={16} />
                <span className="hidden sm:inline">Copy</span>
              </>
            )}
          </button>
        </div>

        {/* Code Content */}
        <div className="bg-[#0d1117] overflow-x-auto">
          <SyntaxHighlighter
            aria-label={`${language} code snippet`}
            language={language}
            style={{
              ...tomorrow,
              'hljs': {
                ...tomorrow['hljs'],
                background: '#0d1117',
                color: '#e6edf3',
              },
              'hljs-comment': { color: '#8b949e', fontStyle: 'italic' },
              'hljs-keyword': { color: '#ff7b72', fontWeight: 'bold' },
              'hljs-string': { color: '#a5d6ff' },
              'hljs-number': { color: '#79c0ff' },
              'hljs-function': { color: '#d2a8ff' },
              'hljs-class': { color: '#ffa657' },
              'hljs-built_in': { color: '#ffa657' },
              'hljs-variable': { color: '#ffa657' },
              'hljs-title': { color: '#d2a8ff', fontWeight: 'bold' },
              'hljs-params': { color: '#e6edf3' },
              'hljs-attr': { color: '#79c0ff' },
              'hljs-name': { color: '#7ee787' },
              'hljs-tag': { color: '#7ee787' },
            }}
            showLineNumbers={showLineNumbers}
            customStyle={{
              margin: 0,
              padding: '1.5rem',
              background: '#0d1117',
              fontSize: '0.9rem',
              lineHeight: '1.6',
            }}
            codeTagProps={{
              style: {
                fontFamily: "'Courier New', 'Consolas', monospace",
                textShadow: '0 0 1px rgba(255,255,255,0.1)',
              }
            }}
          >
            {code}
          </SyntaxHighlighter>
        </div>
      </div>
    </div>
  );
}
