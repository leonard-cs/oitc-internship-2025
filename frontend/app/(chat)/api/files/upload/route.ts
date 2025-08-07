import { z } from "zod";
import { NextResponse } from "next/server";
import { writeFile, mkdir } from "fs/promises";
import { existsSync } from "fs";
import path from "path";


const FileSchema = z.object({
  file: z
    .instanceof(File)
    .refine((file) => file.size <= 5 * 1024 * 1024, {
      message: "File size should be less than 5MB",
    })
    .refine(
      (file) =>
        ["image/jpeg", "image/png", "application/pdf"].includes(file.type),
      {
        message: "File type should be JPEG, PNG, or PDF",
      },
    ),
});


export async function POST(request: Request) {
  if (request.body === null) {
    return new Response("Request body is empty", { status: 400 });
  }

  try {
    const formData = await request.formData();
    const file = formData.get("file") as File;

    if (!file) {
      return NextResponse.json({ error: "No file uploaded" }, { status: 400 });
    }

    const validatedFile = FileSchema.safeParse({ file });

    if (!validatedFile.success) {
      const errorMessage = validatedFile.error.errors
          .map((error) => error.message)
          .join(", ");

      return NextResponse.json({ error: errorMessage }, { status: 400 });
    }

    // Prepare directory
    const uploadsDir = path.join(process.cwd(), "public", "uploads");
    if (!existsSync(uploadsDir)) {
      await mkdir(uploadsDir, { recursive: true });
    }

    // Generate unique filename to prevent conflicts
    const timestamp = Date.now();
    const fileExtension = path.extname(file.name);
    const baseName = path.basename(file.name, fileExtension);
    const filename = `${baseName}_${timestamp}${fileExtension}`;
    const filepath = path.join(uploadsDir, filename);

    // Write file to disk
    const fileBuffer = await file.arrayBuffer();
    await writeFile(filepath, new Uint8Array(fileBuffer));

    return NextResponse.json({
      url: `/uploads/${filename}`,
      pathname: filename,
      contentType: file.type,
    });
  } catch (error) {
    console.error("File upload error:", error);
    return NextResponse.json({ error: "Failed to process request" }, { status: 500 });
  }
}
