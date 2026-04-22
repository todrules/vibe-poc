import type { Metadata } from "next";
import { Manrope } from "next/font/google";

import "./globals.css";

const manrope = Manrope({
  subsets: ["latin"],
  variable: "--font-manrope",
});

export const metadata: Metadata = {
  title: "Requirements Generator",
  description: "Frontend scaffold for structured artifact generation from product requirements.",
};

// The root layout keeps global styling and metadata server-rendered by default.
export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${manrope.variable} bg-canvas font-sans text-ink antialiased`}>
        {children}
      </body>
    </html>
  );
}