import * as React from "react"
import { ChevronDown } from "lucide-react"
import { cn } from "@/lib/utils"

interface CollapsibleProps {
  open?: boolean
  onOpenChange?: (open: boolean) => void
  children: React.ReactNode
  trigger: React.ReactNode
  className?: string
}

export function Collapsible({ open, onOpenChange, children, trigger, className }: CollapsibleProps) {
  return (
    <div className={cn("w-full", className)}>
      <button
        type="button"
        onClick={() => onOpenChange?.(!open)}
        className="w-full"
      >
        {trigger}
      </button>
      <div
        className={cn(
          "overflow-hidden transition-all duration-200 ease-in-out",
          open ? "max-h-[500px] opacity-100" : "max-h-0 opacity-0"
        )}
      >
        <div className="pt-2">
          {children}
        </div>
      </div>
    </div>
  )
}
