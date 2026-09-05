// Add PRODUTO record
query produto verb=POST {
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
    } as $produto
  }

  response = $produto
  guid = "NfYnY-g6wuls6Ax8ewh6i4Cgm1c"
}