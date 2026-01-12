// const API_BASE = process.env.NEXT_PUBLIC_API_URL!;

/* ---------- CHAT ---------- */
export async function sendChatMessage(message: string, history: string[] = []) {
  const res = await fetch(`/ask`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      message,
      history,
    }),
  });

  if (!res.ok) {
    throw new Error("Failed to fetch chat response, error " + res.status);
  }

  return res.json();
}

export async function sendResponseFeedback(
  queryId: string,
  isHelpful: boolean
): Promise<void> {
  try {
    const res = await fetch(`/feedback`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        query_id: queryId,
        isHelpful: isHelpful,
      }),
    });

    if (!res.ok) {
      throw new Error(`Feedback request failed with status ${res.status}`);
    }
  } catch (error) {
    console.error("Failed to send feedback:", error);
  }
}

