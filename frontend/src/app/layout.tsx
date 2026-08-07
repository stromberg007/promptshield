import "@/styles/globals.css";
import Navbar from "@/components/Navbar";

export const metadata = {
  title: "PromptShield AI - Static Analysis Security Scanner for Prompts",
  description: "Enterprise static analysis scanner detecting prompt injections, secrets, jailbreaks, and unicode obfuscation.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <Navbar />
        <main style={{ minHeight: "calc(100vh - 64px)", paddingBottom: 60 }}>
          {children}
        </main>
      </body>
    </html>
  );
}
