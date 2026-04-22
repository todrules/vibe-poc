import type { TextareaHTMLAttributes } from "react";

import { cn } from "@/components/ui/utils";

interface TextareaProps extends TextareaHTMLAttributes<HTMLTextAreaElement> {
  label: string;
  hint?: string;
}

// A typed textarea wrapper keeps the page component focused on structure instead of field markup.
export function Textarea({ className, label, hint, id, ...props }: TextareaProps) {
  return (
    <label htmlFor={id} className="flex w-full flex-col gap-2">
      <span className="text-sm font-semibold text-ink">{label}</span>
      <textarea
        id={id}
        className={cn(
          "min-h-40 rounded-2xl border border-line bg-white px-4 py-3 text-sm text-ink shadow-sm outline-none transition placeholder:text-slate-400 focus:border-accent focus:ring-4 focus:ring-accent/10",
          className,
        )}
        {...props}
      />
      {hint ? <span className="text-sm text-slate-600">{hint}</span> : null}
    </label>
  );
}