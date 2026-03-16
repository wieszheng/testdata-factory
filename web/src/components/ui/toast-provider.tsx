import * as React from "react"
import { Toast, ToastTitle, ToastDescription, ToastClose, ToastIcon } from "./toast"

export interface ToastMessage {
  id: string
  title?: string
  description: string
  variant?: "default" | "success" | "error" | "warning" | "info"
}

interface ToastContextType {
  toasts: ToastMessage[]
  toast: (message: Omit<ToastMessage, "id">) => void
  dismiss: (id: string) => void
}

const ToastContext = React.createContext<ToastContextType | undefined>(undefined)

export function useToast() {
  const context = React.useContext(ToastContext)
  if (!context) {
    throw new Error("useToast must be used within a ToastProvider")
  }
  return context
}

export function ToastProvider({ children }: { children: React.ReactNode }) {
  const [toasts, setToasts] = React.useState<ToastMessage[]>([])

  const toast = React.useCallback((message: Omit<ToastMessage, "id">) => {
    const id = Math.random().toString(36).substring(2, 9)
    setToasts((prev) => [...prev, { ...message, id }])
    
    // 自动消失
    setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== id))
    }, 5000)
  }, [])

  const dismiss = React.useCallback((id: string) => {
    setToasts((prev) => prev.filter((t) => t.id !== id))
  }, [])

  return (
    <ToastContext.Provider value={{ toasts, toast, dismiss }}>
      {children}
      {/* Toast 容器 */}
      <div className="fixed top-4 right-4 z-[100] flex flex-col gap-2 max-w-sm">
        {toasts.map((t) => (
          <Toast
            key={t.id}
            variant={t.variant}
            className="animate-in slide-in-from-right-full"
          >
            <div className="flex items-start gap-3">
              <ToastIcon variant={t.variant} />
              <div className="flex-1">
                {t.title && <ToastTitle>{t.title}</ToastTitle>}
                <ToastDescription>{t.description}</ToastDescription>
              </div>
            </div>
            <ToastClose onClick={() => dismiss(t.id)} />
          </Toast>
        ))}
      </div>
    </ToastContext.Provider>
  )
}
