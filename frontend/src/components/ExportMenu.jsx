import { useState } from 'react';
import { Download, FileText, FileJson, FileType, AlertCircle } from 'lucide-react';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import ConversationPrintView from './ConversationPrintView';
import { createPortal } from 'react-dom';

/**
 * ExportMenu Component - Neobrutalism UI
 * 
 * Dropdown menu for exporting conversations in various formats.
 * Features bold borders, offset shadows, and neobrutalism design.
 * Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6
 */
export default function ExportMenu({ conversationId, userId, conversation }) {
  const [loading, setLoading] = useState(null);
  const [error, setError] = useState(null);
  const [showPrintView, setShowPrintView] = useState(false);

  const API_BASE = import.meta.env.VITE_API_URL 
    ? `${import.meta.env.VITE_API_URL}/api` 
    : '/api';

  const handleExport = async (format) => {
    // Handle PDF export client-side
    if (format === 'pdf') {
      handlePDFExport();
      return;
    }

    // Handle other formats server-side
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
    } catch (error) {
      console.error('Export error:', error);
      setError(error.message);
      // Keep menu open for retry
    } finally {
      setLoading(null);
    }
  };

  const handlePDFExport = () => {
    setLoading('pdf');
    setError(null);

    try {
      // Validate conversation data
      if (!conversation) {
        throw new Error('No conversation data available');
      }

      if (!conversation.messages || conversation.messages.length === 0) {
        throw new Error('Conversation has no messages to export');
      }

      // Show print view which will trigger browser print dialog
      setShowPrintView(true);
    } catch (error) {
      console.error('PDF export error:', error);
      setError(error.message);
    } finally {
      setLoading(null);
    }
  };

  const handleClosePrintView = () => {
    setShowPrintView(false);
  };

  const exportOptions = [
    {
      format: 'markdown',
      label: 'Markdown',
      icon: FileText,
      color: 'bg-green-200',
    },
    {
      format: 'pdf',
      label: 'PDF',
      icon: FileType,
      color: 'bg-orange-200',
    },
    {
      format: 'json',
      label: 'JSON',
      icon: FileJson,
      color: 'bg-blue-200',
    },
  ];

  return (
    <>
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <button
            className="flex items-center justify-center w-12 h-12 text-black bg-yellow-300 hover:bg-yellow-400 border-2 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:translate-x-boxShadowX hover:translate-y-boxShadowY hover:shadow-none transition-all duration-150"
            aria-label="Export conversation"
            title="Export conversation"
          >
            <Download className="w-5 h-5" strokeWidth={2.5} />
          </button>
        </DropdownMenuTrigger>
        
        <DropdownMenuContent className="w-56" align="end">
          <DropdownMenuLabel>
            <Download className="inline w-4 h-4 mr-2" strokeWidth={2.5} />
            Export Format
          </DropdownMenuLabel>
          <DropdownMenuSeparator />
          
          {error && (
            <div className="mx-2 my-2 p-3 bg-red-100 border-2 border-red-500 shadow-[2px_2px_0px_0px_rgba(239,68,68,1)]">
              <div className="flex items-start gap-2">
                <AlertCircle className="w-4 h-4 text-red-700 flex-shrink-0 mt-0.5" strokeWidth={2.5} />
                <div className="flex-1">
                  <p className="font-bold text-sm text-red-700 mb-1">Export Failed</p>
                  <p className="text-xs text-red-700">{error}</p>
                  <button
                    onClick={() => setError(null)}
                    className="mt-2 text-xs text-red-700 hover:text-red-800 font-bold underline"
                  >
                    Dismiss
                  </button>
                </div>
              </div>
            </div>
          )}
          
          {exportOptions.map(({ format, label, icon: Icon, color }) => (
            <DropdownMenuItem
              key={format}
              onClick={() => handleExport(format)}
              disabled={loading !== null}
              className={color}
            >
              <Icon className="w-4 h-4" strokeWidth={2.5} />
              <div className="flex-1">
                <div className="flex items-center justify-between">
                  <span>{label}</span>
                  {loading === format && (
                    <div className="w-4 h-4 border-2 border-black border-t-transparent rounded-full animate-spin ml-2" />
                  )}
                </div>
              </div>
            </DropdownMenuItem>
          ))}
        </DropdownMenuContent>
      </DropdownMenu>

      {/* Print View Portal - Requirements: 1.1, 1.4 */}
      {showPrintView && conversation && createPortal(
        <div className="fixed inset-0 bg-white z-50 overflow-auto">
          <ConversationPrintView 
            conversation={conversation}
            onClose={handleClosePrintView}
            autoPrint={true}
          />
        </div>,
        document.body
      )}
    </>
  );
}
