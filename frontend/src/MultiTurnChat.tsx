import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { Bot, Send, User, Trash2, RefreshCw, StopCircle, Download, Share2, ChevronDown } from "lucide-react";

/**
 * ChatGPT-like Multi‑Turn Chatbot UI (React + Tailwind)
 * ----------------------------------------------------
 * ✅ 重點
 * - 上方：品牌列 + 模型切換（僅 UI）+ 分享按鈕（僅 UI）
 * - 中間：對話串（氣泡）
 * - 下方：固定輸入列（像 ChatGPT）
 * - 支援串流 / 停止 / 重生 / 清空 / 匯出
 * - localStorage 持久化
 *
 * 🔌 串接：傳入 chatProvider（非串流回字串，或 AsyncGenerator 串流 token）
 */

// ——— 型別 ———
export type Role = "system" | "user" | "assistant";
export type ChatMessage = { id: string; role: Role; content: string; ts: number };
export type ChatProvider = (
    history: ChatMessage[],
    options?: { signal?: AbortSignal }
) => AsyncGenerator<string> | Promise<string>;

// ——— 小工具 ———
function nanoid(size = 12) {
    const bytes = crypto.getRandomValues(new Uint8Array(size));
    const alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz-";
    return Array.from(bytes, (b) => alphabet[b % alphabet.length]).join("");
}

