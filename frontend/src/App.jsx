import React from 'react';
import RequirementInput from './components/RequirementInput';
import OutputSection from './components/OutputSection';

const placeholders = [
  { title: 'Acceptance Criteria (Gherkin)', content: '' },
  { title: 'Agent Prompts (System / Task / Persona)', content: '' },
  { title: 'User Stories', content: '' },
  { title: 'Test Cases', content: '' },
];

export default function App() {
  return (
    <main>
      <h1>Requirements Generator</h1>
      <RequirementInput />
      {placeholders.map((item) => (
        <OutputSection key={item.title} title={item.title} content={item.content} />
      ))}
    </main>
  );
}
