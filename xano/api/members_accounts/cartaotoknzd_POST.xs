// Add CARTAOTOKNZD record
query cartaotoknzd verb=POST {
  api_group = "Members & Accounts"

  input {
    dblink {
      table = ""
    }
  }

  stack {
    db.add "" {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $cartaotoknzd
  }

  response = $cartaotoknzd
  guid = "HS45JtrsQ5rV_3CqFnWzlwPL3es"
}