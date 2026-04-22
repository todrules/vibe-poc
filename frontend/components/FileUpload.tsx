"use client";

import type { ChangeEvent } from "react";

import { File02, UploadCloud02 } from "@untitledui/icons";

interface FileUploadProps {
  onChange?: (file: File | null) => void;
}

// This component is a placeholder dropzone-style picker for plain text requirements files.
export function FileUpload({ onChange }: FileUploadProps) {
  const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
    onChange?.(event.target.files?.[0] ?? null);
  };

  return (
    <label
      htmlFor="requirements-file"
      className="flex cursor-pointer flex-col items-center justify-center gap-3 rounded-2xl border border-dashed border-line bg-white px-5 py-8 text-center transition hover:border-accent/50 hover:bg-accent/5"
    >
      <span className="flex size-12 items-center justify-center rounded-2xl bg-accent/10 text-accent">
        <UploadCloud02 aria-hidden="true" className="size-6" />
      </span>
      <div className="space-y-1">
        <p className="text-sm font-semibold text-ink">Upload a text file</p>
        <p className="text-sm text-slate-600">Accepts `.txt` files only in this initial scaffold.</p>
      </div>
      <div className="inline-flex items-center gap-2 rounded-full border border-line px-3 py-1.5 text-xs font-medium text-slate-700">
        <File02 aria-hidden="true" className="size-4" />
        Browse file
      </div>
      <input id="requirements-file" type="file" accept=".txt,text/plain" className="sr-only" onChange={handleChange} />
    </label>
  );
}