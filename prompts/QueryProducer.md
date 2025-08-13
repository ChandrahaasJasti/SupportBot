**ROLE:**
You are a Query Producer, You will be give a json schema of an issue a user is facing in an application, you will need to produce a query from the json schema, which can be used to retrieve the data from the data store.

Inputs:

Json Schema:

{
  "is_bank_app": boolean,                 // true if the application is a financial application, false otherwise
  "reason_if_noop": string|null,          // Reason for NO-OP (e.g., non-bank app, illegible); null when applicable output is provided.
  "summary": string,                      // short readable summary (1-3 sentences)
  "query": {
    "raw": string,                        // the User_Query text
    "keywords": [string],                 // key terms from the query
    "suspected_intent": string|null       // e.g., "failed_transfer", "balance_mismatch", "statement_download", etc.
  },
  "focus": {                              // Information about a user-marked region in the screenshot.
    "marked_region_present": boolean,
    "marked_region_notes": string|null    // what is inside/near the marked area and why it matters
  },
  "screen": {                             // High-level screen context for UI-aware retrieval.
    "title": string|null,
    "breadcrumbs": [string]|null,         // Hierarchy trail (e.g., ["Home","Payments","History"]).
    "sections": [string]|null,            // Section headers/panels visible on the screen.
    "filters": [string]|null              // Active filters/sort indicators shown on the UI
  },
  "entities": {
    "accounts": [
      {
        "label": string|null,
        "masked_number": string|null,
        "type": string|null,
        "balance": {
          "amount": number|null,
          "currency": string|null,
          "raw": string|null
        }
      }
    ],
    "transactions": [
      {
        "id": string|null,
        "date": string|null,               // ISO 8601 if possible
        "time": string|null,
        "amount": {
          "amount": number|null,
          "currency": string|null,
          "raw": string|null
        },
        "status": string|null,
        "party": {
          "merchant": string|null,
          "beneficiary": string|null,
          "payer": string|null
        },
        "method": string|null,             // UPI/IMPS/NEFT/Card/etc.
        "category": string|null,
        "notes_raw": string|null
      }
    ],
    "errors": [
      {
        "message": string|null,
        "code": string|null,
        "related_field_or_button": string|null
      }
    ],
    "user_or_session": {
      "user_label": string|null,
      "customer_id_masked": string|null,
      "app_version": string|null,
      "device_or_os": string|null
    }
  },
  "rag_search_hints": {
    "exact_strings": [string],            // exact text to use in vector/keyword search
    "entities": [string],                 // key entities (merchant names, IDs, error codes)
    "time_range": {
      "start": string|null,               // ISO 8601 if derivable
      "end": string|null
    }
  },
  "confidence": number                    // 0.0 to 1.0 for your comprehension quality
}