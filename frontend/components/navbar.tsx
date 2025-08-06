"use client";

import { Button } from "./ui/button";
import { GitIcon } from "./icons";
import Link from "next/link";

export const Navbar = () => {
  return (
    <div className="p-2 flex flex-row gap-2 justify-between">
      <Link href="https://github.com/vercel-labs/ai-sdk-preview-python-streaming">
        <Button variant="outline">
          <GitIcon /> View Source Code
        </Button>
      </Link>

      <div className="flex-1 flex justify-center">
        <span className="text-lg font-semibold">
          AI SDK Python Streaming Demo
        </span>
      </div>

      {/* Placeholder for right side */}
      <div style={{ width: 140 }} /> {/* Keeps spacing symmetric */}
    </div>
  );
};
