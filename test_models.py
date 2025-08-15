#!/usr/bin/env python3

import sys
import os
sys.path.append(os.getcwd())

import torch
import pronunciationTrainer

print("Testing pronunciation trainer initialization...")

try:
    trainer_de = pronunciationTrainer.getTrainer("de")
    print("✅ German trainer initialized successfully")
    
    trainer_en = pronunciationTrainer.getTrainer("en") 
    print("✅ English trainer initialized successfully")
    
    print("✅ All models loaded successfully! The app should now work properly.")
    
except Exception as e:
    print(f"❌ Error loading models: {e}")
    import traceback
    traceback.print_exc()