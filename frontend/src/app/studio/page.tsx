"use client";

import { Suspense, useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { motion } from "framer-motion";
import { getConversation, stepConversation } from "@/lib/api";
import type { ConversationState } from "@/lib/types";
import { ScriptViewer } from "@/components/script-viewer/ScriptViewer";

function StudioContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const taskId = searchParams.get("task_id");
  const [conversation, setConversation] = useState<ConversationState | null>(null);
  const [feedback, setFeedback] = useState("");
  const [apiKey, setApiKey] = useState("");
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!taskId) {
      router.push("/");
      return;
    }

    setApiKey(sessionStorage.getItem(`chronoshift_api_key_${taskId}`) || "");

    (async () => {
      try {
        const res = await getConversation(taskId);
        setConversation(res.conversation);
      } catch {
        setError("加载创作会话失败");
      } finally {
        setLoading(false);
      }
    })();
  }, [taskId, router]);

  const handleStep = async () => {
    if (!taskId || !feedback.trim()) return;
    setSubmitting(true);
    setError(null);
    try {
      const res = await stepConversation(taskId, feedback, apiKey);
      setConversation(res.conversation);
      setFeedback("");
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : "继续生成失败";
      setError(msg);
    } finally {
      setSubmitting(false);
    }
  };

  if (!taskId) return null;

  return (
    <div className="max-w-6xl mx-auto px-4 py-10 space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <div>
          <h1 className="font-display text-2xl text-chrono-gold">多角色生成室</h1>
          <p className="text-sm text-gray-500">任务 ID：{taskId}</p>
        </div>
        <button
          onClick={() => router.push(`/result?task_id=${taskId}`)}
          className="px-4 py-2 rounded-lg border border-void-700 text-sm text-gray-300 hover:border-chrono-gold hover:text-chrono-gold"
        >
          定稿查看脚本
        </button>
      </div>

      {loading && <p className="text-sm text-gray-500">正在加载创作会话...</p>}
      {error && <p className="text-sm text-red-400">{error}</p>}

      {conversation && (
        <div className="grid grid-cols-1 lg:grid-cols-[1fr_1fr] gap-6">
          <section className="space-y-4">
            <div className="rounded-xl border border-void-800 bg-void-900/50 p-4 space-y-4 max-h-[680px] overflow-y-auto">
              {conversation.messages.map((message, index) => (
                <motion.div
                  key={`${message.created_at}-${index}`}
                  className="rounded-lg border border-void-800 bg-void-950/60 p-4"
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: Math.min(index * 0.04, 0.4) }}
                >
                  <div className="flex items-center justify-between gap-3 mb-2">
                    <span className="text-sm font-medium text-chrono-gold">{message.role}</span>
                    <span className="text-[10px] text-gray-600">{message.phase}</span>
                  </div>
                  <p className="text-sm text-gray-300 leading-relaxed">{message.content}</p>
                </motion.div>
              ))}
            </div>

            <div className="rounded-xl border border-void-800 bg-void-900/50 p-4 space-y-3">
              <textarea
                value={feedback}
                onChange={(event) => setFeedback(event.target.value)}
                rows={3}
                placeholder="例如：更悬疑一点，强化第二幕冲突，把台词改得更像唐传奇。"
                className="w-full rounded-lg border border-void-700 bg-void-950 px-4 py-3 text-sm text-gray-200 outline-none focus:border-chrono-gold"
                disabled={submitting}
              />
              <button
                onClick={handleStep}
                disabled={!feedback.trim() || submitting}
                className="px-4 py-2 rounded-lg bg-chrono-gold text-sm font-semibold text-black disabled:opacity-50"
              >
                {submitting ? "继续创作中..." : "提交反馈并继续生成"}
              </button>
            </div>
          </section>

          <section className="rounded-xl border border-void-800 bg-void-900/40 p-4">
            {conversation.script ? (
              <ScriptViewer script={conversation.script} />
            ) : (
              <p className="text-sm text-gray-500">脚本尚未生成。</p>
            )}
          </section>
        </div>
      )}
    </div>
  );
}

export default function StudioPage() {
  return (
    <Suspense fallback={<div className="max-w-6xl mx-auto px-4 py-10 text-gray-500">加载生成室...</div>}>
      <StudioContent />
    </Suspense>
  );
}
