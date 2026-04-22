"use client";

import { ArrowRight, RefreshCw05 } from "@untitledui/icons";

import { Button } from "@/components/ui/button";

interface GenerateButtonProps {
  isLoading?: boolean;
  disabled?: boolean;
  onClick?: () => void;
}

// Centralizing the CTA makes it easy to later connect transitions, analytics, and submit state from one place.
export function GenerateButton({
  isLoading = false,
  disabled = false,
  onClick,
}: GenerateButtonProps) {
  return (
    <Button className="w-full sm:w-auto" disabled={disabled || isLoading} onClick={onClick}>
      {isLoading ? <RefreshCw05 aria-hidden="true" className="mr-2 size-4 animate-spin" /> : <ArrowRight aria-hidden="true" className="mr-2 size-4" />}
      {isLoading ? "Generating..." : "Generate"}
    </Button>
  );
}