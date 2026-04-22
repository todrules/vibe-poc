"use client";

import { useState } from "react";

import { Check, Copy01 } from "@untitledui/icons";

import { Accordion } from "@/components/ui/accordion";
import { Button } from "@/components/ui/button";

interface OutputSectionProps {
  title: string;
  description: string;
  content: string;
}

// Each output block is intentionally isolated so future generated data can be streamed or refreshed independently.
export function OutputSection({ title, description, content }: OutputSectionProps) {
  const [isCopied, setIsCopied] = useState(false);

  const handleCopy = async () => {
    if (!content) {
      return;
    }

    await navigator.clipboard.writeText(content);
    setIsCopied(true);
    window.setTimeout(() => setIsCopied(false), 2000);
  };

  return (
    <Accordion
      title={title}
      description={description}
      defaultOpen
      actions={
        <Button
          variant="secondary"
          className="px-3 py-2 text-xs"
          onClick={(event) => {
            event.stopPropagation();
            void handleCopy();
          }}
          disabled={!content}
        >
          {isCopied ? <Check aria-hidden="true" className="mr-1.5 size-4" /> : <Copy01 aria-hidden="true" className="mr-1.5 size-4" />}
          {isCopied ? "Copied" : "Copy"}
        </Button>
      }
    >
      <pre className="overflow-x-auto rounded-xl bg-slate-950 px-4 py-4 text-sm leading-6 text-slate-100">
        {content || "Generated output will appear here once generation is connected."}
      </pre>
    </Accordion>
  );
}