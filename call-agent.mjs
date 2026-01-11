import { writeFileSync } from "node:fs";
const apiKey = process.env.MINIMAX_API_KEY;
const payload = {
  model: "MiniMax-M2.1",
  messages: [
    { role: "system", content: "Output MUST be a single unified diff patch only. No markdown." },
    { role: "user", content: process.env.COMMENT_BODY }
  ],
};
const res = await fetch("https://api.minimax.io/v1/chat/completions", {
  method: "POST",
  headers: { 
    "Authorization": `Bearer ${apiKey}`,
    "Content-Type": "application/json" 
  },
  body: JSON.stringify(payload),
});
const data = await res.json();
const content = data?.choices?.[0]?.message?.content || "NO_CHANGES";
writeFileSync("agent_output.txt", content, "utf8");
