export default function RequirementInput() {
  return (
    <section>
      <h2>Input</h2>
      <label htmlFor="requirements-text">Requirements</label>
      <textarea id="requirements-text" placeholder="Type requirements here..." rows={8} />
      <div>
        <label htmlFor="requirements-file">Upload requirement text</label>
        <input id="requirements-file" type="file" accept=".txt" />
      </div>
      <button type="button">Generate</button>
    </section>
  );
}
