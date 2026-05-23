"use client";

import Link from "next/link";
import { motion } from "framer-motion";

export function Header() {
  return (
    <header className="border-b border-void-800 bg-void-950/80 backdrop-blur-sm sticky top-0 z-50">
      <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-3 group">
          <motion.span
            className="text-2xl"
            whileHover={{ rotate: 180 }}
            transition={{ duration: 0.6 }}
            aria-hidden="true"
          >
            ⏳
          </motion.span>
          <span className="font-display text-xl text-chrono-gold font-bold tracking-wide glow-text">
            ChronoShift
          </span>
        </Link>
        <nav className="flex items-center gap-6 text-sm text-gray-400">
          <Link href="/" className="hover:text-chrono-gold transition-colors">
            首页
          </Link>
        </nav>
      </div>
    </header>
  );
}
