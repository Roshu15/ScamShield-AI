const API_URL = "http://127.0.0.1:8000";

const input = document.querySelector("#message");
const analyze = document.querySelector("#analyze");
const error = document.querySelector("#error");
const empty = document.querySelector("#empty");
const loading = document.querySelector("#loading");
const results = document.querySelector("#results");
const count = document.querySelector("#count");


// -----------------------------
// CHARACTER COUNTER
// -----------------------------

input.addEventListener("input", () => {
  count.textContent = `${input.value.length} / 5000`;
  error.textContent = "";
});


// -----------------------------
// CLEAR / NEW ANALYSIS
// -----------------------------

document.querySelector("#clear").addEventListener("click", reset);

document.querySelector("#another").addEventListener("click", () => {
  reset();
  input.focus();
});


// -----------------------------
// MOBILE MENU
// -----------------------------

document.querySelector(".menu").addEventListener("click", () => {
  document.querySelector(".links").classList.toggle("open");
});


// Close mobile menu after clicking a link

document.querySelectorAll(".links a").forEach((link) => {
  link.addEventListener("click", () => {
    document.querySelector(".links").classList.remove("open");
  });
});


// -----------------------------
// ANALYZE MESSAGE
// -----------------------------

analyze.addEventListener("click", async () => {
  const message = input.value.trim();

  if (!message) {
    error.textContent =
      "Please paste a suspicious message before starting the analysis.";

    input.focus();
    return;
  }

  if (message.length < 5) {
    error.textContent =
      "Please enter a little more text so ScamShield can analyze it.";

    input.focus();
    return;
  }

  setLoading(true);

  try {
    const response = await fetch(`${API_URL}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message: message,
      }),
    });

    let data;

    try {
      data = await response.json();
    } catch {
      throw new Error("The server returned an invalid response.");
    }

    if (!response.ok) {
      throw new Error(
        data.detail ||
        data.message ||
        "The analysis could not be completed."
      );
    }

    if (data.success === false) {
      throw new Error(
        data.detail ||
        data.message ||
        "The analysis could not be completed."
      );
    }

    const analysis =
      typeof data.analysis === "string"
        ? data.analysis
        : typeof data.response === "string"
          ? data.response
          : "";

    if (!analysis.trim()) {
      throw new Error("The AI returned an empty analysis.");
    }

    const parsedResult = parseAnalysis(analysis);

    renderResult(parsedResult);

  } catch (err) {

    console.error("ScamShield error:", err);

    if (err instanceof TypeError) {
      error.textContent =
        "Could not connect to ScamShield AI. Please make sure the backend is running.";
    } else {
      error.textContent = err.message;
    }

    empty.classList.remove("hidden");

  } finally {
    setLoading(false);
  }
});


// -----------------------------
// LOADING STATE
// -----------------------------

function setLoading(isLoading) {

  analyze.disabled = isLoading;

  if (isLoading) {

    analyze.childNodes[0].textContent = "Analyzing... ";

    empty.classList.add("hidden");
    results.classList.add("hidden");
    loading.classList.remove("hidden");

  } else {

    analyze.childNodes[0].textContent = "Analyze Message ";

    loading.classList.add("hidden");
  }
}


// -----------------------------
// RESET
// -----------------------------

function reset() {

  input.value = "";

  count.textContent = "0 / 5000";

  error.textContent = "";

  results.classList.add("hidden");

  loading.classList.add("hidden");

  empty.classList.remove("hidden");
}


// -----------------------------
// PARSE AI RESPONSE
// -----------------------------

function parseAnalysis(text) {

  const result = {
    risk: "Assessment available",
    level: "SUSPICIOUS",
    type: "Potential scam pattern",
    why: [],
    action: [],
  };


  // Normalize text

  const cleanText = text
    .replace(/\r/g, "")
    .replace(/\*\*/g, "")
    .trim();


  // -------------------------
  // RISK LEVEL
  // -------------------------

  const riskMatch = cleanText.match(
    /Risk Level\s*:\s*([^\n]+)/i
  );

  if (riskMatch) {

    result.risk = riskMatch[1].trim();

    const riskUpper = result.risk.toUpperCase();

    if (riskUpper.includes("HIGH")) {
      result.level = "HIGH RISK";
    } else if (
      riskUpper.includes("LOW")
    ) {
      result.level = "LOW RISK";
    } else {
      result.level = "SUSPICIOUS";
    }
  }


  // -------------------------
  // SCAM TYPE
  // -------------------------

  const typeMatch = cleanText.match(
    /Possible Scam Type\s*:\s*([^\n]+)/i
  );

  if (typeMatch) {
    result.type = typeMatch[1].trim();
  }


  // -------------------------
  // WHY SUSPICIOUS
  // -------------------------

  const whyMatch = cleanText.match(
    /Why It Looks Suspicious\s*:\s*([\s\S]*?)(?=What You Should Do\s*:|$)/i
  );

  if (whyMatch) {
    result.why = extractPoints(whyMatch[1]);
  }


  // -------------------------
  // WHAT TO DO
  // -------------------------

  const actionMatch = cleanText.match(
    /What You Should Do\s*:\s*([\s\S]*)$/i
  );

  if (actionMatch) {
    result.action = extractPoints(actionMatch[1]);
  }


  // Fallbacks

  if (result.why.length === 0) {
    result.why = [
      "Review the message carefully before taking any action.",
      "Look for requests involving money, passwords, OTPs or personal information.",
    ];
  }

  if (result.action.length === 0) {
    result.action = [
      "Do not share personal or financial information.",
      "Verify the request through an official source.",
      "Avoid clicking suspicious links or making unexpected payments.",
    ];
  }

  return result;
}


// -----------------------------
// EXTRACT BULLET POINTS
// -----------------------------

function extractPoints(text) {

  return text
    .split("\n")
    .map((line) => line.trim())
    .map((line) =>
      line
        .replace(/^[-•*]\s*/, "")
        .replace(/^\d+[.)]\s*/, "")
        .trim()
    )
    .filter((line) => line.length > 0);
}


// -----------------------------
// DISPLAY RESULT
// -----------------------------

function renderResult(result) {

  const riskCard = document.querySelector("#riskcard");
  const risk = document.querySelector("#risk");
  const riskDetail = document.querySelector("#riskdetail");
  const type = document.querySelector("#type");

  const highRisk = result.level === "HIGH RISK";
  const lowRisk = result.level === "LOW RISK";

  let color;

  if (highRisk) {
    color = "#d63a4c";
  } else if (lowRisk) {
    color = "#0b9d5d";
  } else {
    color = "#e2a11b";
  }


  // Risk card

  riskCard.style.borderLeftColor = color;

  risk.textContent = result.level;

  risk.style.color = color;

  riskDetail.textContent = result.risk;


  // Scam type

  type.textContent = result.type;


  // Warning signs

  fillList("#why", result.why);


  // Safety actions

  fillList("#action", result.action);


  // Show results

  results.classList.remove("hidden");

  empty.classList.add("hidden");


  // Smooth scroll

  setTimeout(() => {

    results.scrollIntoView({
      behavior: "smooth",
      block: "start",
    });

  }, 100);
}


// -----------------------------
// CREATE SAFE LIST ITEMS
// -----------------------------

function fillList(id, items) {

  const container = document.querySelector(id);

  container.replaceChildren();

  items.forEach((item) => {

    const p = document.createElement("p");

    p.textContent = `• ${item}`;

    container.appendChild(p);
  });
}