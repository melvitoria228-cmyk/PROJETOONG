// Add OP record
query op verb=POST {
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
    } as $op
  }

  response = $op
  guid = "z0z2NaSU2HdHQZyhHAIemA5biYs"
}