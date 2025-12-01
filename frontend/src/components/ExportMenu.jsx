import { useState } from 'react';
import { Download, FileText, FileJson, FileType } from 'lucide-react';

/**
 * ExportMenu Component - Neobrutalism UI
 * 
 * Dropdown menu for exporting conversations in various formats.
 * Features bold borders, thick shadows, and high contrast colors.
 * Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6
 */
export default function ExportMenu({ conversationId, userId }) {
  const [isOpen, setIsOpen] = useState(false);
  const [loading, setLoading] = useState(null);
  const [error, setError] = useState(null);

  const API_BASE = import.meta.env.VITE_API_URL 
    ? `${import.meta.env.VITE_API_URL}/api` 
    : '/api';

  const handleExport = async (format) => {
    setLoading(format);
    setError(null);
    
    try {
      const response = await fetch(
        `${API_BASE}/conversations/${conversationId}/export/${format}`,
        {
          headers: {
            'X-User-Id': userId,
          },
        }
      );

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Export failed with status ${response.status}`);
      }

      // Get filename from Content-Disposition header or generate one
      const contentDisposition = response.headers.get('Content-Disposition');
      let filename = `conversation_${conversationId}.${format === 'markdown' ? 'md' : format}`;
      
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="?(.+)"?/);
        if (filenameMatch) {
          filename = filenameMatch[1];
        }
      }

      // Download the file
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

      setIsOpen(false);
    } catch (error) {
      console.error('Export error:', error);
      setError(error.message);
      // Keep menu open for retry
    } finally {
      setLoading(null);
    }
  };

  const exportOptions = [
    {
      format: 'markdown',
      label: 'Markdown',
      icon: FileText,
      description: 'Formatted text file',
      color: 'bg-emerald-400',
      hoverColor: 'hover:bg-emerald-300',
    },
    {
      format: 'pdf',
      label: 'PDF',
      icon: FileType,
      description: 'Styled document',
      color: 'bg-amber-400',
      hoverColor: 'hover:bg-amber-300',
    },
    {
      format: 'json',
      label: 'JSON',
      icon: FileJson,
      description: 'Complete data structure',
      color: 'bg-blue-400',
      hoverColor: 'hover:bg-blue-300',
    },
  ];

  return (
    <div className="relative">
      {/* Neobrutalism Export Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-4 py-2.5 text-sm font-bold text-black bg-white border-3 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[2px] hover:translate-y-[2px] active:shadow-none active:translate-x-[4px] active:translate-y-[4px] transition-all duration-100 uppercase tracking-wide"
        style={{ border: '3px solid black' }}
        aria-label="Export conversation"
      >
        <Download className="w-5 h-5" strokeWidth={2.5} />
        <span>Export</span>
      </button>

      {isOpen && (
        <>
          {/* Backdrop */}
          <div
            className="fixed inset-0 z-10"
            onClick={() => {
              setIsOpen(false);
              setError(null);
            }}
          />

          {/* Neobrutalism Dropdown Menu */}
          <div 
            className="absolute right-0 z-20 mt-3 w-72 bg-white border-3 shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] animate-in slide-in-from-top-2 duration-200"
            style={{ border: '3px solid black' }}
          >
            {/* Header */}
            <div className="px-4 py-3 bg-yellow-300 border-b-3" style={{ borderBottom: '3px solid black' }}>
              <p className="text-sm font-black text-black uppercase tracking-wider">
                📥 Export Format
              </p>
            </div>

            {/* Error Message */}
            {error && (
              <div className="mx-3 mt-3 p-3 bg-red-400 border-3 text-black text-sm font-bold" style={{ border: '2px solid black' }}>
                <p className="font-black mb-1">⚠️ Export Failed</p>
                <p className="text-xs font-semibold">{error}</p>
                <button
                  onClick={() => setError(null)}
                  className="mt-2 text-xs underline font-bold hover:no-underline"
                >
                  Dismiss
                </button>
              </div>
            )}

            {/* Export Options */}
            <div className="p-2">
              {exportOptions.map(({ format, label, icon: Icon, description, color, hoverColor }) => (
                <button
                  key={format}
                  onClick={() => handleExport(format)}
                  disabled={loading !== null}
                  className={`w-full flex items-center gap-3 p-3 mb-2 text-left border-3 ${color} ${hoverColor} hover:translate-x-1 transition-all duration-100 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:translate-x-0 group`}
                  style={{ border: '3px solid black' }}
                >
                  <div className={`p-2 bg-white border-2 border-black ${loading === format ? 'animate-pulse' : ''}`}>
                    <Icon className="w-6 h-6 text-black" strokeWidth={2.5} />
                  </div>
                  
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between">
                      <p className="text-base font-black text-black uppercase tracking-wide">
                        {label}
                      </p>
                      {loading === format && (
                        <div className="w-5 h-5 border-3 border-black border-t-transparent rounded-full animate-spin" />
                      )}
                    </div>
                    <p className="text-xs font-bold text-black mt-0.5 opacity-70">
                      {description}
                    </p>
                  </div>
                </button>
              ))}
            </div>

            {/* Footer Tip */}
            <div className="px-4 py-2 bg-gray-100 border-t-3 text-center" style={{ borderTop: '3px solid black' }}>
              <p className="text-xs font-bold text-black">
                💡 All 3 stages included
              </p>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
