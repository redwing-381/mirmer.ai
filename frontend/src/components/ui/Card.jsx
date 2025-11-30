import { clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

const cn = (...inputs) => twMerge(clsx(inputs))

export function Card({ children, className, ...props }) {
  return (
    <div
      className={cn(
        'bg-white border-4 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] p-6',
        className
      )}
      {...props}
    >
      {children}
    </div>
  )
}

export function CardHeader({ children, className, ...props }) {
  return (
    <div className={cn('mb-4', className)} {...props}>
      {children}
    </div>
  )
}

export function CardTitle({ children, className, ...props }) {
  return (
    <h3 className={cn('text-2xl font-bold mb-2', className)} {...props}>
      {children}
    </h3>
  )
}

export function CardDescription({ children, className, ...props }) {
  return (
    <p className={cn('text-gray-600', className)} {...props}>
      {children}
    </p>
  )
}

export function CardContent({ children, className, ...props }) {
  return (
    <div className={cn('', className)} {...props}>
      {children}
    </div>
  )
}

export function CardFooter({ children, className, ...props }) {
  return (
    <div className={cn('mt-6', className)} {...props}>
      {children}
    </div>
  )
}
