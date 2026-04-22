"use client";

import type { ChangeEvent } from "react";

import { Textarea } from "@/components/ui/textarea";

interface RequirementsInputProps {
  value: string;
  onChange: (value: string) => void;
}

// Keeps the requirements textarea isolated so future validation and parsing concerns stay out of the page file.
export function RequirementsInput({ value, onChange }: RequirementsInputProps) {
  const handleChange = (event: ChangeEvent<HTMLTextAreaElement>) => {
    onChange(event.target.value);
  };

  return (
    <Textarea
      id="requirements"
      label="Product requirements"
      hint="Paste raw notes, specs, or backlog text. Generation logic is intentionally not wired up yet."
      placeholder="Describe the feature, constraints, personas, and expected outcomes..."
      rows={10}
      value={value}
      onChange={handleChange}
    />
  );
}