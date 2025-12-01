Here is your **complete, production-ready `README.md` file**, fully updated for your **MongoDB + Next.js + NextAuth** stack.

You can **copy/paste this directly into your repo**.

---

# 📘 **Fincheck.dev**

Fincheck.dev is a modern financial tracking and authentication-enabled application built using:

* **Next.js 16 (App Router + Turbopack)**
* **React 19**
* **NextAuth (Credentials Provider)**
* **MongoDB Atlas**
* **Tailwind CSS**
* **pnpm**

It includes user authentication, signup/signin flows, and a clean modular structure.

---

# 🚀 Tech Stack

### **Frontend / Fullstack**

* Next.js App Router
* React 19
* Tailwind CSS
* NextAuth Credentials Provider

### **Database**

* MongoDB Atlas
* MongoDB Native Driver (high performance, no ORM overhead)

### **Tooling**

* pnpm
* Biome (lint + format)
* TypeScript

---

# 📦 Prerequisites

Make sure you have:

### **Node.js**

[https://nodejs.org](https://nodejs.org)

### **pnpm**

```bash
npm install -g pnpm
```

### **MongoDB Atlas Cluster**

Create one free at: [https://www.mongodb.com/atlas](https://www.mongodb.com/atlas)

---

# 🔧 Installation

```bash
git clone <your-repo-url>
cd fincheck.dev
pnpm install
```

---

# 🔑 Environment Variables

Create a file named `.env` in the project root:

```env
# MongoDB
MONGODB_URI="mongodb+srv://<USER>:<PASSWORD>@<CLUSTER>.mongodb.net/"
MONGODB_DB="finalyear"

# NextAuth
NEXTAUTH_SECRET="<your-secret>"
NEXTAUTH_URL="http://localhost:3000"
```

### Generate a secure secret:

```bash
openssl rand -base64 32
```

---

# 🗄 MongoDB Setup

This project uses the **native MongoDB driver** for maximum speed and flexibility.

#### `lib/mongodb.ts`

```ts
import { MongoClient } from "mongodb";

const uri = process.env.MONGODB_URI!;
declare global {
  var _mongoClientPromise: Promise<MongoClient> | undefined;
}

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

Authentication uses **next-auth/credentials** with MongoDB.

### Route:

```
/api/auth/[...nextauth]
```

### Example authorize logic:

```ts
import bcrypt from "bcryptjs";
import clientPromise from "@/lib/mongodb";
import Credentials from "next-auth/providers/credentials";
import NextAuth from "next-auth";

const handler = NextAuth({
  session: { strategy: "jwt" },

  providers: [
    Credentials({
      name: "Credentials",
      credentials: {
        username: { type: "text" },
        password: { type: "password" }
      },

      async authorize(credentials) {
        if (!credentials) return null;

        const client = await clientPromise;
        const db = client.db(process.env.MONGODB_DB);
        const users = db.collection("users");

        const user = await users.findOne({ username: credentials.username });
        if (!user) return null;

        const isValid = await bcrypt.compare(credentials.password, user.password);
        if (!isValid) return null;

        return { id: user._id.toString(), username: user.username };
      }
    })
  ],

  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.id = user.id;
        token.username = user.username;
      }
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
  if (exists) return new Response("Username already exists", { status: 400 });

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

# ▶️ Running the App

Start development server:

```bash
pnpm dev
```

Open:

👉 [http://localhost:3000](http://localhost:3000)

---

# 📁 Project Structure

```
fincheck.dev
├── app
│   ├── api
│   │   ├── auth/[...nextauth]/route.ts
│   │   └── signup/route.ts
│   ├── intro/page.tsx
│   ├── sign-in/page.tsx
│   ├── sign-up/page.tsx
│   ├── main/page.tsx
│   └── layout.tsx
├── lib
│   └── mongodb.ts
├── types
│   └── next-auth.d.ts
├── README.md
├── package.json
└── pnpm-lock.yaml
```

