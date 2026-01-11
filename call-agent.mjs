import { writeFileSync } from "node:fs";

const apiKey = process.env.AI_KEY;
const baseUrl = process.env.AI_BASE_URL;
const model = process.env.AI_MODEL;

const system =
  "You are a senior code-change agent. " +
  "Output a valid unified diff in git format. " +
  "For existing files use: --- a/file and +++ b/file " +
  "For new files use: --- /dev/null and +++ b/file " +
  "Include proper @@ hunk headers. " +
  "NO markdown fences, NO backticks, NO explanations. " +
  "If no change needed, output: NO_CHANGES";

const user =
  `Repo: ${process.env.REPO}\n` +
  `Issue: #${process.env.ISSUE_NUMBER}\n` +
  `Request:\n${process.env.COMMENT_BODY}\n\n` +
  "Return ONLY a unified diff or NO_CHANGES.";

const res = await fetch(`${baseUrl}/chat/completions`, {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${apiKey}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    model,
    messages: [
      { role: "system", content: system },
      { role: "user", content: user },
    ],
    temperature: 0.1
  }),
});

const data = await res.json();
let content = data?.choices?.[0]?.message?.content || "NO_CHANGES";

// ADVANCED CLEANING: Claude's fix + removing common AI conversational filler
content = content
  .replace(/```[a-z]*\s*\n/g, "") // Removes starting fences
  .replace(/```\s*$/g, "")       // Removes ending fences
  .replace(/^(Certainly|Here is|I have).*\n/gi, "") // Removes conversational preamble
  .replace(/\r\n/g, "\n")
  .trim();

writeFileSync("agent.patch", content + "\n", "utf8");
