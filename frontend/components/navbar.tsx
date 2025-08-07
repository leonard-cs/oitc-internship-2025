"use client";

import { Button } from "./ui/button";
import { GitIcon } from "./icons";
import Link from "next/link";

export const Navbar = () => {
  return (
    <div className="p-2 flex flex-row gap-2 justify-between">
      {/* Left: Source Code Button */}
      <div className="absolute left-2">
        <Link href="https://github.com/vercel-labs/ai-sdk-preview-python-streaming">
          <Button variant="outline">
            <GitIcon /> View Source Code
          </Button>
        </Link>
      </div>

      {/* Center: Title */}
      <div className="flex-1 flex justify-center">
        <span className="text-lg font-semibold">RAG Agent Demo</span>
      </div>

      {/* Right: Empty for symmetry */}
      <div className="absolute right-2" style={{ width: 140 }} />
    </div>
  );
};
