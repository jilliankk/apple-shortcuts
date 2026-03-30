# Use AI From Any App on Your iPhone — No Copy/Paste, No App Switching

**Three Apple Shortcuts that let you proofread text, ask questions by typing or voice, and even ask about the webpage you're looking at — all without leaving the app you're in.**

Works with a **local AI on your phone** (like LocallyAI with Qwen) or OpenAI's ChatGPT — your choice.

---

## What These Shortcuts Do

| Shortcut | Trigger | Use case |
|---|---|---|
| **AI Text Helper** | Copy text → Control Center | Proofread, summarize, or ask a question about selected text |
| **AI Ask** | Control Center | Type or speak any question, get an answer on screen |
| **AI See My Screen** | Control Center | Takes a screenshot + asks your question — AI sees the page you're on |

All three work from **any app** via Control Center. No switching, no copy/paste back and forth.

---

## Before You Start: Choose Your AI

### Option A — LocallyAI (free, private, runs on your phone)

This uses a local model like Qwen that runs entirely on your device. No account, no cost, no data sent anywhere.

**Steps:**

1. Open **LocallyAI** and load your model (e.g. Qwen 3.5 4B)
2. Find the local API server address — look in the app under **Settings** or a menu labeled **Server**, **API**, or **Local Server**
   - It will show something like `http://localhost:8080` or `http://127.0.0.1:1234`
   - Write down the port number (the digits after the last colon — e.g. `8080`)
3. Make sure the server is running before you use the shortcuts (the app needs to be open in the background)

> **Note:** The model name you'll enter in the shortcuts is whatever LocallyAI shows for your loaded model — often something like `qwen3.5:4b` or just `qwen`. Check the app for the exact name.

