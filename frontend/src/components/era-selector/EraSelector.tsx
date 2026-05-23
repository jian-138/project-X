"use client";

import { motion } from "framer-motion";
import { ERA_OPTIONS } from "@/lib/types";

interface Props {
  selected: string | null;
  onSelect: (eraId: string) => void;
  disabled?: boolean;
}

export function EraSelector({ selected, onSelect, disabled }: Props) {
  return (
    <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
      {ERA_OPTIONS.map((era, index) => (
        <motion.button
          key={era.id}
          className={`relative p-4 rounded-xl border text-left transition-all
            ${selected === era.id
              ? "border-chrono-gold bg-chrono-gold/10 glow-gold"
              : "border-void-700 hover:border-gray-500 bg-void-900"}
            ${disabled ? "opacity-50 pointer-events-none" : ""}`}
          onClick={() => onSelect(era.id)}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.08, duration: 0.4 }}
          whileHover={disabled ? {} : { scale: 1.03 }}
          whileTap={disabled ? {} : { scale: 0.98 }}
        >
          <span className="text-2xl block mb-1" aria-hidden="true">
            {era.icon}
          </span>
          <span className="text-sm font-medium text-gray-200">{era.name}</span>
          <span className="text-xs text-gray-500 block mt-1">{era.description}</span>
          {selected === era.id && (
            <motion.div
              className="absolute top-2 right-2 w-5 h-5 rounded-full bg-chrono-gold flex items-center justify-center text-xs text-black font-bold"
              layoutId="era-check"
              aria-hidden="true"
            >
              ✓
            </motion.div>
          )}
        </motion.button>
      ))}
    </div>
  );
}
