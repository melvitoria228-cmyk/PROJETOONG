// Add STATUS_ITEM record
query status_item verb=POST {
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
    } as $status_item
  }

  response = $status_item
  guid = "db0Cu6iK-mtAJBXCGXxSzmz8uxE"
}