**Your API details:**
- URL: `http://localhost:YOUR_PORT/v1/chat/completions`
- Authorization: `Bearer local` (any text works — local servers don't check this)
- Model: your model's name as shown in the app

---

### Option B — OpenAI (ChatGPT, requires account)

Use this if you don't have LocallyAI, or for Shortcut 3 (which needs vision capability).

1. Go to [platform.openai.com](https://platform.openai.com) and sign up or log in
2. Click your profile icon → **API keys** → **Create new secret key**
3. Copy the key — you'll paste it into the shortcuts below
4. Add a payment method (costs are tiny — fractions of a cent per use)

**Your API details:**
- URL: `https://api.openai.com/v1/chat/completions`
- Authorization: `Bearer YOUR_API_KEY_HERE`
- Model: `gpt-4o-mini` (Shortcuts 1 & 2) / `gpt-4o` (Shortcut 3)

---

## Shortcut 1: AI Text Helper

**What it does:** Grabs text you've copied, sends it to your AI, and shows the response on screen.

**How to use it:** Copy any text (select → Copy), then open Control Center and tap this shortcut.

### Steps to build it:

1. Open the **Shortcuts** app → tap **+** to create a new shortcut
2. Tap the title at the top and name it **AI Text Helper**
3. Tap **Add Action** and search for **Get Clipboard** → add it
4. Tap **Add Action** and search for **Get Contents of URL** → add it
   - Tap the action to expand it
   - **URL:**
     - LocallyAI: `http://localhost:YOUR_PORT/v1/chat/completions`
     - OpenAI: `https://api.openai.com/v1/chat/completions`
   - **Method:** POST
   - **Headers:** tap **Add new header**
     - Header 1 — Name: `Authorization`
       - LocallyAI value: `Bearer local`
       - OpenAI value: `Bearer YOUR_API_KEY_HERE`
     - Header 2 — Name: `Content-Type` / Value: `application/json`
   - **Request Body:** select **JSON**
     - Add key: `model`
       - LocallyAI value: your model name (e.g. `qwen3.5:4b`)
       - OpenAI value: `gpt-4o-mini`
     - Add key: `messages` / Value: tap the field, switch to **Array**, then add one **Dictionary** item:
       - Key: `role` / Value: `user`
       - Key: `content` / Value: tap and select **Clipboard** from the variables list
5. Tap **Add Action** → search for **Get Dictionary Value** → add it
   - Key: `choices`
6. Tap **Add Action** → search for **Get Item from List** → add it
   - Set to **First Item**
7. Tap **Add Action** → search for **Get Dictionary Value** → add it
   - Key: `message`
8. Tap **Add Action** → search for **Get Dictionary Value** → add it
   - Key: `content`
9. Tap **Add Action** → search for **Show Result** → add it

Done. Test it by copying some text, running the shortcut, and you should see the AI's response in a popup.

---

## Shortcut 2: AI Ask (Type or Voice)

**What it does:** Asks "How do you want to ask?" — you pick Type or Speak — then sends your question to your AI and shows the answer on screen.

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
   - **URL:**
     - LocallyAI: `http://localhost:YOUR_PORT/v1/chat/completions`
     - OpenAI: `https://api.openai.com/v1/chat/completions`
   - **Method:** POST
   - **Headers:**
     - `Authorization`: `Bearer local` (LocallyAI) or `Bearer YOUR_API_KEY_HERE` (OpenAI)
     - `Content-Type`: `application/json`
   - **Request Body:** JSON
     - `model`: your model name (LocallyAI) or `gpt-4o-mini` (OpenAI)
     - `messages`: Array → Dictionary:
       - `role`: `user`
       - `content`: select **Provided Input** from variables (this captures output from whichever branch ran)

6. Add **Get Dictionary Value** → Key: `choices`
7. Add **Get Item from List** → First Item
8. Add **Get Dictionary Value** → Key: `message`
9. Add **Get Dictionary Value** → Key: `content`
10. Add **Show Result**

---

## Shortcut 3: AI See My Screen

**What it does:** Takes a screenshot of whatever you're looking at, lets you type or speak your question about it, and sends both to an AI that can see images. Shows the answer on screen.

**Example use:** You're on a webpage, tap this shortcut, ask "What is this page about?" or "Summarize the main points" — the AI sees exactly what's on your screen.

> **Important:** This shortcut requires a vision-capable AI model. Most local models including Qwen 3.5 4B do **not** support image input. Use **OpenAI GPT-4o** for this shortcut. If you're using LocallyAI for Shortcuts 1 & 2, you can still use this one with an OpenAI key — they're independent shortcuts.

### Steps to build it:

1. Open the **Shortcuts** app → tap **+** → name it **AI See My Screen**

2. Add **Take Screenshot**
   > This captures whatever is currently on screen when the shortcut runs.

3. Add **Wait** → set to **0.5 seconds**
   > Gives the screenshot action time to complete.

4. Add **Encode Media**
   - The input should be the screenshot from the previous step
   - Set encoding to **Base64**

5. Add a **Text** action
   - Type: `data:image/png;base64,`
   - Then immediately after (no space), tap the variable picker and select the **Encoded Media** from step 4
   > This creates the image data URL that OpenAI needs.

6. Add **Ask for Input**
   - Input Type: **Text**
   - Prompt: `What's your question about this screen?`

   > Or replace this with **Dictate Text** if you prefer to speak.

7. Add **Get Contents of URL**
   - **URL:** `https://api.openai.com/v1/chat/completions`
   - **Method:** POST
   - **Headers:**
     - `Authorization`: `Bearer YOUR_OPENAI_API_KEY`
     - `Content-Type`: `application/json`
   - **Request Body:** JSON
     - `model`: `gpt-4o`
     - `messages`: Array → Dictionary:
       - `role`: `user`
       - `content`: Array → add two Dictionary items:

         **Item 1:**
         - `type`: `text`
         - `text`: select **Provided Input** from variables (your question from step 6)

         **Item 2:**
         - `type`: `image_url`
         - `image_url`: Dictionary:
           - `url`: select the **Text** variable from step 5 (the data URL)

8. Add **Get Dictionary Value** → Key: `choices`
9. Add **Get Item from List** → First Item
10. Add **Get Dictionary Value** → Key: `message`
11. Add **Get Dictionary Value** → Key: `content`
12. Add **Show Result**

---

## Add All Three to Control Center

This is what lets you trigger them from any app without switching.

1. Open **Settings** → **Control Center**
2. Scroll down to **More Controls**
3. Find **Shortcuts** and tap the **+** to add it

**Even better — add each one individually:**
1. In **Settings → Control Center → More Controls**, look for your shortcut names listed individually
2. Add each one as its own button so you can tap directly without an extra menu

---

## How to Use Them Day-to-Day

**Proofreading while typing:**
1. Select the text you want proofread → **Copy**
2. Swipe down for Control Center → tap **AI Text Helper**
3. Read the suggestion in the popup → close → paste your edits manually

**Asking a question without leaving the app:**
1. Swipe down for Control Center → tap **AI Ask**
2. Choose Type or Speak → ask your question
3. Answer appears in a popup right over your current app

**Asking about a webpage:**
1. While on the page → swipe down for Control Center → tap **AI See My Screen**
2. Ask your question (the screenshot is taken automatically)
3. GPT-4o reads the page and answers — no browsing, just what's visible on screen

---

## Troubleshooting

**LocallyAI shortcut returns nothing or errors:**
- Make sure the LocallyAI app is open and the server is running before triggering the shortcut
- Double-check the port number — open LocallyAI, go to Settings/Server, and confirm the exact URL it shows
- Confirm the model name matches exactly what's shown in the app

**"Invalid API key" error (OpenAI):** Double-check you pasted the full key including the `sk-` prefix, with no extra spaces.

**Blank or error response:** The JSON body must be formatted exactly right. Go back into the "Get Contents of URL" step and verify the nested structure (messages → array → dictionary → role + content).

**Screenshot shortcut captures Control Center instead of your app:** Swipe Control Center away quickly after tapping the shortcut — the 0.5s Wait step is designed to help with this, but timing can vary.

**Dictation doesn't stop:** Tap the microphone icon to stop manually, or change the Stop Listening setting to "After Pause."

---

## Cost

**Shortcuts 1 & 2 with LocallyAI:** Free — runs entirely on your device.

**Shortcut 3 (AI See My Screen) with OpenAI:**
- `gpt-4o` with image: roughly $0.001–$0.01 per use depending on screenshot size
- You'd have to use it hundreds of times a day to spend even $1/month
