export default function OutputSection({ title, content }) {
  return (
    <details>
      <summary>{title}</summary>
      <pre>{content || 'Generated output will appear here.'}</pre>
    </details>
  );
}
