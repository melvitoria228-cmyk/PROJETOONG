// Query all CLIENTE records
query cliente verb=GET {
  api_group = "Members & Accounts"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $cliente
  }

  response = $cliente
  guid = "rqWblSu30-mJOxOYHWAAaoC0l1M"
}