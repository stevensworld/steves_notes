#!/bin/bash

curl http://localhost:4000/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "gemma", "messages": [{"role": "user", "content": "say hello"}]}'
