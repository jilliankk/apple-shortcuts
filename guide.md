# Use AI From Any App on Your iPhone — No Copy/Paste, No App Switching

**Three Apple Shortcuts that let you proofread text, ask questions by typing or voice, and even ask about the webpage you're looking at — all without leaving the app you're in.**

Powered by **Claude** (Anthropic's AI). One API key covers all three shortcuts, including vision.

---

## What These Shortcuts Do

| Shortcut | Trigger | Use case |
|---|---|---|
| **AI Text Helper** | Copy text → Control Center | Proofread, summarize, or ask a question about selected text |
| **AI Ask** | Control Center | Type or speak any question, get an answer on screen |
| **AI See My Screen** | Control Center | Takes a screenshot + asks your question — Claude sees the page you're on |

All three work from **any app** via Control Center. No switching, no copy/paste back and forth.

---

## Before You Start: Get a Claude API Key

1. Go to [console.anthropic.com](https://console.anthropic.com) and sign up or log in
2. Click **API Keys** in the left sidebar → **Create Key**
3. Copy the key — you'll paste it into the shortcuts below
4. Add a payment method (costs are tiny — fractions of a cent per use)

> **Which model to use:**
> - `claude-haiku-4-5-20251001` — fast and cheap, great for everyday use
> - `claude-sonnet-4-6` — smarter and more thorough, slightly higher cost
>
> The guide uses `claude-haiku-4-5-20251001` throughout. Swap in `claude-sonnet-4-6` anywhere if you want better quality answers.

---

## Shortcut 1: AI Text Helper

**What it does:** Grabs text you've copied, sends it to Claude, and shows the response on screen.

**How to use it:** Copy any text (select → Copy), then open Control Center and tap this shortcut.

### Steps to build it:

1. Open the **Shortcuts** app → tap **+** to create a new shortcut
2. Tap the title at the top and name it **AI Text Helper**
3. Tap **Add Action** → search for **Get Clipboard** → add it
4. Tap **Add Action** → search for **Get Contents of URL** → add it
   - Tap the action to expand it
   - **URL:** `https://api.anthropic.com/v1/messages`
   - **Method:** POST
   - **Headers:** tap **Add new header**
     - Header 1 — Name: `x-api-key` / Value: `YOUR_API_KEY_HERE`
     - Header 2 — Name: `anthropic-version` / Value: `2023-06-01`
     - Header 3 — Name: `content-type` / Value: `application/json`
   - **Request Body:** select **JSON**
     - Key: `model` / Value: `claude-haiku-4-5-20251001`
     - Key: `max_tokens` / Value: `1024`
     - Key: `messages` / Value: tap the field, switch to **Array**, then add one **Dictionary** item:
       - Key: `role` / Value: `user`
       - Key: `content` / Value: tap and select **Clipboard** from the variables list
5. Tap **Add Action** → search for **Get Dictionary Value** → add it
   - Key: `content`
6. Tap **Add Action** → search for **Get Item from List** → add it
   - Set to **First Item**
7. Tap **Add Action** → search for **Get Dictionary Value** → add it
   - Key: `text`
8. Tap **Add Action** → search for **Show Result** → add it

Done. Test it by copying some text, running the shortcut, and you should see Claude's response in a popup.

---

## Shortcut 2: AI Ask (Type or Voice)

**What it does:** Asks "How do you want to ask?" — you pick Type or Speak — then sends your question to Claude and shows the answer on screen.

### Steps to build it:

1. Open the **Shortcuts** app → tap **+** → name it **AI Ask**
2. Tap **Add Action** → search for **Choose from Menu** → add it
   - Prompt: `How do you want to ask?`
   - Option 1: `Type`
   - Option 2: `Speak`

3. **Under the "Type" branch:**
   - Add **Ask for Input**
     - Input Type: **Text**
     - Prompt: `What's your question?`

4. **Under the "Speak" branch:**
   - Add **Dictate Text**
     - Language: your preferred language
     - (Leave "Stop Listening" as default — it auto-stops after a pause)

5. After the menu (below both branches), add **Get Contents of URL**
   - **URL:** `https://api.anthropic.com/v1/messages`
   - **Method:** POST
   - **Headers:**
     - `x-api-key`: `YOUR_API_KEY_HERE`
     - `anthropic-version`: `2023-06-01`
     - `content-type`: `application/json`
   - **Request Body:** JSON
     - `model`: `claude-haiku-4-5-20251001`
     - `max_tokens`: `1024`
     - `messages`: Array → Dictionary:
       - `role`: `user`
       - `content`: select **Provided Input** from variables (captures output from whichever branch ran)

6. Add **Get Dictionary Value** → Key: `content`
7. Add **Get Item from List** → First Item
8. Add **Get Dictionary Value** → Key: `text`
9. Add **Show Result**

---

## Shortcut 3: AI See My Screen

**What it does:** Takes a screenshot of whatever you're looking at, lets you type or speak your question about it, and sends both to Claude. Claude sees exactly what's on your screen and answers your question.

**Example use:** You're on a webpage, tap this shortcut, ask "What is this page about?" or "Summarize the main points" — Claude sees the page and answers without needing to browse it.

### Steps to build it:

1. Open the **Shortcuts** app → tap **+** → name it **AI See My Screen**

2. Add **Take Screenshot**
   > Captures whatever is on screen when the shortcut runs.

3. Add **Wait** → set to **0.5 seconds**

4. Add **Encode Media**
   - Input: the screenshot from step 2
   - Set encoding to **Base64**

5. Add **Ask for Input**
   - Input Type: **Text**
   - Prompt: `What's your question about this screen?`
   > Or replace with **Dictate Text** if you prefer to speak.

6. Add **Get Contents of URL**
   - **URL:** `https://api.anthropic.com/v1/messages`
   - **Method:** POST
   - **Headers:**
     - `x-api-key`: `YOUR_API_KEY_HERE`
     - `anthropic-version`: `2023-06-01`
     - `content-type`: `application/json`
   - **Request Body:** JSON
     - `model`: `claude-haiku-4-5-20251001`
     - `max_tokens`: `1024`
     - `messages`: Array → Dictionary:
       - `role`: `user`
       - `content`: Array → add two Dictionary items:

         **Item 1 (image):**
         - `type`: `image`
         - `source`: Dictionary:
           - `type`: `base64`
           - `media_type`: `image/png`
           - `data`: select **Encoded Media** from variables (step 4)

         **Item 2 (your question):**
         - `type`: `text`
         - `text`: select **Provided Input** from variables (step 5)

7. Add **Get Dictionary Value** → Key: `content`
8. Add **Get Item from List** → First Item
9. Add **Get Dictionary Value** → Key: `text`
10. Add **Show Result**

---

## Add All Three to Control Center

This is what lets you trigger them from any app without switching.

1. Open **Settings** → **Control Center**
2. Scroll down to **More Controls**
3. Find **Shortcuts** and tap **+** to add it

**Even better — add each one as its own button:**
1. In **Settings → Control Center → More Controls**, look for your shortcut names listed individually
2. Add each one separately so you can tap directly without an extra menu

---

## How to Use Them Day-to-Day

**Proofreading while typing:**
1. Select the text you want proofread → **Copy**
2. Swipe down for Control Center → tap **AI Text Helper**
3. Read Claude's suggestion in the popup → close → paste your edits

**Asking a question without leaving the app:**
1. Swipe down for Control Center → tap **AI Ask**
2. Choose Type or Speak → ask your question
3. Answer appears in a popup right over your current app

**Asking about a webpage:**
1. While on the page → swipe down for Control Center → tap **AI See My Screen**
2. Ask your question (screenshot is taken automatically)
3. Claude reads the page and answers — no browsing, just what's visible on screen

---

## Troubleshooting

**"Invalid API key" error:** Double-check you pasted the full key with no extra spaces.

**Blank or error response:** The JSON body must be structured exactly right. Go back into the "Get Contents of URL" step and check the nested structure — especially that `messages` is an Array containing a Dictionary with `role` and `content` keys.

**Screenshot captures Control Center instead of your app:** Swipe Control Center away quickly after tapping the shortcut. The 0.5s Wait step helps, but timing can vary by device.

**Dictation doesn't stop:** Tap the microphone icon to stop manually, or change Stop Listening to "After Pause."

**Response is cut off:** Increase `max_tokens` from `1024` to `2048` or higher in the "Get Contents of URL" step.

---

## Cost

Claude's pricing is very low for personal use:
- `claude-haiku-4-5-20251001`: roughly $0.0001–$0.001 per shortcut use
- `claude-sonnet-4-6`: roughly $0.001–$0.01 per use

You'd have to use these hundreds of times a day to spend even $1/month.

---

## Want to Use a Local Model Instead?

If you prefer to keep everything on your device with no API costs, two iOS apps expose a local API that these shortcuts can call:

- **[ai.local](https://apps.apple.com/us/app/ai-local/id6741479958)** — Ollama-compatible API, requires iPhone 15 Pro or any iPhone 16
- **[Local LLM Server](https://apps.apple.com/us/app/local-llm-server/id6757007308)** — OpenAI + Ollama compatible API, requires iOS 26+

With either app, replace the URL in each shortcut with `http://localhost:PORT/v1/chat/completions`, change `x-api-key` to `Authorization: Bearer local`, and set the model name to match what's loaded in the app.
