// app/messages/route.ts
import { AI } from "@/constants/chat";
import { PrismaClient } from "@prisma/client";
import { NextRequest, NextResponse } from "next/server";

const prisma = new PrismaClient();

const LLM_API_URL = process.env.LLM_API_URL!;
const LLM_API_KEY = process.env.LLM_API_KEY!;
const LLM_WORKSPACE_ID = process.env.LLM_WORKSPACE_ID!;

// Utility: validate message input
function isValidMessage({ name, avatarUrl, content, position }: any) {
  return name && avatarUrl && content && position;
}

// Utility: send query to AnythingLLM
async function queryLLM(message: string): Promise<string> {
  try {
    const res = await fetch(`${LLM_API_URL}/api/v1/workspace/${LLM_WORKSPACE_ID}/chat`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${LLM_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        mode: 'query',
        sessionId: 'dev', // Or use uuid() here for unique sessions
        reset: false,
      }),
    });

    if (!res.ok) {
      console.error("LLM error:", res.statusText);
      return "Error from LLM";
    }

    const data = await res.json();
    return data.textResponse || "No response from LLM";

  } catch (err) {
    console.log("LLM fetch failed:", err);
    return "LLM service unavailable.";
  }
}

export async function GET() {
  const messages = await prisma.message.findMany({
    orderBy: { time: 'asc' },
  });

  return NextResponse.json(messages);
}

// export async function POST(request: Request) {
//   try {
//     const body = await request.json();
//     // Validate required fields if needed
//     const { name, avatarUrl, content, position } = body;

//     if (!name || !avatarUrl || !content || !position) {
//       return NextResponse.json({ error: 'Missing fields' }, { status: 400 });
//     }

//     // Create new message with current timestamp
//     const newMessage = await prisma.message.create({
//       data: {
//         name,
//         avatarUrl,
//         content,
//         position,
//         time: new Date(),  // assumes your `time` field is a DateTime
//       },
//     });

//     return NextResponse.json(newMessage, { status: 201 });
//   } catch (error) {
//     console.error('POST /api/messages error:', error);
//     return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
//   }
// }

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    if (!isValidMessage(body)) {
      return NextResponse.json({ error: 'Missing fields' }, { status: 400 });
    }

    const { name, avatarUrl, content, position } = body;

    // 1. Save user message
    const userMessage = await prisma.message.create({
      data: { name, avatarUrl, content, position, time: new Date() },
    });

    // 2. Query LLM
    const llmText = await queryLLM(content);

    // 3. Save LLM response
    const llmMessage = await prisma.message.create({
      data: {
        name: AI.name,
        avatarUrl: AI.avatarUrl,
        content: llmText,
        position: AI.position,
        time: new Date(),
      },
    });

    return NextResponse.json({ userMessage, llmMessage }, { status: 201 });

  } catch (error) {
    console.error("POST /api/messages error:", error);
    return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
  }
}