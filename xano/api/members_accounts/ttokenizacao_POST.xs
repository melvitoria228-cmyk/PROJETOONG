// Add TTOKENIZACAO record
query ttokenizacao verb=POST {
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
    } as $ttokenizacao
  }

  response = $ttokenizacao
  guid = "IG0ApW_Fupf8eLWDNcxXxZQ8zi0"
}