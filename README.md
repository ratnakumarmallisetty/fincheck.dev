# Fincheck.dev

A modern authentication-enabled Next.js application using **Next.js App Router**, **NextAuth (Credentials Provider)**, **Prisma ORM**, and **Supabase PostgreSQL**.

---

##  Tech Stack

- **Next.js 16 (App Router + Turbopack)**
- **React 19**
- **NextAuth (Credentials Provider)**
- **Prisma ORM**
- **Supabase PostgreSQL**
- **Tailwind CSS**
- **pnpm** for dependency management

---

# Prerequisites

Install the following before running the project:

### **Node.js**
Download: https://nodejs.org

### **pnpm**
```bash
npm install -g pnpm
````

---

#  Installation

Clone the repository and install dependencies:

```bash
git clone <your-repo-url>
cd fincheck.dev
pnpm install
```

---

#  Environment Variables

Create a file named:

```
.env
```

Add the following:

```env
DATABASE_URL="postgresql://postgres:<YOUR_PASSWORD>@db.<YOUR-PROJECT-ID>.supabase.co:5432/postgres?sslmode=require"
DIRECT_URL="postgresql://postgres:<YOUR_PASSWORD>@db.<YOUR-PROJECT-ID>.supabase.co:5432/postgres?sslmode=require"

NEXTAUTH_SECRET="<your-generated-secret>"
NEXTAUTH_URL="http://localhost:3000"
```

###  IMPORTANT:

Use the **direct database URL (5432)** from Supabase.
**Do NOT use the PgBouncer pooler URL (6543)** — Prisma will not work with it.

---

# Prisma Setup

Push the schema to your Supabase database:

```bash
npx prisma db push
```

Generate Prisma Client:

```bash
npx prisma generate
```

(Optional) Open Prisma Studio:

```bash
npx prisma studio
```

---

#  Running the App

Start the development server:

```bash
pnpm dev
```

Your app will be available at:

👉 [http://localhost:3000](http://localhost:3000)

---

#  Authentication (NextAuth)

This project uses:

* **next-auth/credentials** for username/password login
* **Prisma** as the user store
* Supabase PostgreSQL as the backend database

### Signup Route

```
POST /api/signup
```

### Auth Route

```
/api/auth/[...nextauth]
```

### User Table Schema

```prisma
model User {
  id        Int      @id @default(autoincrement())
  username  String   @unique
  password  String
  createdAt DateTime @default(now())
}
```

---

#  Makefile (Included)

| Command            | Description                                    |
| ------------------ | ---------------------------------------------- |
| `make dev`         | Runs the Next.js development server            |
| `make prisma-push` | Pushes the Prisma schema to Supabase           |
| `make prisma-gen`  | Generates Prisma Client                        |
| `make clean`       | Removes `.next` and resets the dev environment |

### Example Makefile

```makefile
dev:
	pnpm dev

prisma-push:
	npx prisma db push

prisma-gen:
	npx prisma generate

clean:
	rm -rf .next
```

---

#  Project Structure

```
fincheck.dev git:(main) tree
.
├── CONTRIBUTING.md
├── Dockerfile
├── Makefile
├── README.md
├── app
│   ├── IntroPage.tsx
│   ├── MainPage.tsx
│   ├── SignInPage.tsx
│   ├── SignUpPage.tsx
│   ├── api
│   │   ├── auth
│   │   │   └── [...nextauth]
│   │   │       └── route.ts
│   │   └── signup
│   │       └── route.ts
│   ├── favicon.ico
│   ├── globals.css
│   ├── layout.tsx
│   └── page.tsx
├── biome.json
├── docker-compose.yml
├── eslint.config.mjs
├── lib
│   └── prisma.ts
├── next-env.d.ts
├── next.config.ts
├── node_modules
│  
├── package.json
├── pnpm-lock.yaml
├── postcss.config.mjs
├── prisma
│   ├── migrations
│   │   ├── 20251117051417_init
│   │   │   └── migration.sql
│   │   └── migration_lock.toml
│   └── schema.prisma
├── tsconfig.json
└── types
    └── next-auth.d.ts

36 directories, 28 files
➜  fincheck.dev git:(main) 
```
