# Use AI From Any App on Your iPhone — No Copy/Paste, No App Switching

**Three Apple Shortcuts that let you proofread text, ask questions by typing or voice, and even ask about the webpage you're looking at — all without leaving the app you're in.**

---

## What These Shortcuts Do

| Shortcut | Trigger | Use case |
|---|---|---|
| **AI Text Helper** | Copy text → Control Center | Proofread, summarize, or ask a question about selected text |
| **AI Ask** | Control Center | Type or speak any question, get an answer on screen |
| **AI See My Screen** | Control Center | Takes a screenshot + asks your question — AI sees the page you're on |

All three work from **any app** via Control Center. No switching, no copy/paste back and forth.

---

## Before You Start: Get an OpenAI API Key

These shortcuts use OpenAI's API (ChatGPT). You need a free API key.

1. Go to [platform.openai.com](https://platform.openai.com) and sign up or log in
2. Click your profile icon → **API keys** → **Create new secret key**
3. Copy the key and save it somewhere — you'll paste it into the shortcuts below
4. Add a payment method (OpenAI requires one, but costs are tiny — fractions of a cent per use)

> **Tip:** `gpt-4o-mini` is used for Shortcuts 1 & 2 (fast, cheap). Shortcut 3 uses `gpt-4o` for vision support.

---

## Shortcut 1: AI Text Helper

**What it does:** Grabs text you've copied, sends it to ChatGPT, and shows the response on screen.

**How to use it:** Copy any text (select → Copy), then open Control Center and tap this shortcut.

### Steps to build it:

1. Open the **Shortcuts** app → tap **+** to create a new shortcut
2. Tap the title at the top and name it **AI Text Helper**
3. Tap **Add Action** and search for **Get Clipboard** → add it
4. Tap **Add Action** and search for **Get Contents of URL** → add it
   - Tap the action to expand it
   - **URL:** `https://api.openai.com/v1/chat/completions`
   - **Method:** POST
   - **Headers:** tap **Add new header**
     - Header 1 — Name: `Authorization` / Value: `Bearer YOUR_API_KEY_HERE`
     - Header 2 — Name: `Content-Type` / Value: `application/json`
   - **Request Body:** select **JSON**
     - Add key: `model` / Value: `gpt-4o-mini`
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
   - The input should auto-connect to the previous step's output

Done. Test it by copying some text, running the shortcut, and you should see ChatGPT's response in a popup.

---

## Shortcut 2: AI Ask (Type or Voice)

**What it does:** Asks "How do you want to ask?" — you pick Type or Speak — then sends your question to ChatGPT and shows the answer on screen.

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
   - **URL:** `https://api.openai.com/v1/chat/completions`
   - **Method:** POST
   - **Headers:**
     - `Authorization`: `Bearer YOUR_API_KEY_HERE`
     - `Content-Type`: `application/json`
   - **Request Body:** JSON
     - `model`: `gpt-4o-mini`
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

**What it does:** Takes a screenshot of whatever you're looking at, lets you type or speak your question about it, and sends both the image and your question to GPT-4o (which can see images). Shows the answer on screen.

**Example use:** You're on a webpage, tap this shortcut, ask "What is this page about?" or "Summarize the main points" — GPT-4o sees exactly what's on your screen.

### Steps to build it:

1. Open the **Shortcuts** app → tap **+** → name it **AI See My Screen**

2. Add **Take Screenshot**
   > This captures whatever is currently on screen when the shortcut runs.

3. Add **Wait** → set to **0.5 seconds**
   > Gives the screenshot action time to complete before the next step.

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
     - `Authorization`: `Bearer YOUR_API_KEY_HERE`
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
   > If you don't see individual shortcuts listed, tap the Shortcuts control in your Control Center after adding it — it'll let you choose which shortcut to run.

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

**"Invalid API key" error:** Double-check you pasted the full key including the `sk-` prefix, with no extra spaces.

**Blank or error response:** The JSON body must be formatted exactly right. If you get a weird result, go back into the "Get Contents of URL" step and verify the nested structure (messages → array → dictionary → role + content).

**Screenshot shortcut shows the Control Center instead of your app:** This is normal on first run. iOS will capture Control Center in the shot. To fix it: in the Take Screenshot step, make sure there's no extra delay issue — or just swipe Control Center away quickly after tapping. The 0.5s Wait step helps minimize this.

**Dictation doesn't stop:** Tap the microphone icon to stop manually, or change the Stop Listening setting to "After Pause."

---

## Cost

Extremely cheap. At OpenAI's current pricing:
- `gpt-4o-mini` (Shortcuts 1 & 2): roughly $0.0001–$0.001 per use
- `gpt-4o` with image (Shortcut 3): roughly $0.001–$0.01 per use depending on screenshot size

You'd have to use these hundreds of times a day to spend even $1/month.