function formatTime(ts: number) {
    const d = new Date(ts);
    return d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

async function* typewriter(text: string, delayMs = 10) {
    for (const ch of text) {
        await new Promise((r) => setTimeout(r, delayMs));
        yield ch;
    }
}

// ——— 預設 mock（展示串流）———
const mockChatProvider: ChatProvider = async function* (history) {
    const last = [...history].reverse().find((m) => m.role === "user");
    const sys = history.find((m) => m.role === "system");
    const reply = `這是示範回覆（本地模擬串流）。

` +
        (sys ? `System：${sys.content}

` : "") +
        `你剛剛說：「${last?.content ?? "(無)"}」。`;
    yield* typewriter(reply, 8);
};

// ——— Header（上方模型切換 + 分享；僅 UI）———
function Header() {
    return (
        <header className="sticky top-0 z-10 border-b border-slate-200 bg-white/70 backdrop-blur supports-[backdrop-filter]:bg-white/60">
            <div className="mx-auto max-w-5xl px-4 h-12 flex items-center justify-between">
                <div className="flex items-center gap-2 text-slate-800 font-semibold">
                    <Bot className="h-5 w-5" />
                    <span>Chatbot</span>
                    <span className="text-slate-400">·</span>
                    <button disabled className="inline-flex items-center gap-1 rounded-lg border border-slate-200 px-2.5 py-1.5 text-sm text-slate-600 bg-white/70">
                        gpt-like <ChevronDown className="h-3.5 w-3.5" />
                    </button>
                </div>
                <div className="flex items-center gap-2">
                    <button disabled title="尚未實作"
                        className="inline-flex items-center gap-1 rounded-lg border border-slate-200 px-3 py-1.5 text-sm text-slate-600 bg-white/70">
                        <Share2 className="h-4 w-4" /> 分享
                    </button>
                </div>
            </div>
        </header>
    );
}

// ——— 氣泡 ———
function Bubble({ msg }: { msg: ChatMessage }) {
    const isUser = msg.role === "user";
    return (
        <div className={`flex gap-3 ${isUser ? "justify-end" : "justify-start"}`}>
            {!isUser && (
                <div className="mt-1 shrink-0 rounded-full bg-slate-200 p-2 text-slate-700">
                    <Bot className="h-4 w-4" />
                </div>
            )}
            <div className={`${isUser ? "bg-blue-600 text-white" : "bg-white text-slate-900 border border-slate-200"} max-w-[80%] rounded-2xl px-4 py-2 shadow-sm whitespace-pre-wrap leading-relaxed`}>
                <div className="text-[10px] opacity-70 mb-1">{formatTime(msg.ts)}</div>
                {msg.content}
            </div>
            {isUser && (
                <div className="mt-1 shrink-0 rounded-full bg-blue-100 p-2 text-blue-700">
                    <User className="h-4 w-4" />
                </div>
            )}
        </div>
    );
}

// ——— 主元件 ———
export default function ChatbotUI({
    chatProvider = mockChatProvider,
    storageKey = "chatbot-ui-multiturn",
}: {
    chatProvider?: ChatProvider;
    storageKey?: string;
}) {
    const [messages, setMessages] = useState<ChatMessage[]>(() => {
        const raw = localStorage.getItem(storageKey);
        if (raw) { try { return JSON.parse(raw) as ChatMessage[] } catch { /* ignore */ } }
        return [{ id: nanoid(), role: "assistant", content: "嗨！我在這裡，隨時等你提問。", ts: Date.now() }];
    });
    const [systemPrompt, setSystemPrompt] = useState("");
    const [draft, setDraft] = useState("");
    const [isStreaming, setIsStreaming] = useState(false);
    const [abortCtrl, setAbortCtrl] = useState<AbortController | null>(null);

    const endRef = useRef<HTMLDivElement>(null);

    useEffect(() => { localStorage.setItem(storageKey, JSON.stringify(messages)); }, [messages, storageKey]);
    useEffect(() => { endRef.current?.scrollIntoView({ behavior: "smooth" }); }, [messages.length, isStreaming]);

    const fullHistory: ChatMessage[] = useMemo(() => {
        if (!systemPrompt.trim()) return messages;
        const sys: ChatMessage = { id: "sys", role: "system", content: systemPrompt.trim(), ts: Date.now() };
        return [sys, ...messages];
    }, [messages, systemPrompt]);

    const send = useCallback(async () => {
        const content = draft.trim();
        if (!content || isStreaming) return;
        setDraft("");

        const userMsg: ChatMessage = { id: nanoid(), role: "user", content, ts: Date.now() };
        const asstMsg: ChatMessage = { id: nanoid(), role: "assistant", content: "", ts: Date.now() };
        setMessages((prev) => [...prev, userMsg, asstMsg]);

        const controller = new AbortController();
        setAbortCtrl(controller);
        setIsStreaming(true);

        try {
            const stream = await chatProvider([...fullHistory, userMsg], { signal: controller.signal });
            if (typeof (stream as any)[Symbol.asyncIterator] !== "function") {
                setMessages((prev) => prev.map((m) => (m.id === asstMsg.id ? { ...m, content: String(stream as any) } : m)));
            } else {
                for await (const token of stream as AsyncGenerator<string>) {
                    if (controller.signal.aborted) break;
                    setMessages((prev) => prev.map((m) => (m.id === asstMsg.id ? { ...m, content: (m.content || "") + token } : m)));
                }
            }
        } catch (err: any) {
            const msg = err?.name === "AbortError" ? "（已停止）" : `發生錯誤：${err?.message ?? err}`;
            setMessages((prev) => prev.map((m) => (m.id === asstMsg.id ? { ...m, content: msg } : m)));
        } finally {
            setIsStreaming(false);
            setAbortCtrl(null);
        }
    }, [draft, isStreaming, chatProvider, fullHistory]);

    const stop = useCallback(() => { abortCtrl?.abort(); }, [abortCtrl]);

    const clear = useCallback(() => {
        if (isStreaming) return;
        setMessages([{ id: nanoid(), role: "assistant", content: "新對話開始。", ts: Date.now() }]);
    }, [isStreaming]);

    const exportJson = useCallback(() => {
        const blob = new Blob([JSON.stringify({ systemPrompt, messages }, null, 2)], { type: "application/json" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url; a.download = `chat_${new Date().toISOString().replace(/[:.]/g, "-")}.json`; a.click();
        URL.revokeObjectURL(url);
    }, [messages, systemPrompt]);

    const regenerate = useCallback(async () => {
        if (isStreaming) return;
        const lastUserIdx = [...messages].map((m) => m.role).lastIndexOf("user");
        if (lastUserIdx === -1) return;
        const base = messages.slice(0, lastUserIdx + 1);
        const asstMsg: ChatMessage = { id: nanoid(), role: "assistant", content: "", ts: Date.now() };
        setMessages([...base, asstMsg]);

        const controller = new AbortController();
        setAbortCtrl(controller);
        setIsStreaming(true);

        try {
            const history: ChatMessage[] = systemPrompt
                ? [{ id: "sys", role: "system", content: systemPrompt, ts: Date.now() }, ...base]
                : base;
            const stream = await chatProvider(history, { signal: controller.signal });
            if (typeof (stream as any)[Symbol.asyncIterator] !== "function") {
                setMessages((prev) => prev.map((m) => (m.id === asstMsg.id ? { ...m, content: String(stream as any) } : m)));
            } else {
                for await (const token of stream as AsyncGenerator<string>) {
                    if (controller.signal.aborted) break;
                    setMessages((prev) => prev.map((m) => (m.id === asstMsg.id ? { ...m, content: (m.content || "") + token } : m)));
                }
            }
        } catch (err: any) {
            const msg = err?.name === "AbortError" ? "（已停止）" : `發生錯誤：${err?.message ?? err}`;
            setMessages((prev) => prev.map((m) => (m.id === asstMsg.id ? { ...m, content: msg } : m)));
        } finally {
            setIsStreaming(false);
            setAbortCtrl(null);
        }
    }, [messages, chatProvider, isStreaming, systemPrompt]);

    return (
        <div className="min-h-screen w-full bg-slate-50 text-slate-800 flex flex-col">
            <Header />

            {/* 內容 */}
            <main className="flex-1">
                <div className="mx-auto max-w-3xl px-4 pt-4 pb-28 space-y-3">
                    {/* System prompt（可選） */}
                    <div className="rounded-xl border border-slate-200 bg-white/90 p-3">
                        <label className="text-xs text-slate-500">System Prompt（可留空）</label>
                        <textarea
                            className="mt-1 w-full rounded-lg border border-slate-200 bg-white/95 p-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                            placeholder="你是 helpful、謹慎且多語的 AI 助手。回答請簡潔、具條理。"
                            value={systemPrompt}
                            onChange={(e) => setSystemPrompt(e.target.value)}
                            rows={2}
                        />
                    </div>

                    {/* 對話區 */}
                    <div className="space-y-3">
                        {messages.map((m) => (<Bubble key={m.id} msg={m} />))}
                        {isStreaming && (
                            <div className="flex items-center gap-2 text-xs text-slate-500">
                                <div className="h-2 w-2 animate-pulse rounded-full bg-slate-400" /> 產生中…
                            </div>
                        )}
                        <div ref={endRef} />
                    </div>
                </div>
            </main>

            {/* 底部輸入列（固定） */}
            <div className="sticky bottom-0 z-10 border-t border-slate-200 bg-white/90 backdrop-blur supports-[backdrop-filter]:bg-white/70">
                <div className="mx-auto max-w-3xl px-4 py-3">
                    <div className="rounded-2xl border border-slate-200 bg-white p-2 shadow-[0_1px_10px_rgba(0,0,0,0.04)]">
                        <textarea
                            value={draft}
                            onChange={(e) => setDraft(e.target.value)}
                            onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(); } }}
                            rows={3}
                            placeholder={isStreaming ? "正在回覆中…" : "輸入訊息，Shift+Enter 換行，Enter 送出"}
                            disabled={isStreaming}
                            className="w-full resize-none rounded-xl p-3 text-[15px] leading-6 focus:outline-none border border-slate-200 focus:ring-2 focus:ring-blue-500 bg-white/95"
                        />
                        <div className="mt-2 flex items-center justify-between">
                            <div className="text-xs text-slate-500">Enter 送出、Shift+Enter 換行</div>
                            <div className="flex items-center gap-2">
                                <button onClick={exportJson} className="inline-flex items-center gap-1 rounded-xl border border-slate-200 px-3 py-1.5 text-sm hover:bg-slate-50">
                                    <Download className="h-4 w-4" /> 匯出
                                </button>
                                <button onClick={clear} disabled={isStreaming} className="inline-flex items-center gap-1 rounded-xl border border-slate-200 px-3 py-1.5 text-sm hover:bg-slate-50 disabled:opacity-50">
                                    <Trash2 className="h-4 w-4" /> 清空
                                </button>
                                {!isStreaming ? (
                                    <button onClick={regenerate} className="inline-flex items-center gap-1 rounded-xl border border-slate-200 px-3 py-1.5 text-sm hover:bg-slate-50">
                                        <RefreshCw className="h-4 w-4" /> 重生
                                    </button>
                                ) : (
                                    <button onClick={stop} className="inline-flex items-center gap-1 rounded-xl border border-red-200 bg-red-50 px-3 py-1.5 text-sm text-red-700 hover:bg-red-100">
                                        <StopCircle className="h-4 w-4" /> 停止
                                    </button>
                                )}
                                <button onClick={send} disabled={isStreaming || draft.trim().length === 0} className="inline-flex items-center gap-1 rounded-xl bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-blue-700 disabled:opacity-50">
                                    <Send className="h-4 w-4" /> 傳送
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

/*
 * 連接後端：請參考先前訊息中的 simpleProvider / sseProvider，
 * 或把你的 fetch provider 直接傳入 <ChatbotUI chatProvider={...} />。
 */
