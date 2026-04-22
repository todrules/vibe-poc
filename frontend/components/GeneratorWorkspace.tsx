"use client";

import { useState } from "react";

import { AlertCircle, File02, ZapFast } from "@untitledui/icons";

import { FileUpload } from "@/components/FileUpload";
import { GenerateButton } from "@/components/GenerateButton";
import { OutputSection } from "@/components/OutputSection";
import { RequirementsInput } from "@/components/RequirementsInput";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { generateArtifacts } from "@/services/api";
import type {
  AcceptanceCriteriaItem,
  AgentPrompts,
  GenerateResponsePayload,
  OutputSectionState,
} from "@/types/generation";

const outputSections: OutputSectionState[] = [
  {
    category: "acceptanceCriteria",
    title: "Acceptance Criteria",
    description: "Structured conditions of satisfaction for the requested feature.",
    content: "",
  },
  {
    category: "agentPrompts",
    title: "Agent Prompts",
    description: "Placeholder system, persona, and task prompt blocks.",
    content: "",
  },
  {
    category: "userStories",
    title: "User Stories",
    description: "Narratives for users, goals, and expected value.",
    content: "",
  },
  {
    category: "testCases",
    title: "Test Cases",
    description: "Coverage-oriented scenarios and expected results.",
    content: "",
  },
];

function formatAcceptanceCriteria(items: AcceptanceCriteriaItem[]): string {
  if (items.length === 0) {
    return "";
  }

  return items
    .map((item, index) => {
      return `${index + 1}. ${item.title}\n${item.gherkin}`;
    })
    .join("\n\n");
}

function formatAgentPrompts(prompts: AgentPrompts): string {
  return [
    "System",
    prompts.system,
    "",
    "Task",
    prompts.task,
    "",
    "Persona",
    prompts.persona,
  ].join("\n");
}

function formatStringList(items: string[]): string {
  if (items.length === 0) {
    return "";
  }

  return items.map((item, index) => `${index + 1}. ${item}`).join("\n\n");
}

function toSectionContentByCategory(response: GenerateResponsePayload): Record<OutputSectionState["category"], string> {
  return {
    acceptanceCriteria: formatAcceptanceCriteria(response.acceptanceCriteria),
    agentPrompts: formatAgentPrompts(response.agentPrompts),
    userStories: formatStringList(response.userStories),
    testCases: formatStringList(response.testCases),
  };
}

// Client-side interaction state for the scaffold lives here so the route file can remain a server component.
export function GeneratorWorkspace() {
  const [requirements, setRequirements] = useState("");
  const [fileText, setFileText] = useState<string>("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [sectionContents, setSectionContents] = useState<Record<OutputSectionState["category"], string>>({
    acceptanceCriteria: "",
    agentPrompts: "",
    userStories: "",
    testCases: "",
  });

  const handleFileUpload = async (file: File | null): Promise<void> => {
    if (!file) {
      setFileText("");
      return;
    }

    try {
      const content = await file.text();
      setFileText(content);
      setError(null);
    } catch {
      setError("Unable to read the selected file. Please try another .txt file.");
      setFileText("");
    }
  };

  const handleGenerate = async (): Promise<void> => {
    const trimmedRequirements = requirements.trim();
    if (!trimmedRequirements) {
      setError("Please add product requirements before generating outputs.");
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await generateArtifacts({
        requirements: trimmedRequirements,
        fileText: fileText.trim() ? fileText : undefined,
      });

      setSectionContents(toSectionContentByCategory(response));
    } catch (caughtError) {
      const message =
        caughtError instanceof Error
          ? caughtError.message
          : "Something went wrong while generating outputs.";
      setError(message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="mx-auto flex min-h-screen w-full max-w-7xl flex-col gap-8 px-4 py-8 sm:px-6 lg:px-8 lg:py-12">
      <section className="grid gap-6 lg:grid-cols-[1.05fr_0.95fr] lg:items-start">
        <div className="space-y-5">
          <div className="inline-flex items-center gap-2 rounded-full border border-accent/20 bg-accent/8 px-3 py-1 text-sm font-medium text-accent">
            <ZapFast aria-hidden="true" className="size-4" />
            Requirements generator UI scaffold
          </div>

          <div className="space-y-3">
            <h1 className="max-w-3xl text-balance text-4xl font-semibold tracking-tight text-ink sm:text-5xl">
              Turn rough product requirements into structured delivery artifacts.
            </h1>
            <p className="max-w-2xl text-base leading-7 text-slate-600 sm:text-lg">
              Add requirements and generate acceptance criteria, agent prompts, user stories, and test cases from the backend service.
            </p>
          </div>
        </div>

        <Card>
          <CardHeader>
            <p className="text-sm font-semibold uppercase tracking-[0.16em] text-slate-500">Workspace</p>
            <h2 className="text-2xl font-semibold text-ink">Input requirements</h2>
            <p className="text-sm leading-6 text-slate-600">
              Paste a specification or upload a text file, then click Generate to run the backend workflow.
            </p>
          </CardHeader>
          <CardContent className="space-y-5">
            <RequirementsInput value={requirements} onChange={setRequirements} />
            <FileUpload onChange={(file) => void handleFileUpload(file)} />
            <div className="flex flex-col gap-3 border-t border-line/70 pt-5 sm:flex-row sm:items-center sm:justify-between">
              <p className="text-sm text-slate-600">Runs a live request to the backend `/generate` endpoint.</p>
              <GenerateButton
                isLoading={isLoading}
                disabled={!requirements.trim()}
                onClick={() => void handleGenerate()}
              />
            </div>
          </CardContent>
        </Card>
      </section>

      <section className="grid gap-4">
        <div className="flex items-center gap-3">
          <div className="flex size-11 items-center justify-center rounded-2xl bg-white shadow-sm ring-1 ring-line/70">
            <File02 aria-hidden="true" className="size-5 text-slate-700" />
          </div>
          <div>
            <h2 className="text-2xl font-semibold text-ink">Generated outputs</h2>
            <p className="text-sm text-slate-600">Each section updates from the latest backend generation response.</p>
          </div>
        </div>

        {error ? (
          <div className="flex items-start gap-3 rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
            <AlertCircle aria-hidden="true" className="mt-0.5 size-5 shrink-0" />
            <p>{error}</p>
          </div>
        ) : null}

        {isLoading ? (
          <div className="rounded-2xl border border-line/70 bg-white px-5 py-4 text-sm text-slate-600">
            Generating artifacts from your requirements...
          </div>
        ) : null}

        <div className="grid gap-4">
          {outputSections.map((section) => (
            <OutputSection
              key={section.category}
              title={section.title}
              description={section.description}
              content={sectionContents[section.category]}
            />
          ))}
        </div>
      </section>
    </main>
  );
}