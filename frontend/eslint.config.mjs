import nextCoreWebVitals from "eslint-config-next/core-web-vitals";
import nextTypeScript from "eslint-config-next/typescript";

// Next.js now exposes flat configs directly, which avoids compatibility-layer issues with ESLint 9.
const eslintConfig = [
  ...nextCoreWebVitals,
  ...nextTypeScript,
  {
    ignores: [".next/**", "node_modules/**"],
  },
];

export default eslintConfig;