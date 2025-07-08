// app/messages/route.ts
import { PrismaClient } from "@prisma/client";
import { NextResponse } from "next/server";

const prisma = new PrismaClient();

export async function GET() {
  const messages = await prisma.message.findMany({
    orderBy: { time: 'asc' },
  });

  return NextResponse.json(messages);
}

export async function POST(request: Request) {
  try {
    const body = await request.json();
    // Validate required fields if needed
    const { name, avatarUrl, content, position } = body;

    if (!name || !avatarUrl || !content || !position) {
      return NextResponse.json({ error: 'Missing fields' }, { status: 400 });
    }

    // Create new message with current timestamp
    const newMessage = await prisma.message.create({
      data: {
        name,
        avatarUrl,
        content,
        position,
        time: new Date(),  // assumes your `time` field is a DateTime
      },
    });

    return NextResponse.json(newMessage, { status: 201 });
  } catch (error) {
    console.error('POST /api/messages error:', error);
    return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
  }
}
