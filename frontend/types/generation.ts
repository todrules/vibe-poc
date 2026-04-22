// Shared placeholder shapes for the four artifact categories rendered by the UI.

export type OutputCategory =
  | "acceptanceCriteria"
  | "agentPrompts"
  | "userStories"
  | "testCases";

export interface AcceptanceCriteriaItem {
  title: string;
  gherkin: string;
}

export interface AgentPrompts {
  system: string;
  task: string;
  persona: string;
}

export interface GenerateRequestPayload {
  requirements: string;
  fileText?: string;
}

export interface GenerateResponsePayload {
  acceptanceCriteria: AcceptanceCriteriaItem[];
  agentPrompts: AgentPrompts;
  userStories: string[];
  testCases: string[];
}

export interface OutputSectionState {
  category: OutputCategory;
  title: string;
  description: string;
  content: string;
}