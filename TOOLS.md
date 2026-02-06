# Gena's Tools & Learning System

## Available Tools

### 1. Python Execution (Math & Calculations)

Gena can run Python code for you!

**Examples:**
```
You: What's 15 * 847?
Gena: *calculates* The result is 12,705!

You: Calculate the square root of 144
Gena: *uses Python* That's 12!
```

Gena will automatically use `execute_python` when she needs to calculate something.

---

### 2. Learn Facts

Teach Gena facts she should remember!

**Examples:**
```
You: Remember that my favorite color is blue
Gena: Got it! I'll remember that about favorite color.

You: My birthday is July 15th
Gena: Got it! I'll remember that about birthday.
```

Gena stores facts in memory and recalls them later!

---

### 3. Learn Procedures

Teach Gena how to do things step-by-step!

**Command:** `teach <procedure name>`

**Example:**
```
You: teach make coffee
Teaching 'make coffee'. Enter steps (one per line). Type 'done' when finished:
  Step: Fill kettle with water
  Step: Boil water  
  Step: Put coffee grounds in filter
  Step: Pour hot water over grounds
  Step: Wait 4 minutes
  Step: done

Gena: Yay! I learned how to make coffee!
```

**Recall:** `recall make coffee`
```
Gena: Here's how to make coffee:
  1. Fill kettle with water
  2. Boil water
  3. Put coffee grounds in filter
  4. Pour hot water over grounds
  5. Wait 4 minutes
```

---

## Commands

```
exit/quit       - End conversation
memory          - See everything Gena remembers
online          - Check if internet is available
teach <name>    - Teach a procedure step-by-step
recall <name>   - Show learned procedure
```

---

## Examples

### Teaching Gena

```
You: teach morning routine
Teaching 'morning routine'. Enter steps:
  Step: Wake up at 7am
  Step: Brush teeth
  Step: Make coffee
  Step: Check emails
  Step: done

Gena: Yay! I learned how to morning routine!
```

### Using Math

```
You: If I have $50 and spend $12.50, how much is left?
Gena: *calculates* You'd have $37.50 left!
```

### Learning Facts

```
You: My name is Sam
Gena: Nice to meet you Sam!

You: I prefer tea over coffee
Gena: Got it! I'll remember that.
```
