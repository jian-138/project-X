"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { EraSelector } from "@/components/era-selector/EraSelector";
import { UploadZone } from "@/components/upload/UploadZone";
import { uploadVideo } from "@/lib/api";

export default function HomePage() {
  const router = useRouter();
  const [file, setFile] = useState<File | null>(null);
  const [era, setEra] = useState<string | null>(null);
  const [apiKey, setApiKey] = useState("");
  const [creativeBrief, setCreativeBrief] = useState("保留探店推荐的核心，但增强戏剧冲突和时代感。");
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const canSubmit = file && era && !uploading;

  const handleStart = async () => {
    if (!file || !era) return;
    setUploading(true);
    setError(null);

    try {
      const res = await uploadVideo(file, era, creativeBrief, apiKey);
      if (apiKey.trim()) {
        sessionStorage.setItem(`chronoshift_api_key_${res.task_id}`, apiKey.trim());
      }
      router.push(`/studio?task_id=${res.task_id}`);
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : "上传失败，请检查 OpenAI API Key 后重试";
      setError(msg);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto px-4 py-16 space-y-10">
      <motion.div
        className="text-center space-y-4"
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <h1 className="font-display text-4xl md:text-5xl font-bold text-chrono-gold glow-text">
          ChronoShift
        </h1>
        <p className="text-lg text-gray-400">
          上传短视频，让 OpenAI 多角色创作室逐步生成剧情脚本。
        </p>
      </motion.div>

      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.3 }}>
        <UploadZone onUpload={setFile} disabled={uploading} />
        {file && (
          <p className="text-sm text-chrono-gold mt-2 text-center">
            已选择：{file.name} ({(file.size / 1024 / 1024).toFixed(1)}MB)
          </p>
        )}
      </motion.div>

      <motion.div className="space-y-3" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.45 }}>
        <h2 className="text-sm font-medium text-gray-400 text-center">选择目标时代</h2>
        <EraSelector selected={era} onSelect={setEra} disabled={uploading} />
      </motion.div>

      <motion.div className="space-y-4" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.55 }}>
        <label className="block space-y-2">
          <span className="text-sm text-gray-400">OpenAI API Key（可选，后端 .env 已配置时可留空）</span>
          <input
            value={apiKey}
            onChange={(event) => setApiKey(event.target.value)}
            type="password"
            placeholder="sk-..."
            className="w-full rounded-lg border border-void-700 bg-void-900 px-4 py-3 text-sm text-gray-200 outline-none focus:border-chrono-gold"
            disabled={uploading}
          />
        </label>
        <label className="block space-y-2">
          <span className="text-sm text-gray-400">创作要求</span>
          <textarea
            value={creativeBrief}
            onChange={(event) => setCreativeBrief(event.target.value)}
            rows={4}
            className="w-full rounded-lg border border-void-700 bg-void-900 px-4 py-3 text-sm text-gray-200 outline-none focus:border-chrono-gold"
            disabled={uploading}
          />
        </label>
      </motion.div>

      {canSubmit && (
        <motion.div className="text-center" initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }}>
          <button
            onClick={handleStart}
            className="px-8 py-3 bg-chrono-gold text-black font-semibold rounded-xl hover:bg-chrono-gold/90 active:scale-95 transition-all glow-gold"
          >
            启动创作室
          </button>
        </motion.div>
      )}

      {uploading && (
        <div className="text-center">
          <motion.div
            className="inline-block w-8 h-8 border-2 border-chrono-gold border-t-transparent rounded-full"
            animate={{ rotate: 360 }}
            transition={{ repeat: Infinity, duration: 1, ease: "linear" }}
          />
          <p className="text-sm text-gray-500 mt-2">OpenAI 多角色创作室正在生成初版...</p>
        </div>
      )}

      {error && <p className="text-sm text-red-400 text-center">{error}</p>}
    </div>
  );
}
