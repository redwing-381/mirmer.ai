import { useState, createContext, useContext } from 'react'

const AlertDialogContext = createContext()

export function AlertDialog({ children, open: controlledOpen, onOpenChange }) {
  const [internalOpen, setInternalOpen] = useState(false)
  
  const isControlled = controlledOpen !== undefined
  const open = isControlled ? controlledOpen : internalOpen
  const setOpen = isControlled ? onOpenChange : setInternalOpen

  return (
    <AlertDialogContext.Provider value={{ open, setOpen }}>
      {children}
    </AlertDialogContext.Provider>
  )
}

export function AlertDialogTrigger({ children, asChild }) {
  const { setOpen } = useContext(AlertDialogContext)
  
  if (asChild) {
    return <div onClick={() => setOpen(true)}>{children}</div>
  }
  
  return (
    <button onClick={() => setOpen(true)}>
      {children}
    </button>
  )
}

export function AlertDialogContent({ children }) {
  const { open, setOpen } = useContext(AlertDialogContext)
  
  if (!open) return null
  
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Backdrop */}
      <div 
        className="fixed inset-0 bg-black/50"
        onClick={() => setOpen(false)}
      />
      
      {/* Dialog */}
      <div className="relative bg-white border-4 border-black shadow-[12px_12px_0px_0px_rgba(0,0,0,1)] p-8 max-w-md w-full mx-4 z-50">
        {children}
      </div>
    </div>
  )
}

export function AlertDialogHeader({ children }) {
  return <div className="mb-6">{children}</div>
}

export function AlertDialogTitle({ children }) {
  return <h2 className="text-2xl font-black mb-2">{children}</h2>
}

export function AlertDialogDescription({ children }) {
  return <p className="text-base font-bold text-gray-700">{children}</p>
}

export function AlertDialogFooter({ children }) {
  return <div className="flex justify-end space-x-3 mt-6">{children}</div>
}

export function AlertDialogCancel({ children }) {
  const { setOpen } = useContext(AlertDialogContext)
  
  return (
    <button
      onClick={() => setOpen(false)}
      className="px-6 py-2 bg-white border-4 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[-2px] hover:translate-y-[-2px] active:shadow-none active:translate-x-1 active:translate-y-1 transition-all font-black"
    >
      {children}
    </button>
  )
}

export function AlertDialogAction({ children, onClick }) {
  const { setOpen } = useContext(AlertDialogContext)
  
  const handleClick = () => {
    onClick?.()
    setOpen(false)
  }
  
  return (
    <button
      onClick={handleClick}
      className="px-6 py-2 bg-[#FF6B6B] text-white border-4 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[-2px] hover:translate-y-[-2px] active:shadow-none active:translate-x-1 active:translate-y-1 transition-all font-black"
    >
      {children}
    </button>
  )
}
