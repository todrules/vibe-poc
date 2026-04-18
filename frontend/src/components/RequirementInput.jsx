export default function RequirementInput() {
  return (
    <section>
      <h2>Input</h2>
      <textarea placeholder="Type requirements here..." rows={8} />
      <div>
        <input type="file" accept=".txt" />
      </div>
      <button type="button">Generate</button>
    </section>
  );
}
