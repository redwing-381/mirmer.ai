import { useState } from 'react';
import { Download, FileText, FileJson, FileType } from 'lucide-react';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

/**
 * ExportMenu Component - Neobrutalism UI with Shadcn
 * 
 * Dropdown menu for exporting conversations in various formats.
 * Features bold borders, thick shadows, and high contrast colors.
 * Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6
 */
export default function ExportMenu({ conversationId, userId }) {
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
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <button
          className="flex items-center justify-center w-14 h-14 text-black bg-yellow-400 border-4 border-black rounded-full shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[-2px] hover:translate-y-[-2px] active:shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] active:translate-x-[2px] active:translate-y-[2px] transition-all duration-150 hover:scale-110"
          aria-label="Export conversation"
          title="Export conversation"
        >
          <Download className="w-6 h-6" strokeWidth={3} />
        </button>
      </DropdownMenuTrigger>
      
      <DropdownMenuContent className="w-64" align="end">
        <DropdownMenuLabel className="bg-yellow-300 border-b-2 border-black -m-1 mb-1 px-3 py-2">
          📥 EXPORT FORMAT
        </DropdownMenuLabel>
        
        {error && (
          <div className="mx-2 my-2 p-3 bg-red-400 border-2 border-black">
            <p className="font-black text-sm mb-1">⚠️ Export Failed</p>
            <p className="text-xs font-bold">{error}</p>
            <button
              onClick={() => setError(null)}
              className="mt-2 text-xs underline font-bold hover:no-underline"
            >
              Dismiss
            </button>
          </div>
        )}
        
        {exportOptions.map(({ format, label, icon: Icon, description, color }) => (
          <DropdownMenuItem
            key={format}
            onClick={() => handleExport(format)}
            disabled={loading !== null}
            className={`${color} gap-3 my-1 cursor-pointer`}
          >
            <div className={`p-2 bg-white border-2 border-black ${loading === format ? 'animate-pulse' : ''}`}>
              <Icon className="w-5 h-5 text-black" strokeWidth={2.5} />
            </div>
            
            <div className="flex-1">
              <div className="flex items-center justify-between">
                <p className="text-sm font-black uppercase">
                  {label}
                </p>
                {loading === format && (
                  <div className="w-4 h-4 border-2 border-black border-t-transparent rounded-full animate-spin ml-2" />
                )}
              </div>
              <p className="text-xs font-bold opacity-70">
                {description}
              </p>
            </div>
          </DropdownMenuItem>
        ))}
        
        <DropdownMenuSeparator />
        
        <div className="px-3 py-2 text-center bg-gray-100 -m-1 mt-1">
          <p className="text-xs font-bold">
            💡 All 3 stages included
          </p>
        </div>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
