"use client";

import { useState } from "react";
import ReactMarkdown from "react-markdown";
import { sendChatMessage, sendResponseFeedback } from "@/lib/api";

type UserMessage = { role: "user"; text: string };
type AssistantMessage = {
  role: "assistant";
  text: string;
  queryId?: string;
  sources?: string[];
  isUnsafe?: boolean;
  feedback?: "helpful" | "not_helpful" | null;
};

type Message = UserMessage | AssistantMessage;

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function sendMessage() {
    if (!input.trim() || loading) return;

    setError("");
    setMessages((prev) => [...prev, { role: "user", text: input }]);
    setLoading(true);

    try {
      const data = await sendChatMessage(input);

      const assistantMsg: AssistantMessage = {
        role: "assistant",
        queryId: data.query_id,
        text: data.answer,
        sources: data.sources ?? [],
        isUnsafe: !!data.isUnsafe,
        feedback: null,
      };

      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err: any) {
      setError("Failed to reach backend, error: " + (err?.message ?? String(err)));
    } finally {
      setInput("");
      setLoading(false);
    }
  }

  function handleFeedback(queryId?: string, isHelpful?: boolean) {
    if (!queryId) return;

    // Send feedback but don't block the UI (fire-and-forget)
    sendResponseFeedback(queryId, !!isHelpful).catch((e) => {
      console.error("Failed to send feedback", e);
    });

    // Optimistically mark feedback on the message
    setMessages((prev) =>
      prev.map((m) =>
        m.role === "assistant" && m.queryId === queryId
          ? { ...m, feedback: isHelpful ? "helpful" : "not_helpful" }
          : m
      )
    );
  }

  return (
    <main className="max-w-3xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">Yoga Mantri</h1>

      {/* ---------- CHAT WINDOW ---------- */}
      <div className="border rounded p-4 h-[60vh] overflow-y-auto mb-4">
        {messages.map((m, i) => (
          <div key={i} className="mb-4">
            <strong>{m.role === "user" ? "You" : "Assistant"}:</strong>

            <div className="prose max-w-none mt-1">
              {"role" in m && m.role === "assistant" ? (
                <>
                  {m.isUnsafe && (
                    <div className="bg-red-50 border-l-4 border-red-400 p-2 mb-2 text-sm">
                      This question touches on a safety-sensitive topic. The response is general in nature — for personalized advice, consider consulting a qualified professional.
                    </div>
                  )}

                  <ReactMarkdown>{m.text}</ReactMarkdown>

                  {m.sources && m.sources.length > 0 && (
                    <p className="text-sm text-gray-500 mt-1">Sources: {m.sources.join(", ")}</p>
                  )}

                  <div className="flex gap-2 mt-2">
                    <button
                      onClick={() => handleFeedback(m.queryId, true)}
                      disabled={!m.queryId || m.feedback === "helpful"}
                      className="px-2 py-1 text-sm border rounded disabled:opacity-50"
                    >
                      👍 Helpful
                    </button>

                    <button
                      onClick={() => handleFeedback(m.queryId, false)}
                      disabled={!m.queryId || m.feedback === "not_helpful"}
                      className="px-2 py-1 text-sm border rounded disabled:opacity-50"
                    >
                      👎 Not Helpful
                    </button>

                    {m.feedback && (
                      <span className="text-sm text-gray-500 self-center">
                        {m.feedback === "helpful" ? "Thanks for the feedback" : "Thanks — we'll try to improve"}
                      </span>
                    )}
                  </div>
                </>
              ) : (
                <div>
                  <ReactMarkdown>{m.text}</ReactMarkdown>
                </div>
              )}
            </div>

          </div>
        ))}

        {loading && <p className="text-gray-500">Thinking...</p>}
      </div>

      {/* ---------- INPUT ---------- */}
      <div className="flex gap-2">
        <input
          className="border p-2 flex-1"
          placeholder="Ask about yoga, wellness, or safe practice..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              sendMessage();
            }
          }}
          aria-label="Your question"
        />

        <button
          onClick={sendMessage}
          disabled={loading}
          className="bg-black text-white px-4 disabled:opacity-50"
        >
          Send
        </button>
      </div>

      {error && <p className="text-red-500 mt-2">{error}</p>}
    </main>
  );
}
