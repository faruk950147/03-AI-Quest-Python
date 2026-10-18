# Python Noise Library — Full Notes with Code and Output

## 1. What is Noise?

Noise is a mathematical pattern used to generate smooth, natural-looking variations in values.

বাংলায়: Noise এমন একটি pattern, যার মান coordinate পরিবর্তনের সঙ্গে সাধারণত মসৃণভাবে পরিবর্তিত হয়। এটি Game Development, Computer Graphics এবং Procedural Generation-এ ব্যবহৃত হয়।

### Applications

- Mountain and terrain generation
- Cloud patterns
- Water textures
- Game map generation
- Procedural graphics
- Natural-looking textures

---

## 2. Noise vs Random

| Random | Noise |
|---|---|
| মান হঠাৎ পরিবর্তিত হতে পারে | মান সাধারণত মসৃণভাবে পরিবর্তিত হয় |
| Random numbers তৈরিতে ব্যবহৃত হয় | Natural-looking patterns তৈরিতে ব্যবহৃত হয় |
| Dice roll-এর মতো | পাহাড়ের ঢালের মতো |

---

## 3. Install Noise Library

### Code

```bash
python -m pip install noise
```

### Output (installation সফল হলে)

```text
Successfully installed noise
```

নোট: আগে থেকেই install করা থাকলে `Requirement already satisfied` দেখাতে পারে।

---

## 4. Import Noise Library

### Code

```python
import noise

print("Noise library imported successfully!")
```

### Output

```text
Noise library imported successfully!
```

### Explanation

- `import noise` library-টি import করে।
- `print()` message দেখায়।
- `noise` Python-এর built-in library নয়; এটি আলাদাভাবে install করতে হয়।

---

## 5. 1D Perlin Noise

1D noise একটি coordinate ব্যবহার করে noise value তৈরি করে।

### Code

```python
import noise

for x in range(10):
    value = noise.pnoise1(x * 0.1)
    print(round(value, 3))
```

### Output

```text
0.0
0.091
0.142
0.137
0.082
0.0
-0.082
-0.137
-0.142
-0.091
```

Important: উপরের সংখ্যাগুলো output-এর উদাহরণ; নির্দিষ্ট installed package version-এ চালিয়ে যাচাই করা হয়নি।

### Explanation

- `range(10)` ০ থেকে ৯ পর্যন্ত সংখ্যা তৈরি করে।
- `x * 0.1` coordinate-এর পরিবর্তনের ধাপ নির্ধারণ করে।
- `pnoise1()` 1D Perlin noise value তৈরি করে।
- `round(value, 3)` দশমিকের তিন ঘর পর্যন্ত দেখায়।

---

## 6. 2D Perlin Noise

2D noise দুটি coordinate ব্যবহার করে।

### Code

```python
import noise

value = noise.pnoise2(1.5, 2.5)

print(value)
```

### Output

```text
একটি floating-point সংখ্যা
```

### Explanation

- `pnoise2(x, y)` দুটি coordinate গ্রহণ করে।
- একই coordinate এবং configuration-এ সাধারণত একই ফল পাওয়া যায়।
- এটি 2D texture ও terrain তৈরিতে ব্যবহার করা যায়।

Exact output পেতে code-টি নিজের Python environment-এ চালাতে হবে।

---

## 7. Generate a 2D Noise Grid

### Code

```python
import noise

width = 5
height = 5
scale = 0.1

for y in range(height):
    row = []

    for x in range(width):
        value = noise.pnoise2(
            x * scale,
            y * scale
        )

        row.append(round(value, 2))

    print(row)
```

### Output Format

```text
[0.0, ..., ..., ..., ...]
[..., ..., ..., ..., ...]
[..., ..., ..., ..., ...]
[..., ..., ..., ..., ...]
[..., ..., ..., ..., ...]
```

এটি output-এর format দেখায়; এখানে সংখ্যাগুলো placeholder।

### Explanation

- `width = 5`: প্রতিটি row-তে পাঁচটি value।
- `height = 5`: মোট পাঁচটি row।
- `scale = 0.1`: coordinate-এর পরিবর্তনের ধাপ।
- Nested loop প্রতিটি `(x, y)` coordinate পরীক্ষা করে।
- `round(value, 2)` value-কে দুই decimal place-এ round করে।

---

## 8. 3D Perlin Noise

3D noise তিনটি coordinate ব্যবহার করে।

### Code

```python
import noise

value = noise.pnoise3(1.0, 2.0, 3.0)

print(value)
```

### Output

```text
একটি floating-point সংখ্যা
```

### Explanation

- `pnoise3(x, y, z)` তিনটি coordinate গ্রহণ করে।
- 3D texture, volume effects এবং procedural graphics-এ ব্যবহার করা যায়।
- Exact numeric result library-তে code চালিয়ে দেখতে হবে।

---

## 9. Generate Multiple 1D Noise Values

### Code

```python
import noise

values = []

for x in range(5):
    value = noise.pnoise1(x * 0.2)
    values.append(round(value, 3))

print(values)
```

### Output Format

```text
[0.0, ..., ..., ..., ...]
```

### Explanation

- `values = []` একটি empty list তৈরি করে।
- `append()` প্রতিটি noise value list-এ যোগ করে।
- `print(values)` সব value একসঙ্গে দেখায়।

---

## 10. Important Functions

| Function | কাজ |
|---|---|
| `noise.pnoise1(x)` | 1D Perlin noise |
| `noise.pnoise2(x, y)` | 2D Perlin noise |
| `noise.pnoise3(x, y, z)` | 3D Perlin noise |

এগুলো `noise` package-এর Perlin noise functions।

---

## 11. Common Errors

### Error 1: ModuleNotFoundError

```text
ModuleNotFoundError: No module named 'noise'
```

সমাধান:

```bash
python -m pip install noise
```

যে Python interpreter দিয়ে program চালাচ্ছ, সেই interpreter-এই package install করতে হবে।

### Error 2: Import Error

সমাধান:
- Package installation পরীক্ষা করো।
- Virtual environment সক্রিয় আছে কি না দেখো।
- নিজের project-এ `noise.py` নামে file থাকলে rename করো।

---

## 12. Run the Program

একটি file তৈরি করো:

```text
noise_notes.py
```

তার মধ্যে Python code লিখে save করো।

তারপর terminal-এ চালাও:

```bash
python noise_notes.py
```

Package import ঠিক থাকলে এবং code সঠিক হলে program-এর output দেখতে পাবে।

---

## 13. Summary

- Noise natural-looking patterns তৈরি করতে সাহায্য করে।
- Perlin noise একটি noise generation technique।
- `pnoise1()` এক coordinate ব্যবহার করে।
- `pnoise2()` দুই coordinate ব্যবহার করে।
- `pnoise3()` তিন coordinate ব্যবহার করে।
- Noise procedural terrain, textures এবং game graphics-এ কাজে লাগে।
- সঠিক output জানতে code নিজে execute করে দেখা সবচেয়ে নির্ভরযোগ্য।

## Official Resources

Python Package Index: https://pypi.org/project/noise/

Python Package Installation Guide: https://packaging.python.org/en/latest/tutorials/installing-packages/
