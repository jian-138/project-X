"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { UploadZone } from "@/components/upload/UploadZone";
import { EraSelector } from "@/components/era-selector/EraSelector";
import { uploadVideo } from "@/lib/api";

export default function HomePage() {
  const router = useRouter();
  const [file, setFile] = useState<File | null>(null);
  const [era, setEra] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const canSubmit = file && era && !uploading;

  const handleStart = async () => {
    if (!file || !era) return;
    setUploading(true);
    setError(null);

    try {
      const res = await uploadVideo(file, era);
      router.push(`/processing?task_id=${res.task_id}`);
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : "上传失败，请重试";
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
          平行时代转换器 - 让每一段短视频，都能穿越到另一个时代。
        </p>
      </motion.div>

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3, duration: 0.5 }}
      >
        <UploadZone onUpload={setFile} disabled={uploading} />
        {file && (
          <p className="text-sm text-chrono-gold mt-2 text-center">
            已选择：{file.name} ({(file.size / 1024 / 1024).toFixed(1)}MB)
          </p>
        )}
      </motion.div>

      <motion.div
        className="space-y-3"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5, duration: 0.5 }}
      >
        <h2 className="text-sm font-medium text-gray-400 text-center">选择目标时代</h2>
        <EraSelector selected={era} onSelect={setEra} disabled={uploading} />
      </motion.div>

      {canSubmit && (
        <motion.div
          className="text-center"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.3 }}
        >
          <button
            onClick={handleStart}
            className="px-8 py-3 bg-chrono-gold text-black font-semibold rounded-xl hover:bg-chrono-gold/90 active:scale-95 transition-all glow-gold"
          >
            开始穿越
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
          <p className="text-sm text-gray-500 mt-2">正在上传并提交任务...</p>
        </div>
      )}

      {error && <p className="text-sm text-red-400 text-center">{error}</p>}
    </div>
  );
}
