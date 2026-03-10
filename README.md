# Cart Automation Test

Automates one scenario: **search for a product and add it to the cart successfully** on the Shopify demo store.

---

## Scope

This submission covers only the required scenario:

- Search for a product
- Open the product
- Add the product to the cart
- Verify the product is added successfully

As per the assignment, this solution does **not** include:

- Full automation framework setup
- Cross-browser support
- Reporting tool integration
- Coverage for all scenarios

---

## Prerequisites

| Requirement   | Version |
|---------------|---------|
| Python        | 3.8+    |
| Google Chrome | Latest  |

---

## Project Structure

```text
assignment/
├── search.py          ← main test script
├── requirements.txt   ← dependencies
├── README.md          ← this file
├── report.html        ← visual test report (auto-generated)
└── test_output.log    ← plain-text test report (auto-generated)
```

---

## Setup

**1. Clone or download the project into a folder**

**2. Create and activate a virtual environment**

```bash
# Create
python -m venv .venv

# Activate — Windows
.venv\Scripts\activate

# Activate — Mac / Linux
source .venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

`webdriver-manager` automatically downloads the correct ChromeDriver — no manual driver setup needed.

---

## Run the Test

```bash
python search.py
```

Chrome will open automatically. No manual steps needed.

---

## Test Flow

| Step     | Action                                      |
|----------|---------------------------------------------|
| 1        | Login with store password                   |
| 2        | Go to home page                             |
| 3        | Search for "snowboard"                      |
| 4        | Click "The Videographer Snowboard"          |
| 5        | Click Add to cart                           |
| 6        | Dismiss the auto-opened cart dialog         |
| Verify 1 | Cart badge updates to 1                     |
| Verify 2 | Open /cart — product name visible in drawer |
| Verify 3 | Close the cart drawer                       |

---

## Configuration

All settings are at the top of `search.py` — no other file needs editing:

```python
BASE_URL       = "https://adnabu-store-assignment1.myshopify.com"
STORE_PASSWORD = "AdNabuQA"
SEARCH_TERM    = "snowboard"
PRODUCT_NAME   = "The Videographer Snowboard"
TIMEOUT        = 10  # seconds to wait for elements
```

---

## Output Files

Two report files are created automatically in the project folder after every run:

| File              | Description                                  |
|-------------------|----------------------------------------------|
| `test_output.log` | Plain-text step-by-step result log           |
| `report.html`     | Visual HTML report — open in any browser     |

---

## View Report

After the test runs, open the report in your browser:

```bash
# Windows
start report.html

# Mac
open report.html

# Linux
xdg-open report.html
```

---

## Dependencies

```
selenium
webdriver-manager
```