import os
import warnings

# Prefer the new package if available, fall back to the old one.
try:
    import google.genai as genai
    _GENAI_LIB = "genai"
except Exception:
    try:
        import google.generativeai as genai
        _GENAI_LIB = "generativeai"
    except Exception:
        genai = None
        _GENAI_LIB = None


def gemini_response(prompt: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return " GEMINI_API_KEY not found"

    if _GENAI_LIB is None:
        return "No Google GenAI library installed"

    # Suppress the deprecation FutureWarning from the older package so it
    # doesn't interrupt Streamlit execution.
    warnings.filterwarnings(
        "ignore",
        message=r"All support for the `google.generativeai` package has ended.*",
    )

    try:
        if _GENAI_LIB == "generativeai":
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("models/gemini-2.5-flash")
            response = model.generate_content(prompt)
            return getattr(response, "text", str(response))

        # Best-effort support for `google.genai` (newer package). APIs vary
        # between releases; try a couple of common call styles, otherwise
        # return a helpful message.
        if _GENAI_LIB == "genai":
            # If the new package exposes a configure helper, use it.
            if hasattr(genai, "configure"):
                genai.configure(api_key=api_key)
                if hasattr(genai, "GenerativeModel"):
                    model = genai.GenerativeModel("models/gemini-2.5-flash")
                    response = model.generate_content(prompt)
                    return getattr(response, "text", str(response))

            # Try a client-style API if available.
            if hasattr(genai, "TextGenerationClient"):
                try:
                    client = genai.TextGenerationClient()
                    resp = client.generate(model="models/gemini-2.5-flash", input=prompt)
                    # Try common response shapes
                    if hasattr(resp, "candidates") and resp.candidates:
                        return getattr(resp.candidates[0], "content", str(resp.candidates[0]))
                    return str(resp)
                except Exception:
                    pass

            return "`google.genai` is installed but its API surface is unsupported by this adapter."

    except Exception as e:
        return f"Gemini request failed: {e}"
