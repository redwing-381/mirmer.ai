import { cn } from '../../lib/utils'

export function Badge({ 
  children, 
  variant = 'default',
  className,
  ...props 
}) {
  const baseStyles = 'inline-block px-3 py-1 text-sm font-bold border-2 border-black'
  
  const variants = {
    default: 'bg-blue-400 text-black',
    success: 'bg-green-400 text-black',
    warning: 'bg-yellow-400 text-black',
    danger: 'bg-red-400 text-white',
    neutral: 'bg-gray-200 text-black',
  }
  
  return (
    <span
      className={cn(
        baseStyles,
        variants[variant],
        className
      )}
      {...props}
    >
      {children}
    </span>
  )
}
