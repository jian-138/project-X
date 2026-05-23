"use client";

import { useRef, useState, type ChangeEvent, type DragEvent } from "react";
import { motion } from "framer-motion";

interface Props {
  onUpload: (file: File) => void;
  disabled?: boolean;
}

export function UploadZone({ onUpload, disabled }: Props) {
  const [dragging, setDragging] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleDrop = (event: DragEvent) => {
    event.preventDefault();
    setDragging(false);
    const file = event.dataTransfer.files[0];
    if (file && file.type.startsWith("video/")) {
      onUpload(file);
    }
  };

  const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file && file.type.startsWith("video/")) {
      onUpload(file);
    }
  };

  return (
    <motion.div
      className={`relative border-2 border-dashed rounded-2xl p-12 text-center cursor-pointer transition-colors
        ${dragging ? "border-chrono-gold bg-void-800/50" : "border-void-700 hover:border-gray-500"}
        ${disabled ? "opacity-50 pointer-events-none" : ""}`}
      onDragOver={(event) => {
        event.preventDefault();
        setDragging(true);
      }}
      onDragLeave={() => setDragging(false)}
      onDrop={handleDrop}
      onClick={() => inputRef.current?.click()}
      whileHover={{ scale: 1.01 }}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      role="button"
      tabIndex={0}
    >
      <input
        ref={inputRef}
        type="file"
        accept="video/*"
        className="hidden"
        onChange={handleChange}
        disabled={disabled}
      />
      <div className="text-5xl mb-4" aria-hidden="true">
        📤
      </div>
      <p className="text-lg text-gray-300 mb-2">
        拖拽短视频到此处，或点击上传
      </p>
      <p className="text-sm text-gray-500">
        支持 MP4 / MOV / WebM · 最长 30 秒 · 最大 50MB
      </p>
    </motion.div>
  );
}
