export default function Footer() {
  const currentYear = new Date().getFullYear()

  return (
    <footer className="bg-black text-white py-16 border-t-4 border-black">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-12 mb-12">
          {/* Brand */}
          <div>
            <h3 className="text-3xl font-black mb-4">MIRMER AI</h3>
            <p className="text-gray-400 font-bold">
              Multi-LLM consultation system with collective intelligence
            </p>
          </div>

          {/* Product */}
          <div>
            <h4 className="font-black mb-4 text-lg">PRODUCT</h4>
            <ul className="space-y-3">
              <li>
                <a href="#features" className="text-gray-400 hover:text-[#4ECDC4] transition-colors font-bold">
                  Features
                </a>
              </li>
              <li>
                <a href="#pricing" className="text-gray-400 hover:text-[#FFE66D] transition-colors font-bold">
                  Pricing
                </a>
              </li>
            </ul>
          </div>

          {/* Company */}
          <div>
            <h4 className="font-black mb-4 text-lg">COMPANY</h4>
            <ul className="space-y-3">
              <li>
                <a href="#" className="text-gray-400 hover:text-[#4ECDC4] transition-colors font-bold">
                  About
                </a>
              </li>
              <li>
                <a href="#" className="text-gray-400 hover:text-[#FFE66D] transition-colors font-bold">
                  Blog
                </a>
              </li>
            </ul>
          </div>

          {/* Legal */}
          <div>
            <h4 className="font-black mb-4 text-lg">LEGAL</h4>
            <ul className="space-y-3">
              <li>
                <a href="#" className="text-gray-400 hover:text-[#4ECDC4] transition-colors font-bold">
                  Privacy
                </a>
              </li>
              <li>
                <a href="#" className="text-gray-400 hover:text-[#FFE66D] transition-colors font-bold">
                  Terms
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t-4 border-gray-800 pt-8 text-center">
          <p className="text-gray-400 font-black">&copy; {currentYear} MIRMER AI. ALL RIGHTS RESERVED.</p>
        </div>
      </div>
    </footer>
  )
}
