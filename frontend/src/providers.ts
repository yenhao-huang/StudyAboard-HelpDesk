export type Role = "system" | "user" | "assistant";
export type ChatMessage = { role: Role; content: string };

export const simpleProvider = async (history: ChatMessage[], { signal }: { signal?: AbortSignal } = {}) => {
    const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: history }),
        signal,
    });
    const json = await res.json();
    return json.reply as string;
};

export const sseProvider = async function* (history: ChatMessage[], { signal }: { signal?: AbortSignal } = {}) {
    const res = await fetch("/api/chat/stream", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: history }),
        signal,
    });
    const reader = res.body!.getReader();
    const dec = new TextDecoder();
    let buffer = "";
    while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        buffer += dec.decode(value, { stream: true });
        const parts = buffer.split("\n\n");
        buffer = parts.pop() || "";
        for (const chunk of parts) {
            if (!chunk.startsWith("data:")) continue;
            const data = chunk.slice(5).trim();
            if (data === "[DONE]") return;
            yield data;
        }
    }
};
