# =============================================================================
# FASTAPI API TESTING REFERENCE
# =============================================================================
#
# Project:
#   AI Workbench API (Week 2)
#
# Package:
#   lab2b_app
#
# Purpose:
#   Quick reference for running and testing the FastAPI application.
#
# =============================================================================


# =============================================================================
# PRE-REQUISITES
# =============================================================================

# 1. Activate the Python Virtual Environment
#
# Windows PowerShell
#
# .\.venv\Scripts\Activate
#
# (Run this from your project root.)



# 2. Navigate to the folder that contains the package.
#
# Example:
#
# ai_learning_code_python/
# │
# └── module_0/
#     │
#     └── week_2/
#         │
#         └── lab2b_app/
#
# Change directory to:
#
# module_0/week_2
#
# because lab2b_app is the package.



# =============================================================================
# START THE FASTAPI SERVER
# =============================================================================

# Command:
#
# uvicorn lab2b_app.main:app --reload
#
#
# Breakdown:
#
# uvicorn                -> ASGI web server
#
# lab2b_app              -> Python package name
#
# main                   -> main.py
#
# app                    -> FastAPI object
#
# --reload               -> Restart server automatically after code changes
#
#
# When successful:
#
# INFO: Uvicorn running on http://127.0.0.1:8000



# =============================================================================
# TESTING METHOD 1 - WEB BROWSER
# =============================================================================

# Health Endpoint
#
# http://127.0.0.1:8000/health
#
# Returns:
#
# {
#     "status":"healthy",
#     "provider":"openai",
#     "model":"gpt-4.1-nano"
# }



# Swagger UI
#
# http://127.0.0.1:8000/docs
#
# FastAPI automatically generates interactive API documentation.
#
# Recommended for beginners because:
#
# ✔ No JSON escaping issues
# ✔ Shows request schema
# ✔ Shows response schema
# ✔ Allows testing every endpoint



# =============================================================================
# TESTING METHOD 2 - CURL
# =============================================================================

# IMPORTANT
#
# Different operating systems handle "curl" differently.
#
#
# macOS / Linux
# -------------
#
# curl = Real cURL program
#
#
# Windows PowerShell
# ------------------
#
# curl = Alias for Invoke-WebRequest
#
#
# Windows
# -------
#
# curl.exe = Real cURL program
#
#
# Git Bash
# --------
#
# Behaves almost exactly like Linux/macOS.
#
# Recommended when following Linux/macOS tutorials.



# =============================================================================
# HEALTH ENDPOINT (GET)
# =============================================================================

# --------------------------
# macOS / Linux
# --------------------------
#
# curl http://localhost:8000/health



# --------------------------
# Windows PowerShell
# --------------------------
#
# curl
#
# Actually runs:
#
# Invoke-WebRequest
#
# Returns:
#
# StatusCode
# Headers
# Content
# etc.
#
# Command:
#
# curl http://localhost:8000/health



# --------------------------
# Windows PowerShell
# (JSON only)
# --------------------------
#
# curl.exe http://localhost:8000/health



# --------------------------
# Windows PowerShell
# Native REST command
# --------------------------
#
# Invoke-RestMethod http://localhost:8000/health



# =============================================================================
# POST ENDPOINTS
# =============================================================================
#
# Available endpoints:
#
# /summarize
# /rewrite
# /keypoints
# /explain



# =============================================================================
# macOS / Linux
# =============================================================================

# curl -X POST http://localhost:8000/summarize \
# -H "Content-Type: application/json" \
# -d '{"text":"Generative AI enables computers to generate human-like text, images and code."}'



# =============================================================================
# Windows - Git Bash (Recommended)
# =============================================================================
#
# Git Bash behaves like Linux/macOS.
#
# Recommended if following the instructor.
#

# curl -X POST http://localhost:8000/summarize \
# -H "Content-Type: application/json" \
# -d '{"text":"Generative AI enables computers to generate human-like text, images and code."}'



# =============================================================================
# Windows PowerShell (Recommended)
# =============================================================================
#
# Instead of fighting JSON escaping rules,
# use PowerShell's native REST command.
#

# Invoke-RestMethod `
# -Uri "http://localhost:8000/summarize" `
# -Method POST `
# -ContentType "application/json" `
# -Body '{"text":"Generative AI enables computers to generate human-like text, images and code."}'



# =============================================================================
# Windows PowerShell + curl.exe
# =============================================================================
#
# GET requests work perfectly:
#
# curl.exe http://localhost:8000/health
#
#
# POST requests containing inline JSON may fail because
# PowerShell parses the command before passing it to curl.exe.
#
# If you specifically want to use curl for POST requests,
# Git Bash is recommended.



# =============================================================================
# TESTING ORDER (Recommended)
# =============================================================================
#
# Whenever an API doesn't work:
#
# Step 1
# -------
# Start Uvicorn
#
# uvicorn lab2b_app.main:app --reload
#
#
# Step 2
# -------
# Open
#
# http://127.0.0.1:8000/docs
#
#
# Step 3
# -------
# Test the endpoint from Swagger UI.
#
#
# Step 4
# -------
# Test the endpoint using curl (or Invoke-RestMethod).
#
#
# Step 5
# -------
# If Swagger works but curl doesn't,
# the issue is usually with the shell syntax,
# NOT your FastAPI application.



# =============================================================================
# COMMON HTTP STATUS CODES
# =============================================================================
#
# 200 OK
# Request successful.
#
# 400 Bad Request
# Invalid request.
#
# 401 Unauthorized
# Invalid API key.
#
# 404 Not Found
# Endpoint doesn't exist.
#
# 422 Unprocessable Entity
# Request validation failed (Pydantic).
#
# 429 Too Many Requests
# Rate limit exceeded.
#
# 500 Internal Server Error
# Server-side error.
#
# 503 Service Unavailable
# Unable to reach the LLM provider.
#
# =============================================================================