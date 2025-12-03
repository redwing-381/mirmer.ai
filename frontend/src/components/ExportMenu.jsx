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
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

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

  const API_BASE = import.meta.env.VITE_API_URL 
    ? `${import.meta.env.VITE_API_URL}/api` 
    : '/api';

  const handleExport = async (format) => {
    // Handle PDF export client-side
    if (format === 'pdf') {
      await handlePDFExport();
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

  const handlePDFExport = async () => {
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

      // Create a temporary container for rendering
      const container = document.createElement('div');
      container.style.position = 'absolute';
      container.style.left = '-9999px';
      container.style.width = '800px';
      container.style.background = 'white';
      container.style.padding = '40px';
      document.body.appendChild(container);

      // Build HTML content
      let html = `
        <div style="font-family: Arial, sans-serif; color: #000;">
          <h1 style="font-size: 24px; margin-bottom: 10px;">${conversation.title || 'Conversation'}</h1>
          <p style="font-size: 12px; color: #666; margin-bottom: 20px;">
            <strong>Created:</strong> ${new Date(conversation.created_at).toLocaleString()}<br/>
            <strong>ID:</strong> ${conversation.id}<br/>
            <strong>Exported:</strong> ${new Date().toLocaleString()}
          </p>
          <hr style="border: 1px solid #ccc; margin: 20px 0;"/>
      `;

      // Add messages
      conversation.messages.forEach((message, index) => {
        if (message.role === 'user') {
          html += `
            <div style="margin: 20px 0; padding: 15px; background: #f0f9ff; border-left: 4px solid #0ea5e9;">
              <h3 style="font-size: 16px; margin: 0 0 10px 0;">Message ${index + 1}: User</h3>
              <p style="margin: 0; white-space: pre-wrap;">${message.content}</p>
            </div>
          `;
        } else {
          html += `<div style="margin: 20px 0;"><h3 style="font-size: 16px;">Message ${index + 1}: Assistant Response</h3>`;
          
          // Stage 1
          if (message.stage1 && message.stage1.length > 0) {
            html += `<div style="margin: 15px 0; padding: 15px; border-left: 4px solid #3b82f6; background: #eff6ff;">
              <h4 style="font-size: 14px; margin: 0 0 10px 0;">Stage 1: Individual Model Responses</h4>`;
            message.stage1.forEach(response => {
              html += `
                <div style="margin: 10px 0;">
                  <strong style="font-size: 13px;">${response.model}</strong>
                  <p style="margin: 5px 0 0 0; font-size: 12px; white-space: pre-wrap;">${response.response}</p>
                </div>
              `;
            });
            html += `</div>`;
          }

          // Stage 2
          if (message.stage2 && message.stage2.length > 0) {
            html += `<div style="margin: 15px 0; padding: 15px; border-left: 4px solid #f59e0b; background: #fffbeb;">
              <h4 style="font-size: 14px; margin: 0 0 10px 0;">Stage 2: Peer Rankings</h4>`;
            message.stage2.forEach(ranking => {
              html += `
                <div style="margin: 10px 0;">
                  <strong style="font-size: 13px;">${ranking.model}'s Rankings</strong>
                  <p style="margin: 5px 0 0 0; font-size: 12px; white-space: pre-wrap;">${ranking.ranking}</p>
                </div>
              `;
            });
            html += `</div>`;
          }

          // Stage 3
          if (message.stage3) {
            const stage3Content = message.stage3.response || message.stage3.final_answer || 'No synthesis';
            html += `<div style="margin: 15px 0; padding: 15px; border-left: 4px solid #10b981; background: #f0fdf4;">
              <h4 style="font-size: 14px; margin: 0 0 10px 0;">Stage 3: Chairman Synthesis</h4>
              <p style="margin: 0; font-size: 12px; white-space: pre-wrap;">${stage3Content}</p>
            </div>`;
          }

          html += `</div>`;
        }
      });

      html += `
          <hr style="border: 1px solid #ccc; margin: 20px 0;"/>
          <p style="text-align: center; font-size: 10px; color: #999;">Generated by Mirmer AI</p>
        </div>
      `;

      container.innerHTML = html;

      // Generate PDF
      const canvas = await html2canvas(container, {
        scale: 2,
        useCORS: true,
        logging: false,
        backgroundColor: '#ffffff'
      });

      const imgData = canvas.toDataURL('image/png');
      const pdf = new jsPDF('p', 'mm', 'a4');
      
      const pdfWidth = pdf.internal.pageSize.getWidth();
      const pdfHeight = pdf.internal.pageSize.getHeight();
      const imgWidth = pdfWidth - 20; // 10mm margin on each side
      const imgHeight = (canvas.height * imgWidth) / canvas.width;
      
      let heightLeft = imgHeight;
      let position = 10; // Top margin

      // Add first page
      pdf.addImage(imgData, 'PNG', 10, position, imgWidth, imgHeight);
      heightLeft -= (pdfHeight - 20);

      // Add additional pages if needed
      while (heightLeft > 0) {
        position = heightLeft - imgHeight + 10;
        pdf.addPage();
        pdf.addImage(imgData, 'PNG', 10, position, imgWidth, imgHeight);
        heightLeft -= (pdfHeight - 20);
      }

      // Clean up
      document.body.removeChild(container);

      // Generate filename
      const title = conversation.title || 'conversation';
      const safeTitle = title.replace(/[^a-z0-9]/gi, '_').substring(0, 50);
      const timestamp = new Date().toISOString().split('T')[0];
      const filename = `${safeTitle}_${timestamp}.pdf`;

      // Download
      pdf.save(filename);

    } catch (error) {
      console.error('PDF export error:', error);
      setError(error.message || 'Failed to generate PDF');
    } finally {
      setLoading(null);
    }
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
  );
}
