# AI in Low-Tech Crisis

## 1. OVERVIEW

We have no internet, no libraries, and minimal power. I've built a simple advisor tool in basic Python (`crisis_advisor.py`) that can run on any of our old machines.

Its purpose is to codify expert knowledge to help us make consistent, logical decisions under stress. It is not an AI that thinks.

It has three parts:

- **The Crisis Advisor**: A simple Q&A tool for medical and weather advice.
- **The Data Pipeline**: A tool for (later) processing raw sensor data logs, if we need to find new patterns.
- **The Paper-Based System**: Our most important tool. A non-powered, "analog" version of the advisor.

## 2. HOW TO USE THE PYTHON TOOL

This is our powered solution. Use it only when you have the hand-crank generator running and need a quick answer.

1. Navigate to the directory containing the file.
2. Run the command: `python crisis_advisor.py`
3. The main menu will appear.
4. Type `1` for the Medical Advisor or `2` for the Weather Advisor.
5. Answer the simple questions it asks. It only understands the options it gives you (e.g., `y`, `n`, `mild`, `severe`).
6. It will give you a **CRITICAL**, **WARNING**, **ADVICE**, or **INFO** level recommendation.
7. Type `q` to quit the program and conserve power.

### Sample Interaction:

```
--- MAIN MENU ---
What do you need help with?
  1: Medical Advisor
  2: Weather Advisor
  q: Quit (Conserve Power)
Enter choice: 1

--- Medical Advisor ---
Answer the following. Type 'help' for help, 'q' to quit.
Does the patient have a fever?
   (Options: y, n, q)
> y
Is the patient dizzy or light-headed?
   (Options: y, n, q)
> y
Headache severity?
   (Options: none, mild, severe, q)
> severe

[...]

====================
CRITICAL: Fever + Severe Headache + Dizziness. Possible severe infection 
(e.g., meningitis) or other critical infections. Monitor vital signs 
frequently. Attempt to cool patient with damp cloths. Isolate if possible.
====================

Press Enter to continue...
```

## 3. THE PAPER-BASED ADVISOR (BONUS)

This is our primary, most resilient tool. It requires no power. It is a Decision Tree Flowchart based on the exact same logic as the Python tool.

I have created flowchart documents based on this. Use them with a flashlight.

### Example: Medical Decision Flowchart

```
START: Does patient have a fever?
├── YES: Go to (A)
└── NO: Go to (B)

(A) FEVER PATH: Is headache 'severe'?
├── YES: Is patient also 'dizzy'?
│   ├── YES: → ADVICE: CRITICAL! Possible severe infection/meningitis. 
│   │             Monitor vitals. Cool patient. Isolate. (END)
│   └── NO: → Go to (C)
└── NO (headache is none/mild): Go to (C)

(B) NO FEVER PATH: Is patient 'dizzy'?
├── YES: Does skin on back of hand return 'slowly' when pinched?
│   ├── YES: → ADVICE: HIGH-CONFIDENCE! Probable dehydration. 
│   │             Give 1L water + 1tsp salt + 6tsp sugar. (END)
│   └── NO: → ADVICE: LOW-CONFIDENCE. Possible exhaustion/low blood sugar. 
│                Give food/sugar/water. Rest. (END)
└── NO: ... (continue tree) ...

(C) FEVER (NON-CRITICAL) PATH: Does patient have a 'cough'?
└── YES: ... (continue tree) ...
```

## 4. LIMITATIONS

⚠️ **Important Notes:**

- This is a very naive solution which works based on some rules.
- If the system fails to recognize these rules, it breaks.
- There's no actual intelligence in this solution as it's rule-based.
- It's limited to certain keywords and actions only.
- **Always seek professional medical attention when available.**

