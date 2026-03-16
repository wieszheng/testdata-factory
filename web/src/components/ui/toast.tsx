import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"
import { X, CheckCircle, XCircle, AlertCircle, Info } from "lucide-react"
import { cn } from "@/lib/utils"

const toastVariants = cva(
  "group pointer-events-auto relative flex w-full items-center space-x-2 overflow-hidden rounded-md border px-3 py-2 shadow-lg transition-all",
  {
    variants: {
      variant: {
        default: "border bg-[#1a1f2e] text-white",
        success: "border-[#05c4a5]/30 bg-[#05c4a5]/10 text-[#05c4a5]",
        error: "border-red-500/30 bg-red-500/10 text-red-400",
        warning: "border-yellow-500/30 bg-yellow-500/10 text-yellow-400",
        info: "border-[#5a5eff]/30 bg-[#5a5eff]/10 text-[#5a5eff]",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
)

export interface ToastProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof toastVariants> {
  open?: boolean
  onOpenChange?: (open: boolean) => void
}

const Toast = React.forwardRef<HTMLDivElement, ToastProps>(
  ({ className, variant, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn(toastVariants({ variant }), className)}
        {...props}
      />
    )
  }
)
Toast.displayName = "Toast"

const ToastIcon = ({ variant }: { variant?: "default" | "success" | "error" | "warning" | "info" }) => {
  switch (variant) {
    case "success":
      return <CheckCircle className="h-3.5 w-3.5 flex-shrink-0" />
    case "error":
      return <XCircle className="h-3.5 w-3.5 flex-shrink-0" />
    case "warning":
      return <AlertCircle className="h-3.5 w-3.5 flex-shrink-0" />
    case "info":
      return <Info className="h-3.5 w-3.5 flex-shrink-0" />
    default:
      return null
  }
}

const ToastTitle = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLParagraphElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("text-xs font-medium", className)}
    {...props}
  />
))
ToastTitle.displayName = "ToastTitle"

const ToastDescription = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLParagraphElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("text-[11px] opacity-90", className)}
    {...props}
  />
))
ToastDescription.displayName = "ToastDescription"

const ToastClose = React.forwardRef<
  HTMLButtonElement,
  React.ButtonHTMLAttributes<HTMLButtonElement>
>(({ className, ...props }, ref) => (
  <button
    ref={ref}
    className={cn(
      "absolute right-1 top-1/2 -translate-y-1/2 rounded p-0.5 text-white/40 opacity-0 transition-opacity hover:text-white focus:opacity-100 focus:outline-none group-hover:opacity-100",
      className
    )}
    toast-close=""
    {...props}
  >
    <X className="h-3 w-3" />
  </button>
))
ToastClose.displayName = "ToastClose"

export {
  Toast,
  ToastTitle,
  ToastDescription,
  ToastClose,
  ToastIcon,
  toastVariants,
}
