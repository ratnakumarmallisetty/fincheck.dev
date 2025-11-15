# Prerequisites

Make sure the following tools are installed:

### **Node.js**
Download: https://nodejs.org/

### **pnpm**
```bash
npm install -g pnpm
````

### **PostgreSQL**

Download:
[https://www.postgresql.org/download/](https://www.postgresql.org/download/)

> Windows: Use the installer
> macOS: Use Homebrew or the official installer
> Linux: Install via apt/yum (Debian/Ubuntu/Fedora)

### **Rust**

Install from: [https://www.rust-lang.org/tools/install](https://www.rust-lang.org/tools/install)
Or via terminal:

```bash
curl https://sh.rustup.rs -sSf | sh
```

After installation:

**Load Rust environment:**

macOS/Linux:

```bash
source $HOME/.cargo/env
```

Windows (PowerShell):

```powershell
$env:PATH += "$HOME\.cargo\bin"
```

---

#  Getting Started

##  Run the Frontend Development Server

```bash
pnpm dev
```

---

#  PostgreSQL Setup

## Start PostgreSQL Service

### **macOS (Homebrew)**:

```bash
brew services start postgresql
```

### **Linux (systemd)**:

```bash
sudo systemctl start postgresql
```

### **Windows**:

Start PostgreSQL from:

```
Services → PostgreSQL → Start
```

Or through pgAdmin.

---

## Check PostgreSQL Version

```bash
postgres --version
```

---

#  Database Configuration

Set your database connection string:

```bash
DATABASE_URL=postgres://<user>:<password>@localhost:5432/authdb
```

Add this to `.env` file:

```
DATABASE_URL=postgres://mukesh1:mukesh123@localhost:5432/authdb
```

---

#  Create `users` Table

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

#  Generate SeaORM Entities

```bash
sea-orm-cli generate entity \
  -u postgres://mukesh1:mukesh123@localhost:5432/authdb \
  -o src/entity
```

---

#  Rust Backend

## Build the Rust Project

```bash
cargo build
```

## Run the Rust Service

```bash
cargo run
```

## Clean Build Artifacts

```bash
cargo clean
```

---

