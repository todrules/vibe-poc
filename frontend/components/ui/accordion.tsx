"use client";

import type { HTMLAttributes, ReactNode } from "react";
import { useState } from "react";

import { ChevronDown } from "@untitledui/icons";

import { cn } from "@/components/ui/utils";

interface AccordionProps extends HTMLAttributes<HTMLDivElement> {
  title: string;
  description?: string;
  defaultOpen?: boolean;
  actions?: ReactNode;
}

// This lightweight accordion matches the intended information architecture until fuller Untitled UI components are introduced.
export function Accordion({
  title,
  description,
  defaultOpen = false,
  actions,
  children,
  className,
  ...props
}: AccordionProps) {
  const [isOpen, setIsOpen] = useState(defaultOpen);

  return (
    <div className={cn("overflow-hidden rounded-2xl border border-line/70 bg-panel", className)} {...props}>
      <div className="flex w-full items-center gap-3 px-5 py-4 transition hover:bg-black/[0.02]">
        <button
          type="button"
          aria-expanded={isOpen}
          onClick={() => setIsOpen((current) => !current)}
          className="flex min-w-0 flex-1 items-start justify-between gap-4 text-left"
        >
          <div className="space-y-1">
            <p className="text-sm font-semibold text-ink">{title}</p>
            {description ? <p className="text-sm text-slate-600">{description}</p> : null}
          </div>
          <ChevronDown
            aria-hidden="true"
            className={cn("mt-0.5 size-5 shrink-0 text-slate-500 transition-transform", isOpen && "rotate-180")}
          />
        </button>

        {actions ? <div className="flex shrink-0 items-center">{actions}</div> : null}
      </div>

      {isOpen ? <div className="border-t border-line/70 px-5 py-4">{children}</div> : null}
    </div>
  );
}