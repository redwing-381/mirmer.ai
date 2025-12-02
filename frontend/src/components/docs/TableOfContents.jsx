import { useState, useEffect } from 'react';
import { Menu, X } from 'lucide-react';

/**
 * TableOfContents component with smooth scrolling and active section highlighting
 * Sticky sidebar on desktop, collapsible menu on mobile
 * Follows neobrutalist design aesthetic
 */
export default function TableOfContents({ sections, activeSection }) {
  const [isOpen, setIsOpen] = useState(false);

  const scrollToSection = (sectionId) => {
    const element = document.getElementById(sectionId);
    if (element) {
      // Offset for fixed header
      const offset = 100;
      const elementPosition = element.getBoundingClientRect().top;
      const offsetPosition = elementPosition + window.pageYOffset - offset;

      window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth'
      });

      // Close mobile menu after navigation
      setIsOpen(false);
    }
  };

  return (
    <>
      {/* Mobile Toggle Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="lg:hidden fixed top-20 right-4 z-50 p-3 bg-yellow-300 border-4 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[-2px] hover:translate-y-[-2px] transition-all"
        aria-label="Toggle table of contents"
      >
        {isOpen ? <X size={24} /> : <Menu size={24} />}
      </button>

      {/* Mobile Overlay */}
      {isOpen && (
        <div
          className="lg:hidden fixed inset-0 bg-black bg-opacity-50 z-40"
          onClick={() => setIsOpen(false)}
        />
      )}

      {/* Table of Contents */}
      <nav
        className={`
          fixed lg:sticky top-24 lg:top-24 right-0 lg:right-auto
          w-72 lg:w-64 h-[calc(100vh-8rem)] lg:h-auto
          bg-white border-4 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]
          overflow-y-auto z-40
          transition-transform duration-300 ease-in-out
          ${isOpen ? 'translate-x-0' : 'translate-x-full lg:translate-x-0'}
        `}
        role="navigation"
        aria-label="Table of Contents"
        aria-hidden={!isOpen && 'true'}
      >
        {/* Header */}
        <div className="sticky top-0 bg-teal-400 border-b-4 border-black px-4 py-3 z-10">
          <h2 className="font-black text-lg">Contents</h2>
        </div>

        {/* Section Links */}
        <ul className="p-4 space-y-2">
          {sections.map((section) => {
            const isActive = activeSection === section.id;
            return (
              <li key={section.id}>
                <button
                  onClick={() => scrollToSection(section.id)}
                  className={`
                    w-full text-left px-4 py-2 font-bold text-sm
                    border-2 border-black transition-all
                    focus:outline-none focus:ring-4 focus:ring-blue-500 focus:ring-offset-2
                    ${
                      isActive
                        ? 'bg-yellow-300 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] translate-x-[-2px] translate-y-[-2px]'
                        : 'bg-white hover:bg-gray-100 shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[-2px] hover:translate-y-[-2px]'
                    }
                  `}
                  aria-label={`Navigate to ${section.title} section`}
                  aria-current={isActive ? 'location' : undefined}
                >
                  {section.title}
                </button>
              </li>
            );
          })}
        </ul>
      </nav>
    </>
  );
}
