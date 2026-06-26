# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) (or [oxc](https://oxc.rs) when used in [rolldown-vite](https://vite.dev/guide/rolldown)) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.


## 🚀 Quick Start

### Option 1: Using PowerShell Scripts (Recommended)

**Terminal 1 - Backend:**
```powershell
.\START_BACKEND.ps1
```

**Terminal 2 - Frontend:**
```powershell
.\START_FRONTEND.ps1
```

### Option 2: Manual Startup

**Backend (Terminal 1):**
```powershell
cd D:\civiclens-frontend\backend
D:\civiclens-frontend\backend\venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend (Terminal 2):**
```powershell
cd D:\civiclens-frontend
npm run dev
```

### Option 3: Performance Checks
```powershell
cd D:\civiclens-frontend\backend\ml
& "D:\civiclens-frontend\backend\venv\Scripts\python.exe" show_model_performance.py
```

## 🔧 Troubleshooting

### "Unable to connect to server" Error

If you see this error when trying to log in:

1. **Check if backend is running:**
   ```powershell
   .\test-connection.ps1
   ```

2. **Kill conflicting processes on port 8000:**
   ```powershell
   netstat -ano | findstr ":8000"
   # Note the PID numbers, then:
   Stop-Process -Id <PID> -Force
   ```

3. **Restart backend cleanly:**
   - Close all terminals running uvicorn
   - Run `.\START_BACKEND.ps1` in a new terminal
   - Wait for "Application startup complete" message

4. **Restart frontend:**
   - Close the frontend terminal
   - Run `.\START_FRONTEND.ps1` in a new terminal
   - Clear browser cache (Ctrl+Shift+Delete) and reload

5. **Verify Supabase connection:**
   ```powershell
   & "D:\civiclens-frontend\backend\venv\Scripts\python.exe" test-supabase.py
   ```

### Common Issues

- **Port already in use**: Multiple backend instances are running. Kill all Python/uvicorn processes on port 8000.
- **CORS errors**: Make sure backend is running on port 8000 and frontend on port 5173.
- **Login fails**: Verify Supabase credentials in `backend\.env` file.
- **Module not found**: Activate the virtual environment before running Python commands.

## 📝 Important Notes

- **Always run backend and frontend in separate terminal windows**
- **Backend must be running before attempting to login**
- **Default ports**: Backend (8000), Frontend (5173)
- **Environment variables**: Check `.env` files in root and backend directories

## 🚀 Deploying for Free (Vercel + Render + Supabase)

This repo is split into a static frontend (Vite + React) and a FastAPI backend that uses Supabase for auth/data. The fastest free setup:

- Frontend: Vercel (free) or Netlify (free)
- Backend: Render free web service (or Fly/Heroku free alternatives)
- Database/Auth: Supabase free tier

Checklist and exact steps

1) Create a Supabase project (free)

- In Supabase, create the project and copy the `SUPABASE_URL` and `SUPABASE_KEY`.

2) Deploy the backend to Render (or another free Python host)

- Create a new Web Service on Render and point it at the `backend` folder (or the repo root and set the build root to `backend`).
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Set these Environment Variables on Render:

   - `SUPABASE_URL` = (from Supabase)
   - `SUPABASE_KEY` = (from Supabase)
   - `FRONTEND_URL` = your frontend production URL (see step 3)

Note: The backend currently includes ML dependencies (TensorFlow, EasyOCR) in `backend/requirements.txt` which can increase build time and memory usage on free hosts. If Render fails due to resource limits, consider removing ML endpoints or moving ML tasks to a separate service.

3) Deploy the frontend to Vercel

- In Vercel, import the project and set the root to the repository root.
- Build command: `npm run build`
- Output directory: `dist`
- In Vercel Environment Variables (Production), add:

   - `VITE_API_URL` = `https://<your-render-backend>.onrender.com` (replace with your backend URL)

4) Final checks

- Ensure `FRONTEND_URL` (backend env) matches the Vercel site URL to avoid CORS issues.
- Use the `backend/.env.example` and root `.env.example` as references for local testing.

Quick commands (local testing)

```powershell
# Start backend locally
cd backend
venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Start frontend locally
cd ..
npm install
npm run dev
```

If you want, I can also:

- Add a `DEPLOY.md` with screenshots for Vercel/Render setup
- Create a small `render.yaml` or Vercel configuration example


netstat -ano | findstr ":8000"
Get-Process -Id 24236 | Select-Object Id, ProcessName, Path
curl http://localhost:8000/auth/login -Method OPTIONS -Verbose 2>&1 | Select-String -Pattern "StatusCode|ConnectionRefused|Cannot connect"
 
