Below is the **updated README.md** including your **FastAPI backend image upload service**, integrated cleanly as a dedicated section.

You can **copy/paste this entire README** into your repo — it is now complete and production-ready.

---

# 📘 **Fincheck.dev**

Fincheck.dev is a modern financial tracking and authentication-enabled application built using:

* **Next.js 16 (App Router + Turbopack)**
* **React 19**
* **NextAuth (Credentials Provider)**
* **MongoDB Atlas**
* **Tailwind CSS**
* **pnpm**
* **FastAPI backend for additional services (e.g., image upload)**

---

# 🚀 Tech Stack

### **Frontend / Fullstack**

* Next.js App Router
* React 19
* Tailwind CSS
* NextAuth (Credential-based authentication)
* TypeScript

### **Database**

* MongoDB Atlas
* MongoDB Native Driver

### **Backend**

* Python **FastAPI**
* Uvicorn
* aiofiles

### **Package Manager**

* pnpm

---

# 📦 Prerequisites

### Install Node.js

[https://nodejs.org](https://nodejs.org)

### Install pnpm

```bash
npm install -g pnpm
```

### Install Python 3.10+

[https://www.python.org/downloads/](https://www.python.org/downloads/)

---

# 🔧 Installation

```bash
git clone <your-repo-url>
cd fincheck.dev
pnpm install
```

---

# 🔑 Environment Variables

Create a `.env` file:

```env
# MongoDB
MONGODB_URI="mongodb+srv://<USER>:<PASSWORD>@<CLUSTER>.mongodb.net/"
MONGODB_DB="finalyear"

# NextAuth
NEXTAUTH_SECRET="<your-secret>"
NEXTAUTH_URL="http://localhost:3000"
```

Generate a secure secret:

```bash
openssl rand -base64 32
```

---

# 🗄 MongoDB Setup

The project uses the **native MongoDB driver**.

`lib/mongodb.ts`:

```ts
import { MongoClient } from "mongodb";

const uri = process.env.MONGODB_URI!;
declare global { var _mongoClientPromise: Promise<MongoClient> | undefined; }

let client: MongoClient;
let clientPromise: Promise<MongoClient>;

if (process.env.NODE_ENV === "development") {
  if (!global._mongoClientPromise) {
    client = new MongoClient(uri);
    global._mongoClientPromise = client.connect();
  }
  clientPromise = global._mongoClientPromise;
} else {
  client = new MongoClient(uri);
  clientPromise = client.connect();
}

export default clientPromise;
```

---

# 🔐 Authentication (NextAuth)

Credentials-based authentication with MongoDB.

### Route:

```
/api/auth/[...nextauth]
```

### Logic:

```ts
import bcrypt from "bcryptjs";
import clientPromise from "@/lib/mongodb";
import Credentials from "next-auth/providers/credentials";
import NextAuth from "next-auth";

const handler = NextAuth({
  session: { strategy: "jwt" },

  providers: [
    Credentials({
      credentials: {
        username: { type: "text" },
        password: { type: "password" },
      },

      async authorize(credentials) {
        const client = await clientPromise;
        const db = client.db(process.env.MONGODB_DB);
        const user = await db.collection("users").findOne({ username: credentials?.username });

        if (!user) return null;
        const valid = await bcrypt.compare(credentials!.password, user.password);
        if (!valid) return null;

        return { id: user._id.toString(), username: user.username };
      }
    })
  ],

  callbacks: {
    async jwt({ token, user }) {
      if (user) { token.id = user.id; token.username = user.username; }
      return token;
    },
    async session({ session, token }) {
      session.user = { id: token.id, username: token.username };
      return session;
    },
  },
});

export { handler as GET, handler as POST };
```

---

# 📝 Signup Route

```
POST /api/signup
```

```ts
import clientPromise from "@/lib/mongodb";
import bcrypt from "bcryptjs";

export async function POST(req: Request) {
  const { username, password } = await req.json();

  const client = await clientPromise;
  const db = client.db(process.env.MONGODB_DB);
  const users = db.collection("users");

  const exists = await users.findOne({ username });
  if (exists) return new Response("Username exists", { status: 400 });

  const hash = await bcrypt.hash(password, 10);

  const result = await users.insertOne({
    username,
    password: hash,
    createdAt: new Date(),
  });

  return Response.json({ success: true, userId: result.insertedId });
}
```

---

# ▶️ Running the Next.js App

```bash
pnpm dev
```

Open:

👉 [http://localhost:3000](http://localhost:3000)

---

# 🧩 Project Structure

```
fincheck.dev
├── app
│   ├── api
│   │   ├── auth/[...nextauth]/route.ts
│   │   └── signup/route.ts
│   ├── sign-in/page.tsx
│   ├── sign-up/page.tsx
│   ├── intro/page.tsx
│   ├── main/page.tsx
│   └── layout.tsx
├── lib/mongodb.ts
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── uploads/
├── types/next-auth.d.ts
├── README.md
└── package.json
```

---

# ⚡ FastAPI Backend (Image Upload Service)

This backend handles **secure image uploads** with validation & size checks.

### 📌 Features

* Restricts image types (JPEG, PNG, WebP)
* Max file size: **5 MB**
* Saves file to `/uploads`
* Built-in CORS support
* Async file streaming using `aiofiles`

### 📄 `backend/main.py`

```python
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
import aiofiles

app = FastAPI(title="FASTAPI BACKEND", version="1.0.0")

ALLOWED_TYPES = ["image/jpeg", "image/png", "image/webp"]
MAX_FILE_SIZE = 5 * 1024 * 1024

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "FastAPI is running.."}

@app.get("/health")
def health_check():
    return {"message": "ok", "service": "backend"}

@app.post("/upload-image")
async def image_upload(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Invalid image type..")

    total_size = 0
    CHUNK_SIZE = 1024 * 1024

    while chunk := await file.read(CHUNK_SIZE):
        total_size += len(chunk)
        if total_size > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="Exceeding max file size..")

    await file.seek(0)

    ext = file.filename.split(".")[-1]
    saved_name = f"{uuid.uuid4()}.{ext}"
    saved_path = os.path.join("uploads", saved_name)

    os.makedirs("uploads", exist_ok=True)

    async with aiofiles.open(saved_path, "wb") as f:
        while chunk := await file.read(CHUNK_SIZE):
            await f.write(chunk)

    metadata = {
        "original_name": file.filename,
        "saved_name": saved_name,
        "mime_type": file.content_type,
        "size_bytes": total_size,
        "path": saved_path,
    }

    await file.close()

    return JSONResponse(
        status_code=201,
        content={"message": "Image upload successful", "metadata": metadata},
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
```

---

# ▶️ Running the FastAPI Backend

```bash
cd backend
uvicorn main:app --reload
```

Your API will run at:

👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)
👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) (Swagger UI)

-