import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

// Shared class merging avoids repeated string conditionals across the UI scaffold.
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}