import { PrismaClient } from "@prisma/client";
import { NextResponse } from "next/server";

const prisma = new PrismaClient();

export async function GET() {
  const messages = await prisma.message.findMany({
    orderBy: { time: 'asc' },
  });

  return NextResponse.json(messages);
}
