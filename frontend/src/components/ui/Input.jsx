import { cn } from '../../lib/utils'

export function Input({ 
  className,
  type = 'text',
  ...props 
}) {
  return (
    <input
      type={type}
      className={cn(
        'w-full px-4 py-3 text-base font-medium',
        'bg-white border-4 border-black',
        'focus:outline-none focus:ring-4 focus:ring-yellow-400',
        'placeholder:text-gray-400',
        'disabled:bg-gray-100 disabled:cursor-not-allowed',
        className
      )}
      {...props}
    />
  )
}

export function Textarea({ 
  className,
  ...props 
}) {
  return (
    <textarea
      className={cn(
        'w-full px-4 py-3 text-base font-medium',
        'bg-white border-4 border-black',
        'focus:outline-none focus:ring-4 focus:ring-yellow-400',
        'placeholder:text-gray-400',
        'disabled:bg-gray-100 disabled:cursor-not-allowed',
        'resize-none',
        className
      )}
      {...props}
    />
  )
}
