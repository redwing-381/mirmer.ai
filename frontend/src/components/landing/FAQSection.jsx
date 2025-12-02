import { useState } from 'react'

export default function FAQSection() {
  const [openIndex, setOpenIndex] = useState(null)

  const faqs = [
    {
      question: 'How does Mirmer AI work?',
      answer: 'Mirmer AI uses a 3-stage council process: First, 4 leading AI models (GPT-4, Claude, Gemini, etc.) independently respond to your question. Then, each model ranks the others\' responses. Finally, a chairman model synthesizes the best insights into one comprehensive answer.'
    },
    {
      question: 'Which AI models do you use?',
      answer: 'We use the latest versions of GPT-4, Claude, Gemini, and other leading models. Our system automatically selects the best models for your specific query type to ensure optimal results.'
    },
    {
      question: 'How is this different from ChatGPT or Claude?',
      answer: 'Single AI models can have biases and limitations. Mirmer AI combines multiple perspectives, peer-reviews responses, and synthesizes the best answer. You get more balanced, comprehensive, and accurate results than any single AI can provide.'
    },
    {
      question: 'Is my data private and secure?',
      answer: 'Yes! Your conversations are encrypted and private. We never use your data to train AI models. Your queries are processed securely and only you have access to your conversation history.'
    },
    {
      question: 'Can I try it for free?',
      answer: 'Absolutely! The free tier includes 10 queries per day with full access to the 3-stage council process. No credit card required. Just sign in with Google and start getting better answers immediately.'
    },
    {
      question: 'What happens if I run out of queries?',
      answer: 'Free users get 10 queries per day. If you need more, you can upgrade to Pro for 100 queries per day at ₹150/month. Your query count resets daily, so you can always come back tomorrow!'
    }
  ]

  const toggleFAQ = (index) => {
    setOpenIndex(openIndex === index ? null : index)
  }

  return (
    <section className="py-20 bg-white border-b-4 border-black">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="text-center mb-16">
          <h2 className="text-5xl md:text-6xl font-black text-black mb-6">
            FREQUENTLY ASKED QUESTIONS
          </h2>
          <p className="text-xl text-gray-700 font-bold">
            Everything you need to know
          </p>
        </div>

        {/* FAQ List */}
        <div className="space-y-4">
          {faqs.map((faq, index) => (
            <div
              key={index}
              className={`border-4 border-black transition-all duration-300 ${
                openIndex === index
                  ? 'bg-[#FFE66D] shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]'
                  : 'bg-white shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:shadow-[6px_6px_0px_0px_rgba(0,0,0,1)]'
              }`}
            >
              <button
                onClick={() => toggleFAQ(index)}
                className="w-full text-left p-6 flex justify-between items-center"
              >
                <span className="font-black text-lg pr-8">{faq.question}</span>
                <span
                  className={`text-3xl font-black transition-transform duration-300 flex-shrink-0 ${
                    openIndex === index ? 'rotate-45' : ''
                  }`}
                >
                  +
                </span>
              </button>

              <div
                className={`overflow-hidden transition-all duration-300 ${
                  openIndex === index ? 'max-h-96' : 'max-h-0'
                }`}
              >
                <div className="px-6 pb-6 pt-0">
                  <div className="border-t-4 border-black pt-4">
                    <p className="font-bold text-gray-700 leading-relaxed">
                      {faq.answer}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

      </div>
    </section>
  )
}
