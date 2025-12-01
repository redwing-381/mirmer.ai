import { clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

const cn = (...inputs) => twMerge(clsx(inputs))

export function Button({ 
  children, 
  variant = 'default', 
  size = 'default',
  className,
  ...props 
}) {
  const baseStyles = 'font-bold border-4 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] active:shadow-none active:translate-x-1 active:translate-y-1 transition-all'
  
  const variants = {
    default: 'bg-blue-500 hover:bg-blue-600 text-white',
    neutral: 'bg-white hover:bg-gray-50 text-black',
    primary: 'bg-yellow-400 hover:bg-yellow-500 text-black',
    danger: 'bg-red-500 hover:bg-red-600 text-white',
    noShadow: 'bg-white hover:bg-gray-50 text-black',
  }
  
  const sizes = {
    default: 'px-6 py-3 text-base',
    sm: 'px-4 py-2 text-sm',
    lg: 'px-8 py-4 text-lg',
  }
  
  return (
    <button
      className={cn(
        baseStyles,
        variants[variant],
        sizes[size],
        className
      )}
      {...props}
    >
      {children}
    </button>
  )
}
