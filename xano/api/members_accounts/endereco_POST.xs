// Add ENDERECO record
query endereco verb=POST {
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
    } as $endereco
  }

  response = $endereco
  guid = "Kkv-rU45xNATc3Q1-QWclQq-oO4"
}