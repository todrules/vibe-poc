import { GeneratorWorkspace } from "@/components/GeneratorWorkspace";

// The route remains server-rendered while the interactive scaffold lives in a dedicated client component.
export default function Page() {
  return <GeneratorWorkspace />;
}