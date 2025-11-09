# Quick Start Guide

## ✅ Your Project is Ready!

All compatibility issues have been resolved. Here's how to use your ML Debugging Expert System:

---

## Running the Project

### Option 1: Command Line Interface (CLI) - Recommended ✅

```bash
# Activate the virtual environment
source venv/bin/activate

# Run the CLI (automatically uses API key from .env)
python main_cli.py
```

The CLI will **automatically load** the API key from your `.env` file - no need to enter it manually!

### Option 2: Graphical User Interface (GUI)

**Note:** The GUI requires tkinter, which may not be installed by default.

```bash
# First, install tkinter (one-time setup)
brew install python-tk@3.11

# Then run the GUI
source venv/bin/activate
python gui.py
```

The GUI will also **automatically load** and connect using the API key from `.env`!

If you get a tkinter error, use the CLI instead (Option 1).

### Option 3: Test the Expert System Only

```bash
# Activate the virtual environment
source venv/bin/activate

# Run the standalone expert system (no API needed)
python ml_debugging_expert.py
```

---

## Environment Setup

Your `.env` file is already configured with:
```
GOOGLE_API_KEY=AIzaSyB8S2iYl3Q0DpLcL9vN8XMchmmOHXEWCSk
```

The project automatically loads this when you run any script.

---

## What Was Fixed

### 1. Python Version Compatibility ✅
- **Old**: Python 3.14 (too new, incompatible)
- **New**: Python 3.11.14 (stable and fully supported)
- Recreated virtual environment with correct Python version

### 2. Package Updates ✅
- Upgraded `google-generativeai` from 0.3.2 → 0.8.5
- Updated Gemini model: `models/gemini-2.5-flash`
- All dependencies installed successfully

### 3. Compatibility Fixes ✅
- Added `compat.py` for legacy package support
- Updated `ml_debugging_expert.py` to import compatibility shim
- Fixed `collections.Mapping` AttributeError
- Fixed protobuf metaclass error

---

## Testing Your Setup

### Test 1: Expert System (No API Required)
```bash
python ml_debugging_expert.py
```
Expected: See 3 test cases with diagnoses and recommendations

### Test 2: Gemini Integration (API Required)
```bash
python gemini_integration.py
```
Expected: See metric extraction and explanation generation working

### Test 3: Full CLI
```bash
python main_cli.py
```
Expected: Interactive menu appears

---

## Example Usage

### Natural Language Mode
```
Your question: My model gets 95% training accuracy but only 70% test accuracy

Expected Output:
✅ Extracted metrics: {"train_accuracy": 95, "test_accuracy": 70}
🔍 DIAGNOSIS: Overfitting Detected
💡 RECOMMENDATIONS: Add regularization, increase dropout, use data augmentation
```

### Structured Input Mode
```
Training accuracy (0-100): 92
Test accuracy (0-100): 88
Dataset size: 5000
Batch size: 64

Expected Output:
🔍 DIAGNOSIS: Good Model - balanced performance
```

---

## Project Structure

```
expert_systems/
├── venv/                      # Python 3.11 virtual environment
├── .env                       # API key configuration (DO NOT COMMIT!)
├── .env.example              # Template for .env
├── .gitignore                # Prevents committing secrets
├── compat.py                 # Compatibility shim for old packages
├── ml_debugging_expert.py    # Expert system engine (7 rules)
├── gemini_integration.py     # Gemini API integration
├── main_cli.py              # Command-line interface
├── gui.py                   # Graphical interface
├── requirements.txt         # Python dependencies
├── README.md               # Full documentation
├── SETUP_GUIDE.md         # Detailed setup instructions
└── QUICKSTART.md          # This file!
```

---

## Common Issues & Solutions

### Issue: "Module not found" errors
**Solution**: Make sure you activated the venv:
```bash
source venv/bin/activate
```

### Issue: GUI shows "tkinter is not available"
**Solution**: Install tkinter or use the CLI instead:
```bash
# Install tkinter (macOS)
brew install python-tk@3.11

# Or just use the CLI
python main_cli.py
```

### Issue: API errors or "model not found"
**Solution**: Check your `.env` file has the correct API key

### Issue: Python version errors
**Solution**: Make sure you're using Python 3.11 or 3.12:
```bash
python --version  # Should show Python 3.11.x
```

### Issue: CLI asks for API key (doesn't auto-load)
**Solution**: Make sure your `.env` file exists and contains:
```
GOOGLE_API_KEY=your_key_here
```

---

## Next Steps

1. ✅ Test the expert system: `python ml_debugging_expert.py`
2. ✅ Test Gemini integration: `python gemini_integration.py`
3. ✅ Run the CLI: `python main_cli.py`
4. ✅ Try the GUI: `python gui.py`
5. 📝 Document your test cases for your project report

---

## Security Reminder

**Before pushing to GitHub:**

```bash
# Make sure .env is in .gitignore (already done!)
git rm --cached .env  # Remove if already committed
git commit -m "Remove .env from repository"
```

Your `.gitignore` is already configured to exclude:
- `.env` files
- `__pycache__/`
- `venv/`
- `*.pyc`

---

## Need Help?

- Check `README.md` for detailed documentation
- Check `SETUP_GUIDE.md` for installation steps
- Gemini API Docs: https://ai.google.dev/docs
- Experta Docs: https://experta.readthedocs.io/

---

**🎉 Happy Debugging!**
