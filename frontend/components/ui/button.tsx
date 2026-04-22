import type { ButtonHTMLAttributes } from "react";

import { cn } from "@/components/ui/utils";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary";
}

// This keeps button styling centralized and aligned with the intended clean, modern visual direction.
export function Button({ className, variant = "primary", type = "button", ...props }: ButtonProps) {
  return (
    <button
      type={type}
      className={cn(
        "inline-flex items-center justify-center rounded-xl px-4 py-3 text-sm font-semibold transition focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent disabled:cursor-not-allowed disabled:opacity-60",
        variant === "primary" && "bg-ink text-white hover:bg-slate-800",
        variant === "secondary" && "border border-line bg-white text-ink hover:bg-slate-50",
        className,
      )}
      {...props}
    />
  );
}