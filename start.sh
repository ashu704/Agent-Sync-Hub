#!/bin/bash
npx tsx server/index.ts &
npx vite --port 5000 --host 0.0.0.0
